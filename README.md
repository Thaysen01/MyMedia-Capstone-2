# MyMedia - Capstone 2 Project

# Usage:
### Install this by cloning the git repository. 
### To use these applications, the user will need to launch the host application ($ python3 .\host_app.py). Upon launching this, they will be prompted to add or manage their media. They will put in media from their device, such as the media file path, an image file path, and the media type (song/movie). Once the media has been uploaded, they may add additional items, remove old ones, or stream their media to another device. 
### Once completed, a port will open for streaming; on another device, a user will then need to launch the client application ($ python3 .\client_app.py). Upon launching this application, the user will need to connect to the host device's IPv4 Address (the host can find this with: $ ipconfig). The user will then be able to see the Movies and Songs that are ready to be streamed! 
- It should be noted that when running these commands the user needs to be in the exact directory these files are stored in (host_app & client_app respectively).
- With the current implementation, streaming is only available on the same network. 

# Versions:
### These are the versions of the tools and libraries used to run these applications:
- Python3 : 3.12.8  [programming language]
- Pip :     25.0    [package manager]
- PyQt6 :   6.8.0   [library]
- Pillow :  11.1.0  [library]

# Installation: 
### This program is expected to function in future versions. Ensure these are all installed on the device. 
- sudo apt update && sudo apt install -y python3
- sudo apt install -y python3-pip
- pip3 install PyQt6
- pip3 install Pillow

# Database Information
- DB Browser For SQLite v3.13.1
-   https://github.com/sqlitebrowser/sqlitebrowser/releases/tag/v3.13.1-rc1

### This project was created to implement something practical that we found to be less common in project development. Our team of four Computer Science majors worked on different sections of the program. We had in-person brainstorming and status meetings to pull together pieces of our project into one product. We used the liveshare extension to work on one device remotely for many of our later commits. 
