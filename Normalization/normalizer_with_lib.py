from num2words import num2words
import pandas as pd
import numpy as np
import re

def normalize_num(num: str, is_ordinal: bool):
	"""Converts the given number to words"""
	
	if num == "0":
		return 'sıfır'
	
	turkish_str = num2words(int(num), lang='tr', ordinal = is_ordinal)

	aze_str = translate_to_aze(turkish_str)
	
	return aze_str

def translate_to_aze(turkish_str: str):
	"""Translates the given turkish string to azerbaijani"""
	
	aze_str = turkish_str
	
	aze_str = aze_str.replace('dört', 'dörd')
	aze_str = aze_str.replace('yedi', 'yeddi')
	aze_str = aze_str.replace('sekiz', 'səkkiz')
	aze_str = aze_str.replace('dokuz', 'doqquz')
	aze_str = aze_str.replace('yirmi', 'iyirmi')
	aze_str = aze_str.replace('kırk', 'qırx')
	aze_str = aze_str.replace('elli', 'əlli')
	aze_str = aze_str.replace('seksen', 'səksən')
	aze_str = aze_str.replace('doksan', 'doxsan')
	aze_str = aze_str.replace('bin', 'min')
	aze_str = aze_str.replace('milyar', 'milyard')
	aze_str = aze_str.replace('katrilyon', 'kvadrilyon')
	aze_str = aze_str.replace('kentilyon', 'kvintilyon')
	
	return aze_str
	
if __name__ == "__main__":	
	df = pd.read_csv('metadata.csv', delimiter='|')
	# df.insert(2, 'normalized_string', '')
	# df = df.assign(normalized_string = '')
	# df = df.reindex(columns = ['fileName', 'sentence', 'normalized_string'])  
	df['normalized_string'] = 'Hello there'
	print(df.columns)
	
	sentences = df['sentence']
	
	sentences_to_drop = []
	
	for i in df.index:
		sentence = df.at[i, 'sentence']
		
		if type(sentence) is not str: # deleting empty string
			sentences_to_drop.append(i)
			print(i)
			continue
		
		matches = re.findall('(\d+-([a-zöəüğçşı]{3}|[a-zöəüğçşı]{2})|\d+)', sentence)
		
		if matches:
			for match in matches:
				num, group = match
				num = re.search('\d+', num)[0]
				if group in ['cı', 'ci', 'cu', 'cü']:
					sentence_new = sentence.replace(match[0], normalize_num(num, True)[:-1])
				else:
					sentence_new = sentence.replace(match[0], normalize_num(num, False)[:-1] + group)
					
			# df.at[i, 'sentence'] = sentence_new
			# print(i)
			# print('Before assignment: ', df.at[i, 'normalized_string'])
			df.at[i, 'normalized_string'] = sentence_new
			# df.set_value(i, 'normalized_string', sentence_new)
			# print('After assignment: ', df.at[i, 'normalized_string'])


	print(df['normalized_string'])
		
	df = df.drop(sentences_to_drop)
	np.savetxt('new_normalized.csv', df, delimiter='|', fmt='%s')
		