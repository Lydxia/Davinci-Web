import re, base64
html=open('index.html',encoding='utf-8').read()
three=open('three.global.js',encoding='utf-8').read()
m=re.search(r'<script type="module">(.*?)</script>',html,flags=re.S)
app=m.group(1).replace("import * as THREE from 'three';","")
three_script="<script>\n"+three+"\n</script>\n"
app_wrapped="<script>\n(function(){\n'use strict';\n"+app+"\n})();\n</script>"
html=html[:m.start()]+three_script+app_wrapped+html[m.end():]
# inline assets
for fn,mime,key in [('assets/robot.png','image/png','robot'),('assets/logo.png','image/png','logo'),('assets/tunnel.jpg','image/jpeg','tunnel'),('assets/grain.jpg','image/jpeg','grain'),('assets/park.jpg','image/jpeg','park'),('assets/semicon.jpg','image/jpeg','semicon'),('assets/culvert.jpg','image/jpeg','culvert'),('assets/power.jpg','image/jpeg','power'),('assets/datacenter.jpg','image/jpeg','datacenter'),('assets/factory.jpg','image/jpeg','factory'),
    ('assets/m20.jpg','image/jpeg','m20'),('assets/s10.jpg','image/jpeg','s10'),('assets/x30.jpg','image/jpeg','x30'),
    ('assets/mod-bispec.png','image/png','modb'),('assets/mod-gas.png','image/png','modg'),('assets/mod-pano.png','image/png','modp'),
    ('assets/mod-5g.png','image/png','mod5'),('assets/mod-alarm.png','image/png','moda'),('assets/mod-lidar.png','image/png','modl'),
    ('assets/mod-ctrl.jpg','image/jpeg','modc'),
    ('assets/ai-gauge.jpg','image/jpeg','aig'),('assets/ai-digital.jpg','image/jpeg','aid'),('assets/ai-status.jpg','image/jpeg','ais'),
    ('assets/ai-thermal.jpg','image/jpeg','ait'),('assets/ai-vib.jpg','image/jpeg','aiv'),('assets/ai-asset.jpg','image/jpeg','aia'),
    ('assets/ai-gas.jpg','image/jpeg','aigs'),('assets/ai-fire.jpg','image/jpeg','aif'),('assets/ai-water.jpg','image/jpeg','aiw'),
    ('assets/ai-chem.jpg','image/jpeg','aic'),('assets/ai-sec.jpg','image/jpeg','aisec'),('assets/ai-face.jpg','image/jpeg','aifc'),
    ('assets/ai-exit.jpg','image/jpeg','aie'),('assets/ai-park.jpg','image/jpeg','aip'),
    ('assets/plat-live.jpg','image/jpeg','pll'),('assets/plat-risk.jpg','image/jpeg','plr')]:
    b=base64.b64encode(open(fn,'rb').read()).decode()
    html=html.replace(f'src="{fn}"',f'src="data:{mime};base64,{b}"')
    html=html.replace(f'poster="{fn}"',f'poster="data:{mime};base64,{b}"')
    html=html.replace(f"'{fn}'",f"'data:{mime};base64,{b}'")
html=html.replace('<!--__INLINE__-->','')
# inline subsetted fonts
for ph,fb in [('__FONT900__','font-900.b64'),('__FONT700__','font-700.b64')]:
    b=open(fb,encoding='utf-8').read().strip()
    html=html.replace(ph,f'data:font/woff2;base64,{b}')
open('davinci-v3-preview.html','w',encoding='utf-8',newline='').write(html)
print("built",round(len(html)/1024/1024,2),"MB")
