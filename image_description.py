import requests
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import cv2
import base64
from py_translator import Translator

# <Subscription Key> 
subscription_key = "6c2f63ca27b34129bc83762371f255c5"
assert subscription_key

vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"

analyze_url = vision_base_url + "analyze"

def analyser_image(image):
	
	img = base64.b64decode(image); 
	npimg = np.fromstring(img, dtype=np.uint8); 
	image_data = cv2.imdecode(npimg, 1)
	#image_data = cv2.imread(image_path)
	res,encoded_image = cv2.imencode('.png', image_data)
	image_data = encoded_image.tobytes()
	print("Type de l'image: ",type(image_data))
	headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
	              'Content-Type': 'application/octet-stream'}
	params     = {'visualFeatures': 'Categories,Description,Color'}
	response = requests.post(
	    analyze_url, headers=headers, params=params, data=image_data)
	response.raise_for_status()

	# The 'analysis' object contains various fields that describe the image. The most
	# relevant caption for the image is obtained from the 'description' property.
	analysis = response.json()
	image_caption = analysis["description"]["captions"][0]["text"].capitalize()
	s = Translator().translate(text=image_caption, dest='fr').text
	encoded_image = encoded_image.tostring()
	return encoded_image,s