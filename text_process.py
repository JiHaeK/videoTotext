import csv
import re
import time
import json

def text_pre_process(result):
	copy = str(result)
	copy2 = copy.replace("\n", "")
	text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', copy2)
	if text is None or len(text) < 2:
		return '' 
	else : 
		# print(result)
		return text



def text_save(final_result):
	f = open('output.csv', 'w', encoding='utf-8', newline='')
	wr = csv.writer(f)
	wr.writerow(['index', 'start_time', 'end_time', 'contents'])

	num = 1

	# final_result=[' 。 해다만들었다로 매 잔빼고그 8 0미0아치여시르게ㅜ디 111  네『「은 해00ㅣ 01 」제때 져 어져000 __4을이60000드시 7 은ㄴㅅㅅ  43 ㅎ 0110', 
	# ' 。 해다만들었다로 매 잔빼고그 8 0미0아치여시르게ㅜ디 111  네『「은 해00ㅣ 01 」제때 져 어져000 __4을이60000드시 7 은ㄴㅅㅅ  43 ㅎ 0110',
	# 'hello', 'hello', 'hi', 'konmonginad', 'knosdf sdfw', 'sdfasdfasdf', 'sdfasdfasdf']
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

		# for j in range(0, len(final_result)):
		# 	count=0
		# 	if index[j] == index[j+1]:
		# 		count+=1
		# 	else :
		# 		break
		# 