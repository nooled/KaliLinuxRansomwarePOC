# KaliLinuxRansomwarePOC
This is a Proof of Concept Kali Linux program of a ransomware that encrypts a sections of a user's filesystem and requests for a ransom to be paid in return for the key that will be used for decryption and file recovery

This program currently encrypts the following directories:
/home/{username}/testfiles
/home/{username}/Documents
/home/{username}/Music
/home/{username}/Pictures
/home/{username}/Videos

please update them or ensure you have nothing important in these directories before executing the payload

Update sendemail.py to your own email for testing

private key .pem file will need to be in the same directory as the .py/.exe files for the decryption button to work

You can either "python3 encryptor.py" or compile into an .exe to run the program

Run this code to compile the files into an .exe (change whatever you need in the .py files before doing this)
pyinstaller --onefile --hidden-import='PIL._tkinter_finder' --add-data="2spookybgnew.jpg:." encryptor.py

you may need to create a virtual environment for the pyinstaller builder to work correctly
