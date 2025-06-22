# SoccerEventManager
A desktop python application for coaches. Tracks player stats by lifetime, by season, and by game

# How to Install
Not currently possible. The application logic is currently incomplete

# Version History

## Version 0.2 (Current)
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
