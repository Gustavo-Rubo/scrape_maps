import numpy as np
import matplotlib.pyplot as plt

panoids = np.load('panoids.npy')
user_panoids = np.load('user_panoids.npy')

im_usp = plt.imread('usp.png')
plt.imshow(im_usp, zorder=0)
im_w = 1281
im_h = 945

#-23.54893638234242, -46.709208684501455
lat0 = -23.54893638234242
long0 = -46.745772557715696

latd = lat0 + 23.57344373805996
longd = long0 + 46.709208684501455

plt.scatter(
    -im_w*(panoids[:,1].astype('float')-long0)/longd,
    -im_h*(panoids[:,2].astype('float')-lat0)/latd,
    color='blue', marker='.', label='panoids')
plt.scatter(
    -im_w*(user_panoids[:,1].astype('float')-long0)/longd,
    -im_h*(user_panoids[:,2].astype('float')-lat0)/latd,
    color='orange', marker='.', label='user panoids')
plt.legend(loc='upper right')

plt.ylim([800, 50])
plt.xlim([30, 1200])
plt.axis('off')
plt.tight_layout()

plt.show()