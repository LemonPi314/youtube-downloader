import os
import PySimpleGUI as sg
from pytube import YouTube

sg.theme('Black')

layout = [
    [sg.Text("URL", key='url_title')], 
    [sg.Input(key='url')], 
    [sg.Text(key='url_text', size=(40, 2))], 
    [sg.Text("Output folder", key='output_dir_title')], 
    [sg.Input(key='output_dir'), sg.FolderBrowse()], 
    [sg.Text(key='output_dir_text', size=(40, 2))], 
    [sg.Button("Download", key='download_button')]
]

window = sg.Window("YouTube Downloader", layout)
while(True):
    window.refresh()
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    elif event == 'download_button':
        if not os.path.exists(values['output_dir']):
            window['output_dir_text'].update("Invalid folder", text_color='red')

        if values['url'] == '' or values['url'] is None:
            window['url_text'].update("Invalid URL", text_color='red')

        elif os.path.exists(values['output_dir']):
            window['output_dir_text'].update('')
            window['url_text'].update('')
            try:
                video = YouTube(values['url'])
                videoStream = video.streams.get_highest_resolution()
                videoStream.download(values['output_dir'])
                window['url_text'].update("Successfully downloaded", text_color='green')

            except:
                window['url_text'].update("Invalid URL", text_color='red')

window.close()