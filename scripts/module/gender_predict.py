#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospkg

import model
import os
import numpy as np
from PIL import Image
import shutil
import chainer.links
from chainer.datasets import tuple_dataset
from chainer import serializers
import matplotlib.pyplot as plt
import glob


class GenderPredict:
    def __init__(self, persons_path):
        self.model_path = "{}/etc/AlexlikeMSGD.model".format(rospkg.RosPack().get_path('sound_system'))
        self.persons_path = persons_path
        self.female_path = self.persons_path + "females/"
        self.male_path = self.persons_path + "males/"
        self.chainer_model = chainer.links.Classifier(model)
        
        # ディレクトリの初期化
        self.reset_dir(self.male_path)
        self.reset_dir(self.female_path)
    
    @staticmethod
    def reset_dir(dir_path):
        # type:(str)->None
        """
        logディレクトリのリセット
        :param dir_path:
        :return:
        """
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.mkdir(dir_path)
    
    def generate_dataset(self):
        """
        男女推定用データセットの作成
        :return:
        """
        __images__ = []
        __labels__ = []
        
        # 画像の読み込み
        __image_files__ = glob.glob(self.persons_path + "*")
        for image_file in __image_files__:
            __image__ = Image.open(image_file)
            try:
                __transposed_image__ = np.ndarray(np.asanyarray(__image__)).transpose((2, 0, 1)).astype(
                    np.float32) / 255.
            except ValueError:
                continue
            
            __images__.append(__transposed_image__)
            __labels__.append(np.int32(0))
        
        return tuple_dataset.TupleDataset(__images__, __labels__)
    
    def calc_judge(self):
        # type:()->tuple
        """
        男女識別の実行
        :return: (male,female)
        """
        __class_names__ = ['女', '男']
        serializers.load_npz(self.model_path, self.chainer_model)
        dataset = self.generate_dataset()
        
        __male_count__ = 0
        __female_count__ = 0
        for x, t in dataset:
            self.chainer_model.to_cpu()
            y = self.chainer_model.predictor(x[None, ...]).data.argmax(axis=1)[0]
            print "Prediction:", __class_names__[y]
            if y == 0:
                __female_image_name__ = "female_%02d.png" % __female_count__
                plt.imsave(self.female_path + __female_image_name__, x.transpose(1, 2, 0))
                __female_count__ += 1
            else:
                __male_image_name__ = "male_%02d.png" % __male_count__
                plt.imsave(self.male_path + __male_image_name__, x.transpose(1, 2, 0))
                __male_count__ += 1
        
        return __male_count__, __female_count__
