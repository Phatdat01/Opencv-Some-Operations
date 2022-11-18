import cv2
import numpy as np
from matplotlib import pyplot as plt

# SET PARAMETERS
r_1 = 45
eps_1 = 0.3
r_2 = 7
eps_2 = 0.000001
use_opencv = False

def guidedFilter(src, guide, r, eps):
    src = np.array(src, np.float32)
    guide = np.array(guide, np.float32)
    src_pad = np.pad(src, ((r,r),(r,r),(0,0)), 'reflect')
    guide = np.pad(guide, ((r,r),(r,r),(0,0)), 'reflect')
    w = 2 * r + 1
    a_k = np.zeros(src_pad.shape[0:2], np.float32)
    b_k = np.zeros(src_pad.shape[0:2], np.float32)
    out = np.array(src, np.uint8, copy=True)
    for i in range(r, src_pad.shape[0]-r):
        for j in range(r, src_pad.shape[1]-r):
            I = guide[i-r : i+r+1, j-r : j+r+1, 0]
            P = src_pad[i-r : i+r+1, j-r : j+r+1, 0]
            temp = np.dot(np.ndarray.flatten(I), np.ndarray.flatten(P))/(w*w)
            mu_k = np.mean(I)
            del_k = np.var(I)
            P_k_bar = np.mean(P)
            a_k[i,j] = (temp - mu_k * P_k_bar) / (del_k + eps)
            b_k[i,j] = P_k_bar - a_k[i,j] * mu_k
    for i in range(r, src_pad.shape[0]-r):
        for j in range(r, src_pad.shape[1]-r):
            a_k_bar = a_k[i-r : i+r+1, j-r : j+r+1].sum()/(w*w)
            b_k_bar = b_k[i-r : i+r+1, j-r : j+r+1].sum()/(w*w)
            out[i-r,j-r] = np.round(a_k_bar * guide[i,j] + b_k_bar)
    return out

im1 = cv2.imread('./image/rem.jpg')
im2 = cv2.imread('./image/back.jpg')

b1 = np.array(cv2.blur(im1, (31,31)), np.int16)
d1 = np.array(im1, np.int16) - b1

b2 = np.array(cv2.blur(im2, (31,31)), np.int16)
d2 = np.array(im2, np.int16) - b2

plt.figure("Two scale image decomposition")
plt.subplot(231), plt.imshow(im1), plt.title('Original Image I1')
plt.xticks([]), plt.yticks([])
plt.subplot(232), plt.imshow(np.array(b1, np.uint8)), plt.title('Base Layer B1')
plt.xticks([]), plt.yticks([])
plt.subplot(233), plt.imshow(np.array(abs(d1), np.uint8)), plt.title('Detail Layer D1')
plt.xticks([]), plt.yticks([])
plt.subplot(234), plt.imshow(im2), plt.title('Original Image I2')
plt.xticks([]), plt.yticks([])
plt.subplot(235), plt.imshow(np.array(b2, np.uint8)), plt.title('Base Layer B2')
plt.xticks([]), plt.yticks([])
plt.subplot(236), plt.imshow(np.array(abs(d2), np.uint8)), plt.title('Detail Layer D2')
plt.xticks([]), plt.yticks([])
plt.show(block=False)

laplacian1 = abs(cv2.Laplacian(im1, cv2.CV_64F))
s1 = cv2.GaussianBlur(laplacian1, (5,5), 0)
laplacian2 = abs(cv2.Laplacian(im2, cv2.CV_64F))
s2 = cv2.GaussianBlur(laplacian2, (5,5), 0)

# Plot Saliency Maps
plt.figure("Saliency features")
plt.subplot(221), plt.imshow(im1), plt.title('Original Image I1')
plt.xticks([]), plt.yticks([])
plt.subplot(222), plt.imshow(laplacian1), plt.title('Gaussian blurred Laplacian of Image I1')
plt.xticks([]), plt.yticks([])
plt.subplot(223), plt.imshow(im2), plt.title('Original Image I2')
plt.xticks([]), plt.yticks([])
plt.subplot(224), plt.imshow(laplacian2), plt.title('Gaussian blurred Laplacian of Image I2')
plt.xticks([]), plt.yticks([])
plt.show(block=False)

p1 = np.zeros(im1.shape, np.uint8)
p2 = np.zeros(im2.shape, np.uint8)
p1[s1 >= s2] = 1
p2[s2 > s1] = 1

# Plot weight maps
plt.figure("Weight Maps")
plt.subplot(221), plt.imshow(im1), plt.title('Original Image I1')
plt.xticks([]), plt.yticks([])
plt.subplot(222), plt.imshow(p1*255), plt.title('Weight Maps P1')
plt.xticks([]), plt.yticks([])
plt.subplot(223), plt.imshow(im2), plt.title('Original Image I2')
plt.xticks([]), plt.yticks([])
plt.subplot(224), plt.imshow(p2*255), plt.title('Weight Maps P2')
plt.xticks([]), plt.yticks([])
plt.show(block=False)

if(use_opencv):
    gf1 = cv2.ximgproc.createGuidedFilter(im1, r_1, eps_1)
    w1 = gf1.filter(p1)
else:
    w1 = guidedFilter(p1, im1, r_1, eps_1)

if(use_opencv):
    gf2 = cv2.ximgproc.createGuidedFilter(im2, r_2, eps_2)
    w2 = gf1.filter(p2)
else:
    w2 = guidedFilter(p2, im2, r_2, eps_2)
plt.figure("Refined Weight Maps")
plt.subplot(221), plt.imshow(im1), plt.title('Original Image I1')
plt.xticks([]), plt.yticks([])
plt.subplot(222), plt.imshow(w1*255), plt.title('Refined Weight Maps W1')
plt.xticks([]), plt.yticks([])
plt.subplot(223), plt.imshow(im2), plt.title('Original Image I2')
plt.xticks([]), plt.yticks([])
plt.subplot(224), plt.imshow(w2*255), plt.title('Refined Weight Maps W2')
plt.xticks([]), plt.yticks([])
plt.show(block=False)

bf = w1 * b1 + w2 * b2
df = w1 * d1 + w2 * d2

fused_im = np.array(bf+df, np.uint8)

cv2.imshow('Final Fused Image', fused_im)
cv2.waitKey()
cv2.destroyAllWindows()