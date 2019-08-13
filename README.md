# videoTotext

## video_process.py
#### Introduction
동영상에서 이미지를 추출 하기 위한 처리를 합니다. 

* 동영상에서 프레임 추출하기 (1frame per 1s)
* 프레임 저장 하기 



## imgae_process.py
#### Introduction
이미지에서 글자를 추출 하기 위한 처리를 합니다. 

* gray 변환: RGB 3D image 객체 --> gray scale 2D image 객체 

* Morph Gradient: 경계 이미지 추출

* Adaptive threshold: 흑백(Binary) 이미지 반환 
    두가지 옵션 
    * mean adaptive threshold
    * gaussian adaptive threshold

* Morph close: 한 덩어리로 묶기 위함 
    * 이미지에 Dilation 수행을 한 후 Erosion 을 수행

* contour 추출 
    * 단, 40X10 이하의 contour는 추출되지 않음 



## imgae_reco.py
#### Introduction
추출된 이미지에서 OCR 엔진을 통해 글자 인식을 합니다. 
* OCR엔진: tesseract(google)
* 설정: '--oem 3 --psm 6'




## text_process.py
#### Introduction
추출된 글자를 처리를 합니다. 

* 특수문자 제거 
* csv로 저장 