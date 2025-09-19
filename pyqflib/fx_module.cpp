#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <algorithm>
#include <cctype>
#include <string>
#include <stdexcept>

#include <qflib/pricers/simplepricers.hpp>
#include <qflib/exception.hpp>

namespace py = pybind11;

namespace {
int parse_payoff_type(const std::string& option_type)
{
  std::transform(option_type.begin(), option_type.end(), normalized.begin(), [](unsigned char c) { return static_cast<char>(std::tolower(c)); });
  if (normalized == "call")
    return 1;
  if (normalized == "put")
    return -1;
  throw std::invalid_argument("option_type must be either call or put");
}
}

py::dict fx_vanilla_price(double spot, double strike, double time_to_expiry,
                            double domestic_rate, double foreign_rate, double volatility,
                            const std::string& option_type)
{
  if (spot < 0.0)
    throw std::invalid_argument("spot must be non-negative");
  if (strike < 0.0)
    throw std::invalid_argument("strike must be non-negative");
  if (time_to_expiry < 0.0)
    throw std::invalid_argument("time_to_expiry must be non-negative");
  if (volatility < 0.0)
    throw std::invalid_argument("volatility must be non-negative");

  int payoff = parse_payoff_type(option_type);

  try {
    qf::Vector qr = qf::fxOptionGarmanKohlhagen(payoff, spot, strike, time_to_expiry, domestic_rate, foreign_rate, volatility);
    py::dict result;
    result["price"] = qr[0];
    result["delta"] = qr[1];
    result["gamma"] = qr[2];
    result["vega"] = qr[3];
    return result;
  } catch (const qf::Exception& ex) {
    throw py::value_error(ex.what());
  }
}

PYBIND11_MODULE(pyqflib_fx, m)
{
  m.doc() = "pybind11 bindings for qflib FX vanilla option pricing";
  m.def("fx_vanilla_price", &fx_vanilla_price,
        py::arg("spot"),
        py::arg("strike"),
        py::arg("time_to_expiry"),
        py::arg("domestic_rate"),
        py::arg("foreign_rate"),
        py::arg("volatility"),
        py::arg("option_type"),
        "Compute Garman-Kohlhagen price and spot Greeks for an FX vanilla option.");
}
