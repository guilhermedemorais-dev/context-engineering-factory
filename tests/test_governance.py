from __future__ import annotations

from pathlib import Path

from securecontextfactory import cli


def test_parse_plan_approval() -> None:
    txt = "\n".join(
        [
            "## Aprovação do Plan",
            "- Status: APPROVED",
            "- Aprovador: someone",
            "- Data: 2026-02-17",
            "",
        ]
    )
    status, approver = cli._parse_plan_approval(txt)
    assert status == "APPROVED"
    assert approver == "someone"


def test_parse_gaps_and_detect_blocking_open(tmp_path: Path) -> None:
    factory_root = tmp_path / "factory-workflow"
    (factory_root / "context" / "core").mkdir(parents=True, exist_ok=True)
    gaps_path = factory_root / "context" / "core" / "gaps.md"

    gaps_path.write_text(
        "\n".join(
            [
                "# Gaps",
                "",
                "## Gaps Abertos",
                "",
                "### GAP-TEST-001",
                "- ID: GAP-TEST-001",
                "- Data: 2026-02-17",
                "- Descricao: x",
                "- Impacto: BLOQUEIA",
                "- Owner: t",
                "- Status: OPEN",
                "",
                "### GAP-TEST-002",
                "- ID: GAP-TEST-002",
                "- Data: 2026-02-17",
                "- Descricao: y",
                "- Impacto: DOCUMENTACAO",
                "- Owner: t",
                "- Status: OPEN",
                "",
                "### GAP-TEST-003",
                "- ID: GAP-TEST-003",
                "- Data: 2026-02-17",
                "- Descricao: z",
                "- Impacto: BLOQUEIA",
                "- Owner: t",
                "- Status: DECIDED",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    blocking = cli._blocking_open_gaps(factory_root)
    assert blocking == ["GAP-TEST-001"]

