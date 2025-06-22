import os
import json
import library.EncryptionManager as em

# ------------------- CONSTANT PATHS ------------------------

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "Data")

# Directory Paths
PLAYERS_DIR = os.path.join(DATA_DIR, "Players")
PLAYER_IMAGES_DIR = os.path.join(PLAYERS_DIR, "Images")
SEASON_DIR = os.path.join(DATA_DIR, "Seasons")
GAMES_DIR = os.path.join(DATA_DIR, "Games")
CONFIG_DIR = os.path.join(DATA_DIR, "Config")

# Index Files
PLAYER_LIST = os.path.join(PLAYERS_DIR, "playerList.json")
SEASON_LIST = os.path.join(SEASONS_DIR, "seasonList.json")
GAME_LIST = os.path.join(GAMES_DIR, "gameList.json")
OPTIONS_FILE = os.path.join(CONFIG_DIR, "options.json")
LOG_FILE = os.path.join(CONFIG_DIR, "log.txt")

# ------------------- INTIALIZATION -------------------------

def ensure_directories_exist():
	os.makedirs(PLAYER_IMAGES_DIR, exist_ok = True)
	os.makedirs(SEASONS_DIR, exist_ok = True)
	os.makedirs(GAMES_DIR, exist_ok = True)
	os.makedirs(CONFIG_DIR, exist_ok = True)
	
# Make sure method is called on import
ensure_directories_exist()

# ------------------- PATH HELPERS --------------------------

def get_player_path(uid):
	return os.path.join(PLAYERS_DIR, f"{uid}.json")
	
def get_player_image_path(uid, ext = "webp")
	return os.path.join(PLAYER_IMAGES_DIR, f"{uid}.{ext}")
	
def get_season_path(uid):
	return os.path.join(SEASONS_DIR, f"{uid}.json")
	
def get_game_path(uid):
	return os.path.join(GAMES_DIR, f"{uid}.json")
	
# ------------------- JSON HELPERS --------------------------

def load_encrypted_json(path, default = None):
	# Loads encrypted file at given path, converts to json
	
	try:
		with open(path, "rb") as file:
			encrypted_data = file.read()
		return em.decypt_json(encrypted_data)
		
	except FileNotFoundError:
		return default if default is not None else {}
		
	except Exception as e:
		log_error(f"Error loading encrypted file '{path}': {e}")
		return default if default is not None else {}
		
def save_json(path, data):
	# Encrypt data, then save to path
	
	try:
		encrypted_data = em.encrypt_json(data)
		with open(path, "wb") as file:
			file.write(encrypted_data)
		
	except Exception as e:
		log_error(f"Error saving encrypted file '{path}': {e}")
		
# ------------------- LOGGING -------------------------------

	def log_error(message):
		with open(LOG_FILE, "a", encoding = "utf-8") as log:
			log.write(message + "\n")
			
# ------------------- FUNCTIONS INTENDED FOR USE ------------

# ------------------- PLAYER FUNCTIONS ----------------------

def load_player (uid):
	# Load player data by UID, return none if not found
	path = get_player_path(uid)
	data = load_encrypted_json(path, default = None)
	return data
	
def save_player(uid, playerData):
	# Save player data to file by UID
	path = get_player_path(uid)
	save_encrypted_json(path, playerData)
	
# ------------------- SEASON FUNCTIONS ----------------------

def load_season(uid):
	# Load season by UID
	path = get_season_path(uid)
	data = load_encrypted_json(path, default = None)
	return data
	
def save_season(uid, seasonData):
	# Save data to uid
	path = get_season_path(uid)
	save_encrypted_json(path, seasonData)
	
# ------------------- GAME FUNCTIONS ------------------------

def load_game(uid):
	# Load game by UID
	path = get_game_path(uid)
	data = load_encrypted_json(path, default = None)
	return data
	
def save_game(uid, gameData):
	# Save data to UID
	path = get_game_path(uid)
	save_encrypted_json(path, gameData)
	