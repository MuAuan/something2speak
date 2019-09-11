import numpy as np
from PIL import ImageFont, ImageDraw, Image
import pyaudio
import wave
import struct
from pykakasi import kakasi

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

    print(sentence)
    print(conv.do(sentence))
    char_list = list(conv.do(sentence))
    print(char_list)

    kakasi_.setMode('H', 'a') # H(Hiragana) to a(roman)
    conv = kakasi_.getConverter()
    sentences=[]
    for i in range(len(char_list)):
        sent= conv.do(char_list[i])
        sentences.append(sent)
    
    print(sentences)
    f_list=[]
    f_list=sentences

    stream=p.open(format = pyaudio.paInt16,
        channels = 1,
        rate = int(RATE*1.5),
        frames_per_buffer = CHUNK,
        input = True,
        output = True) # inputとoutputを同時にTrueにする

    w = wave.Wave_write("./pyaudio/ohayo005_sin.wav")
    p = (1, 2, RATE, CHUNK, 'NONE', 'not compressed')
    w.setparams(p)
    for i in f_list:
        #=kana2a(i)
        wavfile = './pyaudio/aiueo/'+i+'.wav'
        print(wavfile)
        wr = wave.open(wavfile, "rb")
        input = wr.readframes(wr.getnframes())
        output = stream.write(input)
        w.writeframes(input)
        
while True:
    line = input("> ")
    if not line:
        break

    text2speak(line)
    print(line)       