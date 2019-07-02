#All import we need,OS-get filesize the file encryting
import os
import getpass
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

#function of encryting

def encrypt(key,filename):
    #read 64*1024 byte file at a time.
    chunksize = 64*1024
    outputFile = "(encrypted)"+filename
    #zfill returns the string with 0 filled at start
    filesize = str(os.path.getsize(filename)).zfill(16)
    #used to randomise produce distinct cipher text(initialization vector)
    IV = Random.new().read(16)

    encryptor = AES.new(key,AES.MODE_CBC,IV)

    with open(filename,'rb') as infile:
        with open(outputFile,'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)
            
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    #padding by byte
                    chunk += b' '  * (16 - (len(chunk) % 16))                
                
                outfile.write(encryptor.encrypt(chunk))

def decrypt(key,filename):
    chunksize = 64 * 1024
    #output file without (encrypted) keyword
    outputFile = filename[11:]

    with open(filename,'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)

        decrytor = AES.new(key,AES.MODE_CBC,IV)

        with open(outputFile,'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decrytor.decrypt(chunk))

            #shorten the filesize
            outfile.truncate(filesize)

def getKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

def Main():
    choice = input("Would you like to (E)ncrypt or (D)ecrypt?: ")
    if choice == 'E' or choice == 'e':
        filename = input("File to Encrypt: ")
        password = input("Password: ")

        encrypt(getKey(password),filename)

    elif choice == 'D' or choice == 'd':
        filename = input("File to Decrypt: ")
        password = getpass.getpass("Enter password:")
        decrypt(getKey(password),filename)
        print("Done.")
    
    else:
        print("No option selected!..")n

if __name__ == "__main__":
    Main()
