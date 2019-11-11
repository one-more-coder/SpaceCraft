import numpy
import random


class NeuralNetwork:

    """
    weight[0] will signify the weight between spacecraft and top pipes bottom surface.
    weight[1] will signify the weight between spacecraft and bottom pips top surface.
    """
    weights = [0.0] * 2
    bias = [0.0] * 1


    def __init__(self):
        self.weights[0] = random.random()
        self.weights[1] = (-1) * random.random()
        self.bias[0] = random.random()

    def my_variable(self):
        print(str(self.weights[0]))
        print(str(self.weights[1]))

    def predict(self,inputs):
        #inputs array contain x1 and x2
        #input = inputs
        y = self.weights[0]*int(inputs[0]) + self.weights[1]*int(inputs[1]) + self.bias[0]
        # 1 signifies move upward and 0 downwards
        if y > 0 :
            return 1
        else:
            return  0

#t = NeuralNetwork()
#t.my_variable()
#print(t.predict((2,2)))
