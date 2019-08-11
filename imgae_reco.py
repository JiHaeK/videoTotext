import pytesseract
import cv2

def extract_text(tmp_image):
	pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.0/bin/tesseract'
	custom_oem_psm_config = r'--oem 3 --psm 6'
	custom_config=r'--psm 1 -c preserve_interword_spaces=1'

	# image = cv2.imread(tmp_image)
	gray = cv2.cvtColor(tmp_image, cv2.COLOR_BGR2GRAY)
	# gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	# gray = cv2.medianBlur(gray, 10)
	result = pytesseract.image_to_string(gray, lang='kor', config=custom_oem_psm_config)
	# print('Origin Result \n' + result )

	return result


if __name__ == "__main__":
	main()