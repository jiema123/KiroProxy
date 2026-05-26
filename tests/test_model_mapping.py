import unittest

from kiro_proxy.config import map_model_name


class ModelMappingTests(unittest.TestCase):
    def test_gpt_5_aliases_map_to_expected_kiro_models(self):
        self.assertEqual(map_model_name("gpt-5.4"), "claude-sonnet-4.6")
        self.assertEqual(map_model_name("gpt-5.5"), "claude-opus-4.7")


if __name__ == "__main__":
    unittest.main()
