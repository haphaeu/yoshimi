# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 16:15:51 2017

Read data from MNIST and converts it to be used with the neural network implementation in
network.py

[1] http://yann.lecun.com/exdb/mnist/

 TRAINING SET LABEL FILE (train-labels-idx1-ubyte):
 [offset] [type]          [value]          [description]
 0000     32 bit integer  0x00000801(2049) magic number (MSB first)
 0004     32 bit integer  60000            number of items
 0008     unsigned byte   ??               label
 0009     unsigned byte   ??               label
........
 xxxx     unsigned byte   ??               label

The labels values are 0 to 9.
 TRAINING SET IMAGE FILE (train-images-idx3-ubyte):
 [offset] [type]          [value]          [description]
 0000     32 bit integer  0x00000803(2051) magic number
 0004     32 bit integer  60000            number of images
 0008     32 bit integer  28               number of rows
 0012     32 bit integer  28               number of columns
 0016     unsigned byte   ??               pixel
 0017     unsigned byte   ??               pixel
........
 xxxx     unsigned byte   ??               pixel

 Pixels are organized row-wise. Pixel values are 0 to 255. 0 means background (white), 255 means
 foreground (black).


@author: raf
"""


import gzip
import struct
import numpy as np
from matplotlib import pyplot as plt


def fetch():
    import urllib.request
    from os import path
    print("Fetching data from MNIST.")
    urls = ["http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz",
            "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz",
            "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz",
            "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz"]
    for url in urls:
        fname = path.basename(url)
        if path.exists(fname):
            print(fname, "already exists")
        else:
            print("Downloading", url)
            urllib.request.urlretrieve(url, fname)


def load():
    """Loads training and test data"""

    # reads labels
    with gzip.open('train-labels-idx1-ubyte.gz', 'rb') as pf:
        magic, num = struct.unpack(">II", pf.read(2*4))
        labels = struct.unpack("B" * num, pf.read(num))

    # reads the images.
    with gzip.open('train-images-idx3-ubyte.gz', 'rb') as pf:
        magic, num, rows, cols = struct.unpack(">IIII", pf.read(4*4))
        images = [struct.unpack("B" * rows*cols, pf.read(rows*cols)) for _ in range(num)]
    # re-shapes it to a column vector and normalises it
    images = [np.reshape(x, (rows*cols, 1))/255.0 for x in images]
    # vectorise the labels, eg, 5 will be [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    labels = [vectorise_label(j) for j in labels]
    train_data = list(zip(images, labels))

    with gzip.open('t10k-labels-idx1-ubyte.gz', 'rb') as pf:
        magic, num = struct.unpack(">II", pf.read(2*4))
        labels = struct.unpack("B" * num, pf.read(num))

    with gzip.open('t10k-images-idx3-ubyte.gz', 'rb') as pf:
        magic, num, rows, cols = struct.unpack(">IIII", pf.read(4*4))
        images = [struct.unpack("B" * rows*cols, pf.read(rows*cols)) for _ in range(num)]
    # re-shapes it to a column vector and normalises it
    images = [np.reshape(x, (rows*cols, 1))/255.0 for x in images]
    # note that for the test data, we don't need the vector form of the labels...
    test_data = list(zip(images, labels))

    return (train_data, test_data)


def vectorise_label(j):
    """# vectorise the labels, eg, 5 --> [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]"""
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e


def interpret_vector(v):
    """inverse function of vectorise_label, [0, 0, 0, 0, 0, 1, 0, 0, 0, 0] --> 5"""
    return v.argmax()


def show(images, sz=(28, 28), w=8):
    """plots one of more images and their correct labels"""
    from matplotlib.cm import gray
    num = len(images)
    fig = plt.figure()
    for i, img in enumerate(images):
        raw, lbl = img
        ax = fig.add_subplot((num-1)//w+1, min(w, num), i+1)
        imgplot = ax.imshow(1.0-raw.reshape(sz), cmap=gray)
        imgplot.set_interpolation('nearest')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_axis_off()
        ax.text(28, 28, lbl if isinstance(lbl, int) else interpret_vector(lbl))
    plt.show()


def test_mnist(num=64):
    """simple test of loaded data and plot images"""
    train, test = load()
    np.random.shuffle(train)
    np.random.shuffle(test)
    show(train[:num//2]+test[:num//2])
