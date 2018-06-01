import os 
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

def encrypt(key, filename, infile):
	chunksize = 64*1024
	outputfile = "(encrypted)"+filename

	filesize = str(infile.st_size).zfill(16)

	IV = Random.new().read(16)

	encryptor = AES.new(key, AES.MODE_CBC, IV)

	# with open(filename, "rb") as infile:
	with open(outputfile, "wb") as outfile:
		outfile.write(filesize.encode('utf-8'))
		outfile.write(IV)

		while True:
			chunk = infile.read(chunksize)

			if len(chunk) == 0:
				break
			elif len(chunk) % 16 != 0:
				# To make every chunk a byte 16 we add spaces.
				chunk +=b' ' * (16 - (len(chunk) % 16))
			outfile.write(encryptor.encrypt(chunk))
	f = open(outputfile, "rb")
	return f

def decrypt(key, filename):
	if not os.path.exists('sharefolder'):
		os.makedirs('sharefolder')
	chunksize = 64*1024
	
	with open(filename, 'rb') as infile:
		filesize = int(infile.read(16))
		IV = infile.read(16)

		decryptor = AES.new(key, AES.MODE_CBC, IV)
		with open("sharefolder/"+filename, "wb") as outfile:
			while True:
				chunk = infile.read(chunksize)
				if len(chunk) == 0:
					break
				outfile.write(decryptor.decrypt(chunk))
			# to remove every spaces that was added to make 16 byte
			outfile.truncate(filesize)
		
	os.system("rm "+"(encrypted)"+filename)


def getkey(password="somethingjustlikeyou"):
	hasher = SHA256.new(password.encode('utf-8'))
	return hasher.digest()

# def main():
# 	choice = raw_input("Would you like to E or D? :")
# 	if choice == "e":
# 		filename = raw_input("File to encrypt : ")
# 		encrypt(getkey(), filename)
# 		print("Encryption Done>")
# 	elif choice == "d":
# 		filename = raw_input("File to decrypt: ")
# 		decrypt(getkey(), filename)
# 		print("Decryption Done>")

# main()
