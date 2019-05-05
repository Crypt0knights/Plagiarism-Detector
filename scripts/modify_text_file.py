import nltk
import string
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

clean_source =  open("clean_sample.txt", "w")
source_content = open("sample.txt","r").read()
stop_words = list(stopwords.words("english"))
stop_words.append("the")
stop_words.append("The")

word_list = []
for line in sent_tokenize(source_content):
    print(line)
    word_list = line.split()
    word_list = [word for word in word_list if word not in stop_words]
    line = " ".join(word_list)
    line = line.translate(str.maketrans('', '', string.punctuation))
    clean_source.write(line.upper() + "\n")
