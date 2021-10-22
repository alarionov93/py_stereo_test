import sys
import math
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from interpol import slice_np_arr

def img_to_fun(img, hbi=84, hbj=94):
	img_red_c = img[:,:,2]
	img_green_c = img[:,:,1]
	img_blue_c = img[:,:,0]
	mask_g = (img_green_c < int(hbi)) & (img_blue_c  < int(hbi)) & (img_red_c > int(hbj))
	edges = cv.Canny(img_red_c * mask_g,200,255)
	
	fun = []
	shift = 25
	quaters = slice_np_arr(edges, shift)
	curve_cord = []
	last_x = -1
	last_y = -1

	for r, coords in quaters:
		X,Y = np.where(r>250)
		X_ = X+coords[0]*shift
		Y_ = Y+coords[1]*shift
		a,b,c = np.polyfit(X_,Y_,2)
		fun += [[a,b,c,X_]]

	return fun

def foo(*args):
	a,b,c,X = args[0]
	return np.array(list(zip(X, X**2*a + X*b + c)))

if __name__ == '__main__':
	res = img_to_fun(cv.imread(sys.argv[1],1))
	for i in range(len(res)-1):
		A,B = res[i:i+2]
		print((foo(A)[-1] + foo(B)[0]) / 2)


