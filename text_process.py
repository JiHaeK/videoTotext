import csv
import re
import time
import json

def text_pre_process(result):
	""" 이미지에서 인식된 글자를 정제 합니다. 
	특수문자 제거, 1-2단어 제거, 줄바꿈 및 공백 제거

	:param result: 이미지에서 인식된 글자
	:return: 문자를 전처리한 결과 
	"""	
	copy = str(result)
	copy2 = copy.replace("\n", "")
	copy3 = re.sub('[^ㄱ-힗]', '', copy2)
	# re.sub('[^A-Za-z0-9]', '', copy2)
	result = re.sub('[-=+,#}/\{:^$.@*\※~&%ㆍ!『「』\\‘|\(\)\[_ ""\]\<\>`\'…》]', '', copy3)
	# shortword = re.compile(r'\W*\b\w{1,2}\b')
	# shortword.sub('', result)
	# text2 = re.sub(r'\d','',result)
	if result is not None and len(result) > 3:
		# print(result)
		return result



def text_save(final_result, section, path):
	""" 추출한 글자를 저장합니다. 
	index, start_time, end_time, section, contents

	:param final_result: 전처리 된 문자 
	:param path: csv 파일 저장 경로 
	"""		
	f = open(path, 'w', encoding='utf-8', newline='')
	wr = csv.writer(f)
	wr.writerow(['index', 'start_time', 'end_time', 'section', 'contents'])

	num = 1

	index=[]

	for i in range(0, len(final_result)):
		if(i==0):
			index.insert(0, 0)
			pass
		else: 
			if final_result[i-1] == final_result[i]:
				index.insert(i, i-1)
			else:
				index.insert(i, i)

	final_content=[]
	for i in range(0, len(final_result)):
		d_content={}
		if (index.count(i) == 0):
			pass
		else :
			d_content.update([("start", time.strftime("%H:%M:%S", time.gmtime(i))), 
				("end", time.strftime("%H:%M:%S", time.gmtime(i+index.count(i)))) , 
				('section', section[i]), 
				("contents", final_result[i])])
			final_content.append(d_content)

	for j in range(0, len(final_content)):
		wr.writerow([j, final_content[j]["start"],  final_content[j]["end"], final_content[j]["section"], final_content[j]["contents"]])

	f.close()

def directory_save(dic, section, path):
	f = open(path, 'w', encoding='utf-8', newline='')
	wr = csv.writer(f)
	wr.writerow(['index', 'start_time', 'end_time', 'section', 'contents'])
	
	final_content=[]
	for k, v in dic.items():
		d_content={}
		d_content.update([("start", time.strftime("%H:%M:%S", time.gmtime(int(k)))), 
				("end", time.strftime("%H:%M:%S", time.gmtime(int(k)+1))) , 
				('section', section[k]), 
				("contents", v)])
		final_content.append(d_content)

	for j in range(0, len(final_content)):
		wr.writerow([j, final_content[j]["start"],  final_content[j]["end"], final_content[j]["section"], final_content[j]["contents"]])
