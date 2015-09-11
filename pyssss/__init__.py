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
#  Portions copyright 2015 Lucid Design Group, Inc
#  Author Brandon Matthews <bmatt@luciddg.com>
#                           github.com/thenewwazoo

import binascii
import PySSSS
import StringIO

_padlen = 128     # minimum block size
_padchar = '\x00'

def splitsecret(secret, threshold, numshares):
  """returns list of shares of secret, with t=threshold, k=numshares

  splitsecret splits ``secret`` into ``numshares`` parts, with ``threshold``
  required to reconstruct the secret.

  The secret is padded to 128-character blocks to reduce information about
  the length of the secret. A CRC32 value of the raw secret is also generated (and
  included within the ciphertext) in order to ease validation of reconstruction.

  :param secret: the raw secret to be split
  :param threshold: the minimum number of shares required for successful reconstruction
  :param numshares: the number of shares to generate
  :type secret: string
  :type threshold: int
  :type numshares: int
  :returns: a list of shares
  :rtype: list of strings

  :Example:

  >>> import PySSSS
  >>> secret = "hun\0ter2" # any string will do
  >>> shares = pyssss.splitsecret(secret, 2, 3)
  >>> len(shares)
  3

  """
  global _padlen
  global _padchar

  # Here we track the number of characters we're padding, because the
  #  pad character is in-band.
  passlen = len(secret)
  padnum = _padlen - (passlen % _padlen)
  secret = "{:0=8x}{:0=4x}{}".format(
          binascii.crc32(secret) & 0xFFFFFFFF,
          padnum,
          secret.rjust(_padlen, _padchar))

  outputs = []
  for i in xrange(numshares):
      outputs.append(StringIO.StringIO())

  PySSSS.encode(StringIO.StringIO(secret), outputs, threshold)

  return [ outputs[i].getvalue().encode('hex') for i in xrange(numshares) ]

def recoversecret(shares):
  """returns the reconstructed raw secret

  recoversecret combines the supplied list of shares and returns the raw string.

  This function raises a ``ValueError`` if the CRC32 of the reconstructed secret
  does not match the reconstructed CRC from the ciphertext.

  :param shares: a list of shares
  :type shares: list of strings
  :returns: the raw secret
  :rtype: string

  :Example:

  >>> import pyssss
  >>> shares = [
      '568cd977816ca4ab74c81e37a0d12479ce589211df5c9b2343be80208094af8d0abd8d321150eb1e69dc5d027d53862ca0cb71cf1a5a665866210259adbd2d13ad0915ee1fbfe19519a77f4f5410fa458d9ebfe9c8743881e790efefd40ad9227e8fb82d71126ed0c75511d17547a641104ae76fe66096f39bc403a9ae10142a3a29a276855fdc114d162beff38f921fa63b8a9ef18b7dfb8ecf3a7fd8c32005fd401deca8d2d81a5b3f8cc68b894a6874025b5f0283d042be369561cf024dc88284999c28bf130e2df92fb028e4a8e627f48dde019eed9b43f3fba037b220a24514bdcdab447bd37dfe638eaae603d1114b97ae0364828c1f64e6c55ff3276279991e233b7d4f900948b13b4e8bf960790e91b5bbc6502e',
      '0a2eef4acd925746e1fe58871b71dca9c39380f74f25fa940db3028dbd5ee21f86e14e2688b6ccab68597e4f3f086755a95ee09c694d596f48afd42834016860c8130ce74bcb44b8f57a4a587289591d373fcd66be1ada2958dcd5d551af2dc8b2a0ad33d19f458da32faddf1950b048b546b7af7f7ec745f341f6d4a18486a6e02af8872741040e04d6cd2b7d20244da78f79d3cfdb9850568057cc61859983a68cf9192f3744d9bf3da087e8157219570e8309fa63c25fcc17a309de0a03ec8b5ceae77efd6a24f00352b9779f2488e0753dfbc4c1a1e4d90858c1e46ef62f08896c2952ff255facbaa821d30862fbae1dbb4ba4250ab3dbcdc44b0940957c4f31d14a1893331cc4ccfc288e9f96ebe418ca6d3274e389',
      '5864be0b621e1f8d8b82adb657a1af677e87a758f7cbc24da43abc2ff405e8ee5a2244e3e53a98886a4806bc5e78795b1daf39a691c19f44b49f619336fc403e2944d141b206f6110beebd448eb9a9c26534aa52ecdcfb07ca2b2e2ed8f2c5b6c0a8fc8836a65feb80ea8251850e91666b2195d75b8f621e78f608159fe7e90df283513b71da7cba7b34765eaf1f7f6437e51d458d2b17c7ebf1a299ce91914951e9c1fce36dc4bd28a90deeeec84f75a447b7521982e6657581ed4b4742eb9c5f49d57d712d586db879dcbcc0d6ca594c74dca9771ee899380c62d76351d0b04bbde6f703723c568f7b8ccfe66eb7c597eeabc1b0a3c7d33d920da0381288ab9921a7b70784829ce04ce4f0bd25998da97ef758a6da2e46'
      ]
  >>> print repr(pyssss.recoversecret(shares))
  'hun\x00ter2'

  """

  global _padchar

  output = StringIO.StringIO()
  PySSSS.decode(
          [ StringIO.StringIO(shares[i].decode('hex')) for i in xrange(len(shares)) ], 
          output
          )
  secret = output.getvalue()
  output.close()

  try:
    crc, padnum, secret = int(secret[0:8], 16), int(secret[8:12], 16), secret[12:]
    secret = secret[padnum:]
    if (binascii.crc32(secret) & 0xFFFFFFFF) != crc:
        raise ValueError
  except ValueError:
    raise ValueError("could not reconstruct a valid secret. do you have enough data?")

  return secret


def main():
  password = "hun\0ter2"
  print "the secret is:", repr(password)
  shares = splitsecret(password, 2, 3)
  password = ""
  print "the shares are:"
  for i in range(3):
    print repr(shares[i])
  print "the recovered secret is:"
  for i in range(len(shares)):
      print repr(recoversecret([shares[i], shares[(i+1)%3]]))
  print repr(recoversecret(shares))

if __name__=="__main__":
  main()
