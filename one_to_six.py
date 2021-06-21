# -*- coding: utf-8 -*-
"""

@author: iceland
"""

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
def one_to_6pubkey(upub_hex):
    if len(upub_hex) < 70 : print('Please provide full Uncompressed Pubkey in hex'); exit()
    x = int(upub_hex[2:66],16)
    y = int(upub_hex[66:],16)
    print('Pubkey1 : ', '04'+hex(x)[2:].zfill(64)+hex(y)[2:].zfill(64))
    print('Pubkey2 : ', '04'+hex(x*beta%p)[2:].zfill(64)+hex(y)[2:].zfill(64))
    print('Pubkey3 : ', '04'+hex(x*beta2%p)[2:].zfill(64)+hex(y)[2:].zfill(64))
    print('Pubkey4 : ', '04'+hex(x)[2:].zfill(64)+hex(p-y)[2:].zfill(64))
    print('Pubkey5 : ', '04'+hex(x*beta%p)[2:].zfill(64)+hex(p-y)[2:].zfill(64))
    print('Pubkey6 : ', '04'+hex(x*beta2%p)[2:].zfill(64)+hex(p-y)[2:].zfill(64))

def one_to_6privatekey(pvk_hex):
    pvk = int(pvk_hex,16)
    print('PVK1 : ', hex(pvk)[2:].zfill(64))
    print('PVK2 : ', hex(pvk*lmda%N)[2:].zfill(64))
    print('PVK3 : ', hex(pvk*lmda2%N)[2:].zfill(64))
    print('PVK4 : ', hex(N-pvk)[2:].zfill(64))
    print('PVK5 : ', hex(N-pvk*lmda%N)[2:].zfill(64))
    print('PVK6 : ', hex(N-pvk*lmda2%N)[2:].zfill(64))

###############################################################################
## Example
one_to_6privatekey('08')
one_to_6pubkey('042f01e5e15cca351daff3843fb70f3c2f0a1bdd05e5af888a67784ef3e10a2a015c4da8a741539949293d082a132d13b4c2e213d6ba5b7617b5da2cb76cbde904')