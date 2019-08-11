import cv2
import matplotlib.pyplot as plt
from PIL import Image
import reco
import contour_test as ct 
import text_process as txt
import time

def extract_image_fps(video_path) :
	vidcap = cv2.VideoCapture(video_path)
	fps = vidcap.get(cv2.CAP_PROP_FPS)
	timestamps = [vidcap.get(cv2.CAP_PROP_POS_MSEC)]
	calc_timestamps = [0.0]

	count=0
	success=True

	while(vidcap.isOpened()):
		vidcap.set(cv2.CAP_PROP_POS_MSEC, (count*1000))
		success, image = vidcap.retrieve()
		final_result=''

		out_image=convert_matrix_to_img(image)

		# print(image.shape)
		# print(type(image))
		# print(type(out_image))
		# print(out_image.size)

		# cv2.imshow('image', image)
		# cv2.waitKey(10)
		# cv2.destroyAllWindows()

		cv2.imwrite("./video/output/frame%d.png" % count, image)
		print('{}.sec reading a new frame: {}'.format(count, success))
		# frame_exists, curr_frame = vidcap.read()
		# if frame_exists:
		# 	timestamps.append(vidcap.get(cv2.CAP_PROP_POS_MSEC))
		# 	calc_timestamps.append(calc_timestamps[-1] + 1000/fps)
		# else:
		# 	break
		# print('Frame %d / start: %d/ end: %d :'%(count, (vidcap.get(cv2.CAP_PROP_POS_MSEC))/33/30, (calc_timestamps[-1] )/33 ))
		
		# image = cv2.imread(image)

		gray = ct.get_gray(image)
		cv2.imshow('gray', gray)

		gray1 = ct.get_gradient(gray)
		cv2.imshow('gray1', gray1)

		gray2 = ct.get_threshold(gray1)
		cv2.imshow('gray2', gray2)

		gray3 = ct.get_closing(gray2)
		cv2.imshow('gray3', gray3)

		gray4 = ct.remove_short_line(gray3)
		cv2.imshow('gray4', gray4)

		contours = ct.get_contours(gray3)

		result = ct.draw_contour_rect(image, contours)
		conts = ct.get_cropped_images(image, contours)
		print(len(conts))


		for con in conts :
			# cv2.imshow('contours', con)
			# cv2.waitKey(0)
			# cv2.destroyAllWindows()
			result = reco.extract_text(con)
			final_result = final_result + txt.text_pre_process(result)
		# print(final_result)
		fianl_result_array.append(final_result)

		count += 1



	vidcap.release()
	return fianl_result_array

	# while success:
	# 	vidcap.set(cv2.CAP_PROP_POS_MSEC, (count*1000))
	# 	success, image = vidcap.retrieve()
	# 	# print('Read a new frame: ', success)
	# 	# print(image)
	# 	out_image=convert_matrix_to_img(image)

	# 	print(image.shape)
	# 	print(type(image))
	# 	print(type(out_image))
	# 	print(out_image.size)

	# 	cv2.imshow('image', image)
	# 	cv2.waitKey(10)
	# 	cv2.destroyAllWindows()

	# 	# cv2.imwrite("./video/output/frame%d.png" % count, image)
	# 	print('{}.sec reading a new frame: {}'.format(count, success))
	# 	count += 1




def convert_matrix_to_img(matrix):
	# w, h = 512, 512
	# data = np.zeros((h, w, 3), dtype=np.uint8)
	# data[256, 256] = [255, 0, 0]
	img = Image.fromarray(matrix, 'RGB')

	return img


if __name__ == "__main__":
	fianl_result_array=[]
	ct.read_configs('configs.json')

	video_path='../ocr/video/test_back_2_720.mp4'
	final = extract_image_fps(video_path)
	txt.text_save(final)

	# image_path = 'kang4.png'
	# image = cv2.imread(out_image)


	# gray = ct.get_gray(image)
	# cv2.imshow('gray', gray)

	# canny = ct.get_canny(gray)
	# cv2.imshow('canny', canny)

	# gray1 = ct.get_gradient(gray)
	# cv2.imshow('gray1', gray1)

	# gray2 = ct.get_threshold(gray1)
	# cv2.imshow('gray2', gray2)

	# gray3 = ct.get_closing(gray2)
	# cv2.imshow('gray3', gray3)

	# gray4 = ct.remove_short_line(gray3)
	# cv2.imshow('gray4', gray4)

	# contours = ct.get_contours(gray3)

	# result = ct.draw_contour_rect(image, contours)
	# conts = ct.get_cropped_images(image, contours)
	# print(len(conts))

	# # cv2.imshow('result', result)
	# # cv2.waitKey(0)
	# # cv2.destroyAllWindows()

	# # reco.extract_text(gray)


	# for con in conts :
	# 	# cv2.imshow('contours', con)
	# 	# cv2.waitKey(0)
	# 	# cv2.destroyAllWindows()
	# 	result = reco.extract_text(con)
	# 	final_result = final_result + txt.text_pre_process(result)
	# # print(final_result)
	# fianl_result_array.append(final_result)


	# txt.text_save(fianl_result_array)






	# img='/Users/jihae/Desktop/gmsd.png'
	# reco.extract_text(img)