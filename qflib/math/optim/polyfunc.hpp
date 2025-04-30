/**
@file   polyfunc.hpp
@brief  Definition of a Polynomial functor class
*/

#ifndef QF_POLYFUNC_HPP
#define QF_POLYFUNC_HPP

#include <qflib/defines.hpp>
#include <qflib/exception.hpp>
#include <qflib/math/matrix.hpp>

BEGIN_NAMESPACE(qf)

class Polynomial
{
public:
  Polynomial(qf::Vector const& coeffs) : coeffs_(coeffs) 
  {
    QF_ASSERT(coeffs_.size() > 0, "Polynomial: empty vector of coefficients not allowed!")
  }

  double operator()(double x) 
  {
    double val = coeffs_[0];
    for (size_t i = 1; i < coeffs_.size(); ++i) {
      val += coeffs_[i] * std::pow(x, i);
    }
    return val;
  }

private:
  qf::Vector coeffs_;
};

END_NAMESPACE(qf)

#endif // QF_POLYFUNC_HPP
