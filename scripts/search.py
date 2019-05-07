from .bloom_filter import *
from .aho import *
from collections import deque
import ahocorasick as ahc
import math
global prime_nos,phrases,word_code,input_phrases,input_phrases_idx
prime_nos=(113,117,119,123,129,131,137)
phrases=[]
word_code=[]
input_phrases=[]
input_phrases_idx=[]

def detector(patt_file,input_file):
	f=bloom_filter(10000007)
	input_code=deque()

	phrases,word_code=convertPhrases(patt_file)

	phraseMapping(word_code,f)

	input_phrases,input_phrases_idx=scanInput(input_file,input_code,f)

	patterns=filter_word(phrases,word_code,f)

	input_phrases,input_phrases_idx=exactMatching(input_phrases,patterns)

	commonwords=calc_plag(input_phrases,input_phrases_idx)

	percentage_calc(commonwords,patt_file,input_file)


def convertPhrases(patt_file):
	ascii_code=0
	word=''
	appended=True
	window=deque()
	for c in patt_file:
		if 'A'<=c<'Z':  
			ascii_code=ascii_code+ord(c)-65
			word=word+c
			appended=False
		else: 
			if appended is False:
				word_code.append(ascii_code)
				window.append(word)
				if len(window)==3:
					k=' '.join(list(window))
					phrases.append(k)
					window.popleft()
				ascii_code=0
				word=''
				appended=True
	return phrases,word_code


def rolling_hash(prev,next,present_hash):
	next_hash=present_hash
	for i,prime in  enumerate(prime_nos):
		next_hash[i]=next_hash[i]-prev
		next_hash[i]=next_hash[i]/prime
		next_hash[i]=next_hash[i]+next*math.pow(prime,2)
	return next_hash

def phraseMapping(word_code,f):
	window=deque()
	indices=[0]*7
	a=word_code[0]
	b=word_code[1]
	c=word_code[2]
	for i,prime in enumerate(prime_nos):
		indices[i]=a+b*prime+c*math.pow(prime,2)
	f.set_bit(1,indices)
	window.extend([a,b,c])
	for code in word_code[3:]:
		x=window.popleft()
		window.append(code)
		indices=rolling_hash(x,code,indices)
		f.set_bit(1,indices)


def scanInput(input_file,input_code,f):
	ascii_code=0
	word=''
	shift_no=0
	appended=True
	window=deque()
	indices=[0]*7
	prev=''
	first_letter=True
	pair=[]
	for i,c in enumerate(input_file):
		if 'A'<=c<='Z':
			if first_letter:
				pair.append(i)
				first=False
			appended=False
			ascii_code=ascii_code+ord(c)-65
			word=word+c 
		else:
			if appended is False:
				input_code.append(ascii_code)
				pair.append(i)
				window.append([word,pair])
				if len(input_code)==3:
					if shift_no==0:
						a,b,c=input_code[0],input_code[1],input_code[2];
						for i,prime in enumerate(prime_nos):
							indices[i]=a+b*prime+c*math.pow(prime,2)
					else:
						indices=rolling_hash(prev,ascii_code,indices)

					if f.look_up(1,indices):
						f.set_bit(2,indices)
						input_phrases.append(window[0][0]+' '+window[1][0]+' '+window[2][0])
						input_phrases_idx.append([window[0][1][0],window[2][1][1]])
					prev=input_code.popleft()
					window.popleft()
					shift_no+=1
				ascii_code=0
				word=''
				appended=True
				first_letter=True
				pair=[]
	return input_phrases,input_phrases_idx


def filter_word(patterns,word_code,f):
	shift_no = 0
	window = deque()
	indices = [0]*7
	a=word_code[0]
	b=word_code[1]
	c=word_code[2]
	for i,prime in enumerate(prime_nos):
		indices[i] = a + b * prime + c * math.pow(prime, 2)

	if not f.look_up(2, indices):
		patterns[shift_no] = ' '
	window.extend([a, b, c])

	for code in word_code[3:]:
		x = window.popleft()
		window.append(code)
		shift_no += 1
		indices=rolling_hash(x, code, indices)
		if not f.look_up(2, indices):
			patterns[shift_no] = ' '

	patterns = list(filter(lambda x: x != ' ',patterns))
	return patterns


def exactMatching(input_phrases,patterns):
	k=[]
	A=ahoh()
	line=' '.join(input_phrases)

	k=len(patterns)

	input_phrases,input_phrases_idx=A.searchWords(patterns,k,line)

	return input_phrases,input_phrases_idx



def calc_plag(input_phrases,input_phrases_idx):

	commonwords=[]
	list1=[]
	list2=[]
	length=0
	prev=0

	for i,phrase in enumerate(input_phrases):
		if i==0:
			words=phrase.split()
			for j in range(3):
				commonwords.append(words[j])
				list1.append(words[j])
			prev=words
		else:
			words=phrase.split()
			if input_phrases_idx[i][0]==input_phrases_idx[i-1][1]+2 and (prev[1]==words[0] and prev[2]==words[1]) :
				commonwords.append(words[2])
				list1.append(words[2])
			else:
				if (prev[1]!=words[0]):
					list2.append(' '.join(list1))
					list1=[]
				for j in range(3):
					commonwords.append(words[j])
					list1.append(words[j])
			prev=words

	list2.append(' '.join(list1))

	print("Sentence:-")

	for i in range(len(list2)):
		print(i+1,":",list2[i],".")
	return commonwords



def percentage_calc(common_words,src_content,doc_content):
	src_word=[]
	doc_word=[]
	for one_word in src_content.upper().split():
		letter=one_word[len(one_word)-1]
		if not 'A' <= letter <= 'Z':
			src_word.append(one_word[:len(one_word)-1])
		else:
			src_word.append(one_word)

	for one_word in doc_content.upper().split():
		letter=one_word[len(one_word)-1]
		if not 'A' <= letter <= 'Z':
			doc_word.append(one_word[:len(one_word)-1])
		else:
			doc_word.append(one_word)

	src_size=len(src_word)
	doc_size=len(doc_word)

	d = len(common_words)
	plagPercent1 = (d/float(src_size)) * 100
	plagPercent2 = (d/float(doc_size)) * 100

	print("Plagiarism Percentage in file 1 :",end=' ')
	print(str(plagPercent1)+"%")
	print("Plagiarism Percentage in file 2 :",end=' ')
	print(str(plagPercent2)+"%")



def ss(path_source, path_scraped):
	
	with open(path_source,'r') as file:
		src_content=file.read()
		#print(src_content)
	with open(path_scraped,'r') as file:
		input_content=file.read()
		#print(input_content)
	detector(src_content.upper(),input_content.upper())


if __name__ == '__main__':
	ss()


