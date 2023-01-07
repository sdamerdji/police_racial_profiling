import pandas as pd
import numpy as np
import unittest
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'analysis'))
import ratios as rat


class TestRatios(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        green_dict = {"stop_id": [x for x in range(20)],
                      "race": ['green'] * 20,
                      "dessert": 5 * ["pie"] + 5 * ["ice cream"] + 5 * ["cake"] + 5 * ["beer"]}
        blue_dict = {"stop_id": [20 + x for x in range(20)],
                     "race": ['blue'] * 20,
                     "dessert": 10 * ["pie"] + 2 * ["ice cream"] + 2 * ["cake"] + 6 * ["beer"]}
        cls.df = pd.concat([pd.DataFrame(green_dict), pd.DataFrame(blue_dict)], ignore_index=True)

    def test_add_races(self):
        all = rat.add_races(self.df, ['green', 'blue'], field='dessert')
        self.assertTrue(all['beer'] == 11)
        self.assertTrue(all['ice cream'] == 7)
        self.assertTrue(all['cake'] == 7)
        self.assertTrue(all['pie'] == 15)

    def test_generate_relative_df(self):
        green = rat.add_races(self.df, ['green'], field='dessert')
        blue = rat.add_races(self.df, ['blue'], field='dessert')
        rel = rat.generate_relative_df(green, blue, "green", "blue")
        np.testing.assert_almost_equal(rel["Expected blue"], [5, 5, 5, 5])
        np.testing.assert_almost_equal(rel['Relative'], [1.2, 0.4, 0.4, 2.0], decimal=2)
