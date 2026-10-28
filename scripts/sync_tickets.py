"""Create GitHub labels, milestones and issues from plan/tickets.yaml.

Idempotent: existing labels/milestones are reused, and tickets already in
plan/issue_map.json are skipped.

    uv run --with pyyaml scripts/sync_tickets.py
"""

import json
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "plan" / "tickets.yaml"
MAP = ROOT / "plan" / "issue_map.json"


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def repo() -> str:
    return gh("repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner").strip()


def sync_labels(labels: list[dict]) -> None:
    for label in labels:
        gh(
            "label",
            "create",
            label["name"],
            "--color",
            label["color"],
            "--description",
            label["description"],
            "--force",
        )


def sync_milestones(name: str, milestones: list[dict]) -> dict[str, str]:
    existing = json.loads(gh("api", f"repos/{name}/milestones?state=all&per_page=100"))
    titles = {m["title"] for m in existing}
    for m in milestones:
        if m["title"] not in titles:
            gh(
                "api",
                f"repos/{name}/milestones",
                "-f",
                f"title={m['title']}",
                "-f",
                f"description={m['goal']}",
            )
    return {m["id"]: m["title"] for m in milestones}


def issue_body(ticket: dict, issue_map: dict[str, int]) -> str:
    lines = [f"**ID:** {ticket['id']}", "", ticket["body"].strip(), "", "**Done when**"]
    lines += [f"- [ ] {d}" for d in ticket["done"]]
    if ticket.get("depends"):
        deps = [f"{d} (#{issue_map[d]})" if d in issue_map else d for d in ticket["depends"]]
        lines += ["", "**Depends on:** " + ", ".join(deps)]
    lines += ["", f"Source of truth: `plan/tickets.yaml` → {ticket['id']}."]
    return "\n".join(lines)


def main() -> None:
    plan = yaml.safe_load(PLAN.read_text())
    issue_map = json.loads(MAP.read_text()) if MAP.exists() else {}
    name = repo()
    sync_labels(plan["labels"])
    milestone_titles = sync_milestones(name, plan["milestones"])
    for ticket in plan["tickets"]:
        if ticket["id"] in issue_map:
            continue
        url = gh(
            "issue",
            "create",
            "--title",
            f"{ticket['id']} · {ticket['title']}",
            "--body",
            issue_body(ticket, issue_map),
            "--milestone",
            milestone_titles[ticket["milestone"]],
            *[a for label in ticket["labels"] for a in ("--label", label)],
        ).strip()
        issue_map[ticket["id"]] = int(url.rsplit("/", 1)[1])
        MAP.write_text(json.dumps(issue_map, indent=2) + "\n")
        print(f"{ticket['id']} → {url}")


if __name__ == "__main__":
    main()
