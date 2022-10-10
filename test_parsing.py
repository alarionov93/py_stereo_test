import re
 
x = open('/tmp/AA8_untitled.gcode').read()
 
y = re.findall(r'YER:(\d+)(.*?);((LA)|(En))', x, re.DOTALL | re.MULTILINE)
 
print(y, len(y))
 
layers = ( x[1] for x in y )
 
n = 0
for layer in layers:
    Z = re.findall(r'^G.*?X(\d+\.\d+).*?Y(\d+\.\d+)(.*?E(\d+\.\d+))?', layer, re.MULTILINE)
    for z in Z:
        x = float(z[0])
        y = float(z[1])
        e = float(z[3]) if z[3] else 0
        print(f'l= {n} x={x} y={y} e={e}')
    n += 1