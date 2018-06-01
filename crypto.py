import os 
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

def encrypt(key, filename, infile):
	chunksize = 64*1024
	outputfile = "(encrypted)"+filename
	dir(infile)
	filesize = str(infile.content_length).zfill(16)

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
	outputfile = "sharefolder/"+filename.split('/')[-1][11:]
	with open(filename, 'rb') as infile:
		filesize = int(infile.read(16))
		IV = infile.read(16)

		decryptor = AES.new(key, AES.MODE_CBC, IV)
		with open(outputfile, "wb") as outfile:
			while True:
				chunk = infile.read(chunksize)
				if len(chunk) == 0:
					break
				data = decryptor.decrypt(chunk)
				print(data)
				outfile.write(data)
			# to remove every spaces that was added to make 16 byte
			outfile.truncate(filesize)
		
	os.system("rm "+"\\(encrypted\\)"+filename)


def getkey(password="somethingjustlikeyou"):
	hasher = SHA256.new(password.encode('utf-8'))
	return hasher.digest()

