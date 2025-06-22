import os
import base64
import json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend


# This is storing in the same directory for now, but in the future it should be stored in a different directory
KEY_STORE_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ITERATIONS = 100000

backend = default_backend()

def generate_salt(length = 16):
	# Generate a random byte string of given length
	return os.urandom(length)
	
def derive_key(password, salt, iterations = DEFAULT_ITERATIONS):
	# This function takes password, salt, and iterations, and returns a URL-safe Base64 encoded key
	
	kdf = PBKDF2HMAC(
		algorithm = hashes.SHA256(),
		length = 32,
		salt = salt
		iterations = iterations,
		backend = backend,
	)
	return base64.urlsafe_b64encode(kdf.derive(password.encode()))
	
def generate_data_key():
	# Creates a b64 encoded key
	return Fernet.generate_key()
	
def wrap_data_key(dataKey, derivedKey):
	# Encrypts the dataKey with the users password (derivedKey)
	return Fernet(derivedKey).encrypt(dataKey)
	
def unwrap_data_key(wrappedKye, derivedKey):
	return Fernet(derivedKey).decrypt(wrappedKey)
	
def save_user_key(username, wrappedKey, salt, iterations = DEFAULT_ITERATIONS):
	# Save specific users wrapped data key

	os.makedirs(os.path.dirname(KEY_STORE_PATH), exist_ok = True)
	data = load_user_keys()
	data[username] = {
		"wrapped_key": base64.b64encode(wrappedKey).decode(),
		"salt": base64.b64encode(salt).decode(),
		"iterations": iterations
	}
	with open(KEY_STORE_PATH, "w") as f:
		json.dump(data, f, indent = 4)
		
def load_user_keys():
	# Load all user key entries

	if not os.path.exists(KEY_STORE_PATH):
		return {}
	with open(KEY_STORE_PATH, "r") as f:
		return json.load(f)
		
def get_user_entry(username):
	# Searches data for given username

	users = load_user_keys()
	return users.get(username)
	
def setup_user(username, password, dataKey):
	# Create a new derivedKey from salt and password

	salt = generate_salt()
	derivedKey = derive_key(password, salt)
	if not dataKey:
		dataKey = generate_data_key()
	wrappedKey = wrap_data_key(dataKey, derivedKey)
	save_user_key(username, wrappedKey, salt)
	return dataKey
	
def login_user(username, password):
	# Loads the user and unwraps the data key

	entry = get_user_entry(username)
	if not entry:
		raise ValueError("User not found")
	salt = base64.b64decode(entry["salt"])
	wrappedKey = base64.b64decode(entry["wrapped_key"])
	iterations = entry.get("iterations", DEFAULT_ITERATIONS)
	derivedKey = derive_key(password, salt, iterations)
	return unwrap_data_key(wrappedKey, derivedKey)