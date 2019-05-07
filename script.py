import nltk
import string
from nltk.tokenize import sent_tokenize

def main():
    clean_source =  open("./search.txt", "w")
    source_content = open("file.txt","r").read()

    for line in sent_tokenize(source_content):
        line = line.translate(str.maketrans('', '', string.punctuation))
        clean_source.write(line.upper() + "\n")
print("Applied NLP to PDF data and stored file in ./check/files/search.txt")

#start process
if __name__ == '__main__':
    main()