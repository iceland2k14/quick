# -*- coding: utf-8 -*-
"""
Usage :
 > python small_subgroup_ETH.py 
 
@author: iceland
"""
import os, platform, sys
import random
import ctypes

verbosity = False
# =============================================================================
print('\n[+] Program Starting in ETH mode... Please Wait')
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

ice.privatekey_to_ETH_address.argtypes = [ctypes.c_char_p] # pvk
ice.privatekey_to_ETH_address.restype = ctypes.c_void_p
ice.free_memory.argtypes = [ctypes.c_void_p] # pointer
ice.init_secp256_lib()

def privatekey_to_ETH_address(pvk_int):
    pass_int_value = hex(pvk_int)[2:].encode('utf8')
    res = ice.privatekey_to_ETH_address(pass_int_value)
    addr = (ctypes.cast(res, ctypes.c_char_p).value).decode('utf8')
    ice.free_memory(res)
    return '0x'+addr

###############################################################################
eth_address_filename = 'eth_address.txt'
line_aeparator = ',' #  ''  ';'  ' '
coin_list = [line.split(line_aeparator)[0] for line in open(eth_address_filename,'r')]

eth_list = [x.lower() for x in coin_list if x[0:2] == '0x']  # ETH Address
print('{} ETH address found in the file. Ignored {}'.format(len(eth_list), len(coin_list)-len(eth_list)))
eth_list = set(eth_list)

N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
lmda = 0x5363ad4cc05c30e0a5261c028812645a122e22ea20816678df02967c1b23bd72
lmda2 = 0xac9c52b33fa3cf1f5ad9e3fd77ed9ba4a880b9fc8ec739c2e0cfc810b51283ce      # lmda*lmda
###############################################################################

while True:
    a_largebit_number = random.SystemRandom().randint(2**230, 2**242)
    # k = gmpy2.next_prime(a_largebit_number)    # factor1 * factor2 * factor3
    k = a_largebit_number
    print('\n[+] Starting search for the subgroup : {}     [{} bit]'.format(hex(k),len(bin(k)[2:])))
    
    for m in range(1, N//k):
        small_subgroup_pvk = m * k
        pln = small_subgroup_pvk*lmda%N
        pl2n = small_subgroup_pvk*lmda2%N
        np = N-small_subgroup_pvk
        npln = N-small_subgroup_pvk*lmda%N
        npl2n = N-small_subgroup_pvk*lmda2%N
        
        addr1 = privatekey_to_ETH_address(small_subgroup_pvk)
        addr2 = privatekey_to_ETH_address(pln)
        addr3 = privatekey_to_ETH_address(pl2n)
        addr4 = privatekey_to_ETH_address(np)
        addr5 = privatekey_to_ETH_address(npln)
        addr6 = privatekey_to_ETH_address(npl2n)

        if addr1 in eth_list  or addr5 in eth_list or addr6 in eth_list:
            print('============== KEYFOUND ==============')
            print('[PrivateKey ]:', hex(small_subgroup_pvk) )
            print('[ETH Address]:',addr1)
            print('======================================')
            
        if addr2 in eth_list:
            print('============== KEYFOUND ==============')
            print('[PrivateKey ]:', hex(pln) )
            print('[ETH Address]:',addr2)
            print('======================================')
        
        if addr3 in eth_list:
            print('============== KEYFOUND ==============')
            print('[PrivateKey ]:', hex(pl2n) )
            print('[ETH Address]:',addr3)
            print('======================================')
            
        if addr4 in eth_list:
            print('============== KEYFOUND ==============')
            print('[PrivateKey ]:', hex(np) )
            print('[ETH Address]:',addr4)
            print('======================================')
            
        if addr5 in eth_list:
            print('============== KEYFOUND ==============')
            print('[PrivateKey ]:', hex(npln) )
            print('[ETH Address]:',addr5)
            print('======================================')
            
        if addr6 in eth_list:
            print('============== KEYFOUND ==============')
            print('[PrivateKey ]:', hex(npl2n) )
            print('[ETH Address]:',addr6)
            print('======================================')

        if m%10000 == 0: 
            if verbosity is True: print('[+] Completed : ', 6*m,\
                  '[ETH-1]',addr1, '[ETH-2]',addr2, '[ETH-3]',addr3, \
                  '[ETH-4]',addr4, '[ETH-5]',addr5, '[ETH-6]',addr6, \
                  end='\r')
            else: print('[+] Completed : ', 6*m, '[ETH-1]',addr1, end='\r')
    print('', end='\r')
    
###############################################################################