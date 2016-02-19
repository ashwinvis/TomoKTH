import unittest
from tomokth.operators.math import vintersect_sphcyl


class Test_VIntersect_SphCyl(unittest.TestCase):
    def test1(self):
        """ b > R; r > b + R """
        self.assertAlmostEqual(vintersect_sphcyl(1., 0.2, 0.3), 0.23696, places=4)

    def test2(self):
        """ b = R; r > b + R """
        self.assertAlmostEqual(vintersect_sphcyl(1., 0.2, 0.2), 0.24361, places=4)

    def test3(self):
        """ b < R; r > b + R """
        self.assertAlmostEqual(vintersect_sphcyl(1., 0.2, 0.1), 0.24752, places=4)

    def test4(self):
        """ b < R; r = b + R """
        self.assertAlmostEqual(vintersect_sphcyl(1., 0.8, 0.2), 3.13728, places=4)

    def test5(self):
        """ b = R; r = b + R """
        self.assertAlmostEqual(vintersect_sphcyl(1., 0.5, 0.5), 1.20550, places=4)

    def test6(self):
        """ b > R; r = b + R """
        self.assertAlmostEqual(vintersect_sphcyl(1., 0.2, 0.8), 0.14128, places=4)

    def test7(self):
        """ b < R; r < b + R """
        self.assertAlmostEqual(vintersect_sphcyl(1., 1.0, 0.2), 3.90657, places=4)

    def test8(self):
        """ b = R; r < b + R """
        self.assertAlmostEqual(vintersect_sphcyl(1., 1.2, 1.2), 1.76216, places=4)

    def test9(self):
        """ b > R; r < b + R """
        self.assertAlmostEqual(vintersect_sphcyl(1., 1.0, 1.2), 1.15367, places=4)
