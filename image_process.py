import json
import cv2
import numpy as np 
import config


def resize(image, flag=-1):
	"""
	비디오에서 1초당 하나의 프레임을 추출합니다.

	:param image: 프레임의 cv2 이미지 객체 
	:param flag: flag < 0(default)이면 사이즈를 증가, flag > 0 이면 사이즈를 축소
	:return: 사이즈가 조정된 이미지 
	"""
	standard_height = config.IMAGE_CONFIG['resize_origin']['standard_height']
	standard_width = config.IMAGE_CONFIG['resize_origin']['standard_width']

	height, width = image.shape[:2]
	image_copy = image.copy()
	# print original size (width, height)
	# print("origin (width : " + str(width) + ", height : " + str(height) + ")")
	rate = 1  # default
	if (flag < 0 and height < standard_height) or (flag < 0 and height > standard_height):  # Resize based on height
		rate = standard_height / height
	elif (flag < 0 and width < standard_width) or (flag < 0 and height > standard_height):  # Resize based on width
		rate = standard_width / width
	w = round(width * rate) 
	h = round(height * rate)  
	image_copy = cv2.resize(image_copy, (w, h))
	# print modified size (width, height)
	# print("after resize : (width : " + str(w) + ", height : " + str(h) + ")")
	return image_copy


def get_gray(image_origin):
	""" image 객체를 인자로 받아서 Gray-scale 을 적용한 2차원 이미지 객체로 반환합니다.
	
	:param image_origin: OpenCV 의 BGR image 객체 (3 dimension)
	:return: gray-scale 이 적용된 image 객체 (2 dimension)
	"""
	copy = image_origin.copy()
	image_gray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
	return image_gray


def get_gradient(image_gray):
	""" 이미지에 Dilation 과 Erosion 을 적용하여 그 차이를 이용해 윤곽선을 추출합니다.

	:param image_gray: gray-scale 이 적용된 image 객체 (2 dimension)
	:return: image_gradient: 윤관선 추출한 결과 이미지 (Opencv 이미지)
	"""
	copy = image_gray.copy()

	kernel_size_row = config.IMAGE_CONFIG['gradient']['kernel_size_row']
	kernel_size_col = config.IMAGE_CONFIG['gradient']['kernel_size_col']

	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size_row, kernel_size_col))

	image_gradient = cv2.morphologyEx(copy, cv2.MORPH_GRADIENT, kernel)
	return image_gradient

def get_threshold(image_gray): 
	""" 이미지에 Threshold 를 적용해서 흑백(Binary) 이미지객체를 반환합니다.
	configs 에 적용된 threshold mode 에 따라 mean adaptive threshold / gaussian adaptive threshold
    를 적용할 수 있습니다. 

	:param image_gray: gray-scale 이 적용된 image 객체 (2 dimension)
	:return: image_gradient: Threshold 적용한 흑백(Binary) 이미지 (Opencv 이미지)
	"""
	copy = image_gray.copy()

	mode = config.IMAGE_CONFIG['threshold']['mode']
	block_size = config.IMAGE_CONFIG['threshold']['block_size']
	subtract_val = config.IMAGE_CONFIG['threshold']['subtract_val']

	if mode == 'mean':
		image_threshold = cv2.adaptiveThreshold(copy, 255, 
			cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, block_size, subtract_val)
	elif mode == 'gaussian':
		image_threshold = cv2.adaptiveThreshold(copy, 255, 
			cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, subtract_val)
	# else: 
	# 	image_threshold = get_otsu_threshold(copy)

	return image_threshold

# def get_otsu_threshold(image_gray):
# 	copy = image_gray.copy()
# 	blur = cv2.GaussianBlur(copy, (5, 5), 0)
# 	ret3, imgae_otsu = cv2.threshold(copy, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# 	return imgae_otsu


# def remove_long_line(image_binary):
# 	copy = image_binary.copy()

# 	threshold = config.IMAGE_CONFIG['remove_line']['threshold']
# 	min_line_length = config.IMAGE_CONFIG['remove_line']['min_line_length']
# 	max_line_gap = config.IMAGE_CONFIG['remove_line']['max_line_gap']

# 	lines = cv2.HoughLinesP(copy, 1, np.pi / 180, threshold, min_line_length, max_line_gap)
# 	if lines is not None: 
# 		for line in lines:
# 			x1, y1, x2, y2 = line[0]
# 			cv2.line(copy, (x1, y1), (x2, y2), (0, 0, 0), 2)
# 	return copy 

def get_closing(image_gray):
	""" 이미지에 Morph Close 를 적용한 이미지객체를 반환합니다.
	이미지에 Dilation 수행을 한 후 Erosion 을 수행한 것입니다.
	이 때 인자로 입력되는 이미지는 Gray-scale 이 적용된 2차원 이미지여야 합니다.
	configs 에 의해 kernel size 값을 설정할 수 있습니다.
	
	:param image_gray: Gray-scale 이 적용된 OpenCV image (2 dimension)
	:return: Morph Close 를 적용한 흑백(Binary) 이미지
	"""
	copy = image_gray.copy()

	kernel_size_row = config.IMAGE_CONFIG['close']['kernel_size_row']
	kernel_size_col = config.IMAGE_CONFIG['close']['kernel_size_col']
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size_row, kernel_size_col))
	image_close = cv2.morphologyEx(copy, cv2.MORPH_CLOSE, kernel)
	return image_close


def get_contours(image):
	""" 이미지에서 contour를 추출해 반환합니다.
	이미지 처리(Image processing) 단계를 거친 후 contour 를 잘 추출할 수 있습니다.
	왼쪽 상단 위의 점을 포함한 곳을 섹션구역으로 지정합니다. (config에서 점 위치 변경 가능)
	크기가 40x10 이하인 것은 contour로 뽑지 않습니다. (config에서 기준 사이즈 변경 가능)

	:param image: 전처리가 끝난 OpenCV의 image 객체 (2 dimension)
    :return: 이미지에서 추출한 contours (dictonary)
    """
	min_width = config.IMAGE_CONFIG['contour']['min_width']
	min_height = config.IMAGE_CONFIG['contour']['min_height']
	section_x = config.IMAGE_CONFIG['contour']['section_x']
	section_y = config.IMAGE_CONFIG['contour']['section_y']

	contours, hierachy= cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# contours, hierachy = cv2.findContours(image, retrieve_mode, approx_method)
	# print(hierachy)
	all_contour={}
	final_contours=[]
	section_contour=[]
	for i, con in enumerate(contours) :
		x, y, width, height = cv2.boundingRect(con)
		# area = cv2.contourArea(con)
		if width > min_width and height > min_height :
			if x < section_x < x+width and y < section_y < y+height:
				section_contour.append(con)
			else:
				final_contours.append(con)
	all_contour["contours"]=final_contours
	all_contour["section"]=section_contour


	return all_contour

# def draw_contour_rect(image_origin, contours):
# 	""" 사각형의 Contour 를 이미지 위에 그려서 반환합니다.
#     찾은 Contours들의 영역을 감싸는 외각 사각형을 그립니다. 
# 	섹션 - 빨간색 사각형, 나머지 - 초록색 사각형

#     :param image_origin: OpenCV의 image 객체
#     :param contours: 이미지 위에 그릴 contour 딕셔너리
#     :return: 사각형의 Contour 를 그린 이미지
#     """
# 	rgb_copy = image_origin.copy()
# 	draw_contour = contours["contours"]
# 	draw_sectoin = contours["section"]

# 	min_width = config.IMAGE_CONFIG['contour']['min_width']
# 	min_height = config.IMAGE_CONFIG['contour']['min_height']

# 	if len(draw_contour) == 0:
# 		# print('contours: 0')
# 		return rgb_copy
# 	else : 
# 		for contour in draw_contour:
# 			rect = cv2.minAreaRect(contour)
# 			box = cv2.boxPoints(rect)
# 			box = np.int0(box)
# 			# print(box[0])
# 			cv2.drawContours(rgb_copy, [box], 0, (0, 255, 0), 2)
# 		if len(draw_sectoin) != 0:
# 			rect = cv2.minAreaRect(draw_sectoin.pop())
# 			box = cv2.boxPoints(rect)
# 			box = np.int0(box)
# 			cv2.drawContours(rgb_copy, [box], 0, (0, 0, 255), 2)
			
# 	return rgb_copy


def get_cropped_images(image_origin, contours):
	""" 이미지에서 찾은 Contour 부분들을 잘라내어 반환합니다.
    각 contour 를 감싸는 외각 사각형에 여유분(padding)을 주어 이미지를 잘라냅니다.

    :param image_origin: 원본 이미지
    :param contours: 잘라낼 contour 딕셔너리
    :return: contours 를 기반으로 잘라낸 이미지(OpenCV image 객체) 딕셔너리
    """
	image_copy = image_origin.copy()
	min_width = config.IMAGE_CONFIG['contour']['min_width']
	min_height = config.IMAGE_CONFIG['contour']['min_height']
	padding = config.IMAGE_CONFIG['contour']['padding']

	origin_height, origin_width = image_copy.shape[:2]
	all_cropped={}
	cropped_images = []
	cropped_section=[]
	draw_contour = contours["contours"]
	draw_section = contours["section"]
	# print('get corpped section: %s' %type(draw_section))

	for contour in draw_contour:  # Crop the screenshot with on bounding rectangles of contours
		x, y, width, height = cv2.boundingRect(contour)  # top-left vertex coordinates (x,y) , width, height

		row_from = (y - padding) if (y - padding) > 0 else y
		row_to = (y + height + padding) if (y + height + padding) < origin_height else y + height
		# The range of column to crop (with padding)
		col_from = (x - padding) if (x - padding) > 0 else x
		col_to = (x + width + padding) if (x + width + padding) < origin_width else x + width
		# Crop the image with Numpy Array
		cropped = image_copy[row_from: row_to, col_from: col_to]
		cropped_images.append(cropped)  # add to the list

	
	if( len(draw_section) > 0 ):
		x, y, width, height = cv2.boundingRect(draw_section.pop())
		# area = cv2.contourArea(draw_section.pop())
		if width*height > 2500 :
			cropped_section = image_copy[10: 84, 10: 350]
		else: 
			row_from = (y - padding) if (y - padding) > 0 else y
			row_to  = (y + height + padding) if (y + height + padding) < origin_height else y + height
			col_from = (x - padding) if (x - padding) > 0 else x 
			col_to = (x + width + padding) if (x + width + padding) < origin_width else x + width
			cropped_section = image_copy[row_from: row_to, col_from: col_to]
	else:
		cropped_section = image_copy[10: 84, 10: 350]

	all_cropped["contours"]=cropped_images
	all_cropped["section"]=cropped_section
	
	return all_cropped


def save_crooped_contours(image, path):
	""" 잘라낸 Contour 부분들을 저장합니다.
	:param image: 잘라낸 contour 이미지 
	:param count: 잘라낸 contour 순서 
	"""
	f_name = path 
	file_path = f_name + ".jpg"  # complete file name
	cv2.imwrite(file_path, image)
	


def image_all_process(imgae_file):
	""" 5단계의 이미지 전처리를 실행합니다.

    :param image_file: 프레임 이미지 파일(BGR image)
    :return: contours 를 기반으로 잘라낸 이미지(OpenCV image 객체) 딕셔너리
    """
	gray = get_gray(imgae_file)
	# cv2.imshow('gray', gray)

	gray1 = get_gradient(gray)
	# cv2.imshow('gray1', gray1)

	gray2 = get_threshold(gray1)
	# cv2.imshow('gray2', gray2)

	gray3 = get_closing(gray2)
	# cv2.imshow('gray3', gray3)

	# gray4 = remove_long_line(gray3)
	# cv2.imshow('gray4', gray4)

	contours = get_contours(gray3)
	# print(len(contours["section"]))
	
	# cv2.imshow('All contours', draw_contour_rect(imgae_file, contours))
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	origin = get_cropped_images(imgae_file, contours)
	gray = get_cropped_images(gray, contours)
	final =[]
	final.append(origin)
	final.append(gray)

	return final


if __name__ == '__main__':
	pass