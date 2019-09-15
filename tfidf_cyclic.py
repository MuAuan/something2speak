#>python tfidf_cyclic.py -d C:\PROGRA~1\mecab\dic\ipadic single_sentences.txt  -s stop_words.txt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import MeCab

import argparse
import pyaudio
import wave
from pykakasi import kakasi
import re
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
        try:
            wr = wave.open(wavfile, "rb")
        except:
            wavfile = './pyaudio/aiueo/n.wav'
            continue
        input = wr.readframes(wr.getnframes())
        output = stream.write(input)
        w.writeframes(input)

mecab = MeCab.Tagger("-Owakati" + ("" if not args.dictionary else " -d " + args.dictionary))

questions = []
answers = []
for line in open(args.input, "r", encoding="utf-8"):
    cols = line.strip().split('\t')
    questions.append(mecab.parse(cols[0]).strip())

stop_words = []
if args.stop_words:
    for line in open(args.stop_words, "r", encoding="utf-8"):
        stop_words.append(line.strip())

vectorizer = TfidfVectorizer(token_pattern="(?u)\\b\\w+\\b", stop_words=stop_words)
vecs = vectorizer.fit_transform(questions)

line = input("> ")
line1=line
line2=line
line3=line
while True:
    sims = cosine_similarity(vectorizer.transform([mecab.parse(line)]), vecs)
    index = np.argsort(sims[0])

    print("({:.2f}): {}".format(sims[0][index[-1]],questions[index[-1]]))
    text2speak(questions[index[-1]])
       
    print()
    time.sleep(2)
    line3=line2
    line2=line1
    line1=line
    while True:
        line = questions[index[-np.random.randint(1,7)]]
        if line1==line or line2==line or line3==line:
            continue
        else:
            break
