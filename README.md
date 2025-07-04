# SoccerEventManager
A desktop python application for coaches. Tracks player stats by lifetime, by season, and by game

# How to Install
The Soccer Event Manager is not in a state where it can be compiled and run. The Create_User however, can be. Requires the user to have python installed with the following libraries:
- bcrypt: Used for one-way password hashing
- Pillow (PIL): Used for image manipulation

Simply make sure you keep the same file structure as the repo

# Version History

## Version 0.3 (Current)
No changes to the main concept of the soccer manager for now. This update focussed on the user creation side of things. Implemented another app called Create_User (My creativity knows no bounds) which allows users marked as admin to create a new user. If no admins currently exists, uses a hardcoded admin login. Technically unsafe, but any app operating on a single machine is at the mercy of the machine user, so secure enough.
### Added Features
- User Creation
- Profile Images (320x320)
### Known Issues
- None 

## Version 0.2
Further implementation of the FileManager module (not a class anymore), which allows saving. Also added two new modules which will be in charge of data security. Been a while since my last update, but works been crazy.
### Added Features
- Saving to files
- Encryption/Decryption of data
- New file structure
- User login backend
### Known Issues
- Either FileManager needs some way to pass along the data key required to decrypt/encrypt files, or EncryptionManager will have to be accessed by my DataManager
- Still need to actually implement DataManager
- Still needs a UI

## Version 0.1
First release of code to the repository. Currently only features a class for reading from file structure. Does not support saving data at the moment.
### Added Features
- Reading from files
- Writing errors to log.txt
- Creating directories
### Known Issues
- Need to implement ability to save data
- Need to implement class to track/manage the data
- Need to create a UI
