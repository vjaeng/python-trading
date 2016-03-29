import datetime

import numpy as np

from algotrader.technical import Indicator
from algotrader.utils.time_series import TimeSeries


class ATR(Indicator):
    _slots__ = (
        'length'
    )

    def __init__(self, input, length=14, description="Average True Range"):
        super(ATR, self).__init__(input, "ATR(%s, %s)" % (input.id, length), description)
        self.length = length

    def on_update(self, time_value):
        pass



