import random
import abc

class RandomNumberInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'randrange') and
                callable(subclass.randrange) and
                hasattr(subclass, 'choice') and
                callable(subclass.choice))
    
    @abc.abstractmethod
    def randrange(self, range_low, range_high):
        """Returns a random number from a given range"""
        raise NotImplementedError

    @abc.abstractmethod
    def choice(self, seq):
        """Returns a random choice from a given set of choices"""
        raise NotImplementedError


class ControlledRNG(RandomNumberInterface):
    def __init__(self):
        self.random = random
        self.random.seed(2025)
    
    def randrange(self, range_low, range_high):
        return self.random.randrange(range_low, range_high)

    def choice(self, seq):
        return self.random.choice(seq)
    
