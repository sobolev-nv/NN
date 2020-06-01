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
        for i in range(len(number_of_layers)-1):
            self.layers.append(layer(number_of_layers[i], number_of_layers[i+1]))
        self.layers.append(layer(number_of_layers[-1], 0))

    def start(self, initialisation):
        if (len(self.layers) == 0 or self.layers[0].enter_input(initialisation, "init") == False):
            print("Bye!")
            return []

        for i in range(len(self.layers)-1):
            self.layers[i+1].enter_input(self.layers[i].get_output())
        return self.layers[-1].get_output("final")

class neuron_network_with_teacher(neuron_network):
    def __init__(self, number_of_layers):
        super(neuron_network_with_teacher, self).__init__(number_of_layers)

    def get_error(self, ideal_number):
        if (len(self.layers) == 0):
            print("Bye!")
            return -1

        getted_output = self.layers[-1].get_output("final")
        if (len(ideal_number) != len(getted_output)):
            print("Bye!")
            return -1

        error = 0
        for i in range(len(getted_output)):
            error+= ((ideal_number[i] - getted_output[i])**2)
        error /= len(getted_output)
        error = round(error, 4)*100

        return error

    def correct_weight(self, ideal_number):
        getted_output = self.layers[-1].get_output("final")
        


if __name__ == '__main__':
    net = neuron_network_with_teacher([2, 2, 1])
    net.layers[0].weight = [[0.45, 0.78],[-0.12, 0.13]]
    net.layers[1].weight = [[1.5],[-2.3]]
    print(net.start([1, 0]))
    error = net.get_error([1])
    print("error = %.3f%%" % error)


    # I = layer(2, 2)
    # H = layer(2, 1)
    # O = layer(1, 0)

    # I.enter_input([1, 0], "init")

    # H1input = I.get_output()
    # print("H1input =", H1input)
    # H.enter_input(H1input)
    # print("H1output =", H.neurons)

    # O1input = H.get_output()
    # print("O1input =", O1input)
    # O.enter_input(O1input)
    # print(O.get_output("final"))




# H1IN = (I1*W1 + I2*W2+...)