from algotrader.event.order import OrdAction
from algotrader.event.market_data import MarketDataEventHandler


class Position(object):
    def __init__(self, inst_id):
        self.inst_id = inst_id
        self.orders = {}
        self.size = 0
        self.last_price = 0

    def add_order(self, order):
        if order.inst_id != self.inst_id:
            raise RuntimeError("order[%s] inst_id [%s] is not same as inst_id [%s] of position" % (
                order.ord_id, order.inst_id, self.inst_id))

        if order.ord_id in self.orders:
            raise RuntimeError("order[%s] already exist" % order.ord_id)
        self.orders[order.ord_id] = order
        self.size += order.qty if order.action == OrdAction.BUY else -order.qty

    def filled_qty(self):
        qty = 0
        for key, order in self.orders.iteritems():
            qty += order.filled_qty if order.action == OrdAction.BUY else -order.filled_qty
        return qty

    def current_value(self):
        return self.last_price * self.filled_qty()

    def __repr__(self):
        return "Position(inst_id=%s, orders=%s, size=%s, last_price=%s)" % (
            self.inst_id, self.orders, self.size, self.last_price
        )


class PositionHolder(MarketDataEventHandler):
    def __init__(self):
        self.positions = {}

    def open_position(self, order):
        if order.inst_id not in self.positions:
            self.positions[order.inst_id] = Position(inst_id=order.inst_id)
        position = self.positions[order.inst_id]
        position.add_order(order)
        return position

    def update_position_price(self, time, inst_id, price):
        if inst_id in self.positions:
            position = self.positions[inst_id]
            position.last_price = price


    def on_bar(self, bar):
        self.update_position_price(bar.timestamp, bar.inst_id, bar.close)

    def on_quote(self, quote):
        self.update_position_price(quote.timestamp, quote.inst_id, quote.mid())

    def on_trade(self, trade):
        self.update_position_price(trade.timestamp, trade.inst_id, trade.price)