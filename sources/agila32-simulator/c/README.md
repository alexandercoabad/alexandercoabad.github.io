# C programs for AgilA32 (RV32I)

Build (needs `pip install ziglang` plus `ld.lld` and `llvm-objcopy`/`llvm-objdump` from LLVM):

    ./build.sh examples/blink.c        # writes blink.elf / .bin / .hex / .lst
    STACK=1 ./build.sh prog.c          # adds start.S (sp=0xB4, stack 0xB0-0xB3)

The `.hex` file is the byte string for the GPIO bootloader (length byte is added by the sender).

Limits (from src/mem.v): code and data share the 44-byte window 0xB4-0xDF; 4 bytes of RAM at 0xB0-0xB3;
no multiply/divide (RV32I only), no libc, no interrupts. Keep programs register-only.
Examples were run on the RTL compiled to WebAssembly (simulator), not on silicon or FPGA.
