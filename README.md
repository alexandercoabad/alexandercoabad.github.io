# AgilA32 browser simulator

The chip's Verilog (RV32I CPU and the two-state-machine PIO) compiled to WebAssembly and run in the browser:
`docs/sim/index.html` is one self-contained page (WebAssembly embedded, no server needed). Open it from GitHub Pages or locally.

Scenarios: boot ROM demo, boot ROM without a QSPI Pmod, the PIO signature test, the PIO smoke test, and your own program over the GPIO bootloader.

Verification: the signature scenario reproduces all 20 golden `uo_out` values and the pad sequence of `test/test_pio_gl_sig.py`;
the smoke scenario passes the same checks as `test/test_pio_gl.py`.

Rebuild: `tools/build_wasm_sim.sh` (yosys CXXRTL, then `zig c++` to wasm32-wasi). `sim/sim.cpp` is the wrapper (clock stepping, flash and PSRAM models, trace); `sim/template.html` is the page source.
