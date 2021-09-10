import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import sys

def create_stereo_img(f1, f2, nDisps, blkSz):
   imgL = cv.imread(f1,0)
   imgR = cv.imread(f2,0)

   stereo = cv.StereoBM_create(numDisparities=nDisps, blockSize=blkSz)
   disparity = stereo.compute(imgL,imgR)
   plt.imshow(disparity,'gray')
   disparity = np.rot90(disparity)
   # print(disparity.shape)
   v = 1
   vertexes = []
   faces = []
   for x in range(0, disparity.shape[0]-1):
      for y in range(0, disparity.shape[1]-1):
         v0 = (x,y,disparity[x,y]/100)
         v1 = (x,y+1,disparity[x,y+1]/100)
         v2 = (x+1,y,disparity[x+1,y]/100)
         v += 3
         vertexes += [v0, v1, v2]
         faces += [(v-3, v-2, v-1)]
   open('test_%s_%s.obj' % (f1,f2), 'w').write('\n'.join(['v %s %s %s' % x for x in vertexes])+'\n')
   open('test_%s_%s.obj' % (f1,f2), 'a').write('\n'.join(['f %s %s %s' % x for x in faces]))
   # print(vertexes[0:4])
   # print(faces[0:4])
   # plt.savefig('res/%s_%s_%s_%s.jpeg' % (f1.split('.')[0], f2.split('.')[0], nDisps, blkSz))


if __name__=='__main__':
   # from itertools import product
   # for a, b in product([ x * 16 for x in range(4, 10)], [5]):
   create_stereo_img(sys.argv[1], sys.argv[2], 80, 5)
