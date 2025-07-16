Function fontforge {
    & "${env:ProgramFiles(x86)}\FontForgeBuilds\fontforge.bat" $args
}

Function bitsnpicas {
    & "${env:JAVA_HOME}\bin\java.exe" -jar "$HOME\apps\bitsnpicas\BitsNPicas.jar" $args
}

Function buildFont($eng, $kor, $out) {
    rm "./fonts/$out*"
    python fnt2bdf.py "src/$eng" "src/$kor" "fonts/$out.bdf"
    bitsnpicas convertbitmap -f ttf -o temp.ttf "fonts/$out.bdf"
    fontforge --lang=py --script generate_hangul_syllables.py "fonts/$out"
    if (Test-Path "./FontPatcher/font-patcher") {
      fontforge --lang=py --script ./FontPatcher/font-patcher --careful --complete "fonts/$out.ttf"
    }
    rm temp.ttf
}

buildFont "lstar-eng.fnt" "lstar-han.fnt" "Lstar_6x2x1"
buildFont "wordcomm-eng.fnt" "wordcomm-han.fnt" "Wordcomm_6x2x1"
buildFont "woori-eng.fnt" "woori-han.fnt" "Woori_6x2x1"
buildFont "romax-eng.fnt" "romax-han.fnt" "Romax_6x2x1"
