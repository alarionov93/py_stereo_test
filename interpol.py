import numpy as np

def interpol(edges):
	shift=10
	_shift=10
	res = []
	res_y = []
	for idx in range(0, int(len(np.where(edges>1)[0]+_shift)/10)):
		x = np.where(edges>1)[1][shift-_shift:shift]
		y = np.where(edges>1)[0][shift-_shift:shift]
		res.append((x,np.polyfit(x,y,1)))
		shift+=_shift
		print(shift-_shift, _shift)

	for r in res:
		# r[0] - x
		# y=kx+b (r[1][0]*r[0] + r[1][1])
		res_y.append((r[0], r[1][0]*r[0] + r[1][1]))

	return res_y