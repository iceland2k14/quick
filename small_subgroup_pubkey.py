# -*- coding: utf-8 -*-
"""
Usage :
 > python small_subgroup_pubkey.py 
 
@author: iceland
"""
import os, platform, sys
import random
import ctypes
import math
import time
import bit
verbosity = False
# =============================================================================
print('\n[+] Program Starting in BSGS pubkey mode... Please Wait')
if platform.system().lower().startswith('win'):
    dllfile = 'ice_secp256k1.dll'
    if os.path.isfile(dllfile) == True:
        pathdll = os.path.realpath(dllfile)
        ice = ctypes.CDLL(pathdll)
    else:
        print('File {} not found'.format(dllfile))
    
elif platform.system().lower().startswith('lin'):
    dllfile = 'ice_secp256k1.so'
    if os.path.isfile(dllfile) == True:
        pathdll = os.path.realpath(dllfile)
        ice = ctypes.CDLL(pathdll)
    else:
        print('File {} not found'.format(dllfile))
    
else:
    print('[-] Unsupported Platform currently for ctypes dll method. Only [Windows and Linux] is working')
    sys.exit()

ice.scalar_multiplication.argtypes = [ctypes.c_char_p, ctypes.c_char_p]            # pvk,ret
ice.point_addition.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p] # x1,y1,x2,y2,ret
ice.point_subtraction.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p] # x1,y1,x2,y2,ret
ice.free_memory.argtypes = [ctypes.c_void_p] # pointer
ice.init_secp256_lib()


def _scalar_multiplication(kk):
    ''' Integer value passed to function. 65 bytes uncompressed pubkey output '''
    res = (b'\x00') * 65
    pass_int_value = hex(kk)[2:].encode('utf8')
    ice.scalar_multiplication(pass_int_value, res)
    return res
def scalar_multiplication(kk):
    res = _scalar_multiplication(kk)
    return bytes(bytearray(res))

def _point_addition(pubkey1_bytes, pubkey2_bytes):
    x1 = pubkey1_bytes[1:33]
    y1 = pubkey1_bytes[33:]
    x2 = pubkey2_bytes[1:33]
    y2 = pubkey2_bytes[33:]
    res = (b'\x00') * 65
    ice.point_addition(x1, y1, x2, y2, res)
    return res
def point_addition(pubkey1_bytes, pubkey2_bytes):
    res = _point_addition(pubkey1_bytes, pubkey2_bytes)
    return bytes(bytearray(res))

def _point_subtraction(pubkey1_bytes, pubkey2_bytes):
    x1 = pubkey1_bytes[1:33]
    y1 = pubkey1_bytes[33:]
    x2 = pubkey2_bytes[1:33]
    y2 = pubkey2_bytes[33:]
    res = (b'\x00') * 65
    ice.point_subtraction(x1, y1, x2, y2, res)
    return res
def point_subtraction(pubkey1_bytes, pubkey2_bytes):
    res = _point_subtraction(pubkey1_bytes, pubkey2_bytes)
    return bytes(bytearray(res))
###############################################################################
def pub2upub(pub_hex):
	x = int(pub_hex[2:66],16)
	if len(pub_hex) < 70:
		y = bit.format.x_to_y(x, int(pub_hex[:2],16)%2)
	else:
		y = int(pub_hex[66:],16)
	return bytes.fromhex('04'+ hex(x)[2:].zfill(64) + hex(y)[2:].zfill(64))

def findkey(onePoint, baby_dict, BSnP, BSn, GSn):
    S = onePoint
    found = False
    step = 0
    
    while found is False and step < GSn:
        if S in baby_dict:
            b = baby_dict.get(S)
            
            if scalar_multiplication(k*(step*BSn + b)) == onePoint:
                final_key = k*(step*BSn + b)
                found = True
                break
            elif scalar_multiplication(k*(step*BSn + BSn - b)) == onePoint:
                final_key = k*(step*BSn + BSn - b)
                found = True
                break
            else:
                S = point_subtraction(S, BSnP)
                step = step + 1
        else:
            # Giant step
            S = point_subtraction(S, BSnP)
            step = step + 1
            
    if found == True:
        return final_key
    else:
        return -1

###############################################################################
pubkey_filename = 'Pub50.txt'
# line_separator = #  ','  ';'  ' '
coin_list = [line.split()[0] for line in open(pubkey_filename,'r')]

pub_list = [pub2upub(x) for x in coin_list if len(x) == 66 or len(x) == 130]  # Compressed or Uncompressed
print('{} Pubkeys Read from the file. Ignored {}'.format(len(pub_list), len(coin_list)-len(pub_list)))


N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
###############################################################################

while True:
    a_largebit_number = random.SystemRandom().randint(2**230, 2**242)
    # k = gmpy2.next_prime(a_largebit_number)    # factor1 * factor2 * factor3
    k = a_largebit_number
    
    P = scalar_multiplication(k)
    baby_dict = {P:k}

    P2 = P
    BSn = int(math.sqrt(N//k))
    GSn = 1 + (N//(BSn*k))
    BSnP = scalar_multiplication(BSn*k)
    print('\n[+] Starting search for the subgroup : {}     [{} bit]'.format(hex(k),len(bin(k)[2:])))
    print('[+] [BS {} items]   [GS {} items]'.format(BSn, GSn))
    st = time.time()
    
    for i in range(2, BSn+1):
        P2 = point_addition(P2, P)
        baby_dict[P2] = i

    print('[+] BS Table for this subgroup created in : {0:.5f} sec '.format(time.time()-st))


###############################################################################
    j = 0
    print('='*75)
    for Q in pub_list:
        j += 1
        if verbosity is True: print('[+] Checking Gaint Steps of current Pubkey')
        
        small_subgroup_pvk = findkey(Q, baby_dict, BSnP, BSn, GSn)
        if small_subgroup_pvk >= 0:
            print('============== KEYFOUND ==============')
            print('[PrivateKey ]:', hex(small_subgroup_pvk) )
            print('[Pubkey     ]:',scalar_multiplication(small_subgroup_pvk).hex())
            print('======================================')
            exit()
        else:
            print('[+] Total Pubkeys checked for this subgroup : {} '.format(j), end='\r')
            
    print('', end='\r')
    
###############################################################################