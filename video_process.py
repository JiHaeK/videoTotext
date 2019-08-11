import cv2
import matplotlib.pyplot as plt
from PIL import Image
import imgae_reco as reco
import image_process as ct 
import text_process as txt
import time
import datetime

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

		# cv2.imwrite("./video/output/frame%d.png" % count, image)
		print('{}.sec reading a new frame: {}'.format(count, success))

		frame_exists, curr_frame = vidcap.read()
		if frame_exists:
			timestamps.append(vidcap.get(cv2.CAP_PROP_POS_MSEC))
			calc_timestamps.append(calc_timestamps[-1] + 1000/fps)
		else:
			break

		cropped_images = ct.image_all_process(image)
		# show_result = ct.get_image_with_contours(image)

		for con in cropped_images :
			i = 0
			save_image(con, "crop_" + str(i))
			result = reco.extract_text(con)
			final_result = final_result + txt.text_pre_process(result)
			i += 1
		# print(final_result)
		fianl_result_array.append(final_result)

		count += 1



	vidcap.release()
	return fianl_result_array


def convert_matrix_to_img(matrix):
	img = Image.fromarray(matrix, 'RGB')
	return img

def save_image(image, name_prefix='untitled'):
    """ 이미지(OpenCV image 객체)를 이미지파일(.jpg)로 저장합니다.

    :param image: 저장할 이미지 (OpenCV image 객체)
    :param name_prefix: 파일명을 식별할 접두어 (확장자 제외)
    :return:
    """
    # make file name with the datetime suffix.
    d_date = datetime.datetime.now()  # get current datetime
    current_datetime = d_date.strftime("%Y%m%d%I%M%S")  # datetime to string
    file_path = name_prefix + '_'+ current_datetime + ".jpg"  # complete file name
    cv2.imwrite(file_path, image)


if __name__ == "__main__":
	fianl_result_array=[]
	ct.read_configs('configs.json')

	video_path='test_video/amazing_720p.mp4'
	final = extract_image_fps(video_path)
	txt.text_save(final, 'amazing_output.csv')


