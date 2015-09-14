
import mock
import unittest2
import pyssss as ssss
import PySSSS
import os
import random

_threshold = 2
_numshares = 3
_secret = "hun\0ter2"
_randval = 32

# generated from secret 'hun\0ter2'
_goodsplit = [
    '033f07270b7f0f3e133517281b761f64237a276e2b352f2e334137553b093f1d43ed47f94ba54fb153e657f25bae5fba63a167b56be96ffd73aa77be7be27ff6831c87088b548f40931797039b5f9f4ba350a744ab18af0cb35bb74fbb13bf07c3f7c7e3cbbfcfabd3fcd7e8dbb4dfa0e3bbe7afebf3efe7f3b0f7a4fbf8000102e7061e0a5a0e46122916351a711e6d220e26122a562e4a322536393a7d3e61426946754a314e2d5242565e5a1a5e06626566796a3d6e21724e76527a167e0a8203861f8a5b8e47922896349a709e6ca20fa613aa57ae4bb224b638ba7cbe60c268c674ca30ce2cd243d65fda1bde07e264e678ea3cee20f24ff653fa17fe0b051409480d5c110b151f192b1d222122255829702d7531353561',
    '043108050c491084144b18fa1c3020d8249428b72ce3305934df387c3caf4019443848364c48508a544358cd5c33605f649468816ce4700b74ef787a7c9f807f84bf88eb8ccf90e394c498109cb4a045a413a85cac63b062b468b8a7bc18c0fcc48fc8edccffd089d4f4d816dc84e0f7e423e85aec53f008f458f8a1fc280319071b0b530f4b133817201b681f70232f27372b7f2f673314370c3b443f5c432847304b784f605313570b5b435f5b6304671c6b546f4c733f77277b6f7f778382879a8bd28fca93b997a19be99ff1a3aea7b6abfeafe6b395b78dbbc5bfddc3a9c7b1cbf9cfe1d392d78adbc2dfdae385e79debd5efcdf3bef7a6fbee000102e106180a500e48123b16231a031e06224226342a082e013265363d',
    '053309030d43118a155919ec1d2a21c625b629912dc9317735ed394a3d954127457a49704d0251c45511599b5d69610165f669e76d8e7165759d790c7de58101853d896d8d45916d955699869d2ea1dba5b1a9faadc9b1ccb5dab911bda2c142c54dc92bcd35d147d526d9c0dd5ee129e5c1e9bcedb9f1e6f5aaf957fdd204d508280c6c10d0144f18e31c27208d24c828ff2ca03031348338343ceb40d944f448ee4c9c507a54bf58255cd760ff643868396c50709b747378f27c1b80e4842888688c409048946398a39c0ba0bea4e4a8bfac8cb0a9b4afb874bcc7c0a7c4d8c8aeccb0d0e2d493d865dcfbe0cce414e879ec7cf003f45ff8b2fc37031c071c0b580f44132b17371b1b1f1a236227102b202f2d33553709'
    ]
# generated from secret 'badsplit'
_badsplit = [
    '393c3d7e41d2459949924dd15182559159985d8c6190658b69ef6dfb71ac75b879e47df0811a850e89528d469111950599599d4da156a542a91ead0ab15db549b915bd01c1f1c5e5c9b9cdadd1fad5eed9b2dda6e1bde5a9e9f5ede1f1b6f5a2f9fefdea040c08380c7410f0146718d31c1f20cd248028af2cf8305134eb38443c934059447c487e4c0450da541758955c6f603f64f068e96c88707b749b78027ce380ff843b88638c439073945098889c28a0e5a4b7a8f4accfb0d2b4dcb81fbca4c03cc44bc825cc33d059d420d8cedc58e017e4c7e8b2ecbff0f8f4acf859fcd40100051409480d5c110b151f19431d57214c255829042d1031473553390f3d1b41eb45ff49a34dd55181559059db5dcc61cb65da699b',
    '3a743e3a421246554a4a4e055272566d5a705e68623066276a576e4f723c76247a6c7e74828186998ad18ec992ba96a29aea9ef2a2ada6b5aafdaee5b296b68ebac6bedec2aac6b2cafacee2d291d689dac1ded9e286e69eead6eecef2bdf6a5faedfef5050f093f0d7f11ff157419c41d0421d225a329882dd3317e35d839733da84166453f49394d4f5195554459c25d3461606593698e6de3711475e879757d98818085b889e48dc891fc95c3991f9db3a17aa514a953ad64b17db56fb9a8bd1fc183c588c9e2cdf8d196d5f3d919dd83e1c8e524e955ed54f117f55ff9aefd2f020006180a500e48123b16231a6b1e73222c26342a7c2e643217360f3a473e5f422b46334a7b4e015271566c5a335e28626b66766a23',
    '3b4c3f06435247114b024f49532257395b285f34635067436b3f6f23734c77507b147f088301871d8b598f45932a97369b729f6ea30da711ab55af49b326b73abb7ebf62c36ac776cb32cf2ed341d75ddb19df05e366e77aeb3eef22f34df751fb15000102e3060a0a360e6212ee16411afd1e2922f326c62ae12eae320f368d3a2a3ee5422746fa4af04e92524456b15a3b5ed9628166366a276e5e72a5767d7aec7e15820186268a768e4e9276966d9abd9e05a2c0a6eaaaa1ae82b297b6a1ba6abec9c259c6d6cab0cebed2dcd69dda7bdef5e2b2e61aea67ee72f23df651faacfe390300071c0b580f44132b17371b731f6f230c27102b542f483327373b3b7f3f63436b47774b334f4d532157385b6b5f74630b67126b4b'
    ]

class Tests(unittest2.TestCase):
    counter = 1

    def seq_random(self, low, high):
        self.counter = (self.counter+1)%255
        return self.counter

    @mock.patch('random.SystemRandom.randrange')
    def test_splitsecret(self, RangeMock):
        RangeMock.side_effect = self.seq_random
        shares = PySSSS.splitsecret(_secret, _threshold, _numshares)
        self.assertEqual(shares, _goodsplit)
        self.assertNotEqual(shares, _badsplit)

    def test_recoversecret(self):
        self.assertEqual(PySSSS.recoversecret(_goodsplit), _secret)
        self.assertNotEqual(PySSSS.recoversecret(_badsplit), _secret)

    def test_roundtrip_padded(self):
        secret = str(os.urandom(10))
        (shares, threshold) = self.rand_shares(secret, 8)
        recovered = PySSSS.recoversecret(random.sample(shares, threshold))
        self.assertEqual(recovered, secret)

    def test_roundtrip_unpadded(self):
        secret = str(os.urandom(1024))
        (shares, threshold) = self.rand_shares(secret, 8)
        recovered = PySSSS.recoversecret(random.sample(shares, threshold))
        self.assertEqual(recovered, secret)

    def test_not_enough_shares(self):
        secret = str(os.urandom(100))
        (shares, threshold) = self.rand_shares(secret, 8)
        with self.assertRaises(ValueError):
            PySSSS.recoversecret(random.sample(shares, threshold-1))

    def test_bad_threshold(self):
        with self.assertRaises(ValueError):
            PySSSS.splitsecret(_secret, _numshares, _threshold)

    def test_not_a_share(self):
        with self.assertRaises(ValueError):
            PySSSS.splitsecret(_secret, 1, 1)

    def rand_shares(self, secret, maxshares):
        numshares = random.randrange(3, maxshares)
        threshold = random.randrange(2, numshares)
        shares = PySSSS.splitsecret(secret, threshold, numshares)
        return (shares, threshold)

if __name__=='__main__':
    unittest.main()
