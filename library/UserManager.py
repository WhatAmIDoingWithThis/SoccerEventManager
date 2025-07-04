import json
import os
import bcrypt
from PIL import Image
import uuid
from datetime import datetime

class UserManager:
	
	def __init__(self, filepath):
		self.filepath = filepath
		data_dir = os.path.dirname(filepath)
		image_dir = os.path.join(data_dir, "userImages")
		os.makedirs(image_dir, exist_ok = True)
		if not os.path.exists(filepath):
			with open(filepath, "w") as file:
				json.dump({}, file)
				
	def create_user(self, username, password, role, image_path = None):
	
		# Verify user doesn't exist
		users = self._load_users()
		if username in users:
			return False
			
		# Copy Image to data/userImages if given
		saved_image_path = ""
		if image_path and os.path.isfile(image_path):
			os.makedirs(os.path.join("data", "userImages"), exist_ok = True)
			file_ext = os.path.splitext(image_path)[1]
			unique_name = f"{uuid.uuid4().hex}{file_ext}"
			dest_path = os.path.join("data", "userImages", unique_name)
			
			# Resizing + Saving code
			try:
				with Image.open(image_path) as img:
					resized_img = img.resize((320, 320))
					resized_img.save(dest_path)
				saved_image_path = dest_path
			except Exception as e:
				print(f"Image resizing failed: {e}")
				saved_image_path = ""
			
			
		# Save user
		hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
		users[username] = {
			"password": hashed_pw,
			"role": role,
			"profile_image": saved_image_path
		}
		self._save_users(users)
		return True
		
	def _load_users(self):
		try:
			with open(self.filepath, "r") as file:
				return json.load(file)
		except (json.JSONDecodeError, FileNotFoundError):
		
			# Verify backup directory exists
			backup_dir = os.path.join("data", "backups")
			os.makedirs(backup_dir, exist_ok = True)
			
			# Backup data
			if os.path.exists(self.filepath):
				timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
				base_filename = os.path.basename(self.filepath).replace(".json", "")
				backup_path = os.path.join(backup_dir, f"{base_filename}_corrupt_{timestamp}.json")
				os.rename(self.filepath, backup_path)
				print(f"[WARN] Corrupted users.json backed up to {backup_path}")
				
			# Reset data
			with open(self.filepath, "w") as file:
				json.dump({}, file)
			return {}
			
	def _save_users(self, users):
		with open(self.filepath, "w") as file:
			json.dump(users, file, indent = 4)