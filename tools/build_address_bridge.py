"""Build an optional same-name direccion_mx bridge, without database access.

    python tools/build_address_bridge.py <new-output.zip>

Use in place of the full addon ONLY in a disposable rehearsal. Never load both
copies on addons_path. Catalog models/fields/data declarations/migrations stay;
custom Python methods are excluded temporarily, not the model registration.
"""
import argparse
import ast
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def build(output):
    output = Path(output)
    source_root = ROOT / "direccion_mx"
    if source_root.resolve() in output.resolve().parents:
        raise ValueError("Write the bridge outside the addon source directory")
    # Exclusive creation: never overwrite an existing package or source file.
    with zipfile.ZipFile(output, mode="x", compression=zipfile.ZIP_DEFLATED) as archive:
        for source in sorted(source_root.rglob("*")):
            relative = source.relative_to(source_root)
            if not source.is_file() or "__pycache__" in relative.parts or "tests" in relative.parts:
                continue
            content = source.read_bytes()
            if relative.parts[0] == "models" and source.name != "__init__.py":
                tree = ast.parse(content.decode("utf-8"))
                for node in tree.body:
                    if isinstance(node, ast.ClassDef):
                        node.body = [item for item in node.body
                                     if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))]
                content = (ast.unparse(tree) + "\n").encode("utf-8")
            archive.writestr("direccion_mx/" + relative.as_posix(), content)
        archive.writestr("direccion_mx/BRIDGE_MODE.md", """# Temporary address bridge

Same technical name, models, tables and fields as the full 18.0.2.1.0 port.
No CSV loader, uninstall or SQL deletion. Pre/post validation/backfill scripts
remain included and require an approved disposable database and baseline.

Temporarily disabled: CP-aware search, catalog onchanges, server autofill,
consistency validation and extension of parent-to-child address synchronization.
Stored city/colony text and existing relations remain declared. Views/ACL remain
declared to avoid withdrawing XML records during the temporary update.

Manual address selections do not autofill; do not use for live operations.
Restore the full addon at the same path and restart/update only in a disposable
copy; compare snapshots again before accepting the recovery. Never add GMP or
uninstall direccion_mx. This bridge is untested in an Odoo runtime.
""")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    print(build(parser.parse_args().output))
