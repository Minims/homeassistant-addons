import runpy
from pathlib import Path


script = Path(__file__).with_name("update_installations.py")
assert script.exists(), "The README installation updater is missing"
update = runpy.run_path(str(script))["readme_with_installations"]
root = script.parents[2]
original = "Before\n<!-- installations:start -->\nOld counts\n<!-- installations:end -->\nAfter\n"
counts = {
    "dfd2619f_somfy-protect-2-mqtt": {"total": 306},
    "3a585793_somfy-protect-2-mqtt": {"total": 307},
    "another_repo_somfy-protect-2-mqtt": {"total": 999},
    "dfd2619f_somfy-protect-2-mqtt-dev": {"total": 15},
    "3a585793_somfy-protect-2-mqtt-dev": {"total": 5},
}
configs = sorted(root.glob("*/config.yaml"))
updated = update(original, counts, configs)
assert "[SomfyProtect2MQTT](./SomfyProtect2MQTT) | 613 |" in updated
assert "[SomfyProtect2MQTT-dev](./SomfyProtect2MQTT-dev) | 20 |" in updated
assert "[MyFox2MQTT-dev](./MyFox2MQTT-dev) | 0 |" in updated
assert updated.count("](./") == len(configs)
assert updated.startswith("Before\n") and updated.endswith("\nAfter\n")
assert update(updated, counts, configs) == updated
for readme, analytics in [
    ("No markers", counts),
    (original + original, counts),
    (original, {}),
    (original, {**counts, "dfd2619f_somfy-protect-2-mqtt": {"total": -1}}),
]:
    try:
        update(readme, analytics, configs)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid input must not replace README counts")
print("Installation updater checks passed")
