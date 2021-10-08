import numpy as np

def interpol(edges):
	shift=10
	_shift=10
	res = []
	res_y = []
	X,Y = np.where(edges>1)
	top = np.min(X)
	left = np.min(Y)
	bottom = np.max(X)
	right = np.max(Y)
	print((top,left,bottom,right))
	for idx in range(0, int(len(np.where(edges>1)[0]+_shift)/10)):
		x = np.where(edges>1)[1][shift-_shift:shift]
		y = np.where(edges>1)[0][shift-_shift:shift]

		res.append((x,np.polyfit(x,y,1),y))
		# print(x)
		shift+=_shift
		# print(shift-_shift, _shift)

	for r in res:
		# r[0] - x
		# y=kx+b (r[1][0]*r[0] + r[1][1])
		res_y.append((r[0], r[1][0]*r[0] + r[1][1], r[2]))

	return res_y


def slice_np_arr(a, shift_val):

	shift_x = 0
	val_x = 0
	pairs = []
	for idx in range(0, int(a.shape[0]/shift_val)):
		val_x += shift_val
		pairs.append((shift_x, val_x))
		shift_x += shift_val
	res = []
	for x in range(0,len(pairs)):
		for y in range(0,len(pairs)):
			try:
				r = np.array(a[pairs[x][0]:pairs[x][1], pairs[y][0]:pairs[y][1]])
				if len(np.where(r>1)[0]):
					res.append(a[pairs[x][0]:pairs[x][1], pairs[y][0]:pairs[y][1]])
			except IndexError:
				print('Error with array shape!')
	return res
	# shift_val = 2
	# #TODO: fix if condition to process all pieces of an array
	# pairs = []
	# for idx in range(0,a.shape[0]):
	# 	val_x += shift_val
	# 	pairs.append((shift_x, val_x))
	# 	shift_x += shift_val

	# 	print(a[shift_x:val_x, shift_y:val_y])
	# 	if idx%2:
	# 		shift_x += shift_val
	# 		val_x += shift_val
	# 	else:
	# 		shift_y += shift_val
	# 		val_y += shift_val

