import csv
import re
import time
import json

def text_pre_process(result):
	copy = str(result)
	copy2 = copy.replace("\n", "").replace(' ', '')
	text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!『「』\\‘|\(\)\[\]\<\>`\'…》]', '', copy2)
	text = re.sub(r'\d','',text)
	if text is None or len(text) < 2:
		return '' 
	else : 
		print(text)
		return text



def text_save(final_result, path):
	f = open(path, 'w', encoding='utf-8', newline='')
	wr = csv.writer(f)
	wr.writerow(['index', 'start_time', 'end_time', 'contents'])

	num = 1

	final_result_copy=final_result
	index=[]

	for i in range(0, len(final_result_copy)):
		if(i==0):
			index.insert(0, 0)
			pass
		else: 
			if final_result_copy[i-1] == final_result_copy[i]:
				index.insert(i, i-1)
			else:
				index.insert(i, i)


	final_content=[]
	for i in range(0, len(final_result_copy)):
		d_content={}
		if (index.count(i) == 0):
			pass
		else :
			d_content.update([("start", time.strftime("%H:%M:%S", time.gmtime(i))), 
				("end", time.strftime("%H:%M:%S", time.gmtime(i+index.count(i)))) , 
				("contents", final_result_copy[i])])
			final_content.append(d_content)

	for j in range(0, len(final_content)):
		wr.writerow([j, final_content[j]["start"],  final_content[j]["end"],  final_content[j]["contents"]])
	
	f.close()
