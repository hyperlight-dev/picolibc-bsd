import unittest

from check_license_policy import is_approved


class LicensePolicyTest(unittest.TestCase):
    def test_mit_alternative_with_separate_mit_notice(self):
        self.assertTrue(is_approved(
            "(mit OR apache-2.0 WITH llvm-exception) AND mit", {"apache-2.0", "mit"}
        ))

    def test_unapproved_required_license(self):
        self.assertFalse(is_approved("mit AND gpl-2.0", {"mit"}))

    def test_exception_is_not_approved_by_its_components(self):
        self.assertFalse(is_approved(
            "apache-2.0 WITH llvm-exception", {"apache-2.0", "llvm-exception"}
        ))

    def test_malformed_expression_is_not_approved(self):
        self.assertFalse(is_approved("mit OR", {"mit"}))


if __name__ == "__main__":
    unittest.main()
