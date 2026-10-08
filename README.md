# alexandercoabad.github.io

Developed by Alexander Co Abad with the help of Claude AI (Sonnet 5.5)

Personal site with browser simulators for my chip projects. Each simulator is one self-contained page, so nothing needs to be installed and it also works when opened locally.

| Page | Project |
| :--- | :--- |
| `index.html` | Landing page linking to all projects |
| `agila32/index.html` | AgilA32 simulator (RV32I CPU with RP2040-style PIO) |
| `mc14500b/index.html` | MC14500B simulator (1-bit SoC) |

## AgilA32 browser simulator

The chip's Verilog (RV32I CPU and the two-state-machine PIO) compiled to WebAssembly and run in the browser:
`agila32/index.html` (also kept at `docs/sim/index.html` and `sim/index.html`) is one self-contained page with the WebAssembly embedded.

Scenarios: a 7-segment display looping "AGILA32" (the default, source in `agila_7seg.S`), boot ROM demo, boot ROM without a QSPI Pmod, the PIO signature test, the PIO smoke test, and your own program over the GPIO bootloader.

Verification: the signature scenario reproduces all 20 golden `uo_out` values and the pad sequence of `test/test_pio_gl_sig.py`;
the smoke scenario passes the same checks as `test/test_pio_gl.py`.

Rebuild: `tools/build_wasm_sim.sh` (yosys CXXRTL, then `zig c++` to wasm32-wasi). `sim.cpp` is the wrapper (clock stepping, flash and PSRAM models, trace); `template.html` is the page source. Sources are also collected in `sources/agila32-simulator/`.

## MC14500B browser simulator

`mc14500b/index.html` is a hand-written JavaScript model of `tt_um_mc14500b_soc_extended` (the 1-bit MC14500B-style SoC): 16-opcode ISA, 64-byte program RAM, free-running 6-bit PC, 8 scratch bits, edge detector (address 8), clock divider (address 9), 8-bit output shift latch (address C) and the input taps (D/E/F). It follows `docs/ISA.md` of the MC14500B_IHP repository, including its single-execution-per-instruction timing under the clock divider. There is no WebAssembly step: the page is plain HTML and JavaScript with no build.

Examples (each one has an editable assembler listing, a chip clock menu and a program RAM view with the PC highlighted):

- Kill the Bit (Altair classic), with an external monitor that stops the chip clock like the RP2040 firmware does
- Traffic light (two-way plus pedestrian crossing)
- Elevator (3 floors, E-stop)
- Boolean gates on switches
- Button toggle (edge detector)
- 7-segment display: PILIPINASLASALLE in a loop (5 kHz default, blinking decimal point)
- 7-segment 0-9 counter
- Blink (clock divider)

Controls: BTN is `ui_in[0]` (hold, or press Space), and the checkboxes are `ui_in[5]`, `ui_in[6]` and `ui_in[7]`. The 7-segment programs were produced with a search for the shortest instruction chain per segment; the generator code is in the page source (`johnsonDisplay`, `fsrDisplay`).

Not verified against the Verilog in a simulator: the page was checked by running the examples and comparing their output sequences, not by co-simulation with `project.v`.

## Adding another project

Create a folder with its own `index.html`, add a section to the root `index.html`, and add a section here.
