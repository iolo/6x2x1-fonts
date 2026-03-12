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

buildFont "asc_hlink.fnt" "han_hlink.fnt" "Hlink_6x2x1"
buildFont "asc_mr128.fnt" "han_hgkey.fnt" "Hgkey_6x2x1"
buildFont "asc_mr128.fnt" "han_joong.fnt" "Joong_6x2x1"
buildFont "asc_mr128.fnt" "han_mr128.fnt" "Mr128_6x2x1"
buildFont "asc_romax.fnt" "han_romax.fnt" "Romax_6x2x1"
buildFont "asc_scrn9.fnt" "han_scrn9.fnt" "Scrn9_6x2x1"
buildFont "asc_wcomm.fnt" "han_wcomm.fnt" "Wcomm_6x2x1"
buildFont "asc_woori.fnt" "han_woori.fnt" "Woori_6x2x1"
