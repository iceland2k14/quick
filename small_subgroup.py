# -*- coding: utf-8 -*-
"""
Usage :
 > python small_subgroup.py 
 
@author: iceland
"""
# import gmpy2
# from fastecdsa import curve
# from fastecdsa.point import Point
# import bit
import random
import ctypes
# =============================================================================
# G = curve.secp256k1.G
# N = curve.secp256k1.q
# 
# factor1 = 107361793816595537
# factor2 = 174723607534414371449
# factor3 = 341948486974166000522343609283189
# k = factor1 * factor2 * factor3
# 
# btc_list = ['1PSRcasBNEwPC2TWUB68wvQZHwXy4yqPQ3',
#             '1B5USZh6fc2hvw2yW9YaVF75sJLcLQ4wCt',
#             '1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm',
#             '1JPbzbsAx1HyaDQoLMapWGoqf9pD5uha5m']
# =============================================================================
print('[+] Program Starting ... Please Wait')
ice = ctypes.CDLL('ice_secp256k1.dll')
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
###############################################################################

while True:
    a_largebit_number = random.randint(2**225, 2**235)
    # k = gmpy2.next_prime(a_largebit_number)    # factor1 * factor2 * factor3
    k = a_largebit_number
    print('\n[+] Starting search for the subgroup :', hex(k))
    
    for m in range(1, N//k):
        small_subgroup_pvk = m * k
        addrc = privatekey_to_address(ctypes.c_int(0), True, small_subgroup_pvk)
        addru = privatekey_to_address(0, False, small_subgroup_pvk)
        addr3 = privatekey_to_address(1, True, small_subgroup_pvk)
        addrb = privatekey_to_address(2, True, small_subgroup_pvk)

        if addrc in legacy_btc_list or addru in legacy_btc_list or addr3 in segwit_btc_list or addrb in bech32_btc_list:
            print('============== KEYFOUND ==============')
            print('PrivateKey :', hex(small_subgroup_pvk) )
            print('[C]',addrc,'[U]',addru)
            print('[3]',addr3,'[bc]',addrb)
            print('======================================')

        if m%10000 == 0: print('[+] Completed : ', m,'[C]',addrc,'[U]',addru, '[3]',addr3,'[bc]',addrb, end='\r')
    print('', end='\r')
# =============================================================================
# def factors(n):
#     result = set()
#     n = gmpy2.mpz(n)
#     for i in range(1, gmpy2.isqrt(n) + 1):
#         div, mod = divmod(n, i)
#         if not mod:
#             result |= {gmpy2.mpz(i), div}
#     return result
# =============================================================================
