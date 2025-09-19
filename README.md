# FX Vanilla Option Pricing (Garman–Kohlhagen)

This repository extends `qflib` with a full Garman–Kohlhagen (FX Black–Scholes) implementation. It includes a C++ pricer that returns price and spot Greeks, a pybind11 bridge for Python, unit tests enforcing parity, and a mini Plotly Dash dashboard for quick exploration.

---

## 1. What’s Implemented

### C++ Core (`qflib/pricers/simplepricers.cpp`)
- `fxOptionGarmanKohlhagen(payoffType, spot, strike, timeToExp, rd, rf, vol)`  
  Returns a 4-vector: `[price, delta, gamma, vega]`.
- Reuses `europeanOptionBS` with domestic rate as the discount curve and foreign rate as the “dividend” yield.

Model summary (spot FX `S` quoted in domestic per unit foreign):

\[
\begin{aligned}
d1 &= \frac{\ln(S/K) + (r_d - r_f + 0.5 \sigma^2) T}{\sigma \sqrt{T}} \\
d2 &= d1 - \sigma \sqrt{T} \\
C &= e^{-r_f T} S N(d1) - e^{-r_d T} K N(d2) \\
P &= e^{-r_d T} K N(-d2) - e^{-r_f T} S N(-d1)
\end{aligned}
\]

Greeks match the domestic numéraire convention:
- `delta = ± e^{-r_f T} N(±d1)`
- `gamma = e^{-r_f T} n(d1) / (S σ √T)`
- `vega = e^{-r_f T} S n(d1) √T`

### Python Binding (`pyqflib/fx_module.cpp`)
- Exposes `fx_vanilla_price(spot, strike, time_to_expiry, domestic_rate, foreign_rate, volatility, option_type)` using pybind11.
- Validates inputs and maps qflib exceptions to Python `ValueError`.

### Python API (`pyqflib/qflib/__init__.py`)
- Adds a convenience wrapper so users call `qflib.fx_vanilla_price(...)` and receive a dict with `price`, `delta`, `gamma`, `vega`.

### Unit Tests (`pyqflib/tests/test_fx_vanilla.py`)
- Confirms Python output matches the underlying C++ vector for both calls and puts.
- Enforces call-put parity and Greek symmetry:
  - `C - P = e^{-r_f T} S - e^{-r_d T} K`
  - `Δ_call - Δ_put = e^{-r_f T}`
  - `Γ_call = Γ_put`
  - `Vega_call = Vega_put`

### Plotly Dash Demo (`examples/Python/fx_vanilla_dash.py`)
- Interactive inputs for spot, strike, tenor, rates, vol, and option type.
- Displays a metric table and strike-slice chart (call vs put).

---

## 2. How to Build

### Prereqs
- Visual Studio Build Tools 2022 (CMake, MSVC, Ninja support).
- Conda environment `qfgb` with Python 3.12, NumPy, pybind11.

### Configure & Build (from repo root)
# optional: ensure VC vars are set
"& 'C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat'"

cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build
Artifacts:

lib\qflib*.lib – static library.
pyqflib\qflib\pyqflib*.pyd
pyqflib\qflib\pyqflib_fx*.pyd
3. Unit Tests
Activate the qfgb environment and run:

powershell

conda activate qfgb
pytest pyqflib/tests/test_fx_vanilla.py
4. Python Usage
python

from qflib.qflib import fx_vanilla_price

result = fx_vanilla_price(
    spot=1.12,
    strike=1.10,
    timetoexp=0.75,
    domestic_rate=0.03,
    foreign_rate=0.01,
    volatility=0.18,
    option_type="call",   # or "put"
)

print(result)
# {'price': ..., 'delta': ..., 'gamma': ..., 'vega': ...}
5. Dash Dashboard
powershell

conda activate qfgb
python examples/Python/fx_vanilla_dash.py
Open the URL printed in the console to interact with price and surface charts.

6. Implementation Notes
Domestic rate (rd) is the discounting curve; foreign rate (rf) acts as a continuous dividend yield.
Greeks are spot-based (domestic currency).
Numerical stability: relies on the existing qflib europeanOptionBS, which handles zero time-to-expiry or volatility via internal guards.
pybind11 binding catches qf::Exception and rethrows as Python ValueError.
Tests use high tolerance (1e-9) to flag any regression in pricing or parity.
7. Next Steps / Ideas
Extend Greeks to include theta/rho if needed.
Add batch pricing helpers for vectorized strikes/tenors.
Integrate market data loaders for automated surface generation.
Expand Dash app with volatility smiles or sensitivity sliders.
