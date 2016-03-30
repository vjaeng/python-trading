import datetime

import numpy as np

from algotrader.technical import Indicator
from algotrader.utils.time_series import TimeSeries


def roc(prev_value, curr_value):
    if prev_value != 0.0:
        return (curr_value - prev_value) / prev_value
    return np.nan


class ROC(Indicator):
    _slots__ = (
        'length'
    )

    def __init__(self, input, length=1, description="Rate Of Change"):
        super(ROC, self).__init__(input, "ROC(%s, %s)" % (input.name, length), description)
        self.length = length

    def on_update(self, time_value):
        time, value = time_value
        if self.input.size() > self.length:
            prev_value = self.input.ago(self.length)
            curr_value = self.input.now()
            self.add(time, roc(prev_value, curr_value))
        else:
            self.add(time, np.nan)
