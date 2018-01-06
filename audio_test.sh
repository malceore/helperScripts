#!/bin/bash
set -e

function finish {
  rm test_audio.wav
}

trap finish EXIT

printf ">>Starting ALSA audio test...\n>>Here are the audio devices your PC sees:\n"
arecord -l

printf "\n>>We will now record a five second sound blip and play it back.\n"
arecord -f S16_LE -c 2 -r 192000 -d 5 test_audio.wav
printf "\n>>Playing back test_audio..\n"
aplay -D hw:0,0 test_audio.wav
printf "\n>>If you didn't hear anything or if audio was garbled please check and reconfigure your audio IO.\n"

