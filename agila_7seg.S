# AGILA32 on the 7-segment display (uo_out[6:0] = segments a-g, uo7 = dp)
# 11 words = 44 bytes = the whole program RAM, sent over the GPIO bootloader.
auipc x4, 0         # x4 = address of this program
lbu   x6, 36(x4)    # next pattern from the table below
beq   x6, x0, -8    # 0 = end of table: start again
sb    x6, 0xF0(x0)  # LED_OUT (uo_out) = pattern
lui   x3, 4         # delay: 4 x 4096 loop passes
addi  x3, x3, -1
bne   x3, x0, -4
addi  x4, x4, 1     # next character
jal   x0, -28
.byte 77 3D 30 38 77 4F 5B 00   # A G I L A 3 2 end
