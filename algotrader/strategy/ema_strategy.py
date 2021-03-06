from algotrader.event.order import OrdAction
from algotrader.strategy.strategy import Strategy
from algotrader.technical.talib_wrapper import EMA
from algotrader.utils import logger


class EMAStrategy(Strategy):
    def __init__(self, stg_id=None, stg_configs=None):
        super(EMAStrategy, self).__init__(stg_id=stg_id, stg_configs=stg_configs)
        self.buy_order = None

    def _start(self, app_context, **kwargs):
        self.qty = self.get_stg_config_value("qty", 1)

        self.bar = app_context.inst_data_mgr.get_series("Bar.%s.Time.86400" % self.app_context.app_config.instrument_ids[0])
        self.bar.start(app_context)

        self.ema_fast = EMA(self.bar, 'close', 10)
        self.ema_fast.start(app_context)

        self.ema_slow = EMA(self.bar, 'close', 25)
        self.ema_slow.start(app_context)

        super(EMAStrategy, self)._start(app_context, **kwargs)

    def _stop(self):
        super(EMAStrategy, self)._stop()

    def on_bar(self, bar):
        if self.buy_order is None and self.ema_fast.now('value') > self.ema_slow.now('value'):
            self.buy_order = self.market_order(inst_id=bar.inst_id, action=OrdAction.BUY, qty=self.qty)
            logger.info("%s,B,%s,%s,%.2f,%.2f,%.2f" % (
                bar.timestamp, self.buy_order.cl_id, self.buy_order.cl_ord_id, bar.close, self.ema_fast.now('value'),
                self.ema_slow.now('value')))
        elif self.buy_order is not None and self.ema_fast.now('value') < self.ema_slow.now('value'):
            sell_order = self.market_order(inst_id=bar.inst_id, action=OrdAction.SELL, qty=self.qty)
            logger.info("%s,S,%s,%s,%.2f,%.2f,%.2f" % (
                bar.timestamp, sell_order.cl_id, sell_order.cl_ord_id, bar.close, self.ema_fast.now('value'),
                self.ema_slow.now('value')))
