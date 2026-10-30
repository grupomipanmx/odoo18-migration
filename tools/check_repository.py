"""Read-only, standard-library checks. Does not import Odoo or connect to a DB."""
import ast
import csv
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    python_files = sorted(ROOT.rglob("*.py"))
    xml_files = sorted(ROOT.rglob("*.xml"))
    for path in python_files:
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except (SyntaxError, UnicodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    for path in xml_files:
        try:
            ET.parse(path)
        except ET.ParseError as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    modules = {}
    for path in sorted(ROOT.rglob("__manifest__.py")):
        manifest = ast.literal_eval(path.read_text(encoding="utf-8"))
        module = path.parent
        for item in manifest.get("data", []):
            if not (module / item).is_file():
                errors.append(f"{module.name}: missing data file {item}")
            if Path(item).suffix == ".csv" and not item.startswith("security/"):
                errors.append(f"{module.name}: catalog CSV declared: {item}")
        for bundle, entries in manifest.get("assets", {}).items():
            for item in entries:
                if isinstance(item, str) and item.startswith(module.name + "/"):
                    if not list(ROOT.glob(item)):
                        errors.append(f"{module.name}: missing asset {bundle}: {item}")
        models = set()
        for source in (module / "models").glob("*.py"):
            for node in ast.walk(ast.parse(source.read_text(encoding="utf-8"))):
                if isinstance(node, ast.Assign):
                    if any(isinstance(t, ast.Name) and t.id == "_name" for t in node.targets):
                        models.add(ast.literal_eval(node.value))
        acl = module / "security" / "ir.model.access.csv"
        rows = []
        if acl.exists():
            with acl.open(encoding="utf-8", newline="") as stream:
                rows = list(csv.DictReader(stream))
            for row in rows:
                if row["model_id:id"] not in {"model_" + name.replace(".", "_") for name in models}:
                    errors.append(f"{acl.relative_to(ROOT)}: unresolved local model: {row['model_id:id']}")
                if not row["group_id:id"]:
                    errors.append(f"{acl.relative_to(ROOT)}: ungrouped ACL {row['id']}")
                for key in ("perm_read", "perm_write", "perm_create", "perm_unlink"):
                    if row[key] not in ("0", "1"):
                        errors.append(f"{acl.relative_to(ROOT)}: invalid {key}")
        modules[module.name] = {
            "license_declared": manifest.get("license"),
            "depends": manifest.get("depends", []),
            "data_files": len(manifest.get("data", [])), "acl_rows": len(rows),
            "external_dependencies_installed": "NOT_VERIFIED",
        }
    tests = []
    for path in ROOT.glob("*/tests/test_*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        tests.extend(f"{path.relative_to(ROOT).as_posix()}::{n.name}"
                     for n in ast.walk(tree)
                     if isinstance(n, ast.FunctionDef) and n.name.startswith("test_"))
    result = {
        "python": sys.version.split()[0], "python_files": len(python_files),
        "xml_files": len(xml_files), "modules": modules,
        "odoo_tests_discovered_not_executed": tests,
        "runtime": {key: importlib.util.find_spec(key) is not None for key in ("odoo", "psycopg2", "lxml")},
        "executables": {key: shutil.which(key) for key in ("docker", "psql", "postgres", "pg_ctl")},
        "errors": errors, "static_result": "FAIL" if errors else "PASS",
        "installation_upgrade_result": "NOT_RUN",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
