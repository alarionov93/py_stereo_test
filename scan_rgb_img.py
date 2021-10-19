import sys
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from interpol import slice_np_arr
from geomdl import NURBS, knotvector, convert, multi, exchange
from matplotlib import pyplot as plt
import math
import numpy as np
from sort_pnt_by_circle import Sort_pnt_by_circle

from PIL import Image, ImageDraw
from PIL import ImagePath

refvec = [1, 0]

crv = NURBS.Curve()
crv.degree = 2


img = cv.imread(sys.argv[1],1)

# X,Y = [x for x in np.where(edges>0)]
img_red_c = img[:,:,2]
img_green_c = img[:,:,1]
img_blue_c = img[:,:,0]

# other way:
# X_r = np.where(img_red_c>254)[0]
# Y_r = np.where(img_red_c>254)[1]
# X_b = np.where(img_blue_c<20)[0]
# Y_b = np.where(img_blue_c<20)[1]
# X_g = np.where(img_green_c<20)[0]
# Y_g = np.where(img_green_c<20)[1]

# # TODO: cut array by the shortest one!
# X_ints = np.intersect1d(np.intersect1d(X_r, X_b), np.intersect1d(X_r, X_g))
# Y_ints = np.intersect1d(np.intersect1d(Y_r, Y_b), np.intersect1d(Y_r, Y_g))[:len(x_ints)]

# the working way

mask_g = (img_green_c < 70) & (img_blue_c  < 70) & (img_red_c > 71)
res = img_red_c * mask_g
#plt.imshow(res,cmap = 'gray')
#plt.show()

edges = cv.Canny(res,200,255)
#print(edges)
# res = interpol(edges)
# print(res)
shift = 25
res = slice_np_arr(edges, shift)
curve_cord = []

for r, coords in res:
	X,Y = np.where(r>250)
	X_ = X+coords[0]*shift
	Y_ = Y+coords[1]*shift
	a,b,c = np.polyfit(X_,Y_,2)
	#print(coords[0],coords[1])
	plt.plot(X_, X_**2 * a + X_ * b + c)
	plt.plot(X_, Y_)
	plt.plot(X_[0], Y_[0], 'ro:')
	#plt.plot(X_[-1],Y_[-1], 'ro:')
	lst = []
	lst.append(Y_[0])
	lst.append(X_[0])
	curve_cord.append(lst)
	del lst
	#print(X_[-1])
	#print(Y_[-1])

origin = curve_cord[0]
sort_figure = Sort_pnt_by_circle(origin = origin, refvec = refvec)

curve_cord = sorted(curve_cord, key=sort_figure.sort_pnt_by_circle)
curve_cord.append(curve_cord[0])

crv.ctrlpts = curve_cord
crv.knotvector = knotvector.generate(crv.degree, crv.ctrlpts_size)


curve = np.array(crv.evalpts)

plt.plot(curve[:,0], curve[:,1])

foto_link = sys.argv[1],1
#print(type(str(foto_link)))

nurb_pil = tuple(map(tuple, curve))

img = Image.open('/home/honepa/Документы/цр/трушников/img/lopatka.JPG')
#img = img.rotate(90)
img1 = ImageDraw.Draw(img)
img1.polygon(nurb_pil,  outline ="white")

img.show()
img.save('nurbs_lopatka.jpg', quality=95)

#get centr of figure
centr_x = sum(curve[:,0]) / len(curve)
centr_y = sum(curve[:,1]) / len(curve)
plt.plot(centr_x, centr_y, 'ro:')
plt.show()
# plt.imshow(edges,cmap = 'gray')
# f = plt.figure()
# plt_idx = 1
# for x,z,y in res:
# 	# a = (1,1)
# 	# plt_vals = a[0]*100 + a[1]*10 + plt_idx
# 	# y1 = f.add_subplot(plt_vals)
# 	# y1.plot(r)
# 	plt.scatter(x,y)
# 	plt.plot(x,z)

# plt.show()
