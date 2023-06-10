import numpy as np
import matplotlib.pyplot as plt
from keras.utils.np_utils import normalize
from keras.datasets import mnist
from PIL import Image
(x_train, t_train), (x_test, t_test) = mnist.load_data()
x_train_reshaped = x_train.reshape(60000,784)
x_test_reshaped = x_test.reshape(10000,784)
print(x_train_reshaped.shape)
print(t_train.shape)
img=x_train_reshaped[0]
def img_show(img):
  pil_img=Image.fromarray(np.uint8(img))
  pil_img.show()
label=t_train[0]
print(label)
img=img.reshape(28,28)
img_show(img)
