# YouTube Downloader
By [LemonPi314](https://github.com/LemonPi314)

Download YouTube videos in varying resolutions and bitrates.
## Requirements
### Python File
Any operating system with Python.
- [Python 3.9](https://www.python.org/downloads/) or higher
- [`pytube`](https://pypi.org/project/pytube/)
- [`PySimpleGUI`](https://pypi.org/project/PySimpleGUI/)
- Internet connection
### Windows Systems
Optional executable file for Windows users. Python and the required packages are included in the executable.
- 10 MB of free space for the executable
- 12 MB of free space for temporary files
- Internet connection
## Usage
Paste the URL of the video into the URL field, select an output folder, and click "Get Info". After a few seconds a list of available streams will appear. Select the streams you would like to download and click "Download".

Some streams have both video and audio tracks. However, some streams have only the video track or only the audio track, which will download as separate files. You can combine video and audio tracks using a tool such as [FFmpeg](https://ffmpeg.org/).  
To play some streams you will need to install a codec extension such as the AV1 Video Extension from the Microsoft Store on Windows.
## License
[MIT License](https://choosealicense.com/licenses/mit/)