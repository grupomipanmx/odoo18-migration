from odoo import Command
from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestColoniaSearch(TransactionCase):
    """Regression cases for the public Odoo 18 name_search contract.

    Run only in a disposable database. Fixtures roll back with TransactionCase;
    no CSV catalog is loaded and no existing catalog entry is modified.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        state = cls.env["res.country.state"].create({
            "name": "Migration search test", "code": "GMPTEST",
            "country_id": cls.env.ref("base.mx").id,
        })
        cls.municipality = cls.env["res.country.state.municipio"].create({
            "name": "Migration search test", "state_id": state.id,
        })
        cls.colonies = cls.env["res.country.state.municipio.colonia"].create([
            {"name": "Migration Alameda", "cp": "01234", "municipio_id": cls.municipality.id},
            {"name": "01234", "cp": "54321", "municipio_id": cls.municipality.id},
            {"name": "Migration Centro", "cp": "54321", "municipio_id": cls.municipality.id},
        ])
        cls.catalog = cls.env["res.country.state.municipio.colonia"]
        cls.domain = [("id", "in", cls.colonies.ids)]

    def search_ids(self, term, operator="ilike", args=None, limit=100):
        return {rid for rid, _label in self.catalog.name_search(
            term, args=self.domain if args is None else args,
            operator=operator, limit=limit,
        )}

    def test_postal_code_keeps_leading_zero_and_matches_numeric_name(self):
        self.assertEqual(self.search_ids("01234"), set(self.colonies[:2].ids))

    def test_normal_name_search(self):
        self.assertEqual(self.search_ids("Alameda"), {self.colonies[0].id})

    def test_negative_match_excludes_postal_code_and_name(self):
        self.assertEqual(self.search_ids("01234", "not ilike"), {self.colonies[2].id})

    def test_negative_equality_excludes_both_fields(self):
        self.assertEqual(self.search_ids("01234", "!="), {self.colonies[2].id})

    def test_caller_domain_is_preserved(self):
        self.assertFalse(self.search_ids("01234", args=[("id", "=", self.colonies[2].id)]))

    def test_empty_term_and_limit(self):
        self.assertEqual(self.search_ids(""), set(self.colonies.ids))
        self.assertEqual(len(self.search_ids("", limit=1)), 1)

    def test_internal_user_read_only_and_record_rule(self):
        group = self.env.ref("base.group_user")
        user = self.env["res.users"].with_context(no_reset_password=True).create({
            "name": "Migration catalog reader", "login": "gmp_migration_catalog_reader",
            "groups_id": [Command.set([group.id])],
        })
        self.env["ir.rule"].create({
            "name": "Migration test catalog visibility",
            "model_id": self.env["ir.model"]._get_id(self.catalog._name),
            "domain_force": repr([("id", "!=", self.colonies[0].id)]),
        })
        result = self.catalog.with_user(user).name_search("01234", args=self.domain)
        self.assertEqual({rid for rid, _label in result}, {self.colonies[1].id})
        with self.assertRaises(AccessError):
            self.catalog.with_user(user).create({
                "name": "Forbidden", "municipio_id": self.municipality.id,
            })
