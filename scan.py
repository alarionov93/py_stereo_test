'''
Программа определения кривизны образцов.
'''

import cv2 as cv
import numpy as np
import sys
from glob import glob
from itertools import product

font = cv.FONT_HERSHEY_SIMPLEX
org = (50, 50)
fontScale = 5
color = (255, 0, 0)
thickness = 2

speciments = ['%s%s' % (a,str(b)) for a,b in list(product(list('ABC'),range(1,6)))]
for f, s in zip(glob('img/in/*'), speciments):
	img = cv.imread(f, 0)
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
	img = cv.imread(f, 1)
	img[(Y_.astype(np.int32), X_.astype(np.int32))] = [0,0,255]

	img = cv.putText(img, '[%s] y=%s^2 x + %s x + %s' % (s,round(a,2),round(b,2),round(c,2)), org, font, 
                   fontScale, color, thickness, cv.LINE_AA)
	cv.imwrite('%s_res.jpg' % f, img)


