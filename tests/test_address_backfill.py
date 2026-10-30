"""Exercise the actual post script against synthetic SQLite memory fixtures.

This verifies backfill logic, not PostgreSQL/registry/Upgrade compatibility.
"""
from pathlib import Path
import runpy
import sqlite3
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "direccion_mx/migrations/18.0.2.1.0/post-migrate.py"


class TestAddressBackfill(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.addCleanup(self.connection.close)
        self.cr = self.connection.cursor()
        self.cr.executescript("""
            CREATE TABLE res_country_state_ciudad (id INTEGER PRIMARY KEY, name TEXT);
            CREATE TABLE res_country_state_municipio_colonia (id INTEGER PRIMARY KEY, name TEXT);
            CREATE TABLE res_partner (id INTEGER PRIMARY KEY, ciudad_id INTEGER, municipio_id INTEGER,
                colonia_id INTEGER, city TEXT, l10n_mx_edi_colony TEXT, supplier_rank INTEGER, active INTEGER);
            INSERT INTO res_country_state_ciudad VALUES (7, 'Ciudad catálogo');
            INSERT INTO res_country_state_municipio_colonia VALUES (8, 'Colonia catálogo');
            INSERT INTO res_partner VALUES (10, 7, 6, 8, NULL, NULL, 1, 0);
            INSERT INTO res_partner VALUES (11, 7, 6, 8, 'Ciudad histórica', 'Colonia histórica', 0, 1);
            INSERT INTO res_partner VALUES (12, 7, 6, 8, '', '', 0, 1);
        """)
        self.migrate = runpy.run_path(str(SCRIPT))["migrate"]

    def test_backfill_materializes_names_without_changing_links_or_supplier(self):
        before = self.cr.execute("SELECT id,ciudad_id,municipio_id,colonia_id,supplier_rank,active FROM res_partner ORDER BY id").fetchall()
        self.migrate(self.cr, "14.1")
        self.assertEqual(self.cr.execute("SELECT city,l10n_mx_edi_colony FROM res_partner WHERE id=10").fetchone(),
                         ("Ciudad catálogo", "Colonia catálogo"))
        self.assertEqual(self.cr.execute("SELECT id,ciudad_id,municipio_id,colonia_id,supplier_rank,active FROM res_partner ORDER BY id").fetchall(), before)

    def test_existing_text_and_explicit_empty_values_survive(self):
        self.migrate(self.cr, "14.1")
        rows = self.cr.execute("SELECT city,l10n_mx_edi_colony FROM res_partner WHERE id IN (11,12) ORDER BY id").fetchall()
        self.assertEqual(rows, [("Ciudad histórica", "Colonia histórica"), ("", "")])

    def test_second_execution_is_idempotent(self):
        self.migrate(self.cr, "14.1")
        before = self.cr.execute("SELECT * FROM res_partner ORDER BY id").fetchall()
        self.migrate(self.cr, "18.0.2.0.0")
        self.assertEqual(self.cr.execute("SELECT * FROM res_partner ORDER BY id").fetchall(), before)
