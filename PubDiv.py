# -*- coding: utf-8 -*-
"""
Usage :
 > python PubDiv.py 02CEB6CBBCDBDF5EF7150682150F4CE2C6F4807B349827DCDBDD1F2EFA885A2630 5 keydiv_bit5.txt

@author: iceland
"""
from time import time
import os
import sys
from fastecdsa import curve
from fastecdsa.point import Point
import bit

G = curve.secp256k1.G
N = curve.secp256k1.q


if len(sys.argv) > 4 or len(sys.argv) < 4:
    print('[+] Program Usage.... ')
    print('{} <original_pubkey> <bit_reduction> <output_file_name>\n'.format(sys.argv[0]))
    print('Example to create a text File [upub]:\n{} 02CEB6CBBCDBDF5EF7150682150F4CE2C6F4807B349827DCDBDD1F2EFA885A2630 5 keydiv_bit5.txt'.format(sys.argv[0]))
    sys.exit()


def pub2point(pub_hex):
 x = int(pub_hex[2:66],16)
 if len(pub_hex) < 70:
  y = bit.format.x_to_y(x, int(pub_hex[:2],16)%2)
 else:
  y = int(pub_hex[66:], 16)
 return Point(x,y,curve=curve.secp256k1)

def point2upub(A):
    return '04'+ hex(A.x)[2:].zfill(64) + hex(A.y)[2:].zfill(64)
    
def upub2cpub(upub_bytes):
    x1 = upub_bytes[1:33]
    prefix = str(2 + int(upub_bytes[33:].hex(), 16)%2).zfill(2)
    return bytes.fromhex(prefix)+x1
###############################################################################
pubkey = sys.argv[1]
nbits = int(sys.argv[2])
out_file = sys.argv[3]

total_keys = 2**nbits
print('[+] Result will write Total {} pubkeys in the Output File size Approx. [{:.3f} MB]'.format(total_keys, total_keys*132/(1024*1024)))

Q = pub2point(pubkey)

# k = 1/total_keys
k = pow(total_keys, N-2, N)

st = time()
###############################################################################
out = open(out_file, 'w')

for i in range(total_keys):
    P = Q - (i*G)
    out.write(point2upub(k*P)+'\n')
    if i%100 == 0: print('[+] Completed : ', i, end='\r')
    
out.flush()
os.fsync(out.fileno())
out.close()
print('[+] Finished Total DivKeys # ', total_keys, end= '\n')
print('[+] Completed in {0:.2f} sec'.format(time() - st))
