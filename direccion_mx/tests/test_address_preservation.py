from odoo import Command
from odoo.exceptions import AccessError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestAddressPreservation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.state = cls.env["res.country.state"].create({
            "name": "GMP Address Test", "code": "GMPADR", "country_id": cls.env.ref("base.mx").id,
        })
        cls.city = cls.env["res.country.state.ciudad"].create({"name": "Ciudad prueba", "state_id": cls.state.id})
        cls.municipality = cls.env["res.country.state.municipio"].create({
            "name": "Municipio prueba", "state_id": cls.state.id, "ciudad_id": cls.city.id,
        })
        cls.colony = cls.env["res.country.state.municipio.colonia"].create({
            "name": "Colonia prueba", "cp": "01234", "municipio_id": cls.municipality.id,
        })
        cls.postcode = cls.env["res.country.state.cp"].create({
            "name": "01234", "state_id": cls.state.id, "ciudad_id": cls.city.id,
            "municipio_id": cls.municipality.id,
        })

    def partner(self, **values):
        return self.env["res.partner"].create({"name": "Contacto prueba", **values})

    def test_legacy_tables_and_cp_definition(self):
        for name in ("res.country.state.cp", "res.country.state.ciudad",
                     "res.country.state.municipio", "res.country.state.municipio.colonia"):
            self.assertEqual(self.env[name]._table, name.replace(".", "_"))
        cp = self.env["res.country.state.cp"]
        self.assertEqual(cp._fields["name"].size, 128)
        self.assertFalse(cp._fields["name"].required)
        self.assertEqual(self.postcode.name, "01234")
        self.assertEqual(self.postcode.ciudad_id, self.city)
        self.assertEqual(self.postcode.municipio_id, self.municipality)
        self.assertEqual(self.postcode.state_id, self.state)

    def test_cp_optional_relations_and_existing_id_survive_edit(self):
        cp = self.env["res.country.state.cp"].create({"name": "00001"})
        old_id = cp.id
        cp.write({"municipio_id": self.municipality.id})
        self.env.invalidate_all()
        self.assertEqual(cp.id, old_id)
        self.assertEqual(cp.name, "00001")
        self.assertEqual(cp.municipio_id, self.municipality)

    def test_create_from_colony_completes_server_side(self):
        partner = self.partner(colonia_id=self.colony.id)
        self.assertEqual(partner.municipio_id, self.municipality)
        self.assertEqual(partner.ciudad_id, self.city)
        self.assertEqual(partner.state_id, self.state)
        self.assertEqual(partner.country_id, self.state.country_id)
        self.assertEqual(partner.city, self.city.name)
        self.assertEqual(partner.l10n_mx_edi_colony, self.colony.name)
        self.assertEqual(partner.zip, "01234")

    def test_create_from_city_and_municipality(self):
        city_partner = self.partner(ciudad_id=self.city.id)
        municipality_partner = self.partner(municipio_id=self.municipality.id)
        self.assertEqual(city_partner.city, self.city.name)
        self.assertEqual(municipality_partner.ciudad_id, self.city)
        self.assertEqual(municipality_partner.city, self.city.name)

    def test_explicit_text_is_preserved_in_import_values(self):
        partner = self.partner(colonia_id=self.colony.id, city="Ciudad histórica",
                               l10n_mx_edi_colony="Colonia fiscal histórica", zip="09999")
        self.assertEqual(partner.city, "Ciudad histórica")
        self.assertEqual(partner.l10n_mx_edi_colony, "Colonia fiscal histórica")
        self.assertEqual(partner.zip, "09999")

    def test_free_text_without_mx_catalogs(self):
        partner = self.partner(city="London", country_id=self.env.ref("base.uk").id,
                               l10n_mx_edi_colony="Texto conservado")
        partner.write({"phone": "123"})
        self.assertEqual(partner.city, "London")
        self.assertEqual(partner.l10n_mx_edi_colony, "Texto conservado")
        self.assertFalse(partner.ciudad_id)

    def test_supplier_archived_contact_and_ids_survive_unrelated_write(self):
        values = {"colonia_id": self.colony.id}
        if "supplier_rank" in self.env["res.partner"]._fields:
            values["supplier_rank"] = 1
        partner = self.partner(**values)
        partner.active = False
        fields = ["id", "ciudad_id", "municipio_id", "colonia_id", "city", "l10n_mx_edi_colony"]
        before = partner.read(fields, load=None)
        partner.write({"phone": "456"})
        self.env.invalidate_all()
        self.assertEqual(partner.read(fields, load=None), before)

    def test_clearing_selectors_keeps_saved_address_text(self):
        partner = self.partner(colonia_id=self.colony.id)
        partner.write({"colonia_id": False, "municipio_id": False, "ciudad_id": False})
        self.assertEqual(partner.city, self.city.name)
        self.assertEqual(partner.l10n_mx_edi_colony, self.colony.name)
        self.assertEqual(partner.zip, "01234")

    def test_catalog_rename_preserves_partner_text_and_ids(self):
        partner = self.partner(colonia_id=self.colony.id)
        before = (partner.id, partner.ciudad_id.id, partner.municipio_id.id, partner.colonia_id.id)
        self.city.name = "Ciudad renombrada"
        self.colony.name = "Colonia renombrada"
        self.assertEqual(partner.city, "Ciudad prueba")
        self.assertEqual(partner.l10n_mx_edi_colony, "Colonia prueba")
        self.assertEqual((partner.id, partner.ciudad_id.id, partner.municipio_id.id, partner.colonia_id.id), before)

    def test_batch_create_and_write(self):
        partners = self.env["res.partner"].create([{"name": "Uno"}, {"name": "Dos"}])
        before = partners.ids
        partners.write({"colonia_id": self.colony.id})
        self.assertEqual(partners.ids, before)
        self.assertTrue(all(p.city == self.city.name and p.colonia_id == self.colony for p in partners))

    def test_conflicting_catalog_links_are_rejected_without_replacing_ids(self):
        partner = self.partner(colonia_id=self.colony.id)
        other = self.env["res.country.state.municipio"].create({"name": "Otro", "state_id": self.state.id})
        with self.assertRaises(ValidationError):
            partner.write({"municipio_id": other.id})
        self.assertEqual(partner.municipio_id, self.municipality)
        self.assertEqual(partner.colonia_id, self.colony)

    def test_parent_address_sync_includes_catalog_relations(self):
        company = self.partner(is_company=True, colonia_id=self.colony.id)
        child = self.partner(parent_id=company.id, type="contact")
        self.assertEqual(child.ciudad_id, company.ciudad_id)
        self.assertEqual(child.colonia_id, company.colonia_id)
        self.assertEqual(child.l10n_mx_edi_colony, company.l10n_mx_edi_colony)

    def test_cp_read_permissions_do_not_allow_catalog_creation(self):
        user = self.env["res.users"].with_context(no_reset_password=True).create({
            "name": "CP reader", "login": "gmp_cp_reader",
            "groups_id": [Command.set([self.env.ref("base.group_user").id])],
        })
        self.assertEqual(self.postcode.with_user(user).name, "01234")
        with self.assertRaises(AccessError):
            self.env["res.country.state.cp"].with_user(user).create({"name": "00000"})
