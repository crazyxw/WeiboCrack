# -*- coding: utf-8 -*-
from ims import ims
from PIL import Image
import numpy as np

path = "./images/"


def pic_to_array(image):
    """
    将图片转换成数组
    :param image:
    :return:
    """
    im = Image.open(image)
    # name = image.split(".")[0]
    # im = image
    im = im.convert("L")
    data = im.getdata()
    data = np.matrix(data)
    data = data.tolist()
    return data


def contrast_img(img1,img2):
    im1 = pic_to_array(img1)
    im2 = pic_to_array(img2)
    print(im1 == im2)
    print(im1)
    print(im2)
    print(len(im1[0]))
    print(len(im2[0]))
    is_xt = True
    for i in range(len(im1[0])):
        if im1[0][i] - im2[0][i] > 10:
            is_xt = False
    print(is_xt)


def contrast():
    """
    匹配图片
    :return:
    """
    img = "123.png"
    data = pic_to_array(img)
    for i in ims:
        for k, j in i.items():
            if data == j:
                print(k)


# contrast()
contrast_img("./images/1234.png", "./images/1243.png")
