import cv2
from PIL import Image
import imgae_reco as reco
import image_process as ct 
import text_process as txt
import datetime

def extract_image_fps(video_path) :
	frame_images=[]
	vidcap = cv2.VideoCapture(video_path)
	fps = vidcap.get(cv2.CAP_PROP_FPS)
	timestamps = [vidcap.get(cv2.CAP_PROP_POS_MSEC)]
	calc_timestamps = [0.0]

	count=0
	success=True

	while(vidcap.isOpened()):
		vidcap.set(cv2.CAP_PROP_POS_MSEC, (count*1000))
		success, image = vidcap.retrieve()

		print('{}.sec reading a new frame: {}'.format(count, success))

		frame_exists, curr_frame = vidcap.read()
		if frame_exists:
			timestamps.append(vidcap.get(cv2.CAP_PROP_POS_MSEC))
			calc_timestamps.append(calc_timestamps[-1] + 1000/fps)
		else:
			break

		frame_images.append(image)
		count += 1

	vidcap.release()
	return frame_images
def convert_matrix_to_img(matrix):
	img = Image.fromarray(matrix, 'RGB')
	return img

def save_image(image, count):
	f_name = 'frame' + str(count)
	file_path = f_name + ".jpg"  # complete file name
	cv2.imwrite(file_path, image)

if __name__ == "__main__":
	pass


