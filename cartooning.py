import cv2
import numpy as np
import base64
def cartoon(img):

	# img = cv2.imread("route.png")
	img = base64.b64decode(img); 
	npimg = np.fromstring(img, dtype=np.uint8); 
	img = cv2.imdecode(npimg, 1)

				# 1) Edges
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.medianBlur(gray, 5)
	edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

				# 2) Color
	color = cv2.bilateralFilter(img, 9, 300, 300)

				# 3) Cartoon
	cartoon = cv2.bitwise_and(color, color, mask=edges)
	cartoon = cv2.imencode('.png', cartoon)[1].tostring()
	
	return cartoon
