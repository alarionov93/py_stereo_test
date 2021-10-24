import numpy as np


def slice_np_arr(a, shift_val):

	shift_x = 0
	val_x = 0
	pairs = []
	for idx in range(0, int(a.shape[0]/shift_val)):
		val_x += shift_val
		pairs.append((shift_x, val_x))
		shift_x += shift_val
	res = []
	print(pairs)
	for x in range(0,len(pairs)):
		for y in range(0,len(pairs)):
			try:
				r = np.array(a[pairs[x][0]:pairs[x][1], pairs[y][0]:pairs[y][1]])
				if len(np.where(r>1)[0]):
					res.append((a[pairs[x][0]:pairs[x][1], pairs[y][0]:pairs[y][1]], (x,y)))
			except IndexError:
				print('Error with array shape!')
	return res
