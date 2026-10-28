# alexandercoabad.github.io

Developed by Alexander Co Abad with the help of Claude AI (Sonnet 5.5).

Personal site with browser simulators for my chip projects. Each simulator is one self-contained page, so nothing needs to be installed and it also works when opened locally.

| Page | Project |
| :--- | :--- |
| `index.html` | Landing page linking to all projects |
| `agila32/index.html` | AgilA32 simulator (RV32I CPU with RP2040-style PIO) |
| `mc14500b/index.html` | MC14500B simulator (1-bit SoC) |
| `reram/index.html` | ReRAM crossbar compute-in-memory simulator |

## AgilA32 browser simulator

The chip's Verilog (RV32I CPU and the two-state-machine PIO) compiled to WebAssembly and runs in the browser:
`agila32/index.html` (also available at `docs/sim/index.html` and `sim/index.html`) is a self-contained page with WebAssembly embedded.

Scenarios: a 7-segment display spelling "PILIPINAS AGILA32" (the default, source in `pilipinas_agila.S`, 7 instructions plus a 16-byte table), the same program with "PILIPINAS LASALLE" (`pilipinas.S`), a 7-segment display looping "AGILA32" (`agila_7seg.S`), boot ROM demo, boot ROM without a QSPI Pmod, the PIO signature test, the PIO smoke test, and your own program over the GPIO bootloader.

Verification: the signature scenario reproduces all 20 golden `uo_out` values and the pad sequence of `test/test_pio_gl_sig.py`;
the smoke scenario passes the same checks as `test/test_pio_gl.py`.

Note: the PIO block is an independent implementation of the RP2040 PIO instruction set, not affiliated with or endorsed by Raspberry Pi Ltd; Raspberry Pi, RP2040 and Pico are Raspberry Pi's trademarks. The Pico SDK programs used by the AgilA32 repository are listed in its `NOTICE.md`.

Rebuild: `tools/build_wasm_sim.sh` (yosys CXXRTL, then `zig c++` to wasm32-wasi). `sim.cpp` is the wrapper (clock stepping, flash and PSRAM models, trace); `template.html` is the page source. Sources are also collected in `sources/agila32-simulator/`.

## MC14500B browser simulator

`mc14500b/index.html` is a hand-written JavaScript model of `tt_um_mc14500b_soc_extended` (the 1-bit MC14500B-style SoC): 16-opcode ISA, 64-byte program RAM, free-running 6-bit PC, 8 scratch bits, edge detector (address 8), clock divider (address 9), 8-bit output shift latch (address C), and the input taps (D/E/F). It follows `docs/ISA.md` of the MC14500B_IHP repository, including its single-execution-per-instruction timing under the clock divider. There is no WebAssembly step: the page is plain HTML and JavaScript with no build.

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

## ReRAM crossbar simulator

`reram/index.html` is a generic, textbook model of analog ReRAM compute-in-memory. It is plain HTML and JavaScript with no build. Weights are stored as differential conductance pairs (G+ and G-) in a passive crossbar, inputs are applied as word-line voltages, and each bit line sums its cell currents (Ohm's law per cell, Kirchhoff's current law per column). The pair is subtracted and digitized by an ADC, then compared with the ideal floating-point product.

Controls: array size (2 to 6 rows and columns), input vector, weight matrix, DAC, weight-level and ADC bit depths, ADC range, read voltage, Gmin and Gmax, Gaussian device variation and wire resistance. Wire resistance is solved as a full resistive network (Gauss-Seidel), so IR drop appears in the outputs. A five-step walkthrough (program, drive rows, Ohm's law, sum columns, digitize) animates the crossbar, and one output column can be traced cell by cell.

The write panel models how the weights get into the array. A controller block-erases the cells to the high-resistance state, then writes each one with SET and RESET pulses. In the default program-and-verify mode (incremental step pulse programming) it reads the cell back after every pulse, raises the amplitude by a fixed step while it undershoots, and restarts from the low amplitude when a pulse overshoots. An open-loop mode replays a pulse train calibrated on a nominal device with no read-back, and an ideal mode skips programming. The page draws the write circuitry (pulse generator and DAC, row decoder, bit-line drivers with a current limit, sense amplifier and ADC, comparator, state machine), the loop as a flowchart, the voltage waveform and conductance trajectory of any chosen cell, a per-cell pulse-count map, and the total write time and energy. The conductances produced by the writes are the ones the crossbar then computes with. The cell response (an exponential approach to Gmax and Gmin with per-device strength and pulse-to-pulse noise) and the write energies are illustrative, not fitted to a real device.

The efficiency panel compares the crossbar with a digital multiply-accumulate (MAC) processor for latency and energy at the current size, at 256 x 256, and across array sizes from 4 x 4 to 512 x 512. Array energy comes from the simulated currents (V x I x read pulse). The digital MAC energy, memory fetch energy, DAC and ADC energies and timings are illustrative ballpark values that you can edit, not measurements of any chip. Programming is included as a one-time cost spread over a reuse count you choose, with an energy break-even point. The model leaves out sneak paths, routing and digital post-processing, so small arrays can favor digital.

This is a teaching model, not a novel architecture and not a model of a specific chip. It has not been compared against measured ReRAM hardware or a circuit simulator such as SPICE.

## Adding another project

Create a folder with its own `index.html`, add a section to the root `index.html`, and add a section here.
