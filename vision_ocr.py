import io
import os
import urllib.request 
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
# export GOOGLE_APPLICATION_CREDENTIALS=PATH_TO_KEY_FILE

def image_ocr(path):
    vision_client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    # Loads the image into memory
    # mem = urllib.request.urlopen(url).read()

    file_name = os.path.join(os.path.dirname(__file__), path)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
       content = image_file.read()

    image = types.Image(content=content)

    # Performs text detection on the image file
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations

    # print(texts[0].description)
    if len(texts) > 1 :
        return texts[0].description
    else : 
        return ''
    # print(type(texts[0].description))


if __name__ == '__main__':
    # url = 'https://pbs.twimg.com/media/CW9SmtkUkAA5qMY.jpg'
    # image_ocr('new3/global/frames/frame_114.jpg')
    pass 