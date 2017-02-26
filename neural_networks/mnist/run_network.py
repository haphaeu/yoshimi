import mnist
import network

training_data, test_data = mnist.load()
net = network.Network([784, 30, 10])
net.SGD(training_data, 20, 10, 3.0, test_data=test_data)
