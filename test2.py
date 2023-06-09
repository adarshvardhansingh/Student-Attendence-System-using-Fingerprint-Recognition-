import numpy
import cv2
import cv2
import numpy as np
from math import pi
import matplotlib as mpl
mpl.use('Agg')
import scipy as sp

import matplotlib.pyplot as plt
#from Normalisation import *
#from poincare_index import *
#from direction_field import *
import pandas as pd
#from openpyxl.workbook import Workbook
#from LSE import *
w1 = 16
I_3 = cv2.imread("testimage.png")
#Read the image
I_2 = cv2.imread("testimage.png")
#I = cv2.cvtColor(I_2, cv2.COLOR_BGR2GRAY)


I_2 = cv2.cvtColor(I_2, cv2.COLOR_BGR2GRAY)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
I = cv2.dilate(I_2,kernel,iterations = 1)


G = cv2.GaussianBlur(I,(5,5),0)

#Sobel Operator
Gx = cv2.Sobel(G,cv2.CV_64F,1,0,ksize=3)
Gy = cv2.Sobel(G,cv2.CV_64F,0,1,ksize=3)



J1 = 2*(np.multiply(Gx, Gy))
J2 = np.multiply(Gx, Gx) - np.multiply(Gy, Gy)
J3 = np.multiply(Gx, Gx) + np.multiply(Gy, Gy)

Gradient = np.sqrt(J3)

anisotropy_filter = np.ones((16,16))
sigma_J1 = cv2.filter2D(J1,-1,anisotropy_filter)
sigma_J2 = cv2.filter2D(J2,-1,anisotropy_filter)
sigma_J3 = cv2.filter2D(J3,-1,anisotropy_filter)

anisotropy_filter_0 = np.ones((10,10))
sigma_J3_0 = cv2.filter2D(J3,-1,anisotropy_filter_0)

cv2.imshow('i',sigma_J3)
cv2.waitKey(0)	


theta_bar = 0.5 * np.arctan(np.divide(sigma_J1, sigma_J2))
for i,j in np.argwhere(sigma_J2 == 0):
	if (sigma_J1[i,j] > 0):
		theta_bar[i,j] = 0.25*pi
	elif (sigma_J1[i,j] < 0):
		theta_bar[i,j] = (-0.25)*pi
	else:
		theta_bar[i,j] = 0

theta_dash = (pi/2) + theta_bar

gt = 0.10
Grad_max = np.amax(Gradient)
Grad_min = np.amin(Gradient)

Gth = gt * (abs(Grad_max) - abs(Grad_min)) + abs(Grad_min)
## threshold matrix

block_coherence = np.sqrt(np.multiply(sigma_J1, sigma_J1) + np.multiply(sigma_J2, sigma_J2))
block_coherence = np.divide(block_coherence, sigma_J3)
for i,j in np.argwhere(sigma_J3 < Gth*Gth*(w1*w1)):
	block_coherence[i,j] = (-1)

a = np.zeros(sigma_J1.shape)
for i,j in np.argwhere(block_coherence > 0):
	a[i,j] = 1

for i,j in np.argwhere(block_coherence < 0):
	a[i,j] = -1


cv2.imshow('i0>1', block_coherence)
cv2.waitKey(0)	


cv2.imshow('i+1neg-1', a)
cv2.waitKey(0)	

# sobel operator to find x and y gradient
theta = theta(1)

print('theta shape', theta.shape)
print('a shape', a.shape)
cv2.waitKey(0)	

poincare_image = np.zeros(a.shape)
for i,j in np.argwhere(a != -1):
	#print('i=', i, 'j=', j)
	store = np.zeros([3,3])
	if ((i-1 >= 0) and (i+1 <= a.shape[0]-1) and (j-1 >= 0) and (j+1 <= a.shape[1]-1)):
		
		store[0,0] = theta[i-1,j] - theta[i-1, j-1]
		store[0,1] = theta[i-1, j+1] - theta[i-1, j]
		store[0,2] = theta[i,j+1] - theta[i-1, j+1]
		store[1,2] = theta[i+1, j+1] - theta[i, j+1]
		store[2,2] = theta[i+1,j] - theta[i+1, j+1]
		store[2,1] = theta[i+1, j-1] - theta[i+1, j]
		store[2,0] = theta[i, j-1] - theta[i+1, j-1]
		store[1,0] = theta[i-1, j-1] - theta[i, j-1]
		
		for x,y in np.argwhere(store > pi/2):
			store[x,y] = pi - store[x,y]
			#print('1')

		for x,y in np.argwhere(store < (-0.5)*pi):
			store[x,y] = pi + store[x,y]


		poincare_image[i,j] = store.sum()/(2*pi)
f = 0
delta_image = np.zeros(I_2.shape)
# for x,y in np.argwhere(poincare_image == 0.5):
# 	I_3[x,y] = [0,0,255]
# 	I_3[x+1, y] = [0,0,255]
# 	I_3[x, y+1] = [0,0,255]
# 	I_3[x+1, y+1] = [0,0,255]
print('abcbbcbcbbbbbbbbbbbbbbbbbbbb')
index_1, index_2 = [0,0]
max_gradient = 0	
for x,y in np.argwhere(poincare_image == 0.5):
	if(sigma_J3_0[x,y] > max_gradient):
		index_1,index_2 = x,y
		max_gradient = sigma_J3_0[x,y]

# for x,y in np.argwhere(poincare_image == -0.5):
# 	I_3[x,y] = [0,255,0]
# 	I_3[x+1, y] = [0,255,0]
# 	I_3[x, y+1] = [0,255,0]
# 	I_3[x+1, y+1] = [0,255,0]

I_3[index_1,index_2] = [0,0,255]
I_3[index_1+1, index_2] = [0,0,255]
I_3[index_1, index_2+1] = [0,0,255]
I_3[index_1+1, index_2+1] = [0,0,255]

	

# cv2.imshow('i',I_3)
# cv2.waitKey(0)	
print('index_1 = ', index_1)
print('index_2 = ', index_2)


cv2.imwrite('singularity_found.png',  I_3)