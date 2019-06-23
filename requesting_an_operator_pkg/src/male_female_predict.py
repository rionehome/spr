#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import model as M
import os
import sys
import cv2
import rospy
from std_msgs.msg import String
import numpy as np
import argparse
from PIL import Image

import pickle
import chainer
import chainer.functions as F
import chainer.links as L
import chainer.serializers
from chainer.datasets import tuple_dataset
from chainer import Chain, Variable, optimizers, serializers
from chainer import training
from chainer.training import extensions
import re
import matplotlib.pyplot as plt
import glob
dicpath = os.path.dirname(os.path.abspath(__file__))
dirpath = dicpath.replace("requesting_an_operator_pkg/src","requesting_an_operator_pkg/images/predict/")
modelpath = dicpath.replace("requesting_an_operator_pkg/src","requesting_an_operator_pkg/images/AlexlikeMSGD.model")
female_path = dicpath.replace("requesting_an_operator_pkg/src","requesting_an_operator_pkg/images/female")
male_path = dicpath.replace("requesting_an_operator_pkg/src","requesting_an_operator_pkg/images/male")

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
			imgData = np.asarray(img).transpose(2,0,1).astype(np.float32)/255.
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
		if(y == 0):
			f_image = (female_path+"/female_%02d.jpg" % (f_count))
			plt.imsave(f_image, x.transpose(1, 2, 0));
			f_count = f_count + 1
		else:
			m_image = (male_path+"/male_%02d.jpg" % (m_count))
			plt.imsave(m_image, x.transpose(1, 2, 0));
			m_count = m_count + 1

	all = str(f_count + m_count) + "people"
	males = str(m_count) +"males"
	females = str(f_count) + "females"
	print(str(all))
	print(str(males))
	print(str(females))


	#os.system("espeak -v f5 ' " + all + " ' -s 100")
	#os.system("espeak -v f5 ' " + males + "and" + females + " ' -s 100")
	
	#os.system('espeak -v f5 "{Who would like to play a riddle game with me?}" -s 100')
	#os.system('espeak -v f5 "{I will wait 5 seconds until you come here}" -s 100')
	#sleep(5)
	return m_count
