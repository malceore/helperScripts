#!/usr/bin/python

from os import environ, path

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

MODELDIR = "../pocketsphinx-python/pocketsphinx/model/"
DATADIR = "../pocketsphinx-python/pocketsphinx/test/data/"

config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
#config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
#config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
config.set_string('-lm', 'lang_models/assistant.lm')
config.set_string('-dict', 'lang_models/assistant.dic')
config.set_string('-logfn', '/dev/null')
decoder = Decoder(config)

# stream = open(path.join(DATADIR, 'goforward.raw'), 'rb')
# stream = open('10001-90210-01803.wav', 'rb')
import pyaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()
print("Listening..")

in_speech_bf = False
decoder.start_utt()
while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                print 'Result:', decoder.hyp().hypstr
                decoder.start_utt()
    else:
        break
decoder.end_utt()
