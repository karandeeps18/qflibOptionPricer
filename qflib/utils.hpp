/**
@file  utls.hpp
@brief Utilities for quantity conversions, string processing, etc.
*/

#ifndef QF_UTILS_HPP
#define QF_UTILS_HPP

#include <qflib/defines.hpp>
#include <qflib/exception.hpp>
#include <string>
#include <algorithm>
#include <cmath>

BEGIN_NAMESPACE(qf)

inline
double toContCmpd(double rate, size_t annfreq)
{
  QF_ASSERT(annfreq >= 1.0, "compounding frequency less than 1 not allowed");
  double tmp = std::pow(1.0 + rate / annfreq, annfreq);
  return std::log(tmp);
}

inline
double fromContCmpd(double rate, size_t annfreq)
{
  QF_ASSERT(annfreq >= 1.0, "compounding frequency less than 1 not allowed");
  double tmp = std::exp(rate/annfreq);
  return (tmp - 1.0)*annfreq;
}

END_NAMESPACE(qf)

#endif // QF_UTILS_HPP
