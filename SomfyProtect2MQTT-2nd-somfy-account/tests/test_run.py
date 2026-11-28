"""Run the addon startup script with real yq and a local Supervisor stub.

Requires bash and mikefarah/yq on PATH. No container or credentials are needed.
"""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


class StartupTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.data = self.root / "data"
        self.app = self.root / "app"
        self.bin = self.root / "bin"
        for directory in (self.data, self.app / "somfyProtect2Mqtt/config", self.bin):
            directory.mkdir(parents=True)
        self.options = {
            "somfy_protect": {"username": "private@example.invalid", "password": "somfy-secret"},
            "homeassistant_config": {"code": "9917", "device_macs": [{"device": "Badge", "mac": "AA:BB:CC:DD:EE:FF"}]},
            "mqtt": {},
            "debug": False,
        }
        self.service = {"host": "broker", "port": 1883, "username": "addons", "password": "mqtt-secret", "ssl": False}
        stub = self.root / "bashio.sh"
        stub.write_text("""bashio::log.info() { printf '%s\\n' "$*"; }
bashio::supervisor.timezone() { printf UTC; }
bashio::config.has_value() { yq -e ".$1 != null" "$TEST_OPTIONS" > /dev/null 2>&1; }
bashio::config.true() { yq -e ".$1 == true" "$TEST_OPTIONS" > /dev/null 2>&1; }
bashio::services() { yq -r ".$2" "$TEST_SERVICE"; }
""")
        python = self.bin / "python3"
        python.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > "$TEST_ARGS"\n')
        python.chmod(0o755)
        self.env = {
            **os.environ,
            "PATH": f"{self.bin}:{os.environ['PATH']}",
            "BASH_ENV": str(stub),
            "TEST_OPTIONS": str(self.data / "options.json"),
            "TEST_SERVICE": str(self.root / "mqtt.json"),
            "TEST_ARGS": str(self.root / "args"),
        }
        source = Path(__file__).resolve().parents[1] / "rootfs/etc/s6-overlay/s6-rc.d/SomfyProtect2MQTT/run"
        self.script = self.root / "run"
        # Relocate only the container filesystem; execute the actual shell logic.
        self.script.write_text(
            source.read_text().replace("/usr/bin/SomfyProtect2MQTT", str(self.app)).replace("/data/", f"{self.data}/")
        )

    def run_script(self, malformed=False):
        (self.data / "options.json").write_text("{invalid" if malformed else json.dumps(self.options))
        (self.root / "mqtt.json").write_text(json.dumps(self.service))
        return subprocess.run(["bash", str(self.script)], env=self.env, capture_output=True, text=True, timeout=10)

    def configuration(self):
        args = (self.root / "args").read_text().splitlines()
        path = Path(args[args.index("-c") + 1])
        return path, json.loads(subprocess.check_output(["yq", "-o=json", str(path)], text=True))

    def test_configuration_is_persistent_private_and_typed(self):
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        path, config = self.configuration()
        self.assertEqual(path, self.data / "config.yaml")
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(config["mqtt"], self.service)
        self.assertEqual(config["homeassistant_config"]["device_macs"], {"Badge": "AA:BB:CC:DD:EE:FF"})

    def test_logs_hide_credentials_and_alarm_code(self):
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        for secret in ("private@example.invalid", "somfy-secret", "mqtt-secret", "9917"):
            self.assertNotIn(secret, result.stdout + result.stderr)

    def test_mqtt_credentials_are_literal_strings(self):
        self.service["password"] = 'quote" backslash\\ newline\n$(do-not-execute)'
        self.service["username"] = "true"
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.configuration()[1]["mqtt"], self.service)

    def test_explicit_mqtt_options_and_debug_are_preserved(self):
        self.options["mqtt"] = {**self.service, "host": "custom", "ssl": True}
        self.options["debug"] = True
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.configuration()[1]["mqtt"], self.options["mqtt"])
        self.assertIn("-v", (self.root / "args").read_text().splitlines())

    def test_legacy_token_is_migrated_without_overwriting_persistent_token(self):
        legacy = self.app / "somfyProtect2Mqtt/config/token.json"
        legacy.write_text('{"access_token": "old"}')
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        token = self.data / "token.json"
        self.assertTrue(token.exists())
        self.assertEqual(token.read_text(), legacy.read_text())
        self.assertEqual(token.stat().st_mode & 0o777, 0o600)
        token.write_text('{"access_token": "new"}')
        self.assertEqual(self.run_script().returncode, 0)
        self.assertEqual(token.read_text(), '{"access_token": "new"}')

    def test_invalid_options_do_not_replace_existing_configuration(self):
        config = self.data / "config.yaml"
        config.write_text("previous config")
        result = self.run_script(malformed=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(config.read_text(), "previous config")
        self.assertFalse((self.root / "args").exists())

    def test_finish_does_not_announce_restart_on_clean_exit(self):
        source = Path(__file__).resolve().parents[1] / "rootfs/etc/s6-overlay/s6-rc.d/SomfyProtect2MQTT/finish"
        exitcode = self.root / "exitcode"
        exitcode.write_text("0")
        script = self.root / "finish"
        script.write_text(source.read_text().replace("/run/s6-linux-init-container-results/exitcode", str(exitcode)))
        result = subprocess.run(
            ["bash", str(script), "0", "0"], env=self.env, capture_output=True, text=True, timeout=10
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("restarting", result.stdout)


if __name__ == "__main__":
    unittest.main()
