# -*- coding: utf-8 -*-

from PIL import Image
import numpy as np
import json
import os


# im = Image.open("./images/1234.png")
path = "./images/"
ims = list()


def pic_to_array(image):
    im = Image.open(path+image)
    name = image.split(".")[0]
    im = im.convert("L")
    data = im.getdata()
    data = np.matrix(data)
    # 把data封装成字典
    data = {name: data.tolist()}
    ims.append(data)


def get_all_pic():
    file_list = os.listdir(path)
    for img in file_list:
        pic_to_array(img)
    with open("ims.py", "w+") as f:
        f.write("ims = ")
        json.dump(ims, f)


get_all_pic()