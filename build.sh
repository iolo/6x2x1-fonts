#!/bin/bash

function exec_fontforge {
    fontforge $@
}

function exec_bitsnpicas {
    java -jar ./BitsNPicas.jar $@
}

function buildFont {
    rm "./fonts/$3*"
    node fnt2bdf.js "$1" "$2" "$3.bdf"
    exec_bitsnpicas convertbitmap -f ttf -o temp.ttf "$3.bdf"
    exec_fontforge --script generate_hangul_syllables.py "$3"
    if [ -x "./FontPatcher/font-patcher" ]; then
      exec_fontforge --lang=py --script ./FontPatcher/font-patcher --complete "$3.ttf"
    fi
    rm temp.ttf
}

buildFont "src/lstar-eng.fnt" "src/lstar-han.fnt" "Lstar_6x2x1"
buildFont "src/wordcomm-eng.fnt" "src/wordcomm-han.fnt" "Wordcomm_6x2x1"
buildFont "src/woori-eng.fnt" "src/woori-han.fnt" "Woori_6x2x1"
buildFont "src/romax-eng.fnt" "src/romax-han.fnt" "Romax_6x2x1"
