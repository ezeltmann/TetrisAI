from math import exp

class ActivationFunctions():
    def __init__(self, alpha=0):
        self._alpha = alpha

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, new_alpha):
        if (new_alpha >= 0 and new_alpha <= 1):
            self._alpha = new_alpha
        else:
            raise ValueError(f"The New Alpha value must be between [0,1].  You submitted: {new_alpha}")

    def sigmoid(x):
        return (1/(1 + exp(-x)))

    def relu(x):
        if (x > 0):
            return x
        else:
            return 0

    def tanh(x):
        return ((exp(x) - exp(-x))/(exp(x) + exp(-x)))

    def linear(x):
        return x

    def prelu(self, x):
        if (x >= 0):
            return x
        else:
            return (self.alpha * x)