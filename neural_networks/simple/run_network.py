import numpy as np
from os import path
# import network
# import network_full as network
import network
from random import random
from matplotlib import pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 12, 7


# ################################################################
# Network specific inputs
global count_n
global req_output_sz
count_n = 6
req_output_sz = count_n
network.vectorized_result.sz = req_output_sz


def gen_data(n_train, n_test):
    """This function fakes training and test data.
    Use creativity here to model and train nn on anything =)

    Implemented below is a list of random numbers, with the
    expected output being the index of the highest number.
    So for example:
                 x           =>    vect(y)   => y
        [0.2, 0.4, 0.2, 0.7] => [0, 0, 0, 1] => 3
        [0.9, 0.4, 0.2, 0.5] => [1, 0, 0, 0] => 0
    """
    data_train, data_test = [], []
    for i in range(n_train):
        lst = np.array([random() for _ in range(count_n)])
        tot = network.vectorized_result(np.argmax(lst))
        data_train.append([lst.reshape((count_n, 1)), tot])
    for i in range(n_test):
        lst = np.array([random() for _ in range(count_n)])
        tot = np.argmax(lst)
        data_test.append([lst.reshape((count_n, 1)), tot])
    return data_train, data_test

# ################################################################


"""
Some convenient functions to extend the class Network
"""


def check(net, data):
    for datai in data:
        x, y = datai
        a = np.argmax(net.feedforward(x))
        print('%d --> %d %s' % (y, a, '' if y == a else 'WRONG'))
network.Network.check = check


def save_state(self, fname='netstate'):
    """Save the current weights and biases of the network."""
    import pickle
    with open(fname, 'wb') as pf:
        pickle.dump([self.biases, self.weights], pf)
network.Network.save_state = save_state


def load_state(self, fname='netstate'):
    """Load a previously saved weights and biases of the network."""
    import pickle
    with open(fname, 'rb') as pf:
        self.biases, self.weights = pickle.load(pf)
network.Network.load_state = load_state

# ###
# # quebrando as chamadas pra poder brincar com isso
# ###

training_data, test_data = 0, 0
def load_data():
    global training_data, test_data
    training_data, test_data = gen_data(100000, 10000)


net = 0
def init_net(hidden_layers=15):
    global net
    net = network.Network([count_n, hidden_layers, req_output_sz], cost=network.CrossEntropyCost)


def train(epochs=5, eta=0.5, lmbda=0.5):
    # set lmbda proportional to training set size: 5 for 50000, 0.1 for 1000.
    return net.SGD(training_data, epochs, 10, eta=eta, lmbda=lmbda, evaluation_data=test_data,
                   monitor_evaluation_cost=True, monitor_evaluation_accuracy=True,
                   monitor_training_cost=True, monitor_training_accuracy=True)


def main():

    if True:

        load_data()
        init_net(150)
        ret = train(500, 0.1, 2.0)
        return ret

    epochs = 50
    # Default hydden layers, epochs, eta, lambda
    defaults = [15, 0.5, 0.5]

    cases = {'lmbda': [0.1, 0.2, 0.5, 1.0, 2.0, 5.0],
             'eta': [0.1, 0.2, 0.5, 1.0, 2.0, 5.0],
             'hidden_layers': [15, 35, 70, 150]
             }

    load_data()

    for var in cases:
        for val in cases[var]:
            hidden_layers, eta, lmbda = defaults
            if var == 'lmbda':
                lmbda = val
                title = 'Epochs %d, Layers %d, eta %.2f' % (epochs, hidden_layers, eta)
            elif var == 'eta':
                eta = val
                title = 'Epochs %d, Layers %d, lambda %.2f' % (epochs, hidden_layers, lmbda)
            elif var == 'hidden_layers':
                hidden_layers = val
                title = 'Epochs %d, eta %d, lambda %.2f' % (epochs, eta, lmbda)

            init_net(hidden_layers)
            ret = train(epochs, eta, lmbda)

            plt.subplot(211)
            plt.plot(ret[0], label=var + str(val))
            plt.legend(loc='best')
            plt.title(title)

            plt.subplot(212)
            plt.plot(np.array(ret[1]))

            plt.savefig('%s.png' % var, bbox_inches='tight')
        plt.close()


if __name__ == '__main__':
    ret = main()
