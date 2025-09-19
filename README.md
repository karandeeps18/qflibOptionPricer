# FX Vanilla Option Pricing (Garman–Kohlhagen)

This repository extends **qflib** with a full Garman–Kohlhagen (FX Black–Scholes) implementation.

It includes:

* A C++ pricer returning price and spot Greeks.
* A pybind11 bridge for Python.
* Unit tests enforcing parity.
* A Plotly Dash dashboard for quick exploration.

---

## 1. Features

### C++ Core (`qflib/pricers/simplepricers.cpp`)

* `fxOptionGarmanKohlhagen(payoffType, spot, strike, timeToExp, rd, rf, vol)`
  Returns `[price, delta, gamma, vega]`.
* Reuses `europeanOptionBS`, treating:

  * Domestic rate (`rd`) as the discount curve.
  * Foreign rate (`rf`) as a continuous dividend yield.

**Model:**

$$
\begin{aligned}
 d_1 &= \frac{\ln(S/K) + (r_d - r_f + 0.5\,\sigma^2)\,T}{\sigma\sqrt{T}}, \\
 d_2 &= d_1 - \sigma\sqrt{T}
\end{aligned}
$$

**Prices:**

$$
\begin{aligned}
 C &= e^{-r_f T}\,S\,N(d_1) - e^{-r_d T}\,K\,N(d_2), \\
 P &= e^{-r_d T}\,K\,N(-d_2) - e^{-r_f T}\,S\,N(-d_1)
\end{aligned}
$$

**Greeks (domestic numéraire):**

* Delta:
  $\Delta_{\text{call}} = e^{-r_f T} N(d_1), \qquad \Delta_{\text{put}} = -e^{-r_f T} N(-d_1)$
* Gamma:
  $\Gamma = \frac{e^{-r_f T}\, n(d_1)}{S\,\sigma\sqrt{T}}$
* Vega:
  $\mathcal{V} = e^{-r_f T}\, S\, n(d_1)\,\sqrt{T}$

Here, \$N(\cdot)\$ and \$n(\cdot)\$ are the standard normal CDF and PDF.

---

### Python Binding (`pyqflib/fx_module.cpp`)

* Exposes `fx_vanilla_price(...)` with pybind11.
* Validates inputs and maps qflib exceptions to Python `ValueError`.

### Python API (`pyqflib/qflib/__init__.py`)

* Adds a wrapper so users call `qflib.fx_vanilla_price(...)`.
* Returns a dict: `{price, delta, gamma, vega}`.

### Unit Tests (`pyqflib/tests/test_fx_vanilla.py`)

Confirms Python and C++ outputs match for calls and puts. Enforces:

* Call–put parity:
  $C - P = e^{-r_f T} S - e^{-r_d T} K$
* Delta symmetry:
  $\Delta_{\text{call}} - \Delta_{\text{put}} = e^{-r_f T}$
* Gamma equality:
  $\Gamma_{\text{call}} = \Gamma_{\text{put}}$
* Vega equality:
  $\mathcal{V}_{\text{call}} = \mathcal{V}_{\text{put}}$

### Plotly Dash Demo (`examples/Python/fx_vanilla_dash.py`)

* Interactive inputs for spot, strike, tenor, rates, vol, and type.
* Displays metrics and strike-slice chart (call vs put).

---

## 2. Build Instructions

### Prerequisites

* Visual Studio Build Tools 2022 (CMake, MSVC, Ninja).
* Conda env `qfgb` with Python 3.12, NumPy, pybind11.

### Configure & Build

```bash
cmake -S . -B build -G Ninja
cmake --build build
```

---

## 3. Unit Test

```bash
conda activate qfgb
pytest pyqflib/tests/test_fx_vanilla.py
```

---

## 4. Python Usage

```python
from qflib.qflib import fx_vanilla_price

result = fx_vanilla_price(
    spot=1.12,
    strike=1.10,
    timetoexp=0.75,
    domestic_rate=0.03,
    foreign_rate=0.01,
    volatility=0.18,
    option_type="call",  # or "put"
)

print(result)
# {'price': ..., 'delta': ..., 'gamma': ..., 'vega': ...}
```

---

## 5. Implementation Notes

* Domestic rate = discounting curve.
* Foreign rate = continuous dividend yield.
* Greeks are spot-based (domestic currency).
* Numerical stability: relies on `europeanOptionBS` guards.
* Tests use tolerance `1e-9` to flag regressions.
