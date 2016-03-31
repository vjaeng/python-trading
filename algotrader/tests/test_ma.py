from datetime import datetime
from unittest import TestCase

from algotrader.event.market_data import Bar, Quote, Trade
from algotrader.technical.ma import *
import numpy as np
import math
from algotrader.trading.instrument_data import inst_data_mgr
from algotrader.technical import get_or_create_indicator

class MovingAverageTest(TestCase):
    def test_name(self):
        inst_data_mgr.clear()
        close = inst_data_mgr.get_series("Bar.Close")
        sma = SMA(close, 3)
        self.assertEquals("SMA('Bar.Close',3)", sma.name)

        sma2 = SMA(sma,10)
        self.assertEquals("SMA(SMA('Bar.Close',3),10)", sma2.name)

    def test_empty_at_initialize(self):
        inst_data_mgr.clear()
        close = inst_data_mgr.get_series("Bar.Close")
        sma = SMA(close, 3)
        self.assertEquals(0, len(sma.get_data()))

    def test_nan_before_size(self):
        inst_data_mgr.clear()
        close = inst_data_mgr.get_series("Bar.Close")
        sma = SMA(close, 3)
        t1 = datetime.datetime.now()
        t2 = t1 + datetime.timedelta(0, 3)
        t3 = t2 + datetime.timedelta(0, 3)

        close.add(t1, 2)
        self.assertEquals({t1: np.nan}, sma.get_data())

        close.add(t2, 2.4)
        self.assertEquals({t1: np.nan, t2: np.nan}, sma.get_data())

        close.add(t3, 2.8)
        self.assertEquals({t1: np.nan, t2: np.nan, t3: 2.4}, sma.get_data())

    def test_moving_average_calculation(self):
        inst_data_mgr.clear()
        close = inst_data_mgr.get_series("Bar.Close")
        sma = SMA(close, 3)

        t1 = datetime.datetime.now()
        t2 = t1 + datetime.timedelta(0, 3)
        t3 = t2 + datetime.timedelta(0, 3)
        t4 = t3 + datetime.timedelta(0, 3)
        t5 = t4 + datetime.timedelta(0, 3)

        close.add(t1, 2)
        self.assertTrue(math.isnan(sma.now()))
        close.add(t2, 2.4)
        self.assertTrue(math.isnan(sma.now()))
        close.add(t3, 2.8)
        self.assertEquals(2.4, sma.now())
        close.add(t4, 3.2)
        self.assertEquals(2.8, sma.now())
        close.add(t5, 3.6)
        self.assertEquals(3.2, sma.now())

        self.assertTrue(math.isnan(sma.get_by_idx(0)))
        self.assertTrue(math.isnan(sma.get_by_idx(1)))
        self.assertEquals(2.4, sma.get_by_idx(2))
        self.assertEquals(2.8, sma.get_by_idx(3))
        self.assertEquals(3.2, sma.get_by_idx(4))

        self.assertTrue(math.isnan(sma.get_by_time(t1)))
        self.assertTrue(math.isnan(sma.get_by_time(t2)))
        self.assertEquals(2.4, sma.get_by_time(t3))
        self.assertEquals(2.8, sma.get_by_time(t4))
        self.assertEquals(3.2, sma.get_by_time(t5))

