import json
import os
import datetime

class FileManager:

	# Private Variables
	__season = ""
	__event = ""
	
	# Constant Variables
	__ERROR_LOG = "./log.txt"
	__SEASON_LIST = "./data/Seasons.json"
	__ACTIVE_PLAYERS = "./data/ActivePlayers.json"
	__RETIRED_PLAYERS = "./data/RetiredPlayers.json"
	__OPTIONS = "./data/Options.json"
	
	# When program starts, erase error log
	def __init__(self):
		if os.path.isfile(self.__ERROR_LOG):
			try:
				os.remove(self.__ERROR_LOG)
			except FileNotFoundError:
				self.log_error(f"File '{self.__ERROR_LOG}' not found.")
			except PermissionError:
				self.log_error(f"Permssion denied to delete file '{self.__ERROR_LOG}'.")
			except Exception as e:
				self.log_error(f"Error occurred while deleting file '{self.__ERROR_LOG}': {e}")
		
	# Read the seasons list from file
	def get_season_list(self):
		return self.__read_data_file(self.__SEASON_LIST)
				
	# Read active players from file
	def get_active_players(self):
		return self.__read_data_file(self.__ACTIVE_PLAYERS)
		
	# Read retired players from file
	def get_retired_players(self):
		return self.__read_data_file(self.__RETIRED_PLAYERS)
		
	# Read options from file:
	def get_options(self):
		return self.__read_data_file(self.__OPTIONS)
		
	# Sets the current season. If new season, must have 'n' flag
	def set_season(self, seasonName):
		
		# check directory exists
		if os.path.isdir(f"./{seasonName}"):
			self.__season = f"./{seasonName}")
		else
			self.log_error(f"Season '{seasonName}' not found", True)
			
	# Creates new season and sets it as active
	def create_season(self, seasonName):
	
		# Make sure season doesn't already exist
		if os.path.isdir(f"./{seasonName}"):
			self.log_error(f"Season '{seasonName}' already exists", True)
			
		# set season to new season
		self.__season = f"./{seasonName}"
	
	# Read event list from ./data/SEASON_NAME
	def get_season_events(self):
		return self.__read_data_file(f"{self.__season}/EventList.json")
		
	# Read player list from ./data/SEASON_NAME
	def get_season_players(self):
		return self.__read_data_file(f"{self.__season}/Players.json")
	
	# Sets the current event
	def set_event(self, eventName):
	
		# Check season has been set first
		if not self.__season:
			self.log_error("No season is set", True)
		
		# check directory exists
		if os.path.isdir(f"{self.__season}/{eventName}"):
			self.__event = f"{self.__season}/{eventName}"
		else
			self.log_error(f"Event '{eventName}' not found", True)
			
	# Creates new event, set it as active
	def create_event(self, eventName):
		
		# Check season has been set first
		if not self.__season:
			self.log_error("No season is set", True)
			
		# Make sure event doesn't already exist
		if os.path.isdir(f"{self.__season}/{eventName}"):
			self.log_error(f"Event '{eventName}' already exists", True)
			
		# Set event to new event
		self.__event = f"{self.__season}/{eventName}"
	
	# Read event data from ./data/SEASON_NAME/EVENT_NAME
	def get_event(self):
		return self.__read_data_file(f"{self.__event}/Event.json")
	
	# Read player data from ./data/SEASON_NAME/EVENT_NAME
	def get_event_players(self):
		return self.__read_data_file(f"{self.__event}/Players.json")
	
	# If an error occurs, log it
	def log_error(self, error: str, hardStop: bool = False):
		with open(self.__ERROR_LOG, "a") as file:
			file.write(f"{datetime.datetime.now()}:\n{error}\n\n")
			
		if hardStop:
			raise Exception(error)
			
	# ----------------------- PRIVATE FUNCTIONS -------------------------
	
	# Read data from file and return it
	def __read_data_file(self, filepath: str):
	
		# Check file exists and is not empty
		if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
			os.makedirs(os.path.dirname(filepath), exist_ok = True)
			return []
			
		# Open file, return list
		with open(filepath, "r") as file:
			try:
				return json.load(file)
			except json.JSONDecodeError as e:
				self.log_error(f"JSON Decode Error: {e}")
				return []