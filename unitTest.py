import unittest
import converToCanonical
class TestStringMethods(unittest.TestCase):

    def test_inputMode_InCorrectInputs(self):
        self.assertEqual(converToCanonical.inputMode("x"), 'In Correct Input\n')
        self.assertEqual(converToCanonical.inputMode("x +( = 0"), 'ERROR: Input has incorrect number of nested brackets\n')
        self.assertEqual(converToCanonical.inputMode("x ++( = 0"), 'In Correct Input. *, / , %, ++, -- not supported\n')
        self.assertEqual(converToCanonical.inputMode("x +()) = 0"), 'ERROR: Input has incorrect number of nested brackets\n')
        self.assertEqual(converToCanonical.inputMode("x +(() = 0"), 'ERROR: Input missing sign before brackets\n')
        self.assertEqual(converToCanonical.inputMode("x +( x * y ) = 0"), 'In Correct Input. *, / , %, ++, -- not supported\n')    

    def test_inputMode_Calculate(self):        
        self.assertEqual(converToCanonical.inputMode("x=1"), 'x - 1.0 = 0.0\n')
        self.assertEqual(converToCanonical.inputMode("x=x"), '0 = 0\n')
        self.assertEqual(converToCanonical.inputMode("x + ( x + y ) = x"), 'x + y = 0.0\n')
        self.assertEqual(converToCanonical.inputMode("x + ( x^2 + y ) = x"), 'x^2.0 + y = 0.0\n')
        self.assertEqual(converToCanonical.inputMode("x - (0 - (0 - x)) = 0"), '0 = 0\n')


    def test_inputMode_ComplexExpressions(self):
        self.assertEqual(converToCanonical.inputMode("x (-(+(-3))) = x"), '2.0x = 0.0\n')
        self.assertEqual(converToCanonical.inputMode("-x (-(+(-3))) = x"), '-4.0x = 0.0\n')
        self.assertEqual(converToCanonical.inputMode("x + xx( abc + bca + cab ) = 0 "), '3.0acbx^2.0 + x = 0.0\n')
        self.assertEqual(converToCanonical.inputMode("x + xx( abc + x( ybca + ycab ) + y( xabc + xbca ) ) = 0 "), 'acbx^2.0 + 4.0cbax^3.0y + x = 0.0\n')
        self.assertEqual(converToCanonical.inputMode("x = x( x + abc  - 10x ( cba^2 + bcax + x(abc) ) + 20xxabc )"), '10.0a^2.0cbx^2.0 - 1.0axcb + x - 1.0x^2.0 = 0.0\n')
        self.assertEqual(converToCanonical.inputMode("x( x + abc  - 10x ( cba^2 + bcax + x(abc) ) + 20xxabc ) = x( x + abc  - 10x ( cba^2 + bcax + x(abc) ) + 20xxabc )")\
            ,'0 = 0\n')

if __name__ == '__main__':
    unittest.main()