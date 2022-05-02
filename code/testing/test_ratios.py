import pandas as pd
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
