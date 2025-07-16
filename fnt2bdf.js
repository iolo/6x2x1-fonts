const fs = require('fs');
const path = require('path');
// https://susam.net/code/cp437/cp437.html
const CP437_TO_UNICODE = require('./cp437_to_unicode.json');
// conflict with nerd font glyphs
// https://github.com/ryanoasis/nerd-fonts/wiki/Glyph-Sets-and-Code-Points
//const PUA = 0xe010; 
const PUA = 0xf600;

function reverseBits(byte, ignoreHalfDot) {
  if (ignoreHalfDot) {
        return ((byte & 0x40) >> 5)
          | ((byte & 0x20) >> 3)
          | ((byte & 0x10) >> 1)
          | ((byte & 0x08) << 1)
          | ((byte & 0x04) << 3)
          | ((byte & 0x02) << 5)
          | ((byte & 0x01) << 7);
  }
  return ((byte & 0x80) >> 7)
    | ((byte & 0x40) >> 5)
    | ((byte & 0x20) >> 3)
    | ((byte & 0x10) >> 1)
    | ((byte & 0x08) << 1)
    | ((byte & 0x04) << 3)
    | ((byte & 0x02) << 5)
    | ((byte & 0x01) << 7);
}

function generateGlyphs({ fileName, glyphWidth, glyphHeight, glyphCount, codeMapper }) {
  const result = [];
  const glyphData = fs.readFileSync(fileName);
  const glyphAscent = glyphHeight;
  const glyphDescent = glyphHeight - glyphAscent;
  const glyphWidthBytes = glyphWidth / 8;
  const bytesPerGlyph = glyphWidthBytes * glyphHeight;
  for (let i = 0, offset = 0; i < glyphCount; i++) {
    const code = codeMapper ? codeMapper(i) : i;
    result.push(`STARTCHAR U+${code.toString(16).toUpperCase().padStart(4, `0`)}`);
    result.push(`ENCODING ${code}`);
    result.push(`SWIDTH ${glyphWidth * 1000} 0`);
    result.push(`DWIDTH ${glyphWidth} 0`);
    result.push(`BBX ${glyphWidth} ${glyphHeight} ${-glyphDescent}`);
    result.push(`BITMAP`);
    // column first
    // ex. glyphWidthBytes=2, glyphHeight=3
    // 0 3
    // 1 4
    // 2 5
    for (let y = 0; y < glyphHeight; y++) {
      const hex = [];
      for (let x = 0; x < glyphWidthBytes; x++) {
        const byte = reverseBits(glyphData[(offset + y) + (x * glyphHeight)], x & 0x01);
        hex.push(byte.toString(16).toUpperCase().padStart(2, '0'));
      }
      result.push(hex.join(''));
    }
    // next glyph
    offset += glyphWidthBytes * glyphHeight;
    /*
    // column first
    const hex = [];
    for (let y = 0; y < glyphHeight; y++) {
      hex[y] = [];
    }
    for (let x = 0; x < glyphWidthBytes; x++) {
      for (let y = 0; y < glyphHeight; y++) {
        const byte = glyphData[offset++];
        // reverse bit
        let rev = 0 //((byte & 0x80) >> 7) // ignore apple2's half-dot shift
          | ((byte & 0x40) >> 5)
          | ((byte & 0x20) >> 3)
          | ((byte & 0x10) >> 1)
          | ((byte & 0x08) << 1)
          | ((byte & 0x04) << 3)
          | ((byte & 0x02) << 5)
          | ((byte & 0x01) << 7);
        if (x & 0x01) {
          // even column
          rev <<= 1;
        }
        hex[y].push(rev.toString(16).toUpperCase().padStart(2, '0'));
      }
    }
    for (let y = 0; y < glyphHeight; y++) {
      result.push(hex[y].join(''));
    }
    */
    result.push(`ENDCHAR`);
  }
  return result.join('\n');
}

function generateFont({ fontName, fontWidth, fontHeight, fontAscent, fontDescent = 0, glyphs }) {
  const result = [];
  result.push('STARTFONT 2.1');
  result.push(`FONT ${fontName}`);
  //-${fontFoundary}-${fontName}-medium-r-normal--${glyphHeight}-${fontHeight*10}-72-72-c-${fontWidth*10}-iso10646-1
  result.push(`SIZE ${fontHeight} 72 72`);
  result.push(`FONTBOUNDINGBOX ${fontWidth} ${fontHeight} 0 ${-fontDescent}`);
  result.push(`SWIDTH ${fontWidth * 1000} 0`);
  result.push(`DWIDTH ${fontWidth} 0`);
  result.push(`STARTPROPERTIES 2`);
  result.push(`FAMILY_NAME ${fontName}`);
  result.push(`FONT_ASCENT ${fontAscent ?? fontHeight - fontDescent}`);
  result.push(`FONT_DESCENT ${fontDescent}`);
  result.push(`ENDPROPERTIES`);
  result.push(`CHARS ${glyphs.reduce((sum, glyph) => sum + glyph.glyphCount, 0)}`);
  for (const glyph of glyphs) {
    result.push(generateGlyphs(glyph));
  }
  result.push('ENDFONT');
  return result.join('\n');
}

const engFontFile = process.argv[2] ?? 'eng.fnt';
const hanFontFile = process.argv[3] ?? 'han.fnt';
const bdfFile= process.argv[4] ?? '6x2x1.bdf';
const fontName = process.argv[5] ?? path.parse(bdfFile).name;

fs.writeFileSync(bdfFile, generateFont({
  fontName,
  fontWidth: 8,
  fontHeight: 16,
  glyphs: [
    { fileName: engFontFile, glyphWidth: 8, glyphHeight: 16, glyphCount: 128, codeMapper: (index)=>CP437_TO_UNICODE[(index+16)%128].charCodeAt(0) },
    { fileName: hanFontFile, glyphWidth: 16, glyphHeight: 16, glyphCount: 184, codeMapper: (index)=>(PUA + index) },
  ],
}));
