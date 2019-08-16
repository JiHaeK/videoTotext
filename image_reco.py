import pytesseract
import cv2
# import tensorflow as tf
import config

def extract_text(tmp_image):
	""" 이미지에서 글자를 인식합니다. 
	OCR엔진: tesseract (config에서 사용자 경로를 지정할 수 있습니다)

	:param tmp_image: Opencv 이미지 객체
	:return: 인식된 결과 (str) 
	"""		
	pytesseract.pytesseract.tesseract_cmd = config.RECO_CONFIG['tesseract']

	# image = cv2.imread(tmp_image)
	gray = cv2.cvtColor(tmp_image, cv2.COLOR_BGR2GRAY)
	# gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	# gray = cv2.medianBlur(gray, 10)
	result = pytesseract.image_to_string(gray, lang=config.RECO_CONFIG['lang'], config=config.RECO_CONFIG['custom_oem_psm_config'])
	# print('Origin Result \n' + result )
	return result

# def judge_text():
# 	hello = tf.constant('Hello, TensorFlow!')
# 	sess = tf.compat.v1.Session()
# 	print(sess.run(hello))

if __name__ == "__main__":
	pass