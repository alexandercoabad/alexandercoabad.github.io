import gzip,base64,json
S='/tmp/claude-0/-home-claude/ad649545-d980-5aaf-8ec3-478ea72c4e84/scratchpad/'
R='/home/claude/w32/AgilA32_PIO-main/test/'
w=open(S+'sim/agila.wasm','rb').read(); b64=base64.b64encode(gzip.compress(w,9)).decode()
rd=lambda f:" ".join(open(R+f).read().split())
data={"sig":rd('pio_gl_sig_flash_image.hex'),"smoke":rd('pio_gl_smoke_flash_image.hex'),"stub":[int(x,16) for x in open(R+'flash_handoff_stub.hex').read().split()],"led":open(S+'sim/led_counter.hex').read().strip(),
      "agila":open('agila_7seg.hex').read().strip(),"agilaAsm":open('agila_7seg.S').read().split("\n",2)[2].strip(),
      "pa":open('pilipinas_agila.hex').read().strip(),"paAsm":"\n".join(l for l in open('pilipinas_agila.S').read().split("\n") if not l.strip().startswith((".section",".globl"))).strip(),
      "pili":open('pilipinas.hex').read().strip(),"piliAsm":"\n".join(l for l in open('pilipinas.S').read().split("\n") if not l.strip().startswith((".section",".globl"))).strip()}
import re
C={}
titles={'blink':'blink: LED0 on and off','counter':'counter: 8-bit binary count','chase':'chase: one LED walks across','switches':'switches: LEDs copy the input switches'}
for n in ['blink','counter','chase','switches']:
    d='c/examples/'+n
    src=open(d+'.c').read().rstrip()
    if 'SLOW' in src: src+='\n/* This page builds with SLOW=13 so steps are visible at simulator speed. */'
    asm=[[int(m.group(1),16),m.group(2).strip().replace('\t',' ')] for m in (re.match(r'\s*([0-9a-f]+):\s*(.*)',l) for l in open(d+'.lst')) if m]
    C[n]={'title':titles[n],'src':src,'hex':open(d+'.hex').read().strip(),'asm':asm}
data['c']=C
t=open('template.html').read().replace('%%WASM%%',b64).replace('%%DATA%%',json.dumps(data))
open('index.html','w').write(t); print(len(t))
