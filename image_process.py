import json
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np 


# ============== ver 1.0 start ==================


def read_configs(json_file):
	"""
	.json 파일을 읽어서 configuration 객체를 갖습니다. 
	:param json_file: 
	:return: 읽은 configuration 을 담고 있는 dictionary 형태로 반환 
	"""
	with open('configs.json', 'r', encoding='utf-8') as outfile:
		d = json.load(outfile)
	global configs 
	configs = d
	
	return d


def resize(image, flag=-1):
	global configs
	standard_height = configs['resize_origin']['standard_height']
	standrd_width = configs['resize_origin']['standrd_width']

	height, width = image.shape[:2]
	image_copy = image.copy()
	# print original size (width, height)
	print("origin (width : " + str(width) + ", height : " + str(height) + ")")
	rate = 1  # default
	if (flag > 0 and height < standard_height) or (flag < 0 and height > standard_height):  # Resize based on height
		rate = standard_height / height
	elif (flag > 0 and width < standard_width) or (flag < 0 and height > standard_height):  # Resize based on width
		rate = standard_width / width

	# resize
	w = round(width * rate)  # should be integer
	h = round(height * rate)  # should be integer
	image_copy = cv2.resize(image_copy, (w, h))
	# print modified size (width, height)
	print("after resize : (width : " + str(w) + ", height : " + str(h) + ")")
	return image_copy


def open_img(file_path):
	image_origin = cv2.imread(file_path)
	return image_origin

def get_gray(image_origin):
	copy = image_origin.copy()
	image_gray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
	return image_gray

def get_canny(image_gray):
	copy = image_gray.copy()
	kernel_size = 5
	blur_gray = cv2.GaussianBlur(copy, (kernel_size, kernel_size), 0)
	low_threshold = 50
	high_threshold = 150
	edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
	return edges

def get_gradient(image_gray):
	copy = image_gray.copy()

	global configs
	kernel_size_row = configs['gradient']['kernel_size_row']
	kernel_size_col = configs['gradient']['kernel_size_col']

	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size_row, kernel_size_col))

	image_gradient = cv2.morphologyEx(copy, cv2.MORPH_GRADIENT, kernel)
	return image_gradient

def get_threshold(image_gray): 
	copy = image_gray.copy()

	global configs
	mode = configs['threshold']['mode']
	block_size = configs['threshold']['block_size']
	subtract_val = configs['threshold']['subtract_val']

	if mode == 'mean':
		image_threshold = cv2.adaptiveThreshold(copy, 255, 
			cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, block_size, subtract_val)
	elif mode == 'gaussian':
		image_threshold = cv2.adaptiveThreshold(copy, 255, 
			cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, subtract_val)
	else: 
		image_threshold = get_otsu_threshold(copy)

	return image_threshold

# def get_global_threshold(image_gray, threshold_value=127):
# 	copy = image_gray.copy()  # copy the image to be processed
# 	_, binary_image = cv2.threshold(copy, threshold_value, 255, cv2.THRESH_BINARY)
# 	return binary_image

def get_otsu_threshold(image_gray):
	copy = image_gray.copy()
	blur = cv2.GaussianBlur(copy, (5, 5), 0)
	ret3, imgae_otsu = cv2.threshold(copy, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	return imgae_otsu


def remove_long_line(image_binary):
	copy = image_binary.copy()

	global configs 
	threshold = configs['remove_line']['threshold']
	min_line_length = configs['remove_line']['min_line_length']
	max_line_gap = configs['remove_line']['max_line_gap']

	lines = cv2.HoughLinesP(copy, 1, np.pi / 180, threshold, np.array([]), min_line_length, max_line_gap)
	if lines is not None: 
		for line in lines:
			x1, y1, x2, y2 = line[0]
			cv2.line(copy, (x1, y1), (x2, y2), (0, 0, 0), 2)
	return copy 

def get_closing(image_gray):
	copy = image_gray.copy()
	global configs

	kernel_size_row = configs['close']['kernel_size_row']
	kernel_size_col = configs['close']['kernel_size_col']

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size_row, kernel_size_col))

	image_close = cv2.morphologyEx(copy, cv2.MORPH_CLOSE, kernel)
	return image_close


def get_contours(image):

	global configs
	retrieve_mode = configs['contour']['retrieve_mode']
	approx_method = configs['contour']['approx_method']

	contours, hierachy= cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
	# _, contours = cv2.findContours(image, retrieve_mode, approx_method)

	# print(hierachy)
	
	return contours

def draw_contour_rect(image_origin, contours):
	rgb_copy = image_origin.copy()

	global configs 
	min_width = configs['contour']['min_width']
	min_height = configs['contour']['min_height']

	if len(contours) == 0:
		print('contours: 0')
		return image_copy
	else : 
		for contour in contours:
			rect = cv2.minAreaRect(contour)
			box = cv2.boxPoints(rect)
			box = np.int0(box)
			# print(box[0])
			cv2.drawContours(rgb_copy, [box], 0, (0, 255, 0), 2)

	return rgb_copy



def get_cropped_images(image_origin, contours):
	""" 이미지에서 찾은 Contour 부분들을 잘라내어 반환합니다.
	각 contour 를 감싸는 외각 사각형에 여유분(padding)을 주어 이미지를 잘라냅니다.

	:param image_origin: 원본 이미지
	:param contours: 잘라낼 contour 리스트
	:return: contours 를 기반으로 잘라낸 이미지(OpenCV image 객체) 리스트
	"""
	image_copy = image_origin.copy()  # copy the image to be processed
	# get configs
	global configs
	min_width = configs['contour']['min_width']
	min_height = configs['contour']['min_height']
	padding = 8  # to give the padding when cropping the screenshot
	origin_height, origin_width = image_copy.shape[:2]  # get image size
	cropped_images = []  # list to save the crop image.

	for contour in contours:  # Crop the screenshot with on bounding rectangles of contours
		x, y, width, height = cv2.boundingRect(contour)  # top-left vertex coordinates (x,y) , width, height
		# screenshot that are larger than the standard size
		if width > min_width and height > min_height:
		# The range of row to crop (with padding)
			row_from = (y - padding) if (y - padding) > 0 else y
			row_to = (y + height + padding) if (y + height + padding) < origin_height else y + height
			# The range of column to crop (with padding)
			col_from = (x - padding) if (x - padding) > 0 else x
			col_to = (x + width + padding) if (x + width + padding) < origin_width else x + width
			# Crop the image with Numpy Array
			cropped = image_copy[row_from: row_to, col_from: col_to]
			cropped_images.append(cropped)  # add to the list
	return cropped_images




def ver1Convert(trim_img):
	imggray = cv2.cvtColor(trim_img, cv2.COLOR_BGR2GRAY)
	ret, img_binary = cv2.threshold(imggray, 127, 255, 0)
	contours, hierachy= cv2.findContours(img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

	print(len(contours))
	c0 = contours[0]
	# cv2.drawContours(imggray, [cnt0], 0, (0, 255, 0), 2)
	# outside = (55, 70)
	# inside = (149, 150)


	epsilon1 = 0.01*cv2.arcLength(c0, True)
	epsilon2 = 0.05*cv2.arcLength(c0, True)

	approx1 = cv2.approxPolyDP(c0, epsilon1, True)
	approx2 = cv2.approxPolyDP(c0, epsilon2, True)


	origin_img1 = cv2.drawContours(trim_img, [c0], -1, 7) 
	origin_img2 = cv2.drawContours(trim_img, [approx1], -1, 7)
	origin_img3 = cv2.drawContours(trim_img, [approx2], -1, 7)


	titles = ['Original', '$\epsilon=0.01$', '$\epsilon=0.05$']
	images = [origin_img1, origin_img2, origin_img3]

	for i in range(3):
	    plt.subplot(1, 3, i+1)
	    plt.title(titles[i])
	    plt.imshow(images[i], cmap='gray')
	    plt.axis('off')

	plt.tight_layout()
	plt.show()

# ============== stop ==================



# ============== ver 2.0 start ==================
def ver2Convert(trim_img):
	imggray = cv2.cvtColor(trim_img, cv2.COLOR_BGR2GRAY)
	# ret, img_binary = cv2.threshold(imggray, 127, 255, 0)
	ret, img_binary = cv2.threshold(imggray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	img_blur = cv2.GaussianBlur(img_binary, (3, 3), 0)
	ret, img_result = cv2.threshold(img_blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	
	# ret, img_new_result = cv2.adaptiveThreshold(imggray, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 2)

	cv2.imshow('trim_img', trim_img)
	cv2.imshow('gray', img_binary)
	cv2.imshow('blur', img_result)
	# cv2.imshow('img_new_result', img_new_result)

	cv2.waitKey(0)

	contours, hierachy= cv2.findContours(img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

	print(len(contours))
	# c0 = contours[0]
	# cv2.drawContours(imggray, [cnt0], 0, (0, 255, 0), 2)
	# outside = (55, 70)
	# inside = (149, 150)

	for cnt in contours : 
		epsilon1 = 0.01*cv2.arcLength(cnt, True)
		epsilon2 = 0.05*cv2.arcLength(cnt, True)

		approx1 = cv2.approxPolyDP(cnt, epsilon1, True)
		approx2 = cv2.approxPolyDP(cnt, epsilon2, True)

		origin_img1 = cv2.drawContours(trim_img, [cnt], -1, 7) 
		origin_img2 = cv2.drawContours(trim_img, [approx1], -1, 7)
		origin_img3 = cv2.drawContours(trim_img, [approx2], -1, 7)


	titles = ['Original', '$\epsilon=0.01$', '$\epsilon=0.05$']
	images = [origin_img1, origin_img2, origin_img3]

	for i in range(3):
	    plt.subplot(1, 3, i+1)
	    plt.title(titles[i])
	    plt.imshow(images[i], cmap='gray')
	    plt.axis('off')

	plt.tight_layout()
	plt.show()


def image_all_process(imgae_file):
	gray = get_gray(imgae_file)
	# cv2.imshow('gray', gray)

	gray1 = get_gradient(gray)
	# cv2.imshow('gray1', gray1)

	gray2 = get_threshold(gray1)
	# cv2.imshow('gray2', gray2)

	gray3 = get_closing(gray2)
	# cv2.imshow('gray3', gray3)

	# gray4 = remove_line(gray3)
	# cv2.imshow('gray4', gray4)

	contours = get_contours(gray3)

	return get_cropped_images(imgae_file, contours)


# def get_image_with_contours(imgae_file):
# 	gray = get_gray(imgae_file)

# 	gray1 = get_gradient(gray)

# 	gray2 = get_threshold(gray1)

# 	gray3 = get_closing(gray2)

# 	contours = get_contours(gray3)
# 	image_with_contours = draw_contour_rect(image_origin, contours)


# ============== stop ==================


if __name__ == '__main__':
	# org_img = cv2.imread('../ocr/video/output/frame530.png')
	# trim_img = im_trim(org_img)
	# ver2Convert(trim_img)
	main()



# img1 = cv2.imread('../ocr/video/output/frame530.png')
# img2 = cv2.imread('../ocr/video/output/frame530.png')
# img3 = cv2.imread('../ocr/video/output/frame530.png')

# ret, thr = cv2.threshold(img1gray, 720, 1260, 0)
# _, contours, _ = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

# # contours, hierachy = cv2.cvStartFindContours_Impl(img1, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

# c0 = contours[0]

# epsilon1 = 0.01*cv2.arcLength(c0, True)
# epsilon2 = 0.05*cv2.arcLength(c0, True)

# approx1 = cv2.approxPolyDP(c0, epsilon1, True)
# approx2 = cv2.approxPolyDP(c0, epsilon2, True)

# image1 = cv2.drawContours(img1, [c0], -1, 7)  #
# image2 = cv2.drawContours(img2, [approx1], -1, 7)
# image3 = cv2.drawContours(img3, [approx2], -1, 7)

# titles = ['Original', '$\epsilon=0.01$', '$\epsilon=0.05$']
# images = [image1, image2, image3]

# for i in range(3):
#     plt.subplot(1, 3, i+1)
#     plt.title(titles[i])
#     plt.imshow(images[i], cmap='gray')
#     plt.axis('off')

# plt.tight_layout()
# plt.show()



# ================= TEST ========================== # 

# imggray = cv2.cvtColor(trim_img, cv2.COLOR_BGR2GRAY)
# # cv2.imshow("gray", imggray)
# # cv2.waitKey(0)

# ret, img_binary = cv2.threshold(imggray, 1227, 255, 0)
# contours, hierachy = cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)
# print(len(contours))
# for cnt in contours:
# 	cv2.drawContours(trim_img, [cnt], 0, (0, 255, 0), 2)

# cv2.imshow('result', trim_img)
# cv2.waitKey(0)


# for cnt in contours:
# 	area = cv.contourArea(cnt)
# 	print(area)

# cv2.imshow("result", trim_img)
# cv2.waitKey(0)







