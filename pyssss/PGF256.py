#!/usr/bin/env python
#
#  Copyright 2010 Mathias Herberts
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from __future__ import absolute_import, division, print_function, unicode_literals

from GF256elt import GF256elt

class PGF256:
  """Class for representing polynomials whose coefficients are GF256elt."""
      
  def __init__(self,coeffs):
    # Polynomial coefficients, element i is the coefficient for x^i
    self.__coefficients = []

    for coeff in coeffs:
      if not isinstance(coeff, GF256elt):
        raise Exception()
      self.__coefficients.append(coeff)
          
  def __add__(self,other):
    if isinstance(other, GF256elt):
      c = self.coeffs()
      c[0] += other
      return PGF256(c)

    if not isinstance(other,PGF256):
      raise Exception()
    
    minDeg = min(self.deg(),other.deg())
    maxDeg = max(self.deg(),other.deg())
    
    coeffs = []
    
    for i in range(0,minDeg):
      coeffs.append(self.coeff(i) + other.coeff(i))
    
    for i in range(minDeg,maxDeg):
      if self.deg() > other.deg():
        coeffs.append(self.coeff(i))
      else:
        coeffs.append(other.coeff(i))
            
    return PGF256(coeffs)
  
  def __sub__(self,other):
    if isinstance(other, GF256elt):
      c = self.coeffs()
      c[0] -= other
      return PGF256(c)

    if not isinstance(other,PGF256):
      raise Exception()
            
    minDeg = min(self.deg(),other.deg())
    maxDeg = max(self.deg(),other.deg())
    
    coeffs = []
    
    for i in range(0,minDeg + 1):
      coeffs.append(self.coeff(i) - other.coeff(i))
    
    zero = GF256elt(0)
    
    for i in range(minDeg + 1,maxDeg + 1):
      if self.deg() > other.deg():
        coeffs.append(self.coeff(i))
      else:
        coeffs.append(zero - other.coeff(i))
            
    return PGF256(coeffs)
       
  def __mul__(self,other):
    if isinstance(other, GF256elt):
      c = self.coeffs()
      return PGF256(map(lambda x: x * other,c))

    if not isinstance(other,PGF256):
      raise Exception()

    rescoeffs = [GF256elt(0) for i in range(0,self.deg() + other.deg() + 1)]
    
    for i in range(0,self.deg() + 1):
      for j in range(0,other.deg() + 1):
        rescoeffs[i + j] += self.coeff(i) * other.coeff(j)
                    
    return PGF256(rescoeffs)
                  
  def coeff(self,i):
    "Return the coefficient for x^i."
    
    if i >= len(self.__coefficients):
      return GF256elt(0)
    else:
      return self.__coefficients[i]
      
  def coeffs(self):
    "Return a clone of the array of coefficients"
    
    c = []
    
    zero = GF256elt(0)
    
    for i in range(0,self.deg() + 1):
      c.append(self.coeff(i) + zero)
        
    return c
  
  def __repr__(self):
              
    for i in range(0,len(self.__coefficients)):
      if i == 0:
        p = str(self.coeff(i))        
      elif str(self.coeff(i)) != "0":
        p = str(self.coeff(i)) +"*x^"+str(i)+" + " + p
    
    return p
  
  def deg(self):
    "Return the degree of this polynomial."
    return len(self.__coefficients) - 1
      
  def f(self,x):
    "Compute f(x) where f is the current polynomial. We use Horner's scheme for faster result."

    if not isinstance(x, GF256elt):
      raise Exception()
    
    result = GF256elt(0)
    
    for i in range(1,len(self.__coefficients)+1):
      result = result * x
      result += self.__coefficients[len(self.__coefficients) - i]

    return result
