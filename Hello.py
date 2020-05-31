import random
import math

class layer():
    def __init__(self, number_of_neurons, future_number_of_neurons):
        self.neurons = []
        self.weight = []
        self.number_of_neurons = number_of_neurons
        self.future_number_of_neurons = future_number_of_neurons
        for x in range(0, number_of_neurons):
            self.neurons.append(0)
        for x in range(number_of_neurons):
            self.weight.append([])
            for y in range(future_number_of_neurons):
                self.weight[x].append(random.randint(-4, 4))

    def enter_input(self, data_input, mode=""):
        if(len(self.neurons) != len(data_input)):
            print("Bye!")
            return False
        if(mode == "init"):
            self.neurons = data_input
        else:
            for i in range(len(data_input)):
                self.neurons[i] = self.activated_func(data_input[i])
        return True

    def activated_func(self, inp):
        func = 1/(1+math.exp(-inp))
        return func

    def get_output(self, mode = ""):
        array_output = []
        for j in range(self.future_number_of_neurons):
            summa = 0
            for i in range(self.number_of_neurons):
                print("i =", i, "neiron =", self.neurons[i])
                print("i =", i, "j =", j, "weight =", self.weight[i][j])
                summa+=self.neurons[i]*self.weight[i][j]
                print("summa =", summa)
            array_output.append(summa)
        if(mode == "final"):
            array_output = self.neurons
        return array_output

class neuron_network():
    def __init__(self, number_of_layers):
        self.layers = []
        for i in range(len(number_of_layers)):
            self.layer[i].append(layer(number_of_layers[i], number_of_layers[i+1]))





if __name__ == '__main__':
    net = neuron_network([2, 2, 1])
    print(net.start([1, 0]))

    I = layer(2, 2)
    H = layer(2, 1)
    O = layer(1, 0)
    I.weight = [[0.45, 0.78],[-0.12, 0.13]]
    H.weight = [[1.5],[-2.3]]

    I.enter_input([1, 0], "init")

    H1input = I.get_output()
    print("H1input =", H1input)
    H.enter_input(H1input)
    print("H1output =", H.neurons)

    O1input = H.get_output()
    print("O1input =", O1input)
    O.enter_input(O1input)
    print(O.get_output("final"))




# H1IN = (I1*W1 + I2*W2+...)