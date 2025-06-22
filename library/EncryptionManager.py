import json
from cryptography.fernet import Fernet

dataKey = None
cipher = None

def set_data_key(key):
	# Sets the value of the cipher
	dataKey = key
	cipher = Fernet(dataKey)
	
def encrypt_json(data):
	# Takes the given data, and returns the encrypted version
	jsonData = json.dumps(data).encode('utf-8)
	return cipher.encrypt(jsonData)
	
def decrypt_json(data):
	# Takes the given data, and decrypts it to JSON
	decryptedData = cipher.decrypt(encryptedData)
	return json.loads(decryptedData.decode('utf-8'))