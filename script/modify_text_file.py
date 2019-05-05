import nltk
import string
from nltk.tokenize import sent_tokenize

clean_source =  open("clean_sample.txt", "w")
source_content = open("sample.txt","r").read()

for line in sent_tokenize(source_content):
    line = line.translate(str.maketrans('', '', string.punctuation))
    clean_source.write(line.upper() + "\n")
