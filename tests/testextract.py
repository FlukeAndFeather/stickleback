import pandas as pd
from pandas.testing import assert_index_equal
import numpy as np
from numpy.testing import assert_array_equal
import unittest
import stickleback.util as sb_util

n = 20
idx1 = pd.date_range(start="2020-01-01 00:00", freq="S", periods=n, tz="Etc/GMT+7")
idx2 = pd.date_range(start="2020-02-01 00:00", freq="S", periods=n, tz="Etc/GMT+3")
sensors = {
        "d1": pd.DataFrame({
            "a": np.arange(n),
            "b": np.arange(n) ** 2
        }, index = idx1),
        "d2": pd.DataFrame({
            "a": -np.arange(n),
            "b": -(np.arange(n) ** 2)
        }, index = idx2)
    }
events = {
    "d1": idx1[[2, 6]],
    "d2": idx2[[3, 8]]
}
rng = np.random.Generator(np.random.PCG64(1234))

class ExtractTestCase(unittest.TestCase):
    
    def test_extract_all(self):
        winsz = 3
        result = sb_util.extract_all(sensors, nth=1, win_size=winsz)

        # Size and contents
        self.assertEqual(len(result["d1"]), n - winsz + 1)
        self.assertEqual(len(result["d1"].iloc[0, 0]), winsz)
        assert_array_equal(result["d2"].iloc[-1, -1], -np.arange(n - winsz, n) ** 2)

        # Keys and index
        self.assertEqual(result.keys(), sensors.keys())
        self.assertIsInstance(result["d1"].index, pd.DatetimeIndex)
        assert_index_equal(result["d1"].index, idx1[1:-1])

    def test_extract_nested(self):
        idx = {"d1": idx1[[2, 4]], "d2": idx2[[3, 5]]}
        result = sb_util.extract_nested(sensors, idx, win_size=3)

        for i in idx:
            assert_index_equal(result[i].index, idx[i])

    def test_sample_nonevents(self):
        nonevents = sb_util.sample_nonevents(sensors, events, win_size=3, rng=rng)

        # Verify nonevent windows don't overlap event windows
        for id, windows in nonevents.items():
            for e in events[id]:
                # Assumes 1 s freq and win_size = 3
                assert(np.all(np.abs(e - windows.index) > pd.Timedelta("3s")))
