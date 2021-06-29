# -*- coding: utf-8 -*-
"""

@author: iceland
"""
import bit
import bitcoinlib
###############################################################################
# 6 Pubkeys are
# Pubkey = [x,y]  [x*beta%p, y]  [x*beta2%p, y] [x,p-y]  [x*beta%p, p-y]  [x*beta2%p, p-y]

# 6 Privatekeys are
# pvk, pvk*lmda%N, pvk*lmda2%N, N-pvk, N-pvk*lmda%N, N-pvk*lmda2%N

###############################################################################
## Field parameters
p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

###############################################################################
# Constants Based on Cube root of 1
beta = 0x7ae96a2b657c07106e64479eac3434e99cf0497512f58995c1396c28719501ee
beta2 = 0x851695d49a83f8ef919bb86153cbcb16630fb68aed0a766a3ec693d68e6afa40      # beta*beta
lmda = 0x5363ad4cc05c30e0a5261c028812645a122e22ea20816678df02967c1b23bd72
lmda2 = 0xac9c52b33fa3cf1f5ad9e3fd77ed9ba4a880b9fc8ec739c2e0cfc810b51283ce      # lmda*lmda

###############################################################################
def one_to_6upubkey(pub_hex):
    x = int(pub_hex[2:66],16)
    if len(pub_hex) < 70: y = bit.format.x_to_y(x, int(pub_hex[:2],16)%2)
    else: y = int(pub_hex[66:],16)
    print('Pubkey1 : ', '04'+hex(x)[2:].zfill(64) + hex(y)[2:].zfill(64))
    print('Pubkey2 : ', '04'+hex(x*beta%p)[2:].zfill(64) + hex(y)[2:].zfill(64))
    print('Pubkey3 : ', '04'+hex(x*beta2%p)[2:].zfill(64) + hex(y)[2:].zfill(64))
    print('Pubkey4 : ', '04'+hex(x)[2:].zfill(64) + hex(p-y)[2:].zfill(64))
    print('Pubkey5 : ', '04'+hex(x*beta%p)[2:].zfill(64) + hex(p-y)[2:].zfill(64))
    print('Pubkey6 : ', '04'+hex(x*beta2%p)[2:].zfill(64) + hex(p-y)[2:].zfill(64))
    
def one_to_6cpubkey(pub_hex):
    x = int(pub_hex[2:66],16)
    if len(pub_hex) < 70: y = bit.format.x_to_y(x, int(pub_hex[:2],16)%2)
    else: y = int(pub_hex[66:],16)
    prefix = 2
    print('Pubkey1 : ', str(prefix+(y%2)).zfill(2) + hex(x)[2:].zfill(64))
    print('Pubkey2 : ', str(prefix+(y%2)).zfill(2) + hex(x*beta%p)[2:].zfill(64))
    print('Pubkey3 : ', str(prefix+(y%2)).zfill(2) + hex(x*beta2%p)[2:].zfill(64))
    print('Pubkey4 : ', str(prefix+((p-y)%2)).zfill(2) + hex(x)[2:].zfill(64))
    print('Pubkey5 : ', str(prefix+((p-y)%2)).zfill(2) + hex(x*beta%p)[2:].zfill(64))
    print('Pubkey6 : ', str(prefix+((p-y)%2)).zfill(2) + hex(x*beta2%p)[2:].zfill(64))

def one_to_6privatekey(pvk_hex):
    pvk = int(pvk_hex,16)
    print('PVK1 : ', hex(pvk)[2:].zfill(64))
    print('PVK2 : ', hex(pvk*lmda%N)[2:].zfill(64))
    print('PVK3 : ', hex(pvk*lmda2%N)[2:].zfill(64))
    print('PVK4 : ', hex(N-pvk)[2:].zfill(64))
    print('PVK5 : ', hex(N-pvk*lmda%N)[2:].zfill(64))
    print('PVK6 : ', hex(N-pvk*lmda2%N)[2:].zfill(64))
    
def pvk_to_6cpub(pvk_hex):
    pvk = int(pvk_hex,16)
    print('C Pubkey1 : ', bit.Key.from_int(pvk)._pk.public_key.format(compressed=True).hex())
    print('C Pubkey2 : ', bit.Key.from_int(pvk*lmda%N)._pk.public_key.format(compressed=True).hex())
    print('C Pubkey3 : ', bit.Key.from_int(pvk*lmda2%N)._pk.public_key.format(compressed=True).hex())
    print('C Pubkey4 : ', bit.Key.from_int(N-pvk)._pk.public_key.format(compressed=True).hex())
    print('C Pubkey5 : ', bit.Key.from_int(N-pvk*lmda%N)._pk.public_key.format(compressed=True).hex())
    print('C Pubkey6 : ', bit.Key.from_int(N-pvk*lmda2%N)._pk.public_key.format(compressed=True).hex())
    
def pvk_to_6upub(pvk_hex):
    pvk = int(pvk_hex,16)
    print('U Pubkey1 : ', bit.Key.from_int(pvk)._pk.public_key.format(compressed=False).hex())
    print('U Pubkey2 : ', bit.Key.from_int(pvk*lmda%N)._pk.public_key.format(compressed=False).hex())
    print('U Pubkey3 : ', bit.Key.from_int(pvk*lmda2%N)._pk.public_key.format(compressed=False).hex())
    print('U Pubkey4 : ', bit.Key.from_int(N-pvk)._pk.public_key.format(compressed=False).hex())
    print('U Pubkey5 : ', bit.Key.from_int(N-pvk*lmda%N)._pk.public_key.format(compressed=False).hex())
    print('U Pubkey6 : ', bit.Key.from_int(N-pvk*lmda2%N)._pk.public_key.format(compressed=False).hex())

def pvk_to_24address(pvk_hex):
    pvk = int(pvk_hex, 16)
    print('PVK1 BTC Address : [Compressed  ]  ', bit.format.public_key_to_address(bit.Key.from_int(pvk)._pk.public_key.format(compressed=True)))
    print('PVK1 BTC Address : [Uncompressed]  ', bit.format.public_key_to_address(bit.Key.from_int(pvk)._pk.public_key.format(compressed=False)))
    print('PVK1 BTC Address : [Segwit      ]  ', bit.Key.from_int(pvk).segwit_address)
    print('PVK1 BTC Address : [Bech32      ]  ', bitcoinlib.keys.Address(bit.Key.from_int(pvk).public_key.hex(),encoding='bech32',script_type='p2wpkh').address)
    
    print('PVK2 BTC Address : [Compressed  ]  ', bit.format.public_key_to_address(bit.Key.from_int(pvk*lmda%N)._pk.public_key.format(compressed=True)))
    print('PVK2 BTC Address : [Uncompressed]  ', bit.format.public_key_to_address(bit.Key.from_int(pvk*lmda%N)._pk.public_key.format(compressed=False)))
    print('PVK2 BTC Address : [Segwit      ]  ', bit.Key.from_int(pvk*lmda%N).segwit_address)
    print('PVK2 BTC Address : [Bech32      ]  ', bitcoinlib.keys.Address(bit.Key.from_int(pvk*lmda%N).public_key.hex(),encoding='bech32',script_type='p2wpkh').address)
    
    print('PVK3 BTC Address : [Compressed  ]  ', bit.format.public_key_to_address(bit.Key.from_int(pvk*lmda2%N)._pk.public_key.format(compressed=True)))
    print('PVK3 BTC Address : [Uncompressed]  ', bit.format.public_key_to_address(bit.Key.from_int(pvk*lmda2%N)._pk.public_key.format(compressed=False)))
    print('PVK3 BTC Address : [Segwit      ]  ', bit.Key.from_int(pvk*lmda2%N).segwit_address)
    print('PVK3 BTC Address : [Bech32      ]  ', bitcoinlib.keys.Address(bit.Key.from_int(pvk*lmda2%N).public_key.hex(),encoding='bech32',script_type='p2wpkh').address)
    
    print('PVK4 BTC Address : [Compressed  ]  ', bit.format.public_key_to_address(bit.Key.from_int(N-pvk)._pk.public_key.format(compressed=True)))
    print('PVK4 BTC Address : [Uncompressed]  ', bit.format.public_key_to_address(bit.Key.from_int(N-pvk)._pk.public_key.format(compressed=False)))
    print('PVK4 BTC Address : [Segwit      ]  ', bit.Key.from_int(N-pvk).segwit_address)
    print('PVK4 BTC Address : [Bech32      ]  ', bitcoinlib.keys.Address(bit.Key.from_int(N-pvk).public_key.hex(),encoding='bech32',script_type='p2wpkh').address)
    
    print('PVK5 BTC Address : [Compressed  ]  ', bit.format.public_key_to_address(bit.Key.from_int(N-pvk*lmda%N)._pk.public_key.format(compressed=True)))
    print('PVK5 BTC Address : [Uncompressed]  ', bit.format.public_key_to_address(bit.Key.from_int(N-pvk*lmda%N)._pk.public_key.format(compressed=False)))
    print('PVK5 BTC Address : [Segwit      ]  ', bit.Key.from_int(N-pvk*lmda%N).segwit_address)
    print('PVK5 BTC Address : [Bech32      ]  ', bitcoinlib.keys.Address(bit.Key.from_int(N-pvk*lmda%N).public_key.hex(),encoding='bech32',script_type='p2wpkh').address)
    
    print('PVK6 BTC Address : [Compressed  ]  ', bit.format.public_key_to_address(bit.Key.from_int(N-pvk*lmda2%N)._pk.public_key.format(compressed=True)))
    print('PVK6 BTC Address : [Uncompressed]  ', bit.format.public_key_to_address(bit.Key.from_int(N-pvk*lmda2%N)._pk.public_key.format(compressed=False)))
    print('PVK6 BTC Address : [Segwit      ]  ', bit.Key.from_int(N-pvk*lmda2%N).segwit_address)
    print('PVK6 BTC Address : [Bech32      ]  ', bitcoinlib.keys.Address(bit.Key.from_int(N-pvk*lmda2%N).public_key.hex(),encoding='bech32',script_type='p2wpkh').address)
    

def do_all(pvk_hex):
    one_to_6privatekey(pvk_hex)
#    one_to_6upubkey(bit.Key.from_hex(pvk_hex)._pk.public_key.format(compressed=False).hex())
#    one_to_6cpubkey(bit.Key.from_hex(pvk_hex)._pk.public_key.format(compressed=False).hex())
    pvk_to_6cpub(pvk_hex)
    pvk_to_6upub(pvk_hex)
    pvk_to_24address(pvk_hex)
###############################################################################
## Example
# one_to_6privatekey('08')
# one_to_6upubkey('042f01e5e15cca351daff3843fb70f3c2f0a1bdd05e5af888a67784ef3e10a2a015c4da8a741539949293d082a132d13b4c2e213d6ba5b7617b5da2cb76cbde904')
do_all('1ce')