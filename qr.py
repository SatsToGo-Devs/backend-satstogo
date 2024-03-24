import segno
from binascii import unhexlify
from secp256k1 import PublicKey
import os

random_data = os.urandom(32)
hex_data = random_data.hex()

qrcode = segno.make_qr(f"https://moose-fair-publicly.ngrok-free.app/api/login?tag=login&k1={hex_data}&action=login")
qrcode.save(
    "media/darkblue_qrcode.png",
    scale=5,
    dark="darkblue",
)

def verifyLNUrl():
    k1 = unhexlify('2859102ffac3de2f9b44becbc3c7a8a5039ef0161524010fc24fb91e830690ed')
    key = unhexlify('025bea4bbf4e9b2f9673cba5ae3f51f694283870aa26b703d1bf320d4775533853')
    sig = unhexlify('304402203670b360737428ad3c80bd94afa5b23fd28de24db277fec307b892abb50cfa6702207848d0ef05323291d3ba7b821837edc609b7c6181e7c416690ec1a4ad48f3b60')

    pubkey = PublicKey(key, raw=True)
    sig_raw = pubkey.ecdsa_deserialize(sig)
    r = pubkey.ecdsa_verify(k1, sig_raw, raw=True)
    print(r)
    assert r == True

verifyLNUrl()
# moose-fair-publicly.ngrok-free.app
    
# k1=2859102ffac3de2f9b44becbc3c7a8a5039ef0161524010fc24fb91e830690ed
# sig=304402203670b360737428ad3c80bd94afa5b23fd28de24db277fec307b892abb50cfa6702207848d0ef05323291d3ba7b821837edc609b7c6181e7c416690ec1a4ad48f3b60
# key=025bea4bbf4e9b2f9673cba5ae3f51f694283870aa26b703d1bf320d4775533853