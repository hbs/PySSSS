#!/usr/bin/env python
#
#  Copyright 2021 Mathias Herberts
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

class GF256:
  """A class for representing GF256 (GF(2^8)) elements.
   Those elements are representations of polynomials over GF(2) with
   each bit being the coefficient of x^k for k an integer in [0,7].
   The log/exp tables are generated by generate_logexp_tables or generate_pplogexp_tables."""
       
  logtable = []
  exptable = []

  def __init__(self,generator,primePolynomial):
    self.__G = generator
    self.__PP = primePolynomial
      

    ## Generate logarithm and exponential tables for Gf(256) with a prime
    ## polynomial whose value is 'PP' and a generator value of 'G'."""

    GF = 256
    
    self.logtable = [0 for i in range(GF)]
    self.exptable = [0 for i in range(GF)]

    self.logtable[0] = (1 - GF) & 0xff
    self.exptable[0] = 1

    for i in range(1,GF):
      z = 0
      x = self.exptable[i - 1]
      y = self.__G

      while x > 0:
        if 0 != x & 0x1:
          z = z ^ y
        x = x >> 1
        y = y << 1
        if 0 != y & 0x100:
          y = y ^ self.__PP

      self.exptable[i] = z
      self.logtable[self.exptable[i]]= i % 255
      
  def dump_tables(self):
    print(self.exptable)
    print(self.logtable)

##
## Generate log/exp tables based on a prime polynomial
##
## Possible values of PP are 285 299 301 333 351 355 357 361 369 391 397 425 451 463 487 501
##
##

#
# For Rijndael compatibility (0x11b prime polynomial and 0x03 as generator)
#
RIJNDAEL = GF256(3,0x11b)
QR = GF256(2,0x11d)
