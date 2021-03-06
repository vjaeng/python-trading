import abc

from algotrader.utils.ser_deser import Serializable


class PersistenceMode(object):
    Disable = 0
    Batch = 1
    RealTime = 2


class Persistable(Serializable):
    __metaclass__ = abc.ABCMeta

    def save(self, data_store):
        pass

    def load(self):
        pass
