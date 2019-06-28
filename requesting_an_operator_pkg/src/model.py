from chainer import Chain
from chainer import links as L
from chainer import functions as F

from numpy import argmax, array


# channel width  height
#    3     640    640

class SPR(Chain):
	def __init__(self):
		super(SPR, self).__init__()

		with self.init_scope():
			self.conv1 = L.Convolution2D(None, 16, 5, 1)
			# maxpooling
			self.conv2 = L.Convolution2D(None, 32, 5, 1)
			# maxpooling
			self.conv3 = L.Convolution2D(None, 64, 3, 1)
			self.conv4 = L.Convolution2D(None, 64, 3, 1)
			self.conv5 = L.Convolution2D(None, 32, 3, 1)
			# maxpooling
			self.line6 = L.Linear(None, 2048)
			self.line7 = L.Linear(None, 1024)
			self.line8 = L.Linear(None, 2)

	def __call__(self, x):
		h = F.relu(self.conv1(x))
		h = F.max_pooling_2d(h, 3, 1)
		h = F.relu(self.conv2(h))
		h = F.max_pooling_2d(h, 3, 1)
		h = F.relu(self.conv3(h))
		h = F.relu(self.conv4(h))
		h = F.relu(self.conv5(h))
		h = F.max_pooling_2d(h, 3, 1)
		h = F.relu(self.line6(h))
		h = F.relu(self.line7(h))
		h = F.relu(self.line8(h))

		return h


class Cifar(Chain):
	def __init__(self):
		super(Cifar, self).__init__()

		with self.init_scope():
			self.conv1 = L.Convolution2D(3, 3, 5, pad=2)
			self.conv2 = L.Convolution2D(3, 6, 5, pad=2)
			# maxpooling
			self.conv3 = L.Convolution2D(6, 6, 5, pad=2)
			self.conv4 = L.Convolution2D(6, 12, 5, pad=2)
			# maxpooling
			self.conv5 = L.Convolution2D(12, 12, 4, pad=2)
			self.conv6 = L.Convolution2D(12, 12, 4, pad=2)
			self.conv7 = L.Convolution2D(12, 24, 4, pad=2)
			# maxpooling
			self.conv8 = L.Convolution2D(24, 24, 3, pad=2)
			self.conv9 = L.Convolution2D(24, 24, 3, pad=2)
			self.conv10 = L.Convolution2D(24, 48, 3, pad=2)
			# maxpooling
			self.conv11 = L.Convolution2D(48, 48, 2, pad=2)
			self.conv12 = L.Convolution2D(48, 48, 2, pad=2)
			self.conv13 = L.Convolution2D(48, 96, 2, pad=2)
			# maxpooling
			self.conv14 = L.Convolution2D(96, 96, 2, pad=2)

			self.line1 = L.Linear(11616, 4096)
			self.line2 = L.Linear(4096, 4096)
			self.line3 = L.Linear(4096, 10)

	def __call__(self, x):
		h1 = F.relu(self.conv1(x))
		h2 = F.max_pooling_2d(F.relu(self.conv2(h1)), 2)

		h3 = F.relu(self.conv3(h2))
		h4 = F.max_pooling_2d(F.relu(self.conv4(h3)), 2)

		h5 = F.relu(self.conv5(h4))
		h6 = F.relu(self.conv6(h5))
		h7 = F.max_pooling_2d(F.relu(self.conv7(h6)), 2)

		h8 = F.relu(self.conv8(h7))
		h9 = F.relu(self.conv9(h8))
		h10 = F.max_pooling_2d(F.relu(self.conv10(h9)), 2)

		h11 = F.relu(self.conv11(h10))
		h12 = F.relu(self.conv12(h11))
		h13 = F.max_pooling_2d(F.relu(self.conv13(h12)), 2)

		h14 = F.relu(self.conv14(h13))

		h15 = F.relu(self.line1(h14))
		h16 = F.relu(self.line2(h15))
		h17 = F.relu(self.line3(h16))

		return h17
