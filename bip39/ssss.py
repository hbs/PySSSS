#!/usr/bin/env python
#
#  Copyright 2021-2022 Mathias Herberts
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

import itertools
import os
import sys
import random
import math

sys.path.insert(0,'.')
sys.path.append('pyssss')
from bip39 import BIP39
from pyssss import PySSSS
from pyssss import GF256
import hashlib

srandom = random.SystemRandom()

def sorting(x):
  print(x, type(x))
  return x

def doSplit(N,K):
  K = int(K)
  N = int(N)

  if K < 2 or K > 255 or N < K or N > 255:
    print("N and K MUST be in [2,255] with K <= N")
    exit(1)

  print('------------------------------------------------------------------------------------------------------------')
  print('        W O R D                                                  S P L I T S')
  print('------------------------------------------------------------------------------------------------------------')

  for i in range(0, len(BIP39)):
    ## byte array to convert contains the 16 bits of the word 0-based word index
    data = bytearray()
    data.append((i >> 8) & 0xFF)
    data.append(i & 0xFF)
    secrets = zip(PySSSS.encodeByte(GF256.QR,data[0],N,K),PySSSS.encodeByte(GF256.QR,data[1],N,K))

    first = True
    for secret in secrets:
      encoded = secret[0] + secret[1]
      ## Remove the points with 0 as their X coordinate
      if len(encoded) > 4:
        stripped = bytearray()
        for i in range(0,len(encoded)/2):
          if encoded[i*2] == 0:
            print('STRIPPED')
            continue
          stripped.append(encoded[i*2])
          stripped.append(encoded[i*2+1])
        encoded = stripped

      split = [0,0,0]
      split[0] = (encoded[0] << 2) | ((encoded[1] >> 6) & 0x3)
      split[1] = ((encoded[1] & 0x3F) << 5) | ((encoded[2] >> 3) & 0x1F)
      split[2] = ((encoded[2] & 0x7) << 8) | encoded[3]
      if first:
        print()
        print('[{:>4}]  {:<16}      [{:>4}]  {:<16}   [{:>4}]  {:<16}   [{:>4}]  {:<16}'.format(i+1,BIP39[i],split[0]+1,BIP39[split[0]],split[1]+1,BIP39[split[1]],split[2] + 1,BIP39[split[2]]))
        first = False
      else:
        print('                              [{:>4}]  {:<16}   [{:>4}]  {:<16}   [{:>4}]  {:<16}'.format(split[0]+1,BIP39[split[0]],split[1]+1,BIP39[split[1]],split[2] + 1,BIP39[split[2]]))

def doRecover(words):
  ##
  ## Check word count
  ##

  if 0 == len(words) or len(words) % 3 != 0:
    print('Invalid word count, should be a multiple of 3')
    exit(1)

  ##
  ## Create a map of word to index
  ##

  index = {}

  for i in range(0,len(BIP39)):
    index[BIP39[i]] = i

  ##
  ## Split the words into shares, converting numbers into words
  ##
  
  splits = []
  split = []

  for i in range(0, len(words)):
    # Convert numbers to words
    try:
      num = int(words[i])
      words[i] = BIP39[num - 1]
    except ValueError as err:
      pass

    if not words[i] in index:
      print("Word '" + words[i] + "' is not part of the BIP39 word list")
      exit(1)

    if 0 == i % 3:
      split = []
      splits.append(split)

    split.append(words[i])
    
  ##
  ## Now check all combinations of splts, computing error rates
  ##
  
  checks = {}
  for k in range(1,len(splits)+1):
    values = []
    checks[k] = values
    for combination in itertools.combinations(splits, k):
      # Flatten the combination
      combination = list(itertools.chain.from_iterable(combination))
      shares = []
      share = []
      for i in range(0, int(len(combination) / 3)):
        share = bytearray()
        seq0 = index[combination[i*3]]
        seq1 = index[combination[i*3+1]]
        seq2 = index[combination[i*3+2]]

        share.append((seq0 >> 2) & 0xFF)
        share.append(((seq0 & 0x3) << 6) | ((seq1 >> 5) & 0x3f))
        share.append(((seq1 & 0x1F) << 3) | ((seq2 >> 8) & 0x7))
        share.append(seq2 & 0xff)

        shares.append(share)

      secret = PySSSS.decodeBytes(GF256.QR,shares)

      wordidx = ((secret[0] & 0x7) << 8) | secret[1]

      values.append(wordidx)

  results = []
  firstunique = None
  for k in range(2,len(splits)+1):
    values = checks[k]
    n = len(values)
    unique = len(set(values))
    if 1 == unique:
      results.append(set(values).pop())
      if not firstunique:
        firstunique = k

  if len(results) != len(splits) - firstunique + 1:
    print('Invalid recovery of combinations of ' + str(firstunique) + '+ shares')

  if 1 != len(set(results)):
    print('Some invalid shares, recovered values differ for some combinations')

  print('[%d]  %s  %d/%d' % (results[0] + 1,BIP39[results[0]],firstunique,len(splits)))

def run(args):
  command = args[0]
  if 'split' == command:
    doSplit(args[1],args[2])
  elif 'recover' == command:
    doRecover(args[1:])
  else:
    print("Usage: ssss command params")
    print("")
    print("Commands: split N K")
    print("          recover shares (word list, multiple of 3)")
    print("")
    print("Enter command: ", end='')
    sys.stdout.flush()
    args = sys.stdin.readline().strip().split()
    run(args)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    run([ sys.argv[0], 'help' ])
  else:
    run(sys.argv[1:])

