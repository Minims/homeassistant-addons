import hashlib
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path


REPOSITORY_URL = "https://github.com/minims/homeassistant-addons"
PREFIXES = tuple(
    hashlib.sha1(url.encode()).hexdigest()[:8] + "_"
    for url in (REPOSITORY_URL, REPOSITORY_URL + "/")
)
HISTORY_DAYS = 365
GRAPH_WIDTH = 1100
GRAPH_HEIGHT = 360


def addon_metadata(configs):
    metadata = []
    for config in configs:
        settings = config.read_text(encoding="utf-8")
        metadata.append(
            {
                "name": re.search(r"^name: (.+)$", settings, re.MULTILINE).group(1),
                "slug": re.search(r"^slug: (\S+)$", settings, re.MULTILINE).group(1),
                "directory": config.parent.name,
            }
        )
    return metadata


def installation_counts(analytics, configs):
    if not isinstance(analytics, dict) or not any(
        slug.startswith(PREFIXES) for slug in analytics
    ):
        raise ValueError("Analytics contains no entries for this repository")
    counts = {}
    for addon in addon_metadata(configs):
        totals = [
            analytics.get(prefix + addon["slug"], {"total": 0})["total"]
            for prefix in PREFIXES
        ]
        if any(type(total) is not int or total < 0 for total in totals):
            raise ValueError(f"Invalid installation count for {addon['slug']}")
        counts[addon["directory"]] = sum(totals)
    return counts


def installation_rows(analytics, configs):
    counts = installation_counts(analytics, configs)
    return [
        f"| [{addon['name']}](./{addon['directory']}) | {counts[addon['directory']]} |"
        for addon in addon_metadata(configs)
    ]


def update_history(history, refreshed, counts):
    history = {**history, refreshed: counts}
    cutoff = date.fromisoformat(refreshed) - timedelta(days=HISTORY_DAYS - 1)
    return {
        day: history[day]
        for day in sorted(history)
        if date.fromisoformat(day) >= cutoff
    }


def render_svg(history, configs):
    days = sorted(history)
    addons = addon_metadata(configs)
    values = [history[day].get(addon["directory"], 0) for day in days for addon in addons]
    maximum = max(values, default=1)
    left, top, plot_width, plot_height = 70, 55, 820, 280
    colors = ["#0969da", "#cf222e", "#1a7f37", "#8250df", "#bf8700"]
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 390" role="img">',
        '<title>Home Assistant add-on installations over the last year</title>',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="70" y="22" fill="#24292f" font-size="16" font-weight="bold">Add-on installation history</text>',
        '<text x="18" y="58" fill="#57606a" font-size="11" transform="rotate(-90 18 58)">installations</text>',
    ]
    for tick in range(5):
        value = maximum * tick / 4
        y = top + plot_height - tick * plot_height / 4
        lines.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_width}" y2="{y:.1f}" stroke="#d0d7de"/>')
        lines.append(f'<text x="{left - 8}" y="{y + 4:.1f}" text-anchor="end" fill="#57606a" font-size="11">{value:.0f}</text>')
    if days:
        for index, addon in enumerate(addons):
            points = []
            for position, day in enumerate(days):
                x = left + position * plot_width / max(len(days) - 1, 1)
                count = history[day].get(addon["directory"], 0)
                y = top + plot_height - count * plot_height / maximum
                points.append(f"{x:.1f},{y:.1f}")
            color = colors[index % len(colors)]
            lines.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="2.5"/>')
            lines.append(f'<circle cx="{points[-1].split(",")[0]}" cy="{points[-1].split(",")[1]}" r="3" fill="{color}"/>')
            legend_x = left + index * 210
            latest_count = history[days[-1]].get(addon["directory"], 0)
            lines.append(f'<line x1="{legend_x}" y1="365" x2="{legend_x + 18}" y2="365" stroke="{color}" stroke-width="3"/>')
            lines.append(f'<text x="{legend_x + 24}" y="369" fill="#24292f" font-size="11">{escape(addon["name"])}: {latest_count} installations</text>')
        lines.append(f'<text x="{left}" y="350" fill="#57606a" font-size="11">{days[0]}</text>')
        lines.append(f'<text x="{left + plot_width - 70}" y="350" fill="#57606a" font-size="11">{days[-1]}</text>')
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def readme_with_installations(readme, analytics, configs, refreshed=None):
    refreshed = refreshed or datetime.now(timezone.utc).date().isoformat()
    installation_counts(analytics, configs)
    section = "\n".join(
        [
            "<!-- installations:start -->", "",
            f"Last refreshed: {refreshed} (UTC).", "",
            "<!-- installations:end -->",
        ]
    )
    updated, replacements = re.subn(
        r"<!-- installations:start -->.*?<!-- installations:end -->",
        lambda match: section, readme, flags=re.DOTALL,
    )
    if replacements != 1:
        raise ValueError("README must contain exactly one installation section")
    return updated


def update_files(root, analytics, refreshed=None):
    configs = sorted(root.glob("*/config.yaml"))
    refreshed = refreshed or datetime.now(timezone.utc).date().isoformat()
    counts = installation_counts(analytics, configs)
    history_path = root / ".github/data/installations.json"
    history = json.loads(history_path.read_text(encoding="utf-8")) if history_path.exists() else {}
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history = update_history(history, refreshed, counts)
    history_path.write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")
    (root / ".github/data/installations.svg").write_text(render_svg(history, configs), encoding="utf-8")
    readme = root / "README.md"
    content = readme_with_installations(readme.read_text(encoding="utf-8"), analytics, configs, refreshed)
    marker = "<!-- installations-graph -->"
    graph = f'{marker}\n\n![Installation evolution over the last year](.github/data/installations.svg)\n'
    content = re.sub(r"<!-- installations-graph -->.*?(?=\n### )", graph, content, flags=re.DOTALL)
    if marker not in content:
        content = content.replace("<!-- installations:end -->", "<!-- installations:end -->\n\n" + graph)
    readme.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    update_files(root, json.load(sys.stdin))
