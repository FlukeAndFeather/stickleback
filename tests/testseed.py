import pandas as pd
import pandas.testing as pdtst
import sktime.classification.interval_based
import sktime.classification.compose
from stickleback.stickleback import Stickleback
import stickleback.data
import stickleback.util
import unittest
from numpy.random import default_rng

# Load sample data
sensors, events = stickleback.data.load_lunges()

# Split into test and train (2 deployments each)
rng = default_rng(12345)
key_list = list(sensors.keys())
rng.shuffle(list(key_list))  # randomize key order inplace
test_deployids = key_list[0:2]
train_deployids = key_list[2:]
sensors_train = {k: sensors[k] for k in train_deployids}
sensors_test = {k: sensors[k] for k in test_deployids}
events_train = {k: events[k] for k in train_deployids}
events_test = {k: events[k] for k in test_deployids}

# Define, fit, predict, assess
def run_stickleback():
    # Define model
    # Supervised Time Series Forests ensembled across the columns of `sensors`
    cols = sensors[list(sensors.keys())[0]].columns
    tsc = sktime.classification.interval_based.SupervisedTimeSeriesForest(n_estimators=2,
                                                                          random_state=4321)
    stsf = sktime.classification.compose.ColumnEnsembleClassifier(
        estimators = [('STSF_{}'.format(col),
                      tsc,
                      [i])
                      for i, col in enumerate(cols)]
    )

    sb = Stickleback(
        local_clf=stsf,
        win_size=20,
        tol=pd.Timedelta("5s"),
        nth=20,
        n_folds=2,
        seed=1234
    )

    # Fit, predict, assess
    sb.fit(sensors_train, events_train)
    predictions = sb.predict(sensors_test)
    outcomes = sb.assess(predictions, events_test)
    
    return predictions, outcomes

# Run the Stickleback define-fit-predict-assess pipeline twice
# They should be the same!
pred1, out1 = run_stickleback()
pred2, out2 = run_stickleback()

class SeedTestCase(unittest.TestCase):
    
    def test_predictions(self):
        id = 'bw180905-42'
        # Assert local probability equality
        pdtst.assert_series_equal(pred1[id][0], pred2[id][0])
        # Assert event prediction equality
        pdtst.assert_index_equal(pred1[id][1], pred2[id][1])
        # Assert outcome equality
        pdtst.assert_series_equal(out1[id], out2[id])
