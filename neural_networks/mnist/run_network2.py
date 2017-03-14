import mnist
import time
import numpy as np
from os import path
# import network
# import network_full as network
import network2 as network


class MyImage():

    size = (28, 28)

    def __init__(self, fname, num):
        from PIL import Image
        im = Image.open(fname)
        self.num = num
        self.fname = fname

        if not MyImage.size == im.size:
            im = im.resize(self.size)

        self.im = im
        szx, szy = self.size
        # f handles getpixel() returning a single int for grayscales and a tuple for others
        f = (lambda x: x) if len(im.getpixel((0,0))) == 1 else max
        raw = np.array([f(im.getpixel((x, y))) for y in range(szy) for x in range(szx)])
        raw = np.reshape(raw, (szx*szy, 1)) / 255
        self.data = [raw, num]

    def negative(self):
        self.data[0] = 1 - self.data[0]

    def save(self):
        nm, ext = path.splitext(self.fname)
        self.im.save(nm+'_res'+ext)

    def show(self):
        szx, szy = self.size
        for i in range(szx*szy):
            print('%d' % self.data[0][i][0], end='')
            if not i%szx: print()


"""
Some convenient functions to extend the class Network
"""
def check(net, data):
    for datai in data:
        x, y = datai
        a = np.argmax(net.feedforward(x))
        print('%d --> %d' % (y, a))
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
    training_data, test_data = mnist.load()

net = 0
def init_net():
    global net
    net = network.Network([784, 80, 10], cost=network.CrossEntropyCost)


def train(epochs=5):
    # set lmbda proportional to training set size: 5 for 50000, 0.1 for 1000.
    net.SGD(training_data, epochs, 10, 3.0, evaluation_data=test_data, lmbda=5.0,
            monitor_evaluation_cost=True, monitor_evaluation_accuracy=True,
            monitor_training_cost=True, monitor_training_accuracy=True)


def test_my_images():
    imsR = [r'images\r{}.png'.format(i) for i in range(10)]
    imsM = [r'images\m{}.png'.format(i) for i in range(10)]
    # Rafs
    imgs = [MyImage(f, i) for i, f in enumerate(imsR)]
    _ = [im.negative() for im in imgs]
    # [im.save() for im in imgs]
    net.check([im.data for im in imgs])
    print('Rafs score', net.evaluate([im.data for im in imgs]))
    # Maries
    imgs = [MyImage(f, i) for i, f in enumerate(imsM)]
    _ = [im.negative() for im in imgs]
    # [im.save() for im in imgs]
    net.check([im.data for im in imgs])
    print('Maries score', net.evaluate([im.data for im in imgs]))

load_data()
init_net()
train()
#net.load_state()
#test_my_images()
