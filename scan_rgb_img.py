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

refvec = [0, 1]

crv = NURBS.Curve()
crv.degree = 2

def add_two_list(list1, list2):
	for i in range(len(list1)):
		list1[i].append(list2[i])
	return list1

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

mask_g = (img_green_c < 70) & (img_blue_c  < 70) & (img_red_c > 70)
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
	#plt.plot(X_, Y_)
	#plt.plot(X_[0], X_[0]**2 * a + X_[0] * b + c, 'ro:')
	#plt.plot(X_[-1],Y_[-1], 'ro:')
	lst = []
	lst.append(X_[0])
	lst.append(int(X_[0]**2 * a + X_[0] * b + c))

	curve_cord.append(lst)
	del lst

	#print(X_[-1])
	#print(Y_[-1])
centr_x = sum([x for x, y in curve_cord]) / len(curve_cord)
centr_y = sum([y for x, y in curve_cord]) / len(curve_cord)
diff = [[x1 - centr_x, y1-centr_y] for x1, y1 in curve_cord]

kv1 = [[x,y] for x, y in diff if x> 0 and y>=0]
kv2 = [[x,y] for x, y in diff if x>= 0 and y<0]
kv3 = [[x,y] for x, y in diff if x<= 0 and y<0]
kv4 = [[x,y] for x, y in diff if x< 0 and y>=0]

dif1 = [a/b for a, b in kv1]
dif2 = [a/b for a, b in kv2]
dif3 = [a/b for a, b in kv3]
dif4 = [a/b for a, b in kv4]
print(dif4)
kv1 = add_two_list(kv1, dif1)
kv2 = add_two_list(kv2, dif2)
kv3 = add_two_list(kv3, dif3)
kv4 = add_two_list(kv4, dif4)

kv1 = sorted(kv1, key=lambda row : row[2])
kv2 = sorted(kv2, key=lambda row : row[2])
kv3 = sorted(kv3, key=lambda row : row[2])
kv4 = sorted(kv4, key=lambda row : row[2])
print(kv4	)
sorted_cord =[]
for i in range(len(kv1)):
	lst = [[a + centr_x, b + centr_y] for a, b, c in kv1]
	sorted_cord.append(lst[i])
for i in range(len(kv2)):
	lst = [[a + centr_x, b + centr_y] for a, b, c in kv2]
	sorted_cord.append(lst[i])
for i in range(len(kv3)):
	lst = [[a + centr_x, b + centr_y] for a, b, c in kv3]
	sorted_cord.append(lst[i])
for i in range(len(kv4)):
	lst = [[a + centr_x, b + centr_y] for a, b, c in kv4]
	sorted_cord.append(lst[i])
#curve_cord = [[150, 130], [175, 131], [200, 127], [200, 94], [176, 99], [175, 98], [150, 98], [139, 98], [125, 100], [100, 99], [75, 114], [56, 112],  [85, 124], [100, 127], [125, 129]]
#sorted_cord = [x for x in curve_cord if x not in sorted_cord]
print(sorted_cord)
sorted_cord.append(sorted_cord[0])
for i in range(len(sorted_cord)):
	plt.plot(sorted_cord[i][0], sorted_cord[i][1], 'ro:')

crv.ctrlpts = sorted_cord
crv.knotvector = knotvector.generate(crv.degree, crv.ctrlpts_size)


curve = np.array(crv.evalpts)

plt.plot(curve[:,0], curve[:,1])

foto_link = sys.argv[1],1
#print(type(str(foto_link)))

nurb_pil = tuple(map(tuple, curve))
#print(nurb_pil)
img = Image.open('/home/honepa/Документы/цр/трушников/img/lopatka.JPG')
#img = img.rotate(90)
img1 = ImageDraw.Draw(img)
img1.polygon(nurb_pil,  outline ="white")

#img.show()
#img.save('nurbs_lopatka.jpg', quality=95)

#get centr of figure
#centr_x = sum(curve[:,0]) / len(curve)
#centr_y = sum(curve[:,1]) / len(curve)
plt.plot(centr_x, centr_y, 'ro:')
print(centr_x)
print(centr_y)
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
