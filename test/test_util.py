import unittest

from lib.util import extract_variables
from lib.vtype import VType

class TestUtil(unittest.TestCase):
    def assertFloatList(self, expected, got):
        self.assertEqual(len(expected), len(got))
        for i in range(len(expected)):
            self.assertEqual(expected[i][0], got[i][0])
            self.assertEqual(expected[i][1], got[i][1])
            self.assertAlmostEqual(expected[i][2], got[i][2])

    def test_extract_variables_single(self):
        self.assertEqual([('a', VType(VType.INTEGER), 12)], extract_variables('a = 12'))
        self.assertEqual([('numPerson', VType(VType.INTEGER), 999)], extract_variables('numPerson = 999'))
        self.assertEqual([('numPerson', VType(VType.INTEGER), 0)], extract_variables('numPerson = 0'))
        self.assertEqual([('numPerson', VType(VType.INTEGER), -5)], extract_variables('numPerson = -5'))
        self.assertEqual([('numPerson', VType(VType.INTEGER), -51)], extract_variables('numPerson = -51'))

        self.assertAlmostEqual([('prob', VType(VType.FLOAT), 0.51)], extract_variables('prob = 0.51'))
        self.assertAlmostEqual([('prob', VType(VType.FLOAT), 0.51)], extract_variables('prob = .51'))
        self.assertAlmostEqual([('prob', VType(VType.FLOAT), 0.0051)], extract_variables('prob = .0051'))
        self.assertAlmostEqual([('prob', VType(VType.FLOAT), 1.51)], extract_variables('prob = 1.51'))
        self.assertAlmostEqual([('prob', VType(VType.FLOAT), 10.51)], extract_variables('prob = 10.51'))
        self.assertAlmostEqual([('prob', VType(VType.FLOAT), 10.0051)], extract_variables('prob = 10.0051'))
        self.assertAlmostEqual([('prob', VType(VType.FLOAT), 10.)], extract_variables('prob = 10.'))

        self.assertAlmostEqual([('prob', VType(VType.FLOAT), -0.51)], extract_variables('prob = -0.51'))
        self.assertAlmostEqual([('prob', VType(VType.FLOAT), -0.51)], extract_variables('prob = -.51'))
        self.assertAlmostEqual([('prob', VType(VType.FLOAT), -0.0051)], extract_variables('prob = -.0051'))
        self.assertAlmostEqual([('prob', VType(VType.FLOAT), -1.51)], extract_variables('prob = -1.51'))
        self.assertAlmostEqual([('prob', VType(VType.FLOAT), -10.51)], extract_variables('prob = -10.51'))
        self.assertAlmostEqual([('prob', VType(VType.FLOAT), -10.0051)], extract_variables('prob = -10.0051'))
        self.assertAlmostEqual([('prob', VType(VType.FLOAT), -10.)], extract_variables('prob = -10.'))

        self.assertEqual([('b', VType(VType.BOOLEAN), True)], extract_variables('b = true'))
        self.assertEqual([('b', VType(VType.BOOLEAN), False)], extract_variables('b = false'))

        self.assertEqual([('s', VType(VType.STRING), "BORK")], extract_variables('s = "BORK"'))
        self.assertEqual([('s', VType(VType.STRING), "Doge Drill")], extract_variables('s = "Doge Drill"'))
        self.assertEqual([('slang', VType(VType.STRING), "doggo")], extract_variables('slang = "doggo"'))
        self.assertEqual([('slang', VType(VType.STRING), "")], extract_variables('slang = ""'))
        self.assertEqual([('error', VType(VType.STRING), "null")], extract_variables('error = "null"'))

        self.assertEqual([('x', VType(VType.NULL), None)], extract_variables('x = null'))

        self.assertEqual([('ages', VType(VType.LIST, VType(VType.INTEGER)), [21, 22])], extract_variables('ages = [21,22]'))
        self.assertEqual([('ages', VType(VType.LIST, VType(VType.INTEGER)), [21, 22])], extract_variables('ages = [21, 22]'))
        self.assertEqual([('ages', VType(VType.LIST, VType(VType.INTEGER)), [21, 22])], extract_variables('ages = [21 ,22]'))
        self.assertEqual([('ages', VType(VType.LIST, VType(VType.INTEGER)), [21, 22])], extract_variables('ages = [21 , 22]'))
        self.assertEqual([('ages', VType(VType.LIST, VType(VType.INTEGER)), [8])], extract_variables('ages = [8]'))
        self.assertEqual([('pos', VType(VType.LIST, VType(VType.INTEGER)), [-54, 0, 11])], extract_variables('pos = [-54,0,11]'))
        self.assertEqual([('pos', VType(VType.LIST, VType(VType.INTEGER)), [-54, 0, 11])], extract_variables('pos = [-54, 0, 11]'))
        self.assertEqual([('pos', VType(VType.LIST, VType(VType.INTEGER)), [-54, 0, 11])], extract_variables('pos = [-54,\n0,\n11]'))

        self.assertFloatList([('dist', VType(VType.LIST, VType(VType.FLOAT)), [1, 0, 0.5])], extract_variables('dist = [1,0,0.5]'))
        self.assertFloatList([('dist', VType(VType.LIST, VType(VType.FLOAT)), [-1, 0.242])], extract_variables('dist = [-1.,0.242]'))

        # Special case for unknown type
        self.assertEqual([('ages', VType(VType.LIST, VType(VType.NULL)), [])], extract_variables('ages = []'))

        self.assertEqual([('holey', VType(VType.LIST, VType(VType.INTEGER)), [-54, 0, None, 11])], extract_variables('holey = [-54,0,null,11]'))
        self.assertEqual([('troll', VType(VType.LIST, VType(VType.STRING)), ['Zuljin', 'Senjin', None])], extract_variables('troll = ["Zuljin","Senjin",null]'))


    def test_extract_variables_multi(self):
        self.assertEqual([
            ('a', VType(VType.INTEGER), 10),
            ('b', VType(VType.INTEGER), -99)
        ], extract_variables('a = 10, b = -99'))

        self.assertEqual([
            ('name', VType(VType.STRING), 'Kratos'),
            ('age', VType(VType.INTEGER), 9991)
        ], extract_variables('name = "Kratos", age = 9991'))

        self.assertEqual([
            ('name', VType(VType.STRING), 'Kratos'),
            ('age', VType(VType.INTEGER), 9991),
            ('hasChild', VType(VType.BOOLEAN), True)
        ], extract_variables('name = "Kratos", age = 9991, hasChild = true'))

        self.assertEqual([
            ('name', VType(VType.STRING), 'Kratos'),
            ('age', VType(VType.INTEGER), 9991),
            ('hasChild', VType(VType.BOOLEAN), True),
            ('blades', VType(VType.LIST, VType(VType.STRING)), ['chaos', 'athena', 'exile', None]),
            ('health', VType(VType.FLOAT), 0.981)
        ], extract_variables('name = "Kratos", age = 9991, hasChild = true, blades = ["chaos","athena","exile",null], health = 0.981'))


    def test_extract_variables_value_only(self):
        self.assertEqual([(None, VType(VType.INTEGER), 12)], extract_variables('12', value_only=True))
        self.assertEqual([(None, VType(VType.INTEGER), 999)], extract_variables('999', value_only=True))
        self.assertEqual([(None, VType(VType.INTEGER), 0)], extract_variables('0', value_only=True))
        self.assertEqual([(None, VType(VType.INTEGER), -5)], extract_variables('-5', value_only=True))
        self.assertEqual([(None, VType(VType.INTEGER), -51)], extract_variables('-51', value_only=True))

        self.assertAlmostEqual([(None, VType(VType.FLOAT), 0.51)], extract_variables('0.51', value_only=True))
        self.assertAlmostEqual([(None, VType(VType.FLOAT), 0.51)], extract_variables('.51', value_only=True))
        self.assertAlmostEqual([(None, VType(VType.FLOAT), 0.0051)], extract_variables('.0051', value_only=True))
        self.assertAlmostEqual([(None, VType(VType.FLOAT), 1.51)], extract_variables('1.51', value_only=True))
        self.assertAlmostEqual([(None, VType(VType.FLOAT), 10.51)], extract_variables('10.51', value_only=True))
        self.assertAlmostEqual([(None, VType(VType.FLOAT), 10.0051)], extract_variables('10.0051', value_only=True))
        self.assertAlmostEqual([(None, VType(VType.FLOAT), 10.)], extract_variables('10.', value_only=True))

        self.assertAlmostEqual([(None, VType(VType.FLOAT), -0.51)], extract_variables('-0.51', value_only=True))
        self.assertAlmostEqual([(None, VType(VType.FLOAT), -0.51)], extract_variables('-.51', value_only=True))
        self.assertAlmostEqual([(None, VType(VType.FLOAT), -0.0051)], extract_variables('-.0051', value_only=True))
        self.assertAlmostEqual([(None, VType(VType.FLOAT), -1.51)], extract_variables('-1.51', value_only=True))
        self.assertAlmostEqual([(None, VType(VType.FLOAT), -10.51)], extract_variables('-10.51', value_only=True))
        self.assertAlmostEqual([(None, VType(VType.FLOAT), -10.0051)], extract_variables('-10.0051', value_only=True))
        self.assertAlmostEqual([(None, VType(VType.FLOAT), -10.)], extract_variables('-10.', value_only=True))

        self.assertEqual([(None, VType(VType.BOOLEAN), True)], extract_variables('true', value_only=True))
        self.assertEqual([(None, VType(VType.BOOLEAN), False)], extract_variables('false', value_only=True))

        self.assertEqual([(None, VType(VType.STRING), "BORK")], extract_variables('"BORK"', value_only=True))
        self.assertEqual([(None, VType(VType.STRING), "Doge Drill")], extract_variables('"Doge Drill"', value_only=True))
        self.assertEqual([(None, VType(VType.STRING), "doggo")], extract_variables('"doggo"', value_only=True))
        self.assertEqual([(None, VType(VType.STRING), "")], extract_variables('""', value_only=True))

        self.assertEqual([(None, VType(VType.LIST, VType(VType.INTEGER)), [21, 22])], extract_variables('[21,22]', value_only=True))
        self.assertEqual([(None, VType(VType.LIST, VType(VType.INTEGER)), [8])], extract_variables('[8]', value_only=True))
        self.assertEqual([(None, VType(VType.LIST, VType(VType.INTEGER)), [-54, 0, 11])], extract_variables('[-54,0,11]', value_only=True))

        # Special case for unknown type
        self.assertEqual([(None, VType(VType.LIST, VType(VType.NULL)), [])], extract_variables('[]', value_only=True))

        self.assertEqual([(None, VType(VType.LIST, VType(VType.INTEGER)), [-54, 0, None, 11])], extract_variables('[-54,0,null,11]', value_only=True))
        self.assertEqual([(None, VType(VType.LIST, VType(VType.STRING)), ['Zuljin', 'Senjin', None])], extract_variables('["Zuljin","Senjin",null]', value_only=True))


if __name__ == '__main__':
    unittest.main()
