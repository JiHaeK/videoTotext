# videoTotext
## 프로젝트 개요

### 동영상에서 세부 글자(자막, 타이틀) 추출
* OpenCV 를 이용하여 여섯 단계의 이미지처리를 통해 글자로 추정되는 부분을 찾기
* 딥러닝 Image Classification 을 통해서 찾은 부분이 글자인지 아닌지 판단
* OCR 엔진을 통해 글자이미지에서 TEXT 추출

### 개발환경
* Python >= 3
* OpenCV
* Tesseract (OCR engine)


## video_process.py
#### Introduction
동영상에서 이미지를 추출 하기 위한 처리를 합니다. 

```def extract_frame_from_video(video_path):
* 동영상에서 프레임 추출하기 (1frame per 1s)
	__:param video_path:__ 동영상 경로 
	__:return:__ 프레임들이 저장되어 있는 배열
```

```def save_image(image, count):
* 추출한 프레임 이미지를 저장합니다. 
	_:param image:_ 프레임 
	_:param count:_ 초   
```

## imgae_process.py
#### Introduction
이미지에서 글자를 추출 하기 위한 처리를 합니다. 

``` def get_gray(image_origin):
* gray 변환: RGB 3D image 객체 --> gray scale 2D image 객체 
	:param image_origin: OpenCV 의 BGR image 객체 (3 dimension)
	:return: gray-scale 이 적용된 image 객체 (2 dimension)
```

``` def get_gradient(image_gray):
* Morph gradient 적용 
* 이미지에 Dilation 과 Erosion 을 적용하여 그 차이를 이용해 윤곽선을 추출합니다.
	_:param image_gray:_ gray-scale 이 적용된 image 객체 (2 dimension)
	_:return: image_gradient:_ 윤관선 추출한 결과 이미지 (Opencv 이미지)
```

``` def get_threshold(image_gray):
* 이미지에 Threshold 를 적용해서 흑백(Binary) 이미지객체를 반환합니다.
	_:param image_gray:_ gray-scale 이 적용된 image 객체 (2 dimension)
	_:return: image_gradient:_ Threshold 적용한 흑백(Binary) 이미지 (Opencv 이미지)
    두가지 옵션 
    * mean adaptive threshold
    * gaussian adaptive threshold
```

```def get_closing(image_gray):
* 이미지에 Morph Close 를 적용한 이미지객체를 반환합니다.
	_:param image_gray:_ Gray-scale 이 적용된 OpenCV image (2 dimension)
	_:return:_ Morph Close 를 적용한 흑백(Binary) 이미지
```

``` def get_contours(image):
* contour 추출 
    * 단, 40X10 이하의 contour는 추출되지 않음 
	_:param image:_ 전처리가 끝난 OpenCV의 image 객체 (2 dimension)
    _:return:_ 이미지에서 추출한 contours (dictonary) 
 ```

``` def get_cropped_images(image_origin, contours):
* 이미지에서 찾은 Contour 부분들을 잘라내어 반환합니다.
* 각 contour 를 감싸는 외각 사각형에 여유분(padding)을 주어 이미지를 잘라냅니다.
    _:param image_origin:_ 원본 이미지
    _:param contours:_ 잘라낼 contour 딕셔너리
    _:return:_ contours 를 기반으로 잘라낸 이미지(OpenCV image 객체) 딕셔너리
```

```def save_crooped_contours(image, path):
* 잘라낸 Contour 부분들을 저장합니다.
	_:param image:_ 잘라낸 contour 이미지 
	_:param count:_ 잘라낸 contour 순서 
```

``` def image_all_process(imgae_file):
* 5단계의 이미지 전처리를 실행합니다.
    _:param image_file:_ 프레임 이미지 파일(BGR image)
    _:return:_ contours 를 기반으로 잘라낸 이미지(OpenCV image 객체) 딕셔너리
```

## imgae_judge.py
#### Introduction
이미지가 텍스트인지 아닌지 판단합니다. 
* 딥러닝 모델: resnet50 
* Activatoin: softamx 
* Loss: Binary-crossentropy 

``` def get_text_image():
* 잘려진 conotur가 텍스트인지 아닌지 판단합니다.
	_:param contour_path:_ gray-scale 처리된 contour가 저장된 경로 
    _:return:_ output[0] = 0이면 negative(not_text),
               output[0] == 1이면 positive(text)
```


## imgae_reco.py
#### Introduction
추출된 이미지에서 OCR 엔진을 통해 글자 인식을 합니다. 
```def extract_text(tmp_image):
* OCR엔진: tesseract(google)
* 설정: '--oem 3 --psm 6'
	_:param tmp_image:_ Opencv 이미지 객체
	_:return:_ 인식된 결과 (str) 
```



## text_process.py
#### Introduction
추출된 글자를 처리를 합니다. 

``` def text_pre_process(result):
* 이미지에서 인식된 글자를 정제 합니다. 
* 특수문자 제거, 1-2단어 제거, 줄바꿈 및 공백 제거
	_:param result:_ 이미지에서 인식된 글자
	_:return:_ 문자를 전처리한 결과
``` 
* csv로 저장 
``` def text_save(final_result, section, path):
* 추출한 글자를 저장합니다. 
* 컬럼: index, start_time, end_time, section, contents

	_:param final_result:_ 전처리 된 문자 
	_:param path:_ csv 파일 저장 경로 
```

## 라이센스 (License)
MIT license 