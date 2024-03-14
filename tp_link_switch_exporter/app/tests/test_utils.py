import unittest
from enum import Enum
from tp_link_switch_exporter.app import utils


class TestEnum(Enum):
    FOO = 'foo'
    BAR = 'bar'


class TestUtils(unittest.TestCase):
    def test_normalize_name_works_for_enum(self):
        test_enum = TestEnum.FOO
        expected_name = 'FOO'
        expected_value = 'foo'
        self.assertIsInstance(test_enum, Enum)
        self.assertEqual(test_enum.name, expected_name)
        self.assertEqual(test_enum.value, expected_value)
        result = utils.normalize_name(test_enum)
        self.assertIsNotNone(result)
        self.assertNotEqual(test_enum, result)
        self.assertEqual(test_enum.value, result)
        self.assertEqual(expected_value, result)


if __name__ == '__main__':
    unittest.main()
