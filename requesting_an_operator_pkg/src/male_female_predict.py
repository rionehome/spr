#!/usr/bin/env python
# -*- coding: utf-8 -*-

import model as M
import os
import numpy as np
from PIL import Image
import shutil
import chainer.links as L
from chainer.datasets import tuple_dataset
from chainer import serializers
import matplotlib.pyplot as plt
import glob

dicpath = os.path.dirname(os.path.abspath(__file__))
dirpath = dicpath.replace("requesting_an_operator_pkg/src", "requesting_an_operator_pkg/images/predict/")
modelpath = dicpath.replace("requesting_an_operator_pkg/src", "requesting_an_operator_pkg/images/AlexlikeMSGD.model")
female_path = dicpath.replace("requesting_an_operator_pkg/src", "requesting_an_operator_pkg/images/female")
male_path = dicpath.replace("requesting_an_operator_pkg/src", "requesting_an_operator_pkg/images/male")


def image2data(pathsAndLabels):
	allData = []
	for pathAndLabel in pathsAndLabels:
		path = pathAndLabel[0]
		label = pathAndLabel[1]
		imagelist = glob.glob(path + "*")
		for imgName in imagelist:
			allData.append([imgName, label])
	allData = np.random.permutation(allData)

	imageData = []
	labelData = []
	for pathAndLabel in allData:
		img = Image.open(pathAndLabel[0])
		try:
			imgData = np.asarray(img).transpose(2, 0, 1).astype(np.float32) / 255.
		except ValueError:
			continue
		imageData.append(imgData)
		labelData.append(np.int32(pathAndLabel[1]))
	data = tuple_dataset.TupleDataset(imageData, labelData)

	return data


def main(msg):
	print(msg)
	cls_names = ['女', '男']

	model = M.Alex()
	model = L.Classifier(model)

	# ファイルの削除&生成
	if os.path.exists(female_path):
		shutil.rmtree(female_path)
	os.mkdir(female_path)

	# ファイルの削除&生成
	if os.path.exists(male_path):
		shutil.rmtree(male_path)
	os.mkdir(male_path)

	serializers.load_npz(modelpath, model)

	pathsAndLabels = []
	pathsAndLabels.append(np.asarray([dirpath, 0]))

	data = image2data(pathsAndLabels)

	f_count = 0
	m_count = 0

	for x, t in data:
		model.to_cpu()
		y = model.predictor(x[None, ...]).data.argmax(axis=1)[0]
		print(" Prediction : " + cls_names[y])
		if (y == 0):
			f_image = (female_path + "/female_%02d.png" % f_count)
			plt.imsave(f_image, x.transpose(1, 2, 0))
			f_count = f_count + 1
		else:
			m_image = (male_path + "/male_%02d.png" % m_count)
			plt.imsave(m_image, x.transpose(1, 2, 0))
			m_count = m_count + 1

	all = str(f_count + m_count) + "people"
	males = str(m_count) + "males"
	females = str(f_count) + "females"
	print(str(all))
	print(str(males))
	print(str(females))
	return m_count
