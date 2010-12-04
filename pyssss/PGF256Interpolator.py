from GF256elt import GF256elt
from PGF256 import PGF256

class PGF256Interpolator:
  """Lagrange Polynomial Interpolator.
     see http://en.wikipedia.org/wiki/Lagrange_polynomial"""
  
  def interpolate(self,points):
    """Returns a PGF256 polynomial interpolating all GF256xGF256 tuples in points."""

    #
    # Check that all points have different X
    #
    
    for i in xrange(0,len(points)):
      if points[i][0] in map(lambda x: x[0],points[i+1:]):
        raise Exception("Duplicate point exception")
        
    #
    # Build the interpolating polynomial
    #
    # L(x) = sigma(j=0,j <= k,yj * Lj(x))
    # Where k = len(points) - 1
    # and Lj(x) = pi(i=0,i <= k and i != j, (x-xi)/(xj - xi))
    # Lj(xi) = kronecker_delta(i,j)
    # 
    
    result = PGF256([GF256elt(0)])
    
    for j in xrange(0,len(points)):
      result = result + (self.__Lj(points,j) * points[j][1])

    return result
              
  def __Lj(self,points,j):
    result = GF256elt(1)
    x = PGF256((GF256elt(0),GF256elt(1)))
    for i in xrange(0,len(points)):
      if j == i:
        continue
      
      # P = x
      P = x
      
      P = (P - points[i][0]) * (GF256elt(1) / (points[j][0] - points[i][0])) 

      result = P * result
                    
    return result
