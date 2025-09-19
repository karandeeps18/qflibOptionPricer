# FX Vanilla Option Pricing (Garman–Kohlhagen)

This repository extends **qflib** with a full Garman–Kohlhagen (FX Black–Scholes) implementation.  
It includes:
- A C++ pricer returning price and spot Greeks.
- A pybind11 bridge for Python.
- Unit tests enforcing parity.
- A Plotly Dash dashboard for quick exploration.

---

## 1. Features

### C++ Core (`qflib/pricers/simplepricers.cpp`)
- `fxOptionGarmanKohlhagen(payoffType, spot, strike, timeToExp, rd, rf, vol)`  
  Returns `[price, delta, gamma, vega]`.
- Reuses `europeanOptionBS`, treating:
  - Domestic rate (`rd`) as the discount curve.
  - Foreign rate (`rf`) as a continuous dividend yield.

**Model:**

\[
d1 = \frac{\ln(S/K) + (r_d - r_f + 0.5 \sigma^2) T}{\sigma \sqrt{T}}, \quad
d2 = d1 - \sigma \sqrt{T}
\]

\[
C = e^{-r_f T} S N(d1) - e^{-r_d T} K N(d2), \quad
P = e^{-r_d T} K N(-d2) - e^{-r_f T} S N(-d1)
\]

**Greeks (domestic numéraire):**
- Delta: `± e^{-r_f T} N(±d1)`
- Gamma: `e^{-r_f T} n(d1) / (S σ √T)`
- Vega:  `e^{-r_f T} S n(d1) √T`

---

### Python Binding (`pyqflib/fx_module.cpp`)
- Exposes `fx_vanilla_price(...)` with pybind11.
- Validates inputs, maps qflib exceptions to Python `ValueError`.

### Python API (`pyqflib/qflib/__init__.py`)
- Adds a wrapper so users call `qflib.fx_vanilla_price(...)`.
- Returns a dict: `{price, delta, gamma, vega}`.

### Unit Tests (`pyqflib/tests/test_fx_vanilla.py`)
- Confirms Python and C++ outputs match for calls and puts.
- Enforces:
  - Call–put parity: `C - P = e^{-r_f T} S - e^{-r_d T} K`
  - Delta symmetry: `Δ_call - Δ_put = e^{-r_f T}`
  - Gamma equality: `Γ_call = Γ_put`
  - Vega equality: `Vega_call = Vega_put`

### Plotly Dash Demo (`examples/Python/fx_vanilla_dash.py`)
- Interactive inputs for spot, strike, tenor, rates, vol, and type.
- Displays metrics and strike-slice chart (call vs put).

---

## 2. Build Instructions

### Prerequisites
- Visual Studio Build Tools 2022 (CMake, MSVC, Ninja).
- Conda env `qfgb` with Python 3.12, NumPy, pybind11.

### Configure & Build

cmake -S . -B build -G Ninja
cmake --build build
