# -*- coding: utf-8 -*-
"""
Usage :
 > python small_subgroup.py 
 
@author: iceland
"""
import os, platform, sys
import random
import ctypes

verbosity = False
# =============================================================================
print('\n[+] Program Starting ... Please Wait')
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

ice.privatekey_to_address.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]  # 012,comp,pvk
ice.privatekey_to_address.restype = ctypes.c_char_p
ice.init_secp256_lib()

def privatekey_to_address(addr_type, iscompressed, pvk_int):
    # type = 0 [p2pkh],  1 [p2sh],  2 [bech32]
    pass_int_value = hex(pvk_int)[2:].encode('utf8')
    res = ice.privatekey_to_address(addr_type, iscompressed, pass_int_value)
    return res.decode('utf8')

###############################################################################
btc_address_filename = 'btc_address.txt'
coin_list = [line.split()[0] for line in open(btc_address_filename,'r')]

legacy_btc_list = [x for x in coin_list if x[0] == '1']  # BTC Legacy Address
segwit_btc_list = [x for x in coin_list if x[0] == '3']  # BTC Segwit Address
bech32_btc_list = [x for x in coin_list if x[0] == 'b' and len(x) < 45]      # BTC bech32. ignore multisig address.
print('{0} Legacy BTC, {1} Segwit BTC, {2} bech32 BTC,  address found in the file'.format(len(legacy_btc_list), len(segwit_btc_list), len(bech32_btc_list)))

legacy_btc_list = set(legacy_btc_list)
segwit_btc_list = set(segwit_btc_list)
bech32_btc_list = set(bech32_btc_list)

N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
lmda = 0x5363ad4cc05c30e0a5261c028812645a122e22ea20816678df02967c1b23bd72
lmda2 = 0xac9c52b33fa3cf1f5ad9e3fd77ed9ba4a880b9fc8ec739c2e0cfc810b51283ce      # lmda*lmda
###############################################################################

while True:
    a_largebit_number = random.SystemRandom().randint(2**220, 2**240)
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
        
        addrc1 = privatekey_to_address(0, True, small_subgroup_pvk)
        addru1 = privatekey_to_address(0, False, small_subgroup_pvk)
        addr31 = privatekey_to_address(1, True, small_subgroup_pvk)
        addrb1 = privatekey_to_address(2, True, small_subgroup_pvk)
        
        addrc2 = privatekey_to_address(0, True, pln)
        addru2 = privatekey_to_address(0, False, pln)
        addr32 = privatekey_to_address(1, True, pln)
        addrb2 = privatekey_to_address(2, True, pln)
        
        addrc3 = privatekey_to_address(0, True, pl2n)
        addru3 = privatekey_to_address(0, False, pl2n)
        addr33 = privatekey_to_address(1, True, pl2n)
        addrb3 = privatekey_to_address(2, True, pl2n)
        
        addrc4 = privatekey_to_address(0, True, np)
        addru4 = privatekey_to_address(0, False, np)
        addr34 = privatekey_to_address(1, True, np)
        addrb4 = privatekey_to_address(2, True, np)
        
        addrc5 = privatekey_to_address(0, True, npln)
        addru5 = privatekey_to_address(0, False, npln)
        addr35 = privatekey_to_address(1, True, npln)
        addrb5 = privatekey_to_address(2, True, npln)
        
        addrc6 = privatekey_to_address(0, True, npl2n)
        addru6 = privatekey_to_address(0, False, npl2n)
        addr36 = privatekey_to_address(1, True, npl2n)
        addrb6 = privatekey_to_address(2, True, npl2n)

        if addrc1 in legacy_btc_list or addru1 in legacy_btc_list or addr31 in segwit_btc_list or addrb1 in bech32_btc_list:
            print('============== KEYFOUND ==============')
            print('PrivateKey :', hex(small_subgroup_pvk) )
            print('[C]',addrc1,'[U]',addru1)
            print('[3]',addr31,'[bc]',addrb1)
            print('======================================')
            
        if addrc2 in legacy_btc_list or addru2 in legacy_btc_list or addr32 in segwit_btc_list or addrb2 in bech32_btc_list:
            print('============== KEYFOUND ==============')
            print('PrivateKey :', hex(pln) )
            print('[C]',addrc2,'[U]',addru2)
            print('[3]',addr32,'[bc]',addrb2)
            print('======================================')
        
        if addrc3 in legacy_btc_list or addru3 in legacy_btc_list or addr33 in segwit_btc_list or addrb3 in bech32_btc_list:
            print('============== KEYFOUND ==============')
            print('PrivateKey :', hex(pl2n) )
            print('[C]',addrc3,'[U]',addru3)
            print('[3]',addr33,'[bc]',addrb3)
            print('======================================')
            
        if addrc4 in legacy_btc_list or addru4 in legacy_btc_list or addr34 in segwit_btc_list or addrb4 in bech32_btc_list:
            print('============== KEYFOUND ==============')
            print('PrivateKey :', hex(np) )
            print('[C]',addrc4,'[U]',addru4)
            print('[3]',addr34,'[bc]',addrb4)
            print('======================================')
            
        if addrc5 in legacy_btc_list or addru5 in legacy_btc_list or addr35 in segwit_btc_list or addrb5 in bech32_btc_list:
            print('============== KEYFOUND ==============')
            print('PrivateKey :', hex(npln) )
            print('[C]',addrc5,'[U]',addru5)
            print('[3]',addr35,'[bc]',addrb5)
            print('======================================')
            
        if addrc6 in legacy_btc_list or addru6 in legacy_btc_list or addr36 in segwit_btc_list or addrb6 in bech32_btc_list:
            print('============== KEYFOUND ==============')
            print('PrivateKey :', hex(npl2n) )
            print('[C]',addrc6,'[U]',addru6)
            print('[3]',addr36,'[bc]',addrb6)
            print('======================================')

        if m%10000 == 0: 
            if verbosity is True: print('[+] Completed : ', 6*m,\
                  '[C-1]',addrc1,'[U-1]',addru1, '[3-1]',addr31,'[bc-1]',addrb1, \
                  '[C-2]',addrc2,'[U-2]',addru2, '[3-2]',addr32,'[bc-2]',addrb2, \
                  '[C-3]',addrc3,'[U-3]',addru3, '[3-3]',addr33,'[bc-3]',addrb3, \
                  '[C-4]',addrc4,'[U-4]',addru4, '[3-4]',addr34,'[bc-4]',addrb4, \
                  '[C-5]',addrc5,'[U-5]',addru5, '[3-5]',addr35,'[bc-5]',addrb5, \
                  '[C-6]',addrc6,'[U-6]',addru6, '[3-6]',addr36,'[bc-6]',addrb6, \
                  end='\r')
            else: print('[+] Completed : ', 6*m, end='\r')
    print('', end='\r')
    
###############################################################################