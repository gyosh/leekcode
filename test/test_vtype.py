import unittest

from lib.vtype import VType

class TestVType(unittest.TestCase):
    def test_equality(self):
        self.assertEquals(VType(VType.INTEGER), VType(VType.INTEGER))
        self.assertEquals(VType(VType.BOOLEAN), VType(VType.BOOLEAN))
        self.assertEquals(VType(VType.STRING), VType(VType.STRING))

        self.assertNotEquals(VType(VType.INTEGER), VType(VType.STRING))
        self.assertNotEquals(VType(VType.INTEGER), VType(VType.BOOLEAN))
        self.assertNotEquals(VType(VType.STRING), VType(VType.BOOLEAN))

        self.assertEquals(VType(VType.LIST, VType(VType.INTEGER)), VType(VType.LIST, VType(VType.INTEGER)))
        self.assertNotEquals(VType(VType.LIST, VType(VType.STRING)), VType(VType.LIST, VType(VType.INTEGER)))


    def test_is_ambiguous(self):
        self.assertFalse(VType(VType.INTEGER).is_ambiguous())
        self.assertFalse(VType(VType.BOOLEAN).is_ambiguous())
        self.assertFalse(VType(VType.STRING).is_ambiguous())
        self.assertTrue(VType(VType.NULL).is_ambiguous())
        self.assertFalse(VType(VType.LIST, VType(VType.INTEGER)).is_ambiguous())
        self.assertFalse(VType(VType.LIST, VType(VType.STRING)).is_ambiguous())
        self.assertFalse(VType(VType.LIST, VType(VType.BOOLEAN)).is_ambiguous())
        self.assertTrue(VType(VType.LIST, VType(VType.NULL)).is_ambiguous())
        self.assertFalse(VType(VType.LIST, VType(VType.LIST, VType(VType.BOOLEAN))).is_ambiguous())

        self.assertTrue(VType(VType.LIST, None).is_ambiguous())
        self.assertTrue(VType(VType.LIST, VType(VType.LIST, None)).is_ambiguous())
        self.assertTrue(VType(VType.LIST).is_ambiguous())
        self.assertTrue(VType(VType.LIST, VType(VType.LIST)).is_ambiguous())


if __name__ == '__main__':
    unittest.main()
