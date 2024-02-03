from numpy import exp, array, random, dot, maximum

class Layer:
    def __init__(self, inputSize: int, outputSize: int) -> None:
        self.synaptic_weights = 2 * random.random((inputSize, outputSize)) - 1
        #print(self.synaptic_weights)

    def produce(self, inputs):
        return self.__sigmoid(dot(inputs, self.synaptic_weights))

    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))


class NeuralNetwork:
    def __init__(self) -> None:
        self.layers: list[Layer] = []
        pass

    def add(self, layer: Layer):
        self.layers.append(layer)

    def train(self, x_train, y_train, epochs: int):
        layersN = len(self.layers)
        lastIndex = layersN - 1
        for iteration in range(epochs):
            history = self.get_history(x_train)
            #0,1,2,3,4
            inputs = history[0]
            outputs = history[1]
            
            input = inputs[lastIndex]
            output = outputs[lastIndex]
            error = y_train - output
            delta = error * self.__sigmoid_derivative(output)
            adjustment = dot(input.T, delta)
            self.layers[lastIndex].synaptic_weights += adjustment
            for i in reversed(range(lastIndex)):
                error = dot(delta, self.layers[i+1].synaptic_weights.T)
                delta = error * outputs[i]
                input = inputs[i]
                adjustment = dot(input.T, delta)
                self.layers[i].synaptic_weights += adjustment

            #error = training_set_outputs - output
            #delta = error * self.__sigmoid_derivative(output)
            #adjustment = dot(training_set_inputs.T, delta)

#4*3 4*1 4*3
    def get_history(self, input):
        outputs = []
        inputs = []
        layerInput = input
        layerOutput = []
        for layer in self.layers:
            layerOutput = layer.produce(layerInput)
            inputs.append(layerInput)
            outputs.append(layerOutput)
            layerInput = layerOutput
        return [inputs, outputs]
        
    def predict(self, input):
        layerInput = input
        layerOutput = []
        for layer in self.layers:
            layerOutput = layer.produce(layerInput)
            layerInput = layerOutput
        return layerOutput
    
    def __sigmoid_derivative(self, x):
        return x * (1 - x)


if __name__ == "__main__":
    network = NeuralNetwork()
    network.add(Layer(3, 2))
    network.add(Layer(2, 1))
    training_set_inputs = array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])
    training_set_outputs = array([[0, 1, 1, 0]]).T
    network.train(training_set_inputs, training_set_outputs, 10000)
    print(network.predict(array([0, 0, 1])))
