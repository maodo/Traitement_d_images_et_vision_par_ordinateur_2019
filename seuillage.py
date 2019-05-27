# #####Simple thresholding##################
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import base64
from io import BytesIO

# def simpleThresholding(seuil,image):
# 	#img = cv.imread('lena.png',0)

# 	img = base64.b64decode(image); 
# 	npimg = np.fromstring(img, dtype=np.uint8); 
# 	img = cv2.imdecode(npimg, 1)

# 	ret,thresh1 = cv.threshold(img,seuil,255,cv.THRESH_BINARY)
# 	ret,thresh2 = cv.threshold(img,seuil,255,cv.THRESH_BINARY_INV)
# 	ret,thresh3 = cv.threshold(img,seuil,255,cv.THRESH_TRUNC)
# 	ret,thresh4 = cv.threshold(img,seuil,255,cv.THRESH_TOZERO)
# 	ret,thresh5 = cv.threshold(img,seuil,255,cv.THRESH_TOZERO_INV)
# 	titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
# 	images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
# 	for i in range(6):
# 	    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
# 	    plt.title(titles[i])
# 	    plt.xticks([]),plt.yticks([])
# 	plt.show()
# 	figfile = BytesIO()
#     plt.savefig(figfile, format='png')
#     figfile.seek(0)
#     figdata_png = base64.b64encode(figfile.getvalue())
#     result = figdata_png
# 	thresholded = cv2.imencode('.png', img)[1].tostring()

########Adaptative thresholding#################
def adaptativeThreshold(image):

	#img = cv.imread('lena.png',0)
	img = base64.b64decode(image); 
	npimg = np.fromstring(img, dtype=np.uint8); 
	img = cv.imdecode(npimg, 0)
	img = cv.medianBlur(img,5)
	thresh,imgbin=cv.threshold(img,0,255,cv.THRESH_OTSU)
	ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
	th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
	            cv.THRESH_BINARY,11,2)
	th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
	            cv.THRESH_BINARY,11,2)
	titles = ['Methode OTSU', 'Thresholding Simple (v = 127)',
	            'Mean Thresholding', 'Gaussian Thresholding']
	images = [imgbin, th1, th2, th3]
	for i in range(4):
	    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
	    plt.title(titles[i])
	    plt.xticks([]),plt.yticks([])
	
	#plt.show()
	figfile = BytesIO()
	plt.savefig(figfile,format='png')
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue()).decode('ascii')
	return figdata_png