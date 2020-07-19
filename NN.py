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
                # print("i =", i, "neiron =", self.neurons[i])
                # print("i =", i, "j =", j, "weight =", self.weight[i][j])
                summa+=self.neurons[i]*self.weight[i][j]
                # print("summa =", summa)
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
        self.E = 0.7
        self.alfa = 0.3

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
        delta = [[]]#массив дельт нейронов
        delta_w = []#массив дельт весов
        delta_w_prev = [i*0 for i in range(0,6)]
                                                                #Метод обратного распространения
        for i in range(len(getted_output)):
            delta[0].append((ideal_number[i] - getted_output[i])*((1 -getted_output[i])*getted_output[i]))#ищем дельту и записываем для нейронов выходного слоя
                                                                                                          #по соответствующей формуле
        # print("delta", delta)

        #цикл для поиска дельты скрытых слоев. Идем с по сети с конца, исключая входной слой(так как для него не нужна дельта)
        #и выходной(для него уже найдена дельта)
        for i in reversed(range(len(self.layers[1:-1]))):
            delta.append([])
            for neuron in range(len(self.layers[i].neurons)):#внутри выбранного скрытого слоя идем по нейронам
                delta[len((self.layers[1:-1]))-i].append(((1 - self.layers[i+1].neurons[neuron])*self.layers[i+1].neurons[neuron]))#считаем первую часть
                for k in self.layers[i+1].weight[neuron]:#множаем посчитанную первую часть формулы на сумму весов синапсов и дельт инцидентных им нейронов
                    delta[len((self.layers[1:-1]))-i][neuron] *= k*delta[len((self.layers[1:-1]))-i-1][neuron-1]#нашли дельту для всех нейронов,
                                                                                                                #теперь нужно найти градиент и 
                                                                                                                #перераспределить веса
        delta.append([])#добавили еще один подмассив для входного слоя(он будет пустым)
        delta.reverse()#переворачиваем массив с дельтами, потому что они были записаны vice versa
        print("delta", delta)

        #цикл для рассчета градиентов для каждого синапса по найденным в предыдущем цикле дельтам
        for layer in range(len(self.layers)-1):
            for neuron in range(len(self.layers[layer].neurons)):
                for weight in range(len(self.layers[layer].weight[neuron])):
                    grad_w = delta[layer+1][weight]*self.layers[layer].neurons[neuron]#щем градиент для синапса
                    delta_w.append(self.E * grad_w + self.alfa*delta_w_prev[weight])#ищем дельту веса
                    self.layers[layer].weight[neuron][weight] += delta_w[-1]#смещаем вес синапса на полученную дельту, тем самым обновляя его
        print("correct_weight",self.layers[0].weight, self.layers[1].weight)

                                                                #Метод обратного распространения

if __name__ == '__main__':
    net = neuron_network_with_teacher([2, 2, 1])
    net.layers[0].weight = [[0.45, 0.78],[-0.12, 0.13]]
    net.layers[1].weight = [[1.5],[-2.3]]
    print(net.start([1, 0]))
    error = net.get_error([1])
    print("error = %.3f%%" % error)
    # print(net.layers[])
    while error!=0:
        net.correct_weight([1])
        print(net.start([1, 0]))
        error = net.get_error([1])
        print("error = %.3f%%" % error)
    # print(net.layers[0].weight)


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