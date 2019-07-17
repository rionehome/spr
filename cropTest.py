# -*- coding: utf-8 -*-
from PIL import Image
import face_recognition

# 画像のpath指定
imgname = "test"
imgpath = imgname + ".jpg"

# Dlib
dlib_img = face_recognition.load_image_file(imgpath)

# Dlib CNN
# faces = face_recognition.face_locations(dlib_img, model="cnn")  # CNNモデルで顔認識
faces = face_recognition.face_locations(dlib_img)  # 顔認識 1s未満 速さと精度のトレードオフ

print "検出結果", len(faces), "人"

# cropするためにPILで画像を開く
img = Image.open(imgpath)

# 取得したRect（top, right, bottom, left）から 96x96 にcrop
for i in range(len(faces)):
    [top, right, bottom, left] = faces[i]
    print (faces[i])
    imgCroped = img.crop((left, top, right, bottom)).resize((96, 96))
    filename = "images/predict/%s_%02d.jpg" % (imgname.split(".")[0], i)
    #filename = "%s_%02d.jpg" % (imgname.split(".")[0], i)
    imgCroped.save(filename)
