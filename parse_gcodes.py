import re

# g = re.findall(r'([G,M]\d{1,3})\s', t)

# r = re.findall(r'([X,Y,Z,E,F]\d+[\.]*\d+)[\s]*', t)

f = [x for x in open('/Users/sanya/Downloads/AA8_untitled.gcode', 'r').readlines() if x.startswith('G') or x.startswith(';LAY')]
layer_count = int(re.findall(r'(\;LAYER_COUNT:)(\d+)', ''.join(f).replace('\n', ' '))[0][1])
print(f'[ INFO ]: Total layers: {layer_count}.')
active_layer = layer_count-1
layer_number = 0
last_layer_number = 0
style = "display: none;"
# start = ""
# end = ""
try:
	svg_file = open('gcodes.svg', 'w')
	svg_file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?> \
	<svg version = "1.1" \
     baseProfile="full" \
     xmlns = "http://www.w3.org/2000/svg" \
     xmlns:xlink = "http://www.w3.org/1999/xlink" \
     xmlns:ev = "http://www.w3.org/2001/xml-events" \
	 height = "4000px"  width = "4000px"><g fill-opacity="0.6" stroke="black" stroke-width="0.5px">')
	for src, dst in zip(f[:-1], f[1:]):
		data = ''.join([src,dst]).replace('\n', ' ')
		try:
			try:
				layer_number = int(re.findall(r'(\;LAYER:)(\d+)', data)[0][1])
				# last_layer_number = layer_number
				# print(layer_number == active_layer)
				# print(active_layer)
				if layer_number == active_layer:
					style = ""
				else:
					style = "display: none;"
				# if layer_number > last_layer_number:
				# 	l = Layer()
			except IndexError:
				pass
				# print('[ ERROR ]: Layer string not found!')
			res = re.findall(r'([X,Y,E]\d+[\.]*\d+)[\s]*', data)
			x,y,e = (
				[x.split('X')[1] for x in res if 'X' in x],
				[x.split('Y')[1] for x in res if 'Y' in x],
				[x.split('E')[1] for x in res if 'E' in x],
			)
			start = f'<circle cx="{x[0]}px" cy="{y[0]}px" r="1px" fill="red" transform="" />'
			end = f'<circle cx="{x[1]}px" cy="{y[1]}px" r="1px" fill="red" transform="" />'
			try:
				width = float(e[0])/1000
				stroke = "orange"
			except IndexError:
				width = "1"
				stroke = "green"
			rr = f'{start}<line layer="{layer_number}" x1="{x[0]}" y1="{y[0]}" x2="{x[1]}" y2="{y[1]}" stroke="{stroke}" fill="transparent" style="{style}" stroke-width="{width}" />{end}'
			svg_file.write(rr)
			# break;
		except IndexError:
			pass
			# print('[ ERROR ]')
	svg_file.write('</g></svg>')
	svg_file.close()
	print(f'[ INFO ]: File is written.')
except IOError as ex:
	print(f'[ ERROR ] Some problem with file! {ex}')

class Layer(object):
	def __init__(self, num, coords):
		self.number = num
		self.show = False
		self.coords = coords
