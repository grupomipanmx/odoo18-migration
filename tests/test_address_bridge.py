import ast
from pathlib import Path
import tempfile
import unittest
import zipfile

from tools.build_address_bridge import build, ROOT


class TestAddressBridge(unittest.TestCase):
    def test_bridge_preserves_all_field_and_table_declarations(self):
        with tempfile.TemporaryDirectory() as directory:
            output = build(Path(directory) / "bridge.zip")
            with zipfile.ZipFile(output) as archive:
                self.assertFalse(any("tests/" in name or "__pycache__" in name for name in archive.namelist()))
                for filename in ("address_catalog.py", "res_partner.py"):
                    before = ast.parse((ROOT / "direccion_mx" / "models" / filename).read_text(encoding="utf-8"))
                    after = ast.parse(archive.read("direccion_mx/models/" + filename))
                    assignments = lambda tree: [ast.dump(n, include_attributes=False) for n in ast.walk(tree)
                                                if isinstance(n, ast.ClassDef)
                                                for n in n.body if isinstance(n, ast.Assign)]
                    self.assertEqual(assignments(before), assignments(after))
                    self.assertFalse(any(isinstance(n, ast.FunctionDef) for n in ast.walk(after)))
                    compile(after, filename, "exec")
                self.assertIn("direccion_mx/migrations/18.0.2.1.0/pre-migrate.py", archive.namelist())
                self.assertEqual(archive.read("direccion_mx/__manifest__.py"),
                                 (ROOT / "direccion_mx/__manifest__.py").read_bytes())

    def test_existing_output_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "bridge.zip"
            output.write_bytes(b"keep this file")
            with self.assertRaises(FileExistsError):
                build(output)
            self.assertEqual(output.read_bytes(), b"keep this file")
