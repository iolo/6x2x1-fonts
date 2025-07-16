#!/bin/bash

function exec_fontforge {
    fontforge $@
}

function exec_bitsnpicas {
    java -jar ./BitsNPicas.jar $@
}

function buildFont {
    rm "./fonts/$3*"
    python3 fnt2bdf.py "src/$1" "src/$2" "fonts/$3.bdf"
    exec_bitsnpicas convertbitmap -f ttf -o temp.ttf "fonts/$3.bdf"
    exec_fontforge --script generate_hangul_syllables.py "fonts/$3"
    if [ -x "./FontPatcher/font-patcher" ]; then
      exec_fontforge --lang=py --script ./FontPatcher/font-patcher --complete --out fonts "fonts/$3.ttf"
    fi
    rm temp.ttf
}

buildFont "lstar-eng.fnt" "lstar-han.fnt" "Lstar_6x2x1"
buildFont "wordcomm-eng.fnt" "wordcomm-han.fnt" "Wordcomm_6x2x1"
buildFont "woori-eng.fnt" "woori-han.fnt" "Woori_6x2x1"
buildFont "romax-eng.fnt" "romax-han.fnt" "Romax_6x2x1"
