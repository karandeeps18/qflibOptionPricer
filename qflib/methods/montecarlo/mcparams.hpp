/**
@file  mcparams.hpp
@brief Monte Carlo parameters
*/

#ifndef QF_MCPARAMS_HPP
#define QF_MCPARAMS_HPP

#include <qflib/defines.hpp>
#include <qflib/exception.hpp>

BEGIN_NAMESPACE(qf)


/** Monte Carlo parameters
*/
struct McParams
{
  /** The known URNG types */
  enum class UrngType
  {
    MINSTDRAND,
    MT19937,
    RANLUX3,
    RANLUX4
  };

  /** The known path generator types */
  enum class PathGenType
  {
    EULER
  };


  /** Default ctor */
  McParams(UrngType u = UrngType::MT19937, PathGenType p = PathGenType::EULER);

  // state
  UrngType urngType;
  PathGenType pathGenType;
};

///////////////////////////////////////////////////////////////////////////////
// Inline definitions

inline
McParams::McParams(UrngType u, PathGenType p)
: urngType(u), pathGenType(p)
{}

END_NAMESPACE(qf)

#endif // QF_MCPARAMS_HPP
