import cv2
from PIL import Image
import image_process as ct 
import text_process as txt
import datetime

def extract_frame_from_video(video_path) :
	"""
	비디오에서 1초당 하나의 프레임을 추출합니다.  

	:param video_path: 동영상 경로 
	:return: 프레임들이 저장되어 있는 배열 
	"""
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

		# print('{}.sec reading a new frame: {}'.format(count, success))

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

def save_image(image, path):
	"""
	추출한 프레임 이미지를 저장합니다. 
	
	:param image: 프레임 
	:param count: 초   
	"""
	cv2.imwrite(path, image)

if __name__ == "__main__":
	pass


