#!/bin/sh
# Build the browser simulator: yosys -> CXXRTL C++ -> WebAssembly (zig c++) -> embedded in docs/sim/index.html
# Needs: pip install yowasp-yosys ziglang      (no emscripten required)
set -e
SRC=../src
CXXRTL=$(python3 -c "import yowasp_yosys,os;print(os.path.join(os.path.dirname(yowasp_yosys.__file__),'share/include/backends/cxxrtl/runtime'))")
cd "$(dirname "$0")/../sim"
yowasp-yosys -q -p "read_verilog -sv -DSYNTHESIS -I $SRC $SRC/tt_um_agila32.v $SRC/rv32i_core.v $SRC/mem.v $SRC/qspi_shared_engine.v $SRC/pio.v $SRC/pio_sm.v $SRC/pio_fifo.v; hierarchy -top tt_um_agila32; proc; flatten; opt -fast; write_cxxrtl -header agila.cc"
python3 -m ziglang c++ -target wasm32-wasi -mexec-model=reactor -O2 -std=c++17 -fno-exceptions -I "$CXXRTL" -Wno-nullability-completeness sim.cpp agila.cc -o agila.wasm
echo "agila.wasm built; run build.py (paths inside) to embed it in the page"
