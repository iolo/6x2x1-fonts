#!/usr/bin/fontforge -script

import fontforge
import sys

name = sys.argv[1]

f = fontforge.open('temp.ttf')

NUM_CHO = 19 # no filler
NUM_JUNG = 21 # no filler
NUM_JONG = 27 # no filter

CHO_KIND = 6
JUNG_KIND = 2
JONG_KIND = 1

# 자모 초성/중성/종성
JAMO_CHO = 0x1100
JAMO_JUNG = 0x1161
JAMO_JONG = 0x11a8

# 가~힣
KOR = 0xac00
# PUA(0xe000~0xf8ff) 영역에 조합용 한글 초성/중성/종성 글립이 들어있음
#PUA = 0xe010
# conflict with nerd font glyphs
# https://github.com/ryanoasis/nerd-fonts/wiki/Glyph-Sets-and-Code-Points
PUA = 0xf600

PUA_FILL = PUA
PUA_JUNG = PUA + 1
PUA_CHO = PUA_JUNG + NUM_JUNG * JUNG_KIND
PUA_JONG = PUA_CHO + NUM_CHO * CHO_KIND

#                        ㅏ ㅐ ㅑ ㅒ ㅓ ㅔ ㅕ ㅖ ㅗ ㅘ ㅙ ㅚ ㅛ ㅜ ㅝ ㅞ ㅟ ㅠ ㅡ ㅢ ㅣ
cho_kind_without_jong = [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 0];
cho_kind_with_jong    = [3, 3, 3, 3, 3, 3, 3, 3, 4, 5, 5, 5, 4, 4, 5, 5, 5, 4, 4, 5, 3];

#             ㄱ ㄲ ㄴ ㄷ ㄸ ㄹ ㅁ ㅂ ㅃ ㅅ ㅆ ㅇ ㅈ ㅉ ㅊ ㅋ ㅌ ㅍ ㅎ
#             ㄱ ㅁ ㅂ ㅅ ㅌ ㅍ ㅎ ㅈ ㄴ ㄷ ㄹ ㅇ ㅊ ㅋ ㄲ ㅆ ㄸ ㅃ ㅉ
#              0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18
cho_glyphs = [ 0,14, 8, 9,16,10, 1, 2,17, 3,15,11, 7,18,12,13, 4, 5, 6]
#              ㅏ ㅐ ㅑ ㅒ ㅓ ㅔ ㅕ ㅖ ㅗ ㅘ ㅙ ㅚ ㅛ ㅜ ㅝ ㅞ ㅟ ㅠ ㅡ ㅢ ㅣ
#              ㅏ ㅐ ㅣ ㅓ ㅔ ㅑ ㅕ ㅒ ㅖ ㅗ ㅛ ㅜ ㅠ ㅡ ㅘ ㅙ ㅚ ㅟ ㅝ ㅞ ㅢ
#               0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20
jung_glyphs = [ 0, 1, 5, 7, 3, 4, 6, 8, 9,14,15,16,10,11,18,19,17,12,13,20, 2]
#              ㄱ ㄲ ㄳ ㄴ ㄵ ㄶ ㄷ ㄹ ㄺ ㄻ ㄼ ㄽ ㄾ ㄿ ㅀ ㅁ ㅂ ㅄ ㅅ ㅆ ㅇ ㅈ ㅊ ㅋ ㅌ ㅍ ㅎ
#              ㄱ ㅁ ㅂ ㅅ ㅌ ㅍ ㅎ ㅈ ㄴ ㄷ ㄹ ㅇ ㅊ ㅋ ㄲ ㅆ ㄳ ㄵ ㄶ ㄺ ㄻ ㄼ ㄽ ㄾ ㄿ ㅀ ㅄ
#               0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26
jong_glyphs = [ 0,14,16, 8,17,18, 9,10,19,20,21,22,23,24,25, 1, 2,26, 3,15,11, 7,12,13, 4, 5, 6];

code = JAMO_CHO
for cho in range(NUM_CHO):
    c = f.createChar(code)
    c.addReference(fontforge.nameFromUnicode(PUA_CHO + cho_glyphs[cho]))
    code += 1

code = JAMO_JUNG
for jung in range(NUM_JUNG):
    c = f.createChar(code)
    c.addReference(fontforge.nameFromUnicode(PUA_JUNG + jung_glyphs[jung]))
    code += 1

code = JAMO_JONG
for jong in range(NUM_JONG):
    c = f.createChar(code)
    c.addReference(fontforge.nameFromUnicode(PUA_JONG + jong_glyphs[jong]))
    code += 1

code = KOR
for cho in range(NUM_CHO):
    for jung in range(NUM_JUNG):
        # without jong
        #print(f'cho={cho},jung={jung}->code={code:04x},char={chr(code)}')
        cho_kind = cho_kind_without_jong[jung];
        jung_kind = 0
        jong_kind = 0
        cho_code = PUA_CHO + NUM_CHO * cho_kind + cho_glyphs[cho]
        jung_code = PUA_JUNG + NUM_JUNG * jung_kind + jung_glyphs[jung]
        c = f.createChar(code)
        c.addReference(fontforge.nameFromUnicode(cho_code))
        c.addReference(fontforge.nameFromUnicode(jung_code))
        code += 1
        for jong in range(NUM_JONG):
            # without jong
            #print(f'cho={cho},jung={jung},jong={jong}->code={code:04x},char={chr(code)}')
            cho_kind = cho_kind_with_jong[jung];
            jung_kind = 1
            jong_kind = 0
            cho_code = PUA_CHO + NUM_CHO * cho_kind + cho_glyphs[cho]
            jung_code = PUA_JUNG + NUM_JUNG * jung_kind + jung_glyphs[jung]
            jong_code = PUA_JONG + NUM_JONG * jong_kind + jong_glyphs[jong]
            c = f.createChar(code)
            c.addReference(fontforge.nameFromUnicode(cho_code))
            c.addReference(fontforge.nameFromUnicode(jung_code))
            c.addReference(fontforge.nameFromUnicode(jong_code))
            code += 1

f.os2_version = 4
f.os2_family_class = 49
f.os2_codepages = (0x00200000, 0x00000000)
f.os2_unicoderanges = (0x10000001, 0x11000000, 0x00000000, 0x00000000)

f.generate(f'{name}.ttf', flags=('short-post'))
f.generate(f'{name}.otf', flags=('short-post'))
f.generate(f'{name}.woff')
f.generate(f'{name}.woff2')

