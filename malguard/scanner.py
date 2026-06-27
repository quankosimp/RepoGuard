from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterable, List

from malguard.models import Finding
from malguard.rules import ast_rules


EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "dist",
    "build",
}


def scan(path: str) -> list[Finding]:
    root = Path(path).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Scan target does not exist: {path}")

    py_files = _iter_python_files(root) if root.is_dir() else (
        [root] if root.suffix == ".py" else []
    )
    findings: list[Finding] = []
    for py_file in py_files:
        target = str(py_file.relative_to(root)) if root.is_dir() else str(py_file)
        findings.extend(_scan_file(py_file, target))
    return _dedupe(findings)


def _iter_python_files(root: Path) -> Iterable[Path]:
    for file in root.rglob("*.py"):
        if any(part in EXCLUDE_DIRS for part in file.parts):
            continue
        if file.is_file():
            yield file


def _scan_file(file: Path, display_path: str) -> list[Finding]:
    source = _read_text(file)
    try:
        tree = ast.parse(source, filename=str(file))
    except SyntaxError:
        return []
    findings: list[Finding] = []
    for rule in getattr(ast_rules, "RULES", [ast_rules.detect]):
        if callable(rule):
            findings.extend(rule(tree, display_path, source))
    return findings


def _read_text(file: Path) -> str:
    try:
        return file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return file.read_text(encoding="utf-8", errors="replace")


def _dedupe(findings: list[Finding]) -> list[Finding]:
    seen = set()
    out: list[Finding] = []
    for item in findings:
        key = (item.file, item.line, item.rule_id, item.title, item.snippet)
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out
