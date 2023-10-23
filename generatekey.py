'''
pip install pycryptodome
'''
import os
import random
import string
import getpass
from Crypto.PublicKey import RSA

def generate_key():
    key = RSA.generate(2048)
    privateKey = key.export_key()
    publicKey = key.publickey().export_key()

    # Generate a random reference number of 10 characters
    characters = string.ascii_letters + string.digits  
    reference_number = ''.join(random.choice(characters) for _ in range(10))

    # Need to be root user for the permissions to work, so change the username
    # to yours
    username = 'syed'
    # Construct the path to the Desktop directory
    desktop_path = os.path.join('/home', username, 'Desktop')
    #desktop_path = os.path.expanduser('/home/syed/Desktop')
    file_path = os.path.join(desktop_path, 'reference_number.txt')

    with open(file_path, 'w') as file:
        file.write('This is your reference number, don''t lose it!\n' + reference_number)
        
    private_name = reference_number + '_private.pem'

    public_name = reference_number + '_public.pem'

    # save private key to file
    #with open(private_name, 'wb') as f:
    #    f.write(privateKey)

    # save public key to file
    #with open(public_name, 'wb') as f:
    #    f.write(publicKey)

    #print('Private key saved to private.pem')
    #print('Public key saved to public.pem')
    #print('Keygen Done')
    #print(f"keygen ref: {reference_number}")
    return reference_number, privateKey, publicKey, private_name
    #print(privateKey)
