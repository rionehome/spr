# -*- coding: utf-8 -*-
import chainer
import chainer.links as L
import chainer.functions as F


class Alex(chainer.Chain):

	def __init__(self):
		super(Alex, self).__init__(
			conv1=L.Convolution2D(3, 48, 3, stride=1),
			bn1=L.BatchNormalization(48),
			conv2=L.Convolution2D(48, 128, 3, pad=1),
			bn2=L.BatchNormalization(128),
			conv3=L.Convolution2D(128, 192, 3, pad=1),
			conv4=L.Convolution2D(192, 192, 3, pad=1),
			conv5=L.Convolution2D(192, 128, 3, pad=1),
			fc6=L.Linear(None, 1024),
			fc7=L.Linear(None, 1024),
			fc8=L.Linear(None, 2)
		)
		self.train = True

	def __call__(self, x):
		h = self.bn1(self.conv1(x))
		h = F.max_pooling_2d(F.relu(h), 3, stride=2)
		h = self.bn2(self.conv2(h))
		h = F.max_pooling_2d(F.relu(h), 3, stride=2)
		h = F.relu(self.conv3(h))
		h = F.relu(self.conv4(h))
		h = F.relu(self.conv5(h))
		h = F.max_pooling_2d(F.relu(h), 2, stride=2)
		h = F.dropout(F.relu(self.fc6(h)))
		h = F.dropout(F.relu(self.fc7(h)))
		h = self.fc8(h)
		return h


class Model:
	def __init__(self):
		self.model = L.Classifier(Alex())

	def load(self, filename):
		chainer.serializer.load_npz(filename, self.model)

	def save(self, filename):
		chainer.serializer.save_npz(filename, self.model)

	def predictor(self, x):
		return self.model.predictor(x)

	def get_model(self):
		return self.model


class GoogLeNet(chainer.Chain):
	insize = 224

	def __init__(self):
		super(GoogLeNet, self).__init__(

			conv1=L.Convolution2D(3, 64, 7, stride=2, pad=3),

			conv2_reduce=L.Convolution2D(64, 64, 1),

			conv2=L.Convolution2D(64, 192, 3, stride=1, pad=1),

			inc3a=L.Inception(192, 64, 96, 128, 16, 32, 32),

			inc3b=L.Inception(256, 128, 128, 192, 32, 96, 64),

			inc4a=L.Inception(480, 192, 96, 208, 16, 48, 64),

			inc4b=L.Inception(512, 160, 112, 224, 24, 64, 64),

			inc4c=L.Inception(512, 128, 128, 256, 24, 64, 64),

			inc4d=L.Inception(512, 112, 144, 288, 32, 64, 64),

			inc4e=L.Inception(528, 256, 160, 320, 32, 128, 128),

			inc5a=L.Inception(832, 256, 160, 320, 32, 128, 128),

			inc5b=L.Inception(832, 384, 192, 384, 48, 128, 128),

			loss3_fc=L.Linear(1024, 1000),

			loss1_conv=L.Convolution2D(512, 128, 1),

			loss1_fc1=L.Linear(2048, 1024),

			loss1_fc2=L.Linear(1024, 1000),

			loss2_conv=L.Convolution2D(528, 128, 1),

			loss2_fc1=L.Linear(2048, 1024),

			loss2_fc2=L.Linear(1024, 1000)

		)

		self.train = True

	def __call__(self, x):
		h = F.relu(self.conv1(x))

		h = F.local_response_normalization(

			F.max_pooling_2d(h, 3, stride=2), n=5, k=1, alpha=2e-05)

		h = F.relu(self.conv2_reduce(h))

		h = F.relu(self.conv2(h))

		h = F.max_pooling_2d(

			F.local_response_normalization(h, n=5, k=1, alpha=2e-05), 3, stride=2)

		h = self.inc3a(h)

		h = self.inc3b(h)

		h = F.max_pooling_2d(h, 3, stride=2)

		h = self.inc4a(h)

		l = F.average_pooling_2d(h, 5, stride=3)

		l = F.relu(self.loss1_conv(l))

		l = F.relu(self.loss1_fc1(l))

		l = self.loss1_fc2(l)

		h = self.inc4b(h)

		h = self.inc4c(h)

		h = self.inc4d(h)

		l = F.average_pooling_2d(h, 5, stride=3)

		l = F.relu(self.loss2_conv(l))

		l = F.relu(self.loss2_fc1(l))

		l = self.loss2_fc2(l)

		h = self.inc4e(h)

		h = F.max_pooling_2d(h, 3, stride=2)

		h = self.inc5a(h)

		h = self.inc5b(h)

		h = F.average_pooling_2d(h, 7, stride=1)

		y = self.loss3_fc(F.dropout(h, 0.4, train=self.train))

		return y
