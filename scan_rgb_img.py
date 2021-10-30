import sys
import math
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from interpol import slice_np_arr
from geomdl import NURBS, knotvector


def get_nurbs_crv(pts):
	refvec = [1, 0]

	crv = NURBS.Curve()
	crv.degree = 290
	crv.ctrlpts = pts
	crv.knotvector = knotvector.generate(crv.degree, crv.ctrlpts_size)
	curve = np.array(crv.evalpts)

	return curve

def get_polar_coords(coords):
	pure_x,pure_y = coords[:2]
	avg_x,avg_y = coords[2:]
	x = pure_x - avg_x
	y = pure_y - avg_y
	ph = 0

	if x>0 and y>0:
		ph = math.degrees(math.atan(abs(y/x)))
	elif x>0 and y<0:
		ph = 360-math.degrees(math.atan(abs(y/x)))
	elif x<0 and y<0:
		ph = 180+math.degrees(math.atan(abs(y/x)))
	elif x<0 and y>0:
		ph = 180-math.degrees(math.atan(abs(y/x)))
	else:
		print("ФУЦКИНГ ERROR!!")

	ro = int(math.sqrt(x**2 + y**2))

	return (ro, ph, int(pure_x), int(pure_y))

def sort_edges(edges):
	X,Y = np.where(edges>250)
	avg_x, avg_y = (np.mean(X), np.mean(Y))
	res = [get_polar_coords((x, y, avg_x, avg_y)) for x, y in zip(X,Y)]
	# print(avg_x, avg_y)

	return sorted(res, key=lambda e: e[1])

def img_to_edges_sorted(img, hbi=84, hbj=94):
	img_red_c = img[:,:,2]
	img_green_c = img[:,:,1]
	img_blue_c = img[:,:,0]
	mask_g = (img_green_c < int(hbi)) & (img_blue_c  < int(hbi)) & (img_red_c > int(hbj))
	edges = cv.Canny(img_red_c * mask_g,200,255)
	# plt.imshow(edges)
	fun = []
	# quaters = slice_np_arr(edges, shift)
	curve_cord = []

	# s_edges is in polar coordinates and in casterian (ro, ph, x, y)!
	s_edges = sort_edges(edges)
	# print(s_edges)
	# # TODO: remove this фуцкинг шыт from отсюда!
	# X,Y = np.where(edges>250)
	# avg_x, avg_y = (np.mean(X), np.mean(Y))
	# res = []
	# for s in s_edges:
	# 	x = s[0] + math.cos(s[1])
	# 	y = s[0] + math.sin(s[1])
	# 	res += [(x,y)]

	# for r, coords in quaters:
	# 	X,Y = np.where(r>250)
	# 	X_ = X+coords[0]*shift
	# 	Y_ = Y+coords[1]*shift
	# 	a,b,c = np.polyfit(X_,Y_,2)
	# 	fun += [[a,b,c,X_]]
	# print(res)
	return s_edges

# def find_middle_pts(fun):
# 	def foo(*args):
# 		a,b,c,X = args[0]
# 		return np.array(list(zip(X, X**2*a + X*b + c)))
# 	res = []
# 	for i in range(len(fun)-1):
# 		A,B = fun[i:i+2]
# 		res += [(foo(A)[-1] + foo(B)[0]) // 2]

# 	return res

def draw_pts(img,pts):
	for p in pts:
		# print(p)
		cv.circle(img, (int(p[1]), int(p[0])), 4,(255,255,255), -1)
	cv.imwrite('%s_res.jpg' % (sys.argv[1].split(".")[0]), img)

if __name__ == '__main__':
	img = cv.imread(sys.argv[1],1)
	res = img_to_edges_sorted(img)
	# draw_pts(img, res)
	# X = [r[1] for r in res]
	res += [res[-1]]
	RO_ = [res[i][0]-res[i-1][0] for i in range(1, len(res))]
	dRO_min = np.mean(RO_) - np.ceil(np.std(RO_))
	dRO_max = np.mean(RO_) + np.ceil(np.std(RO_))
	try:
		X_res = [res[i] for i in range(len(res)-1) if dRO_min<RO_[i]<dRO_max]
		X_res += [res[0]]
		# plt.plot([X_res[i][2] for i in range(len(X_res))],[X_res[i][3] for i in range(len(X_res))])
		curve = get_nurbs_crv([[X_res[i][2],X_res[i][3]] for i in range(len(X_res))])
		plt.imshow(img)
		plt.plot(curve[:,1], curve[:,0])
	except IndexError:
		print(u"\U0001F914 Эээм...")
	except TypeError:
		print(u"\U0001F610 Ой!")
	except Exception as e:
		print(u"\U0001F643 Упс! Почитайте про ошибку ниже..")
		print(e)
	# plt.plot(X,Y)
	# plt.show()
	# print(X_res)
	plt.show()
