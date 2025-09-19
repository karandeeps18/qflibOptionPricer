import math

import pytest

from qflib.qflib import fx_vanilla_price
import qflib.pyqflib as core


@pytest.mark.parametrize('option_type,payoff', [('call', 1), ('put', -1)])
def test_fx_vanilla_matches_euro_bs(option_type, payoff):
    spot = 1.25
    strike = 1.20
    time_to_expiry = 0.75
    domestic_rate = 0.03
    foreign_rate = 0.01
    volatility = 0.20

    result = fx_vanilla_price(spot, strike, time_to_expiry, domestic_rate, foreign_rate, volatility, option_type)
    baseline = core.euroBS(payoff, spot, strike, time_to_expiry, domestic_rate, foreign_rate, volatility)

    assert result['price'] == pytest.approx(baseline[0], rel=1e-9, abs=1e-9)
    assert result['delta'] == pytest.approx(baseline[1], rel=1e-9, abs=1e-9)
    assert result['gamma'] == pytest.approx(baseline[2], rel=1e-9, abs=1e-9)
    assert result['vega'] == pytest.approx(baseline[4], rel=1e-9, abs=1e-9)


def test_fx_call_put_parity():
    spot = 0.92
    strike = 0.95
    time_to_expiry = 1.5
    domestic_rate = 0.025
    foreign_rate = 0.012
    volatility = 0.18

    call = fx_vanilla_price(spot, strike, time_to_expiry, domestic_rate, foreign_rate, volatility, 'call')
    put = fx_vanilla_price(spot, strike, time_to_expiry, domestic_rate, foreign_rate, volatility, 'put')

    forward_discount = math.exp(-foreign_rate * time_to_expiry)
    strike_discount = math.exp(-domestic_rate * time_to_expiry)

    expected_price_gap = forward_discount * spot - strike_discount * strike

    assert call['price'] - put['price'] == pytest.approx(expected_price_gap, rel=1e-9, abs=1e-9)
    assert call['delta'] - put['delta'] == pytest.approx(forward_discount, rel=1e-9, abs=1e-9)
    assert call['gamma'] == pytest.approx(put['gamma'], rel=1e-9, abs=1e-9)
    assert call['vega'] == pytest.approx(put['vega'], rel=1e-9, abs=1e-9)
