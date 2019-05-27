import numpy as np
import cv2
from scipy import ndimage

class HPF(object):
    def __init__(self, kernel, image):
        self.kernel = np.array(kernel)
        self.image = image

    def process(self):
        return ndimage.convolve(self.image, self.kernel)


if __name__ == "__main__":
    #enter ur image location
    image = cv2.imread("route.png", 0)
    cv2.imshow("Original",image)
    kernel3x3 = [[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]
    kernel5x5 = [[-1, -1, -1, -1, -1],
    [-1, 1, 2, 1, -1],
    [-1, 2, 4, 2, -1],
    [-1, 1, 2, 1, -1],
    [-1, -1, -1, -1, -1]]

    hpf1 = HPF(kernel3x3, image)
    hpfimage1 = hpf1.process()
    hpf2 = HPF(kernel5x5, image)
    hpfimage2 = hpf2.process()
    cv2.imshow("3x3",hpfimage1)
    cv2.imshow("5x5",hpfimage2)

    k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

	cv2.destroyAllWindows() 
    #cv2.waitKey()
    #cv2.destroyAllWindows()