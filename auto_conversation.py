#>python auto_conversation.py -d C:\PROGRA~1\mecab\dic\ipadic conversation_.csv  -s stop_words.txt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import MeCab

import argparse
import pyaudio
import wave
from pykakasi import kakasi
import re
import csv
import time

parser = argparse.ArgumentParser(description="convert csv")
parser.add_argument("input", type=str, help="faq tsv file")
parser.add_argument("--dictionary", "-d", type=str, help="mecab dictionary")
parser.add_argument("--stop_words", "-s", type=str, help="stop words list")
args = parser.parse_args()

def text2speak(num0):
    RATE=44100
    CHUNK = 22050
    p=pyaudio.PyAudio()
    kakasi_ = kakasi()

    sentence=num0

    kakasi_.setMode('J', 'H')  # J(Kanji) to H(Hiragana)
    kakasi_.setMode('H', 'H') # H(Hiragana) to None(noconversion)
    kakasi_.setMode('K', 'H') # K(Katakana) to a(Hiragana)

    conv = kakasi_.getConverter()

    char_list = list(conv.do(sentence))

    kakasi_.setMode('H', 'a') # H(Hiragana) to a(roman)
    conv = kakasi_.getConverter()
    sentences=[]
    for i in range(len(char_list)):
        sent= conv.do(char_list[i])
        sentences.append(sent)
    
    f_list=[]
    f_list=sentences

    stream=p.open(format = pyaudio.paInt16,
        channels = 1,
        rate = int(RATE*1.8),
        frames_per_buffer = CHUNK,
        input = True,
        output = True) # inputとoutputを同時にTrueにする

    w = wave.Wave_write("./pyaudio/ohayo005_sin.wav")
    p = (1, 2, RATE, CHUNK, 'NONE', 'not compressed')
    w.setparams(p)
    for i in f_list:
        i = re.sub(r"[^a-z]", "", i)
        if i== '':
            continue
        else:
            wavfile = './pyaudio/aiueo/'+i+'.wav'
        #print(wavfile)
        try:
            wr = wave.open(wavfile, "rb")
        except:
            wavfile = './pyaudio/aiueo/n.wav'
            continue
        input = wr.readframes(wr.getnframes())
        output = stream.write(input)
        w.writeframes(input)

def save_questions(line):
    with open('conversation_new.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow({line})
        
def conversation(questions,vecs,mecab):
    line = input("> ")
    line1=line
    line2=line
    line3=line
    with open('conversation_.csv', 'a', newline='') as f: #a+ #w
        writer = csv.writer(f)
        while True:
            writer.writerow({line})
            sims = cosine_similarity(vectorizer.transform([mecab.parse(line)]), vecs)
            index = np.argsort(sims[0])
            line3=line2
            line2=line1
            line1=line
            while True:
                index_= index[-np.random.randint(1,10)]
                line = questions[index_]
                if line1==line or line2==line or line3==line:
                    continue
                else:
                    break
                conv_new=read_conv(mecab)
                s=1
                ss=1
                for j in range(0,len(conv_new),1):
                    if line==conv_new[j]: 
                        s=0
                    else:
                        s=1
                    ss *= s
                    #print(ss,s)
                if ss == 0:
                    continue
                else:
                    break
            save_questions(line)
            print("({:.2f}): {}".format(sims[0][index_],questions[index_]))
            text2speak(questions[index_])
            time.sleep(2)
            line = input("> ")
            save_questions(line)
            if not line:
                break

def train_conv(mecab):
    questions = []
    with open('conversation_.csv') as f:
        cols = f.read().strip().split('\n')
        for i in range(len(cols)):
            questions.append(mecab.parse(cols[i]).strip())
    return questions        

def read_conv(mecab):
    conv_new = []
    with open('conversation_new.csv') as f:
        cols = f.read().strip().split('\n')
        for i in range(len(cols)):
            conv_new.append(mecab.parse(cols[i]).strip())
    return conv_new

mecab = MeCab.Tagger("-Owakati" + ("" if not args.dictionary else " -d " + args.dictionary))
stop_words = []
if args.stop_words:
    for line in open(args.stop_words, "r", encoding="utf-8"):
        stop_words.append(line.strip())

while True:
    questions = train_conv(mecab)
    vectorizer = TfidfVectorizer(token_pattern="(?u)\\b\\w+\\b", stop_words=stop_words)
    vecs = vectorizer.fit_transform(questions)
    conversation(questions,vecs,mecab)
   