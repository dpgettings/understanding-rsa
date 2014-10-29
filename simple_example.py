from __future__ import division, print_function
import sys
import math

# ###############################################
# Modular Exponentiation Function
# ###############################################
def modpow(base=None, exponent=None, modulus=None):
    """
    Translated from pseudocode example found at: 
    https://en.wikipedia.org/wiki/Modular_exponentiation

    Equivalent to calculating:
       result = base**exponent % modulus
    """
    assert base is not None
    assert exponent is not None
    assert modulus is not None
    #Assert :: (modulus - 1) * (modulus - 1) does not overflow base

    n_iter = 0
    result = 1
    base = base % modulus
    while exponent > 0:
        n_iter += 1
        if (exponent % 2 == 1):
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

# ###############################################
# Break message into chunks
# ###############################################
def chunk_message_hex(message_hex_str, chunkbytes=1):

    # Pad message to be multiple of chunkbytes
    message_nbytes = len(message_hex_str) // 2  # Each hex digit is 4 bits
    message_padbytes = chunkbytes - (message_nbytes % chunkbytes)
    message_padding = '00' * message_padbytes
    padded_message_hex_str = message_hex_str + message_padding
    padded_message_nbytes = len(padded_message_hex_str) // 2  # Each hex digit is 4 bits
    # Chunk message
    num_chunks = padded_message_nbytes // chunkbytes
    chunked_message_hex_str = []
    for i in xrange(num_chunks):
        chunk_slice = slice(i*chunkbytes*2, (i+1)*chunkbytes*2)
        chunked_message_hex_str.append(padded_message_hex_str[chunk_slice])

    return chunked_message_hex_str


# ###############################################
# Main Program
# ###############################################

### Choose two prime numbers
p1 = 53
p2 = 59

# ==================================
# Step 1 -- Generate Public Key
# ==================================

### Choose exponent e. Requirements:
### (1) Integer; (2) Not a factor of n=p1*p2; (3) 1 < e < phi(n)
e = 3  # Choose 3 for the sake of example

### Generate public key
# The "public key" is, in some sense, both n and e
pubkey = {}
pubkey['n'] = p1 * p2
pubkey['e'] = e 

print("\nPRIMES-----------------------------------------------------------------------")
print("P1 = {} \nP2 = {}".format(p1,p2))

print("\nPUBLIC KEY-----------------------------------------------------------------------")
print("n = {n} \ne = {e}".format(**pubkey))

# ==================================
# Step 2 -- Generate Private Key
# ==================================

### Calculate phi(n)
phi_n = (p1 - 1) * (p2 - 1)

### Calculate Private Key
privkey = {}
privkey['d'] = (2 * phi_n + 1) // e
privkey['n'] = pubkey['n']


print()
print("phi(n) = {}".format(phi_n))

print("\nPRIVATE KEY-----------------------------------------------------------------------")
print("d = {d} \nn = {n}".format(**privkey))


# ==================================
# Step 3 -- Encryption with Public Key
# ==================================

# ### Select a message
message = "OHAI you can read me!"

### CHUNK THE MESSAGE UP
message_hex_str = message.encode('hex')
message_hex_chunks = chunk_message_hex(message_hex_str)
message_int_chunks = map(lambda x: int(x,16), message_hex_chunks)
### Encrypt the message
encrypted_message_int_chunks = map(lambda x: pow(x, pubkey['e'], pubkey['n']), message_int_chunks)



# ==================================
# Step 4 -- Decryption with Private Key
# ==================================
### Decryption function (for encrypted message c):  
###    m(c) = c**d % n
decrypted_message_int_chunks = map(lambda x: pow(x, privkey['d'], privkey['n']), encrypted_message_int_chunks)


print(message_int_chunks)
print(encrypted_message_int_chunks)
print(decrypted_message_int_chunks)



