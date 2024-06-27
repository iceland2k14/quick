#-------------------------------------------------------------------------
# Name:        PubDiv
# Author:      iceland
# Created:     07.06.2024
# Usage:       python PubDiv.py 02CEB6CBBCDBDF5EF7150682150F4CE2C6F4807B349827DCDBDD1F2EFA885A2630 15 keydiv_bit5.txt
#-------------------------------------------------------------------------

from time import time
import os
import sys
import secp256k1 as ice

#=========================================================================
if len(sys.argv) > 4 or len(sys.argv) < 4:
    print('[+] Program Usage.... ')
    print(f'python {sys.argv[0]} <original_pubkey> <bit_reduction> <output_file_name>\n')
    print(f'Example to create a text File:\n\npython {sys.argv[0]} 02CEB6CBBCDBDF5EF7150682150F4CE2C6F4807B349827DCDBDD1F2EFA885A2630 15 keydiv_bit5.txt\n')
    sys.exit()

pubkey = sys.argv[1]
nbits = int(sys.argv[2])
out_file = sys.argv[3]
#=========================================================================

N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
total_keys = 2**nbits
Q = ice.pub2upub(pubkey)

# k = 1/total_keys
k = pow(total_keys, N - 2, N)
st = time()
out = open(out_file, 'w')

#=========================================================================
print(f'[+] Result will write Total {total_keys} pubkeys in the Output File size Approx. [{total_keys*132/(1024*1024):.3f} MB]')
#=========================================================================

for i in range(total_keys):
    P = ice.point_subtraction(Q, ice.scalar_multiplication(i))
    out.write(f'{ice.point_multiplication(P, k).hex()}\n')
    if i % 1000 == 0: print(f'[+] Completed: {i}', end='\r')
    
out.flush()
os.fsync(out.fileno())
out.close()
print(f'[+] Finished Total DivKeys: {total_keys}\n')
print(f'[+] Completed in {time() - st:.2f} sec')
