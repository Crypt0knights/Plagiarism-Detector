import nltk
import string
from nltk.tokenize import sent_tokenize

def main():
    clean_source =  open("./check/files/search.txt", "w")
    print("Hello world")
    source_content = open("sample.txt","r").read()

    for line in sent_tokenize(source_content):
        line = line.translate(str.maketrans('', '', string.punctuation))
        clean_source.write(line.upper() + "\n")

#start process
if __name__ == '__main__':
    main()