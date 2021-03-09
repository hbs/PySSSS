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
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import random
import binascii

from GF256elt import GF256elt
from PGF256 import PGF256
from PGF256Interpolator import PGF256Interpolator

def pickRandomPolynomial(degree,zero):
  """Pick a random PGF256 polynomial P such that P(0) = zero"""
   
  coeffs = []
  
  # Set f(0)
  coeffs.append(zero)
  
  # Pick coefficients for x^n with n < degree
  
  for c in range(1,degree):
    coeffs.append(GF256elt(random.randint(0,255)))
          
  # Pick non null coefficient for x^degree
  
  coeffs.append(GF256elt(random.randint(1,255)))
  
  return PGF256(coeffs)


def encodeByte(byte,n,k):
  # Allocate array to track duplicates
  picked = [False for i in range(0,256)]
  
  # Pick a random polynomial
  P = pickRandomPolynomial(k-1,GF256elt(byte))
  
  # Generate the keys
  keys = [bytearray() for i in range(0,n)]
  
  for i in range(0,n):

    #        
    # Pick a not yet picked X value in [0,255],
    # we need a value in [1,255] but to have a credible entropy for bytes we pick it in [0,255]
    # and simply output garbage if we picked 0
    # If we do not do that then the output keys will NEVER have 00 in even positions (starting at 0) which would be a little suspicious for some random data
    #
        
    pick = random.randint(1,255)
            
    while picked[pick] or pick == 0:
      # 0 values will be discarded but output it anyway with trailing garbage
      if pick == 0:
        keys[i].append(0)
        keys[i].append(random.randint(0,255))
          
      pick = random.randint(1,255)
    
    # Keep track of the value we just picked    
    picked[pick] = True
    
    X = GF256elt(pick)
    Y = P.f(X)
    
    keys[i].append(int(X))
    keys[i].append(int(Y))

  return keys

def encode(data,outputs,k):
      
  n = len(outputs)

  # Loop through the chars        
  while True:
    char = data.read(1)
    if 0 == len(char):
      break
    byte = ord(char)
    
    charkeys = encodeByte(byte,n,k)

    for i in range(0,n):
      outputs[i].write(charkeys[i])

def decode(keys,output):
  
  interpolator = PGF256Interpolator()
  zero = GF256elt(0)
  
  data = ""
  

  # End Of Key    
  eok = False

  while not eok:
    points = []
    for i in range(0,len(keys)):
      while True:
        b = keys[i].read(1)
        if 0 == len(b):
          eok = True
          break
        # Skip points with X value of 0, they were added to respect the entropy of the output
        X = ord(b)
        if 0 == X:
          keys[i].seek(keys[i].tell() + 1)
        else:
          break

      if eok:
        break
      
      # Extract X/Y
      Y = ord(keys[i].read(1))
      
      # Push point
      points.append((GF256elt(X),GF256elt(Y)))

    if eok:
      if 0 != i:
        raise Exception('Unexpected EOF while reading key %d' % i)
      break                        

    # Decode next byte
    byte = interpolator.interpolate(points).f(zero)
    output.write(bytearray((int(byte),)))

if __name__ == "__main__":
  from io import BytesIO
  input = BytesIO("Too many secrets, Marty!".encode('UTF-8'))
  outputs = []
  n = 5
  k = 3
  for i in range(n):
    outputs.append(BytesIO())

  encode(input,outputs,k)

  for i in range(n):
    print(binascii.hexlify(outputs[i].getvalue()).decode('UTF-8'))

  inputs = []
  for i in range(k):
    inputs.append(outputs[i+1])

  for i in range(k):
    inputs[i].seek(0)

  output = BytesIO()
  decode(inputs,output)  
  print(output.getvalue().decode('UTF-8'))
