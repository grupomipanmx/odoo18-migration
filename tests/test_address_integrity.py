import copy
import unittest

from tools.address_integrity import FIELDS, compare


class TestAddressIntegrity(unittest.TestCase):
    def setUp(self):
        self.before = {"format": 1, "models": {
            name: {"table": name.replace(".", "_"), "fields": fields,
                   "rows": {"7": "same-row-digest"}} for name, fields in FIELDS.items()
        }}
        self.after = copy.deepcopy(self.before)

    def test_identical_snapshot(self):
        self.assertEqual(compare(self.before, self.after), [])

    def test_missing_cp_is_not_accepted(self):
        del self.after["models"]["res.country.state.cp"]
        self.assertTrue(compare(self.before, self.after))

    def test_recreated_ids_fail_even_if_count_is_unchanged(self):
        self.after["models"]["res.partner"]["rows"] = {"8": "same-row-digest"}
        self.assertTrue(any("IDs changed" in e for e in compare(self.before, self.after)))

    def test_changed_relation_or_text_digest_fails(self):
        self.after["models"]["res.partner"]["rows"]["7"] = "different-relation-or-text"
        self.assertTrue(any("fingerprints" in e for e in compare(self.before, self.after)))

    def test_table_change_fails(self):
        self.after["models"]["res.country.state.cp"]["table"] = "replacement_cp"
        self.assertTrue(compare(self.before, self.after))

    def test_incomplete_snapshot_fails(self):
        self.before["models"]["res.partner"]["fields"] = ["city"]
        self.assertTrue(compare(self.before, self.before))


if __name__ == "__main__":
    unittest.main()
