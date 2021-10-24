import sys
import math
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from interpol import slice_np_arr


def sort_edges(a):
	shift = 25 # TODO: shift need to be passed to function!!
	for res, coords in a:
		quater_center_x = np.mean()
		X,Y = np.where(res>250)
		X_ = X+coords[0]*shift
		Y_ = Y+coords[1]*shift
		pass

	q = a[0][0]
	X,Y = np.where(q>250)
	print(X,Y)
	return None


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

	quaters = sort_edges(quaters)

	for r, coords in quaters:
		X,Y = np.where(r>250)
		X_ = X+coords[0]*shift
		Y_ = Y+coords[1]*shift
		a,b,c = np.polyfit(X_,Y_,2)
		fun += [[a,b,c,X_]]

	return fun

def find_middle_pts(fun):
	def foo(*args):
		a,b,c,X = args[0]
		return np.array(list(zip(X, X**2*a + X*b + c)))
	res = []
	for i in range(len(fun)-1):
		A,B = fun[i:i+2]
		res += [(foo(A)[-1] + foo(B)[0]) // 2]

	return res

def draw_pts(img,pts):
	for p in pts:
		cv.circle(img, (int(p[1]), int(p[0])), 4,(255,255,255), -1)
	cv.imwrite('%s_res.jpg' % (sys.argv[1].split(".")[0]), img)

if __name__ == '__main__':
	img = cv.imread(sys.argv[1],1)
	res = img_to_fun(img)
	draw_pts(img, find_middle_pts(res))

