import unittest

from lib.util import extract_variables
from lib.vtype import VType

class TestUtil(unittest.TestCase):
    def test_extract_variables_single(self):
        self.assertEquals([('a', VType(VType.INTEGER), 12)], extract_variables('a = 12'))
        self.assertEquals([('numPerson', VType(VType.INTEGER), 999)], extract_variables('numPerson = 999'))
        self.assertEquals([('numPerson', VType(VType.INTEGER), 0)], extract_variables('numPerson = 0'))
        self.assertEquals([('numPerson', VType(VType.INTEGER), -5)], extract_variables('numPerson = -5'))
        self.assertEquals([('numPerson', VType(VType.INTEGER), -51)], extract_variables('numPerson = -51'))

        self.assertEquals([('b', VType(VType.BOOLEAN), True)], extract_variables('b = true'))
        self.assertEquals([('b', VType(VType.BOOLEAN), False)], extract_variables('b = false'))

        self.assertEquals([('s', VType(VType.STRING), "BORK")], extract_variables('s = "BORK"'))
        self.assertEquals([('s', VType(VType.STRING), "Doge Drill")], extract_variables('s = "Doge Drill"'))
        self.assertEquals([('slang', VType(VType.STRING), "doggo")], extract_variables('slang = "doggo"'))
        self.assertEquals([('slang', VType(VType.STRING), "")], extract_variables('slang = ""'))
        self.assertEquals([('error', VType(VType.STRING), "null")], extract_variables('error = "null"'))

        self.assertEquals([('x', VType(VType.NULL), None)], extract_variables('x = null'))

        self.assertEquals([('ages', VType(VType.LIST, VType(VType.INTEGER)), [21, 22])], extract_variables('ages = [21,22]'))
        self.assertEquals([('ages', VType(VType.LIST, VType(VType.INTEGER)), [8])], extract_variables('ages = [8]'))
        self.assertEquals([('pos', VType(VType.LIST, VType(VType.INTEGER)), [-54, 0, 11])], extract_variables('pos = [-54,0,11]'))

        # Special case for unknown type
        self.assertEquals([('ages', VType(VType.LIST, VType(VType.NULL)), [])], extract_variables('ages = []'))

        self.assertEquals([('holey', VType(VType.LIST, VType(VType.INTEGER)), [-54, 0, None, 11])], extract_variables('holey = [-54,0,null,11]'))
        self.assertEquals([('troll', VType(VType.LIST, VType(VType.STRING)), ['Zuljin', 'Senjin', None])], extract_variables('troll = ["Zuljin","Senjin",null]'))


    def test_extract_variables_multi(self):
        self.assertEquals([
            ('a', VType(VType.INTEGER), 10),
            ('b', VType(VType.INTEGER), -99)
        ], extract_variables('a = 10, b = -99'))

        self.assertEquals([
            ('name', VType(VType.STRING), 'Kratos'),
            ('age', VType(VType.INTEGER), 9991)
        ], extract_variables('name = "Kratos", age = 9991'))

        self.assertEquals([
            ('name', VType(VType.STRING), 'Kratos'),
            ('age', VType(VType.INTEGER), 9991),
            ('hasChild', VType(VType.BOOLEAN), True)
        ], extract_variables('name = "Kratos", age = 9991, hasChild = true'))

        self.assertEquals([
            ('name', VType(VType.STRING), 'Kratos'),
            ('age', VType(VType.INTEGER), 9991),
            ('hasChild', VType(VType.BOOLEAN), True),
            ('blades', VType(VType.LIST, VType(VType.STRING)), ['chaos', 'athena', 'exile', None])
        ], extract_variables('name = "Kratos", age = 9991, hasChild = true, blades = ["chaos","athena","exile",null]'))


    def test_extract_variables_value_only(self):
        self.assertEquals([(None, VType(VType.INTEGER), 12)], extract_variables('12', value_only=True))
        self.assertEquals([(None, VType(VType.INTEGER), 999)], extract_variables('999', value_only=True))
        self.assertEquals([(None, VType(VType.INTEGER), 0)], extract_variables('0', value_only=True))
        self.assertEquals([(None, VType(VType.INTEGER), -5)], extract_variables('-5', value_only=True))
        self.assertEquals([(None, VType(VType.INTEGER), -51)], extract_variables('-51', value_only=True))

        self.assertEquals([(None, VType(VType.BOOLEAN), True)], extract_variables('true', value_only=True))
        self.assertEquals([(None, VType(VType.BOOLEAN), False)], extract_variables('false', value_only=True))

        self.assertEquals([(None, VType(VType.STRING), "BORK")], extract_variables('"BORK"', value_only=True))
        self.assertEquals([(None, VType(VType.STRING), "Doge Drill")], extract_variables('"Doge Drill"', value_only=True))
        self.assertEquals([(None, VType(VType.STRING), "doggo")], extract_variables('"doggo"', value_only=True))
        self.assertEquals([(None, VType(VType.STRING), "")], extract_variables('""', value_only=True))

        self.assertEquals([(None, VType(VType.LIST, VType(VType.INTEGER)), [21, 22])], extract_variables('[21,22]', value_only=True))
        self.assertEquals([(None, VType(VType.LIST, VType(VType.INTEGER)), [8])], extract_variables('[8]', value_only=True))
        self.assertEquals([(None, VType(VType.LIST, VType(VType.INTEGER)), [-54, 0, 11])], extract_variables('[-54,0,11]', value_only=True))

        # Special case for unknown type
        self.assertEquals([(None, VType(VType.LIST, VType(VType.NULL)), [])], extract_variables('[]', value_only=True))

        self.assertEquals([(None, VType(VType.LIST, VType(VType.INTEGER)), [-54, 0, None, 11])], extract_variables('[-54,0,null,11]', value_only=True))
        self.assertEquals([(None, VType(VType.LIST, VType(VType.STRING)), ['Zuljin', 'Senjin', None])], extract_variables('["Zuljin","Senjin",null]', value_only=True))


if __name__ == '__main__':
    unittest.main()
