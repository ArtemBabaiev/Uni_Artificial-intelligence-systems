import numpy as np
import sys
from PIL import Image
from keras.datasets import mnist
from keras.preprocessing import image
from keras import utils
import matplotlib.pyplot as plt

class Layer:
    def __init__(self, inputSize: int, outputSize: int) -> None:
        self.synaptic_weights = 2 * np.random.random((inputSize, outputSize)) - 1
        #print(self.synaptic_weights)

    def produce(self, inputs):
        return self.__sigmoid(np.dot(inputs, self.synaptic_weights))

    def __sigmoid(self, x):
        return 1 / (1 + np.exp(-x))


class NeuralNetwork:
    def __init__(self) -> None:
        self.layers: list[Layer] = []
        pass

    def add(self, layer: Layer):
        self.layers.append(layer)

    def train(self, x_train, y_train, epochs: int, learning_rate):
        layersN = len(self.layers)
        lastIndex = layersN - 1
        for iteration in range(epochs):
            sys.stdout.write("\rEpoch " + str(iteration) + " started")
            history = self.get_history(x_train)
            #0,1,2,3,4
            inputs = history[0]
            outputs = history[1]
            
            input = inputs[lastIndex]
            output = outputs[lastIndex]
            error = y_train - output
            delta = error * self.__sigmoid_derivative(output)
            adjustment = np.dot(input.T, delta) * learning_rate
            self.layers[lastIndex].synaptic_weights += adjustment
            for i in reversed(range(lastIndex)):
                error = np.dot(delta, self.layers[i+1].synaptic_weights.T)
                delta = error * outputs[i]
                input = inputs[i]
                adjustment = np.dot(input.T, delta) * learning_rate
                self.layers[i].synaptic_weights += adjustment
            sys.stdout.flush()
        print()



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
    (x_train, y_train), _ = mnist.load_data()

    index = 103
    #print("\n".join(["".join(["{:4}".format(item) for item in row]) for row in x_train[index]]))

    plt.imshow(x_train[index].reshape(28, 28), cmap=plt.cm.binary)
    plt.show()

    num_pixels = x_train.shape[1] * x_train.shape[2]
    x_train = np.array(x_train.reshape((x_train.shape[0], num_pixels)), dtype=np.longdouble)

    x_train = x_train / 255
    
    y_train = utils.to_categorical(y_train)

    network = NeuralNetwork()
    network.add(Layer(784, 380))
    network.add(Layer(380, 10))

    network.train(x_train[:100], y_train[:100], 10000, 0.005)
    
    prediction = network.predict(x_train[index])
    print(np.argmax(prediction))
    print(prediction)
    print(y_train[index])

    img_path = "./3.png"
    img = image.load_img(img_path, target_size=(28, 28), color_mode = "grayscale")
    plt.imshow(img.convert('RGBA'))
    plt.show()
    x = image.img_to_array(img)
    x = x.reshape(1, 784)
    x = 255 - x
    x = x/255
    prediction = network.predict(x)
    print(np.argmax(prediction))
    
