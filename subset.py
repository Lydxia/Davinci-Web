import re, base64, io
from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

html = open('index.html', encoding='utf-8').read()
# CJK ideographs + full-width punctuation actually used on the page
chars = sorted(set(re.findall(r'[一-鿿，。、；：！？（）「」《》]', html)))
open('chars.txt', 'w', encoding='utf-8').write(''.join(chars))
print('CJK chars in page:', len(chars))

def subset(src, out_b64):
    opts = Options()
    opts.flavor = 'woff2'
    opts.layout_features = []
    opts.hinting = False
    opts.desubroutinize = True
    opts.notdef_outline = True
    opts.recalc_bounds = True
    font = TTFont(src)
    ss = Subsetter(options=opts)
    ss.populate(text=''.join(chars))
    ss.subset(font)
    buf = io.BytesIO()
    font.save(buf)
    data = buf.getvalue()
    b64 = base64.b64encode(data).decode()
    open(out_b64, 'w', encoding='utf-8').write(b64)
    cmap = len(font.getBestCmap())
    print(f'{out_b64}: {len(data)//1024} KB woff2, cmap glyphs={cmap}')
    return cmap

c9 = subset('fonts-full/noto-sans-sc-chinese-simplified-900-normal.woff2', 'font-900.b64')
c7 = subset('fonts-full/noto-sans-sc-chinese-simplified-700-normal.woff2', 'font-700.b64')
assert c9 >= len(chars) and c7 >= len(chars), 'coverage mismatch!'
print('OK: coverage >= page chars for both weights')
