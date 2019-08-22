import pytesseract
import cv2
import re
# import tensorflow as tf
import config
import image_process as ip

def extract_text(tmp_image):
	""" 이미지에서 글자를 인식합니다. 
	OCR엔진: tesseract (config에서 사용자 경로를 지정할 수 있습니다)

	:param tmp_image: Opencv 이미지 객체
	:return: 인식된 결과 (str) 
	"""
	if (len(tmp_image) == 0):
		return ''

	pytesseract.pytesseract.tesseract_cmd = config.RECO_CONFIG['tesseract']

	# image = cv2.imread(tmp_image)
	# image = ip.resize(tmp_image)
	# image = cv2.resize(tmp_image, dsize=(320, 240), interpolation=cv2.INTER_AREA)
	image = cv2.pyrUp(tmp_image)
	# gray = cv2.cvtColor(tmp_image, cv2.COLOR_BGR2GRAY)
	# gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	# ret3, imgae_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	# gray = cv2.medianBlur(gray, 10)
	result = pytesseract.image_to_string(image, lang=config.RECO_CONFIG['lang'], config=config.RECO_CONFIG['custom_oem_psm_config'])
	# print('Origin Result \n' + result )

	
	return result




# def judge_text():
# 	hello = tf.constant('Hello, TensorFlow!')
# 	sess = tf.compat.v1.Session()
# 	print(sess.run(hello))

if __name__ == "__main__":
	# extract_text('new3/jjan/section/section_424.jpg')
	pass 