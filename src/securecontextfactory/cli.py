from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

import yaml


app = typer.Typer(add_completion=False, no_args_is_help=True)
gap_app = typer.Typer(add_completion=False, no_args_is_help=True)
hook_app = typer.Typer(add_completion=False, no_args_is_help=True)
squad_app = typer.Typer(add_completion=False, no_args_is_help=True)
project_app = typer.Typer(add_completion=False, no_args_is_help=True)
app.add_typer(gap_app, name="gap")
app.add_typer(hook_app, name="hook")
app.add_typer(squad_app, name="squad")
app.add_typer(project_app, name="project")

console = Console()


BLOCKED_EXIT_CODE = 2


@dataclass(frozen=True)
class Gap:
    gap_id: str
    status: str
    impact: str


STATUS_RE = re.compile(r"^\s*-\s*Status:\s*(?P<status>[A-Z_]+)\s*$")
IMPACT_RE = re.compile(r"^\s*-\s*Impacto:\s*(?P<impact>.+?)\s*$")
ID_RE = re.compile(r"^\s*-\s*ID:\s*(?P<id>.+?)\s*$")

PLAN_STATUS_RE = re.compile(r"^\s*-\s*Status:\s*(?P<status>[A-Z_]+)\s*$", re.MULTILINE)
PLAN_APPROVER_RE = re.compile(r"^\s*-\s*Aprovador:\s*(?P<approver>.+?)\s*$", re.MULTILINE)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_workspace(workspace: Path) -> Path:
    return workspace.resolve()


def _factory_root(workspace: Path) -> Path:
    root = workspace / "factory-workflow"
    if not root.exists():
        raise typer.BadParameter(f"factory-workflow not found under workspace: {workspace}")
    return root


def _runtime_cli_path(factory_root: Path) -> Path:
    return factory_root / "bots" / "runtime" / "cli.py"


def _audit_log_path(factory_root: Path) -> Path:
    # Gitignored by default.
    return factory_root / "bots" / "runtime" / "out" / "securecontextfactory.events.jsonl"


def _append_audit(factory_root: Path, event: dict) -> None:
    p = _audit_log_path(factory_root)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": _now_iso(), **event}, ensure_ascii=False) + "\n")


def _gaps_path(factory_root: Path) -> Path:
    return factory_root / "context" / "core" / "gaps.md"


def _squads_dir(factory_root: Path) -> Path:
    return factory_root / "squads"


def _find_squad_file(factory_root: Path, squad: str) -> Optional[Path]:
    d = _squads_dir(factory_root)
    for ext in ("yaml", "yml"):
        p = d / f"{squad}.{ext}"
        if p.exists():
            return p
    return None


def _load_yaml(path: Path) -> dict:
    data = yaml.safe_load(_read_text(path)) or {}
    if not isinstance(data, dict):
        raise ValueError(f"invalid yaml root (expected mapping): {path}")
    return data


def _default_squad_template(name: str) -> dict:
    return {
        "name": name,
        "description": "Governed squad template (manager only).",
        "manager": {
            "role": f"{name} manager",
            "goal": "Deliver tasks under non-negotiable governance (no assumptions, audit everything).",
            "backstory": "You operate under SecureContextFactory policy-engine and must stop on gaps.",
        },
        "expected_output": "Deliverable with steps, evidence, and no missing gaps.",
        "process": "sequential",
    }


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _parse_gaps(gaps_text: str) -> list[Gap]:
    gaps: list[Gap] = []
    current_id: Optional[str] = None
    current_status: Optional[str] = None
    current_impact: Optional[str] = None

    for raw in gaps_text.splitlines():
        line = raw.rstrip("\n")
        if line.strip().startswith("### "):
            # Flush previous block if possible
            if current_id and current_status and current_impact:
                gaps.append(Gap(gap_id=current_id, status=current_status, impact=current_impact))
            current_id = None
            current_status = None
            current_impact = None
            continue

        m = ID_RE.match(line)
        if m:
            current_id = m.group("id").strip()
            continue

        m = STATUS_RE.match(line)
        if m:
            current_status = m.group("status").strip().upper()
            continue

        m = IMPACT_RE.match(line)
        if m:
            current_impact = m.group("impact").strip()
            continue

    if current_id and current_status and current_impact:
        gaps.append(Gap(gap_id=current_id, status=current_status, impact=current_impact))
    return gaps


def _blocking_open_gaps(factory_root: Path) -> list[str]:
    p = _gaps_path(factory_root)
    if not p.exists():
        return ["gaps.md missing"]
    gaps = _parse_gaps(_read_text(p))
    out: list[str] = []
    for g in gaps:
        if g.status == "OPEN" and "BLOQUEIA" in g.impact.upper():
            out.append(g.gap_id)
    # de-dup preserving order
    seen: set[str] = set()
    dedup: list[str] = []
    for x in out:
        if x in seen:
            continue
        seen.add(x)
        dedup.append(x)
    return dedup


def _plan_path(factory_root: Path, feature: str) -> Path:
    # Runtime canonical path (see factory-workflow/bots/runtime/shared/autopilot.py).
    return factory_root / "docs" / "autopilot" / feature / "plan.md"


def _parse_plan_approval(plan_text: str) -> tuple[str, Optional[str]]:
    status_m = PLAN_STATUS_RE.search(plan_text)
    approver_m = PLAN_APPROVER_RE.search(plan_text)
    status = status_m.group("status").strip().upper() if status_m else "UNKNOWN"
    approver = approver_m.group("approver").strip() if approver_m else None
    return status, approver


def _is_plan_approved(plan_path: Path) -> bool:
    if not plan_path.exists():
        return False
    status, _ = _parse_plan_approval(_read_text(plan_path))
    return status == "APPROVED"


def _require_no_blocking_gaps(factory_root: Path) -> None:
    blocking = _blocking_open_gaps(factory_root)
    if blocking:
        _append_audit(factory_root, {"event": "blocked_by_gaps", "gaps": blocking})
        console.print(f"[red]BLOCKED[/red] blocking gaps: {', '.join(blocking)}")
        raise typer.Exit(BLOCKED_EXIT_CODE)


def _require_plan_approved(factory_root: Path, feature: str) -> Path:
    plan = _plan_path(factory_root, feature)
    if not _is_plan_approved(plan):
        _append_audit(factory_root, {"event": "blocked_by_plan", "feature": feature, "plan": str(plan)})
        console.print("[red]BLOCKED[/red] plan not approved.")
        console.print(f"expected: {plan}")
        raise typer.Exit(BLOCKED_EXIT_CODE)
    return plan


def _run_runtime(factory_root: Path, args: list[str], *, workspace: Path) -> int:
    cli = _runtime_cli_path(factory_root)
    if not cli.exists():
        console.print(f"[red]runtime CLI not found:[/red] {cli}")
        return BLOCKED_EXIT_CODE

    cmd = [sys.executable, str(cli), *args, "--workspace", str(workspace)]
    _append_audit(factory_root, {"event": "runtime_cmd", "cmd": cmd})
    proc = subprocess.run(cmd)
    return int(proc.returncode)


@app.command()
def init(
    workspace: Path = typer.Option(Path("."), "--workspace", "-w", help="Project workspace root"),
    create_env: bool = typer.Option(True, "--env/--no-env", help="Create .env placeholders"),
    create_mcp: bool = typer.Option(True, "--mcp/--no-mcp", help="Create factory-workflow/config/mcp.toml"),
    non_interactive: bool = typer.Option(False, "--non-interactive", help="Do not prompt"),
) -> None:
    """
    Bootstrap SecureContextFactory in the current workspace (env + mcp + basic sanity).
    """
    workspace = _resolve_workspace(workspace)
    factory_root = _factory_root(workspace)

    _append_audit(factory_root, {"event": "init", "workspace": str(workspace)})

    if create_env:
        env_path = workspace / ".env"
        if env_path.exists() and not non_interactive:
            if not Confirm.ask(".env exists. Keep it (recommended)?"):
                env_path.unlink()
        if not env_path.exists():
            env_path.write_text(
                "\n".join(
                    [
                        "# SecureContextFactory env",
                        "CONTEXT7_TOKEN=",
                        "GITHUB_TOKEN=",
                        "HUGGINGFACE_TOKEN=",
                        "STACKOVERFLOW_KEY=",
                        "PLAYWRIGHT_ENDPOINT=http://localhost:3000",
                        "CHROME_DEVTOOLS_ENDPOINT=http://localhost:9222",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            console.print(f"created: {env_path}")

    if create_mcp:
        mcp_path = factory_root / "config" / "mcp.toml"
        if not mcp_path.exists():
            template = factory_root / "config" / "mcp.example.toml"
            if not template.exists():
                console.print(f"[red]missing MCP template:[/red] {template}")
                raise typer.Exit(BLOCKED_EXIT_CODE)
            mcp_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(template, mcp_path)
            console.print(f"created: {mcp_path}")

    console.print("[bold]init OK[/bold]")


@app.command()
def install(
    workspace: Path = typer.Option(Path("."), "--workspace", "-w"),
    codex_skills: bool = typer.Option(False, "--codex-skills", help="Install skills to ~/.codex/skills"),
    all_skills: bool = typer.Option(False, "--all-skills", help="Install all skills from library/skills"),
    kickconfig: bool = typer.Option(False, "--kickconfig", help="Run MCP kickconfig wizard"),
    non_interactive: bool = typer.Option(False, "--non-interactive"),
) -> None:
    """
    Install wizard: skills + MCP config (optional).
    """
    workspace = _resolve_workspace(workspace)
    factory_root = _factory_root(workspace)
    _append_audit(factory_root, {"event": "install", "workspace": str(workspace)})

    if kickconfig:
        rc = _run_runtime(factory_root, ["kickconfig", "--factory", str(factory_root)], workspace=workspace)
        if rc != 0:
            raise typer.Exit(rc)

    if codex_skills:
        src = workspace / "library" / "skills"
        if not src.exists():
            console.print(f"[red]skills source not found:[/red] {src}")
            raise typer.Exit(BLOCKED_EXIT_CODE)

        codex_home = Path.home() / ".codex" / "skills"
        codex_home.mkdir(parents=True, exist_ok=True)

        if all_skills:
            to_copy: Iterable[Path] = [p for p in src.iterdir() if p.is_dir()]
        else:
            to_copy = [src / "factory-dev-workflow"]

        for skill_dir in to_copy:
            if not skill_dir.exists():
                console.print(f"[yellow]skip missing:[/yellow] {skill_dir}")
                continue
            dst = codex_home / skill_dir.name
            if dst.exists():
                if non_interactive:
                    shutil.rmtree(dst)
                else:
                    if Confirm.ask(f"overwrite existing skill {dst.name}?"):
                        shutil.rmtree(dst)
                    else:
                        continue
            shutil.copytree(skill_dir, dst)
            console.print(f"installed: {dst}")

    console.print("[bold]install OK[/bold]")


@app.command("autopilot-start")
def autopilot_start(
    workspace: Path = typer.Option(Path("."), "--workspace", "-w"),
    feature: str = typer.Option("current", "--feature"),
    config: Path = typer.Option(
        Path("factory-workflow/bots/runtime/config.yaml"),
        "--config",
        help="Runtime config path (workspace-relative or absolute)",
    ),
    factory: Path = typer.Option(Path("factory-workflow"), "--factory", help="Factory root (workspace-relative)"),
    sync_docs: bool = typer.Option(True, "--sync-docs/--no-sync-docs", help="Sync docs.prd -> docs before run"),
) -> None:
    """
    Queue context-sync + planner (creates DRAFT plan).
    """
    workspace = _resolve_workspace(workspace)
    factory_root = (workspace / factory).resolve()
    _require_no_blocking_gaps(factory_root)

    if sync_docs:
        src = workspace / "docs.prd"
        dst = workspace / "docs"
        required = ["prd.md", "tech.md", "ui-ux.md"]
        missing = [f for f in required if not (src / f).exists()]
        if missing:
            console.print(f"[red]BLOCKED[/red] missing PRD files in {src}: {', '.join(missing)}")
            raise typer.Exit(BLOCKED_EXIT_CODE)
        dst.mkdir(parents=True, exist_ok=True)
        for f in required:
            shutil.copyfile(src / f, dst / f)
        _append_audit(factory_root, {"event": "sync_docs", "src": str(src), "dst": str(dst), "files": required})

    args = ["autopilot-start", "--factory", str(factory_root), "--config", str((workspace / config).resolve()), "--feature", feature]
    rc = _run_runtime(factory_root, args, workspace=workspace)
    raise typer.Exit(rc)


@app.command("autopilot-build")
def autopilot_build(
    workspace: Path = typer.Option(Path("."), "--workspace", "-w"),
    feature: str = typer.Option("current", "--feature"),
    project: Path = typer.Option(..., "--project", help="Project path under /apps for dev bot"),
    with_e2e: bool = typer.Option(False, "--with-e2e", help="Include qa-e2e"),
    config: Path = typer.Option(Path("factory-workflow/bots/runtime/config.yaml"), "--config"),
    factory: Path = typer.Option(Path("factory-workflow"), "--factory"),
) -> None:
    """
    Queue dev + qa after plan APPROVED.
    """
    workspace = _resolve_workspace(workspace)
    factory_root = (workspace / factory).resolve()

    _require_no_blocking_gaps(factory_root)
    _require_plan_approved(factory_root, feature)

    args = [
        "autopilot-build",
        "--factory",
        str(factory_root),
        "--config",
        str((workspace / config).resolve()),
        "--feature",
        feature,
        "--project",
        str(project),
    ]
    if with_e2e:
        args.append("--with-e2e")
    rc = _run_runtime(factory_root, args, workspace=workspace)
    raise typer.Exit(rc)


@app.command("autopilot-graph")
def autopilot_graph(
    workspace: Path = typer.Option(Path("."), "--workspace", "-w"),
    feature: str = typer.Option("current", "--feature"),
    non_interactive: bool = typer.Option(False, "--non-interactive"),
) -> None:
    """
    Minimal stateful orchestrator (LangGraph optional) with gates as conditional nodes.
    """
    workspace = _resolve_workspace(workspace)
    factory_root = _factory_root(workspace)

    try:
        from langgraph.graph import START, StateGraph  # type: ignore
        from langgraph.checkpoint.sqlite import SqliteSaver  # type: ignore
    except Exception:
        console.print("LangGraph not installed. Install: pip install \"securecontextfactory[langgraph]\"")
        raise typer.Exit(BLOCKED_EXIT_CODE)

    def gate_context(state: dict) -> dict:
        blocking = _blocking_open_gaps(factory_root)
        _append_audit(factory_root, {"event": "gate_context", "feature": feature, "blocking": blocking})
        return {**state, "blocked": bool(blocking), "blocking_gaps": blocking}

    def ensure_plan(state: dict) -> dict:
        plan = _plan_path(factory_root, feature)
        plan.parent.mkdir(parents=True, exist_ok=True)
        if not plan.exists():
            plan.write_text(
                "\n".join(
                    [
                        f"# Plan — {feature}",
                        "",
                        "## Aprovação do Plan",
                        "- Status: DRAFT",
                        "- Aprovador: (pendente)",
                        "- Data: (pendente)",
                        "- Observações:",
                        "",
                        "## Escopo",
                        "### Inclui",
                        "-",
                        "",
                        "### Nao inclui",
                        "-",
                        "",
                        "## Plano de testes",
                        "-",
                        "",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            _append_audit(factory_root, {"event": "plan_created", "feature": feature, "plan": str(plan)})
        return {**state, "plan": str(plan)}

    def gate_plan(state: dict) -> dict:
        plan = Path(state["plan"])
        approved = _is_plan_approved(plan)
        if not approved and not non_interactive:
            console.print(f"plan pending approval: {plan}")
            if Confirm.ask("Approve plan now (will set Status: APPROVED)?"):
                txt = _read_text(plan)
                txt = txt.replace("- Status: DRAFT", "- Status: APPROVED")
                txt = txt.replace("- Aprovador: (pendente)", f"- Aprovador: {os.getenv('USER','human')}")
                txt = txt.replace("- Data: (pendente)", f"- Data: {datetime.now().date().isoformat()}")
                plan.write_text(txt, encoding="utf-8")
                approved = True
        _append_audit(factory_root, {"event": "gate_plan", "feature": feature, "approved": approved})
        return {**state, "blocked": not approved, "plan_approved": approved}

    builder = StateGraph(dict)
    builder.add_node("gate_context", gate_context)
    builder.add_node("ensure_plan", ensure_plan)
    builder.add_node("gate_plan", gate_plan)

    builder.add_edge(START, "gate_context")

    def route_after_context(state: dict) -> str:
        return "ensure_plan" if not state.get("blocked") else "__end__"

    builder.add_conditional_edges("gate_context", route_after_context, {"ensure_plan": "ensure_plan", "__end__": "__end__"})
    builder.add_edge("ensure_plan", "gate_plan")

    def route_after_plan(state: dict) -> str:
        return "__end__"

    builder.add_conditional_edges("gate_plan", route_after_plan, {"__end__": "__end__"})

    db_path = factory_root / "bots" / "runtime" / "out" / "securecontextfactory.checkpoints.sqlite"
    with SqliteSaver.from_conn_string(str(db_path)) as checkpointer:
        graph = builder.compile(checkpointer=checkpointer)
        result = graph.invoke({"feature": feature})
        console.print(f"[bold]graph done[/bold] keys={list(result.keys())}")


@app.command("run-squad")
def run_squad(
    squad: str = typer.Argument(..., help="Squad name"),
    task: str = typer.Option(..., "--task", help="Task description"),
    workspace: Path = typer.Option(Path("."), "--workspace", "-w"),
    feature: str = typer.Option("current", "--feature", help="Feature id for plan gating"),
) -> None:
    """
    Execute a squad/crew (CrewAI optional) with governance checks.
    """
    workspace = _resolve_workspace(workspace)
    factory_root = _factory_root(workspace)

    _require_no_blocking_gaps(factory_root)
    _require_plan_approved(factory_root, feature)

    try:
        from crewai import Agent, Crew, Process, Task  # type: ignore
    except Exception:
        console.print("CrewAI not installed. Install: pip install \"securecontextfactory[crewai]\"")
        raise typer.Exit(BLOCKED_EXIT_CODE)

    _append_audit(factory_root, {"event": "run_squad_start", "squad": squad, "feature": feature})

    squad_file = _find_squad_file(factory_root, squad)
    squad_def = _load_yaml(squad_file) if squad_file else _default_squad_template(squad)

    manager_def = squad_def.get("manager") or {}
    if not isinstance(manager_def, dict):
        manager_def = {}

    role = str(manager_def.get("role") or f"{squad} manager")
    goal = str(
        manager_def.get("goal")
        or "Deliver tasks under non-negotiable governance (no assumptions, audit everything)."
    )
    backstory = str(
        manager_def.get("backstory")
        or "You operate under SecureContextFactory policy-engine and must stop on gaps."
    )
    expected_output = str(
        squad_def.get("expected_output") or "Deliverable with steps, evidence, and no missing gaps."
    )

    process_name = str(squad_def.get("process") or "sequential").strip().lower()
    process = Process.sequential
    if process_name in {"hierarchical", "hierarchy"} and hasattr(Process, "hierarchical"):
        process = Process.hierarchical  # type: ignore[attr-defined]

    manager = Agent(role=role, goal=goal, backstory=backstory, verbose=True)
    t = Task(description=task, expected_output=expected_output, agent=manager)
    crew = Crew(agents=[manager], tasks=[t], process=process, verbose=True)
    crew.kickoff()

    _append_audit(
        factory_root,
        {
            "event": "run_squad_done",
            "squad": squad,
            "feature": feature,
            "squad_file": str(squad_file) if squad_file else None,
        },
    )
    console.print("[bold]run-squad done[/bold]")


@app.command()
def audit(
    workspace: Path = typer.Option(Path("."), "--workspace", "-w"),
    feature: str = typer.Option("current", "--feature"),
) -> None:
    """
    Quick governance audit (gaps + plan + key files).
    """
    workspace = _resolve_workspace(workspace)
    factory_root = _factory_root(workspace)

    index_path = factory_root / "context" / "INDEX.md"
    mcp_path = factory_root / "config" / "mcp.toml"
    plan = _plan_path(factory_root, feature)
    blocking = _blocking_open_gaps(factory_root)

    console.print(f"workspace: {workspace}")
    console.print(f"factory_root: {factory_root}")
    console.print(f"context index: {'OK' if index_path.exists() else 'MISSING'} ({index_path})")
    console.print(f"mcp config: {'OK' if mcp_path.exists() else 'MISSING'} ({mcp_path})")
    console.print(f"plan: {'APPROVED' if _is_plan_approved(plan) else 'NOT_APPROVED'} ({plan})")
    console.print(f"blocking gaps: {', '.join(blocking) if blocking else 'none'}")

    _append_audit(factory_root, {"event": "audit", "feature": feature, "blocking_gaps": blocking, "plan": str(plan)})

    if blocking:
        raise typer.Exit(BLOCKED_EXIT_CODE)


@gap_app.command("list")
def gap_list(
    workspace: Path = typer.Option(Path("."), "--workspace", "-w"),
) -> None:
    """
    List open blocking gaps.
    """
    workspace = _resolve_workspace(workspace)
    factory_root = _factory_root(workspace)
    blocking = _blocking_open_gaps(factory_root)
    if not blocking:
        console.print("no blocking gaps")
        return
    for g in blocking:
        console.print(g)


@gap_app.command("add")
def gap_add(
    gap_id: str = typer.Option(..., "--id", help="Gap id (e.g. GAP-SEC-001)"),
    desc: str = typer.Option(..., "--desc", help="Short description"),
    impacto: str = typer.Option("BLOQUEIA", "--impacto", help="Impact (e.g. BLOQUEIA)"),
    owner: str = typer.Option("TBD", "--owner"),
    workspace: Path = typer.Option(Path("."), "--workspace", "-w"),
) -> None:
    """
    Append a GAP to gaps.md with a required suggested solution.
    """
    workspace = _resolve_workspace(workspace)
    factory_root = _factory_root(workspace)
    p = _gaps_path(factory_root)
    if not p.exists():
        console.print(f"[red]missing gaps file:[/red] {p}")
        raise typer.Exit(BLOCKED_EXIT_CODE)

    suggestion = Prompt.ask("Suggested solution (required)").strip()
    if not suggestion:
        console.print("[red]suggested solution is required[/red]")
        raise typer.Exit(BLOCKED_EXIT_CODE)

    block_lines = [
        f"### {gap_id}",
        f"- ID: {gap_id}",
        f"- Data: {datetime.now().date().isoformat()}",
        f"- Descricao: {desc}",
        f"- Impacto: {impacto}",
        f"- Owner: {owner}",
        "- Status: OPEN",
        f"- **Sugestao de Solucao:** {suggestion}",
        "",
    ]

    lines = _read_text(p).splitlines(True)
    open_idx = next((i for i, l in enumerate(lines) if l.strip() == "## Gaps Abertos"), None)
    resolved_idx = next((i for i, l in enumerate(lines) if l.strip() == "## Gaps Resolvidos"), None)

    if open_idx is None or resolved_idx is None or open_idx >= resolved_idx:
        # Fallback: append
        if lines and not lines[-1].endswith("\n"):
            lines[-1] = lines[-1] + "\n"
        lines.append("\n" + "\n".join(block_lines))
    else:
        insert_at = open_idx + 1
        # Skip a single blank line after header if present.
        if insert_at < len(lines) and lines[insert_at].strip() == "":
            insert_at += 1

        # Remove placeholder line if present.
        if insert_at < len(lines) and "(sem gaps abertos no momento)" in lines[insert_at]:
            del lines[insert_at]
            if insert_at < len(lines) and lines[insert_at].strip() == "":
                del lines[insert_at]

        payload = "\n".join(block_lines)
        if not payload.endswith("\n"):
            payload += "\n"
        lines.insert(insert_at, payload)

    p.write_text("".join(lines), encoding="utf-8")
    _append_audit(factory_root, {"event": "gap_add", "id": gap_id})
    console.print(f"added: {gap_id}")


@gap_app.command("close")
def gap_close(
    gap_id: str = typer.Option(..., "--id", help="Gap id"),
    status: str = typer.Option("DECIDED", "--status", help="DECIDED or DEFERRED"),
    workspace: Path = typer.Option(Path("."), "--workspace", "-w"),
) -> None:
    """
    Update a GAP status in gaps.md (simple text replace).
    """
    status = status.strip().upper()
    if status not in {"DECIDED", "DEFERRED"}:
        raise typer.BadParameter("status must be DECIDED or DEFERRED")

    workspace = _resolve_workspace(workspace)
    factory_root = _factory_root(workspace)
    p = _gaps_path(factory_root)
    txt = _read_text(p)

    if gap_id not in txt:
        console.print(f"[red]gap id not found:[/red] {gap_id}")
        raise typer.Exit(BLOCKED_EXIT_CODE)

    # Best-effort: replace first "- Status:" after the gap header.
    parts = txt.split(f"### {gap_id}")
    if len(parts) < 2:
        console.print(f"[red]gap header not found:[/red] ### {gap_id}")
        raise typer.Exit(BLOCKED_EXIT_CODE)

    head = parts[0]
    rest = f"### {gap_id}" + parts[1]

    lines = rest.splitlines(True)
    updated = False
    seen_header = False
    for i, line in enumerate(lines):
        if not seen_header and line.strip().startswith("### "):
            seen_header = True
            continue
        if seen_header and line.strip().startswith("- Status:"):
            lines[i] = f"- Status: {status}\n"
            updated = True
            break
        if seen_header and line.strip().startswith("### ") and i > 0:
            break

    if not updated:
        console.print("[red]failed to update status (no - Status: line found)[/red]")
        raise typer.Exit(BLOCKED_EXIT_CODE)

    new_txt = head + "".join(lines)
    p.write_text(new_txt, encoding="utf-8")
    _append_audit(factory_root, {"event": "gap_close", "id": gap_id, "status": status})
    console.print(f"updated: {gap_id} -> {status}")


@app.command()
def doctor(
    workspace: Path = typer.Option(Path("."), "--workspace", "-w"),
    feature: str = typer.Option("current", "--feature"),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON"),
) -> None:
    """
    Environment + governance diagnostics (no secret leakage).
    """
    workspace = _resolve_workspace(workspace)

    results: list[dict] = []

    def add(level: str, check: str, detail: str, action: Optional[str] = None) -> None:
        results.append({"level": level, "check": check, "detail": detail, "action": action})

    # Python / venv
    py_ok = sys.version_info >= (3, 11)
    add(
        "OK" if py_ok else "ERROR",
        "python",
        f"{sys.version.split()[0]} ({sys.executable})",
        "Install Python 3.11+." if not py_ok else None,
    )

    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    add(
        "OK" if in_venv else "WARN",
        "venv",
        "active" if in_venv else "not active",
        "Use a virtualenv for isolation." if not in_venv else None,
    )

    # Workspace / factory root
    try:
        factory_root = _factory_root(workspace)
        add("OK", "factory_root", str(factory_root))
    except Exception as exc:
        add("ERROR", "factory_root", str(exc))
        factory_root = None  # type: ignore[assignment]

    if factory_root is not None:
        # Key files
        index_path = factory_root / "context" / "INDEX.md"
        add("OK" if index_path.exists() else "ERROR", "context_index", str(index_path))

        tooling_mcp = factory_root / "context" / "tooling" / "mcp-policy.md"
        tooling_rt = factory_root / "context" / "tooling" / "runtime.md"
        add("OK" if tooling_mcp.exists() else "ERROR", "mcp_policy", str(tooling_mcp))
        add("OK" if tooling_rt.exists() else "ERROR", "runtime_policy", str(tooling_rt))

        # Blocking gaps
        blocking = _blocking_open_gaps(factory_root)
        if blocking:
            add("ERROR", "gaps", f"blocking open gaps: {', '.join(blocking)}", "Close or defer blocking gaps.")
        else:
            add("OK", "gaps", "no blocking open gaps")

        # Plan approval (for execution)
        plan = _plan_path(factory_root, feature)
        if not plan.exists():
            add("WARN", "plan", f"missing: {plan}", "Run autopilot-start to generate a DRAFT plan.")
        else:
            add(
                "OK" if _is_plan_approved(plan) else "WARN",
                "plan",
                f"{'APPROVED' if _is_plan_approved(plan) else 'NOT_APPROVED'}: {plan}",
                "Set Status: APPROVED in plan.md before autopilot-build/run-squad." if not _is_plan_approved(plan) else None,
            )

        # Env + MCP config (no value printing)
        env_path = workspace / ".env"
        add(
            "OK" if env_path.exists() else "WARN",
            "env_file",
            str(env_path),
            "Run securecontextfactory init to create .env placeholders." if not env_path.exists() else None,
        )

        mcp_path = factory_root / "config" / "mcp.toml"
        add(
            "OK" if mcp_path.exists() else "WARN",
            "mcp_config",
            str(mcp_path),
            "Run securecontextfactory init or securecontextfactory install --kickconfig." if not mcp_path.exists() else None,
        )

        # PRD files
        prd_dir = workspace / "docs.prd"
        required_prd = [prd_dir / "prd.md", prd_dir / "tech.md", prd_dir / "ui-ux.md"]
        missing_prd = [str(p) for p in required_prd if not p.exists()]
        add(
            "OK" if not missing_prd else "WARN",
            "docs_prd",
            "ok" if not missing_prd else f"missing: {', '.join(missing_prd)}",
            "Fill docs.prd/ templates (prd/tech/ui-ux)." if missing_prd else None,
        )

        # Runtime deps presence (optional)
        try:
            import langgraph  # type: ignore  # noqa: F401

            add("OK", "extra_langgraph", "installed")
        except Exception:
            add("WARN", "extra_langgraph", "not installed", "pip install \"securecontextfactory[langgraph]\"")

        try:
            import crewai  # type: ignore  # noqa: F401

            add("OK", "extra_crewai", "installed")
        except Exception:
            add("WARN", "extra_crewai", "not installed", "pip install \"securecontextfactory[crewai]\"")

    if json_output:
        print(json.dumps({"workspace": str(workspace), "feature": feature, "results": results}, ensure_ascii=False, indent=2))
        raise typer.Exit(0)

    table = Table(title="SecureContextFactory doctor")
    table.add_column("Level", style="bold")
    table.add_column("Check")
    table.add_column("Detail")
    table.add_column("Action")

    any_error = False
    for r in results:
        level = str(r["level"])
        if level == "ERROR":
            any_error = True
        style = "red" if level == "ERROR" else ("yellow" if level == "WARN" else "green")
        table.add_row(f"[{style}]{level}[/{style}]", str(r["check"]), str(r["detail"]), str(r.get("action") or ""))

    console.print(table)
    raise typer.Exit(BLOCKED_EXIT_CODE if any_error else 0)


def _upsert_marked_block(existing: str, *, begin: str, end: str, block: str) -> str:
    if begin in existing and end in existing and existing.index(begin) < existing.index(end):
        pre = existing.split(begin, 1)[0]
        post = existing.split(end, 1)[1]
        return pre + begin + "\n" + block.rstrip() + "\n" + end + post

    # Append at end
    s = existing.rstrip()
    if s:
        s += "\n\n"
    return s + begin + "\n" + block.rstrip() + "\n" + end + "\n"


def _install_agents_md(workspace: Path) -> Path:
    path = workspace / "AGENTS.md"
    begin = "<!-- SECURECONTEXTFACTORY:BEGIN -->"
    end = "<!-- SECURECONTEXTFACTORY:END -->"
    block = "\n".join(
        [
            "# SecureContextFactory Agent Instructions",
            "",
            "Non-negotiables:",
            "- Read `factory-workflow/context/INDEX.md` in order.",
            "- Follow RPI: Research -> Plan -> Implement.",
            "- If anything is missing/ambiguous: add a GAP in `factory-workflow/context/core/gaps.md` with a suggested solution and STOP.",
            "- No code changes without an approved plan (`Status: APPROVED`).",
            "- No deploy/release without QA evidence; no destructive actions without explicit human approval.",
            "",
            "Quick commands:",
            "- `securecontextfactory doctor`",
            "- `securecontextfactory autopilot-start --feature current`",
            "- `python factory-workflow/bots/runtime/cli.py daemon --workspace .`",
            "- approve plan in `factory-workflow/docs/autopilot/<feature>/plan.md`",
            "- `securecontextfactory autopilot-build --feature <feature> --project apps/<project>`",
            "",
        ]
    )
    existing = _read_text(path) if path.exists() else ""
    path.write_text(_upsert_marked_block(existing, begin=begin, end=end, block=block), encoding="utf-8")
    return path


def _install_cursorrules(workspace: Path) -> Path:
    path = workspace / ".cursorrules"
    begin = "# SECURECONTEXTFACTORY:BEGIN"
    end = "# SECURECONTEXTFACTORY:END"
    block = "\n".join(
        [
            "You are operating under SecureContextFactory governance.",
            "- Read factory-workflow/context/INDEX.md in order.",
            "- RPI is mandatory. No implementation without plan APPROVED.",
            "- If missing info: open GAP with suggested solution and STOP.",
            "- No destructive actions / prod deploy without explicit human approval.",
        ]
    )
    existing = _read_text(path) if path.exists() else ""
    path.write_text(_upsert_marked_block(existing, begin=begin, end=end, block=block), encoding="utf-8")
    return path


def _install_vscode_tasks(workspace: Path) -> Path:
    vscode_dir = workspace / ".vscode"
    vscode_dir.mkdir(parents=True, exist_ok=True)
    path = vscode_dir / "tasks.json"

    desired_inputs = [
        {"id": "scf_feature", "type": "promptString", "description": "Feature id", "default": "current"},
        {"id": "scf_project", "type": "promptString", "description": "Project path (relative)", "default": "apps/<project>"},
    ]

    desired_tasks = [
        {
            "label": "SecureContextFactory: Doctor",
            "type": "shell",
            "command": "securecontextfactory doctor --feature ${input:scf_feature}",
            "problemMatcher": [],
        },
        {"label": "SecureContextFactory: Init", "type": "shell", "command": "securecontextfactory init", "problemMatcher": []},
        {
            "label": "SecureContextFactory: Install (kickconfig)",
            "type": "shell",
            "command": "securecontextfactory install --kickconfig",
            "problemMatcher": [],
        },
        {
            "label": "SecureContextFactory: Autopilot Start",
            "type": "shell",
            "command": "securecontextfactory autopilot-start --feature ${input:scf_feature}",
            "problemMatcher": [],
        },
        {
            "label": "SecureContextFactory: Daemon",
            "type": "shell",
            "command": "python factory-workflow/bots/runtime/cli.py daemon --workspace .",
            "problemMatcher": [],
        },
        {
            "label": "SecureContextFactory: Autopilot Build",
            "type": "shell",
            "command": "securecontextfactory autopilot-build --feature ${input:scf_feature} --project ${input:scf_project}",
            "problemMatcher": [],
        },
        {
            "label": "SecureContextFactory: Audit",
            "type": "shell",
            "command": "securecontextfactory audit --feature ${input:scf_feature}",
            "problemMatcher": [],
        },
    ]

    data = {"version": "2.0.0", "tasks": [], "inputs": []}
    if path.exists():
        try:
            data = json.loads(_read_text(path))
        except Exception:
            # Keep user's file intact and create a new one.
            backup = path.with_suffix(".json.bak")
            shutil.copyfile(path, backup)
            data = {"version": "2.0.0", "tasks": [], "inputs": []}

    tasks = list(data.get("tasks") or [])
    inputs = list(data.get("inputs") or [])

    def upsert_by_key(items: list[dict], key: str, new_item: dict) -> None:
        for i, it in enumerate(items):
            if isinstance(it, dict) and it.get(key) == new_item.get(key):
                items[i] = {**it, **new_item}
                return
        items.append(new_item)

    for inp in desired_inputs:
        upsert_by_key(inputs, "id", inp)

    for t in desired_tasks:
        upsert_by_key(tasks, "label", t)

    data["version"] = data.get("version") or "2.0.0"
    data["tasks"] = tasks
    data["inputs"] = inputs

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


@hook_app.command("install")
def hook_install(
    target: str = typer.Argument(..., help="vscode | agents | cursor | all"),
    workspace: Path = typer.Option(Path("."), "--workspace", "-w"),
) -> None:
    """
    Install workspace hooks (idempotent).
    """
    workspace = _resolve_workspace(workspace)

    installed: list[Path] = []
    t = target.strip().lower()
    if t in {"all", "agents"}:
        installed.append(_install_agents_md(workspace))
    if t in {"all", "cursor"}:
        installed.append(_install_cursorrules(workspace))
    if t in {"all", "vscode"}:
        installed.append(_install_vscode_tasks(workspace))

    if not installed:
        console.print("[red]unknown target[/red] (expected: vscode | agents | cursor | all)")
        raise typer.Exit(BLOCKED_EXIT_CODE)

    for p in installed:
        console.print(f"installed: {p}")


@squad_app.command("list")
def squad_list(
    workspace: Path = typer.Option(Path("."), "--workspace", "-w"),
) -> None:
    """
    List squads defined in factory-workflow/squads/*.yml.
    """
    workspace = _resolve_workspace(workspace)
    factory_root = _factory_root(workspace)
    d = _squads_dir(factory_root)
    if not d.exists():
        console.print("no squads directory yet. Create one with: securecontextfactory squad init <name>")
        raise typer.Exit(0)

    files = sorted([*d.glob("*.yml"), *d.glob("*.yaml")], key=lambda p: p.name)
    if not files:
        console.print("no squads found")
        raise typer.Exit(0)

    table = Table(title="Squads")
    table.add_column("Name", style="bold")
    table.add_column("Description")
    table.add_column("Path")
    for p in files:
        try:
            data = _load_yaml(p)
        except Exception:
            data = {}
        name = str(data.get("name") or p.stem)
        desc = str(data.get("description") or "")
        table.add_row(name, desc, str(p))
    console.print(table)


@squad_app.command("show")
def squad_show(
    squad: str = typer.Argument(..., help="Squad name"),
    workspace: Path = typer.Option(Path("."), "--workspace", "-w"),
) -> None:
    workspace = _resolve_workspace(workspace)
    factory_root = _factory_root(workspace)
    p = _find_squad_file(factory_root, squad)
    if not p:
        console.print(f"[red]squad not found:[/red] {squad}")
        raise typer.Exit(BLOCKED_EXIT_CODE)
    console.print(_read_text(p))


@squad_app.command("init")
def squad_init(
    squad: str = typer.Argument(..., help="Squad name"),
    workspace: Path = typer.Option(Path("."), "--workspace", "-w"),
    force: bool = typer.Option(False, "--force", help="Overwrite existing"),
    non_interactive: bool = typer.Option(False, "--non-interactive"),
) -> None:
    """
    Create a squad YAML template under factory-workflow/squads/.
    """
    workspace = _resolve_workspace(workspace)
    factory_root = _factory_root(workspace)
    d = _squads_dir(factory_root)
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{squad}.yaml"

    if path.exists() and not force:
        console.print(f"[red]already exists:[/red] {path} (use --force to overwrite)")
        raise typer.Exit(BLOCKED_EXIT_CODE)

    tpl = _default_squad_template(squad)
    if not non_interactive:
        tpl["description"] = Prompt.ask("description", default=str(tpl["description"]))
        mgr = tpl["manager"]
        mgr["role"] = Prompt.ask("manager.role", default=str(mgr["role"]))
        mgr["goal"] = Prompt.ask("manager.goal", default=str(mgr["goal"]))
        mgr["backstory"] = Prompt.ask("manager.backstory", default=str(mgr["backstory"]))
        tpl["expected_output"] = Prompt.ask("expected_output", default=str(tpl["expected_output"]))

    path.write_text(yaml.safe_dump(tpl, sort_keys=False), encoding="utf-8")
    console.print(f"created: {path}")


@project_app.command("init")
def project_init(
    name: str = typer.Argument(..., help="Project name (creates apps/<name>/)"),
    workspace: Path = typer.Option(Path("."), "--workspace", "-w"),
) -> None:
    """
    Scaffold a new project folder under apps/ and work artifacts under docs.fabrication.
    """
    workspace = _resolve_workspace(workspace)
    factory_root = _factory_root(workspace)

    apps_dir = workspace / "apps" / name
    apps_dir.mkdir(parents=True, exist_ok=True)
    readme = apps_dir / "README.md"
    if not readme.exists():
        readme.write_text(f"# {name}\n\nProject scaffolded by SecureContextFactory.\n", encoding="utf-8")

    work_dir = factory_root / "docs.fabrication" / "projects" / name / "work" / "current"
    work_dir.mkdir(parents=True, exist_ok=True)
    (work_dir / "research.md").write_text("# Research\n\n- Evidence:\n  -\n", encoding="utf-8")
    (work_dir / "plan.md").write_text(
        "\n".join(
            [
                f"# Plan — {name}/current",
                "",
                "## Aprovação do Plan",
                "- Status: DRAFT",
                "- Aprovador: (pendente)",
                "- Data: (pendente)",
                "- Observações:",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    console.print(f"apps: {apps_dir}")
    console.print(f"work: {work_dir}")
