import re

# g = re.findall(r'([G,M]\d{1,3})\s', t)

# r = re.findall(r'([X,Y,Z,E,F]\d+[\.]*\d+)[\s]*', t)

# ! (;LAYER:\d+\n)((\w+[\.]*\w+)\s\n*)+

# (;LAYER:\d+\\n)(([A-Z0-9.]+\s*|\\n))+

f = [x for x in open('/Users/sanya/Downloads/AA8_untitled.gcode', 'r').readlines() if x.startswith('G') or x.startswith(';LAY')]
y = re.findall(r'YER:(\d+)(.*?);((LA)|(En))', ''.join(f), re.DOTALL | re.MULTILINE)

layer_count = len(y)
layers = (x[1] for x in y)

print(f'[ INFO ]: Total layers: {layer_count}.')
active_layer = layer_count-1
layer_number = 0

try:
	svg_file = open('gcodes.svg', 'w')
	svg_file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?> \
	<svg version = "1.1" \
     baseProfile="full" \
     xmlns = "http://www.w3.org/2000/svg" \
     xmlns:xlink = "http://www.w3.org/1999/xlink" \
     xmlns:ev = "http://www.w3.org/2001/xml-events" \
	 height = "4000px"  width = "4000px"><g fill-opacity="0.6" stroke="black" stroke-width="0.5px">')
	last_n_rr = ()
	for layer in layers:
		n_rr = re.findall(r'^G.*?X(\d+\.\d+).*?Y(\d+\.\d+)(.*?E(\d+\.\d+))?', layer, re.MULTILINE)
		print(len(n_rr))
		l = 0
		if last_n_rr:
			print('Set prev layer last coords..')
			n_rr.insert(0, last_n_rr)
		for src, dst in zip(n_rr[:-1], n_rr[1:]):
			print(src, dst)
			try:
				x0 = float(src[0])
				x1 = float(dst[0])
				y0 = float(src[1])
				y1 = float(dst[1])
				if layer_number == active_layer:
					style = ""
					start = f'<circle cx="{x0}px" cy="{y0}px" r="1px" fill="red" transform="" />'
					end = f'<circle cx="{x1}px" cy="{y1}px" r="1px" fill="red" transform="" />'
				else:
					style = "display: none;"
					start = end = ""
				try:
					e = float(dst[3]) if dst[3] else 0
					width = float(e)/5000
					stroke = "orange"
				except IndexError:
					width = "0.3"
					stroke = "green"
				rr = f'{start}<line layer="{layer_number}" x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{stroke}" fill="transparent" style="{style}" stroke-width="{width}" />{end}'
				svg_file.write(rr)
				l += 1
				# break;
			except IndexError:
				pass
				print('[ ERROR ]')
		last_n_rr = n_rr[-1]
		layer_number += 1
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
