import video_process as vp
import image_process as ct 
import image_judge as judge
import image_reco as reco
import text_process as txt
import cv2
import re
import os 
import vision_ocr as vision
import glob

def main():

# =================== 동영상 테스트 ================================
    fianl_result_array=[]
    section_result_array=[]

    video_path='test_video/final_jjan.mp4'
    # video에서 프레임 추출 
    frame_images = vp.extract_frame_from_video(video_path)
    f_len=len(frame_images)
    # 추출된 프레임에서 글자 영역 찾기 
    num = 0 
    num2 = 0
    for i, frame in enumerate(frame_images):
        vp.save_image(frame,'output/jjan/frames/frame_{}.jpg'.format(i))
        final_result=[]
        copy = ct.resize(frame)
        cropped_images=ct.image_all_process(copy)
        # 섹션 추출 
        ct.save_crooped_contours(cropped_images[0]["section"], 'output/jjan/section/section_{}'.format(i))
        
        for con in cropped_images[0]["contours"]:
            # 프레임에서 추출한 영역들 저장 (origin 로)
            ct.save_crooped_contours(con, 'output/jjan/contours/contours_{}_frame_{}_'.format(num2, i))
            num2 += 1
        
        # 한 프레임의 글자 영역들에서 텍스트 추출 과정 시작 
        for con in cropped_images[1]["contours"]:
            # 프레임에서 추출한 영역들 저장 (gray-scale로)
            ct.save_crooped_contours(ct.get_gradient(con), 'final_new/jjan/contours_{}_frame_{}_'.format(num,i))
            num += 1

    judge_result = judge.get_text_image(num, 'final_new/')

    path_dir ='/Users/jihae/Documents/GitHub/videoTotext/output/jjan/contours'



    num_text = 0
    num_not_text = 0
    tmp_result={}
    section={}

    flie_list = os.listdir(path_dir)
    flie_list.sort()

    for j in range(1, num):
        print(flie_list[j])
        second = flie_list[j].split('_')[-2]

        # 섹션 처리하기 
        if (second in section.keys()):
            pass
        else :
            section[second] = vision.image_ocr('output/jjan/section/section_{}.jpg'.format(second))

        # 텍스트인 contour 찾아내기 
        if judge_result[j] == 'text':
            val = vision.image_ocr('output/jjan/contours/'+flie_list[j])
            if second in tmp_result:
                tmp_result[second] = [tmp_result[second], val]
            else : 
                tmp_result[second] = val
            # print('num: %d, text: %s' %(num_text, val))
            num_text += 1

 # 모든 결과 값들 저장 하기
    txt.directory_save(tmp_result, section, 'output/jjan/jjan.csv')

if __name__ == "__main__":
    main()

