import gzip,base64,json
S='/tmp/claude-0/-home-claude/ad649545-d980-5aaf-8ec3-478ea72c4e84/scratchpad/'
R='/home/claude/w32/AgilA32_PIO-main/test/'
w=open(S+'sim/agila.wasm','rb').read(); b64=base64.b64encode(gzip.compress(w,9)).decode()
rd=lambda f:" ".join(open(R+f).read().split())
data={"sig":rd('pio_gl_sig_flash_image.hex'),"smoke":rd('pio_gl_smoke_flash_image.hex'),"stub":[int(x,16) for x in open(R+'flash_handoff_stub.hex').read().split()],"led":open(S+'sim/led_counter.hex').read().strip(),
      "agila":open('agila_7seg.hex').read().strip(),"agilaAsm":open('agila_7seg.S').read().split("\n",2)[2].strip()}
t=open('template.html').read().replace('%%WASM%%',b64).replace('%%DATA%%',json.dumps(data))
open('index.html','w').write(t); print(len(t))
