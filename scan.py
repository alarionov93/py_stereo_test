import cv2 as cv
import numpy as np
import sys

img = cv.imread(sys.argv[1], 0)
# np.unique(img)
white_pxs = int(np.histogram(img, 10)[1][9])
img[np.where(img >=white_pxs)] = 255
img[np.where(img < white_pxs)] = 0

Y,X = np.where(img >= white_pxs)
a,b,c = np.polyfit(X,Y,2)

x0 = np.min(X)
x1 = np.max(X)
X_ = np.linspace(x0, x1, x1-x0)
Y_ = (X_**2)*a + X_*b + c
Y_[np.where((Y_< 0) | (Y_> np.max(Y)))] = 0
X_[np.where((X_< 0) | (X_> np.max(X)))] = 0
img = cv.imread(sys.argv[1], 1)
img[(Y_.astype(np.int32), X_.astype(np.int32))] = [0,0,255]
cv.imwrite('%s_res.jpg' % sys.argv[1], img)