import os
import PySimpleGUI as sg
from pytube import YouTube, Stream

sg.theme('Black')

layout = [
    [
        sg.Column([
            [sg.Text("URL", key='url_title')], 
            [sg.Input(key='url', size=(54, 1))], 
            [sg.Text(key='url_text', size=(40, 2))], 
            [sg.Text("Output folder", key='output_dir_title')], 
            [sg.Input(key='output_dir'), sg.FolderBrowse()], 
            [sg.Text(key='output_dir_text', size=(40, 2))], 
            [sg.Button("Get info", key='next_button')], 
            [sg.Text("Info", key='info_title')], 
            [sg.Multiline(key='video_info', size=(54, 5), disabled=True, no_scrollbar=True)]
        ], vertical_alignment='top'),
        sg.VerticalSeparator(),
        sg.Column([
            [sg.Text("Streams", key='stream_list_title')], 
            [sg.Listbox(values=[], key='stream_list', size=(40, 16), enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)], 
            [sg.Button("Download", key='download_button', disabled=True)]
        ], vertical_alignment='top')
    ],
    [
        sg.Column([
            [sg.Text(key='progress_text', size=(40, 1))], 
            [sg.ProgressBar(max_value=1000, key='progress_bar', size=(65, 20))]
        ], justification='center')
    ]
]

def progressUpdate(stream, chunk, bytesRemaining):
    totalSize = stream.filesize
    bytesDone = totalSize - bytesRemaining
    percent = round(bytesDone / totalSize * 100)
    window['progress_text'].update("Downloading... {}% ({}/{})".format(percent, currentItem, items))
    progressBar.update(bytesDone, totalSize)

def formatStreams(streams: list[Stream]):
    formattedStreams = []
    for stream in streams:
        formattedStream = []
        if stream.includes_video_track:
            formattedStream.append("Video")
            formattedStream.append(stream.subtype)
            formattedStream.append(stream.resolution)
            formattedStream.append(str(stream.fps) + "fps")
            if stream.filesize > 1024 * 1024:
                formattedStream.append(str(round(stream.filesize / (1024 * 1024), 2)) + " MB")

            else:
                formattedStream.append(str(round(stream.filesize / 1024, 2)) + " KB")
        
        if stream.includes_audio_track:
            formattedStream.insert(1, "Audio")

        if not stream.includes_video_track:
            formattedStream.append(stream.subtype)
            formattedStream.append(stream.abr)
            formattedStream.append(stream.audio_codec)
            if stream.filesize > 1024 * 1024:
                formattedStream.append(str(round(stream.filesize / (1024 * 1024), 2)) + " MB")

            else:
                formattedStream.append(str(round(stream.filesize / 1024, 2)) + " KB")

        formattedStreams.append(", ".join(formattedStream))
    
    return formattedStreams

window = sg.Window("YouTube Downloader", layout)
progressBar = window['progress_bar']
currentItem = 0
while(True):
    window.refresh()
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    elif event == 'next_button':
        if not os.path.exists(values['output_dir']):
            window['output_dir_text'].update("Invalid folder", text_color='red')

        if values['url'] == '' or values['url'] is None:
            window['url_text'].update("Invalid URL", text_color='red')

        elif os.path.exists(values['output_dir']):
            window['output_dir_text'].update('')
            window['url_text'].update('')
            try:
                window['progress_text'].update("Getting info...")
                window.refresh()
                video = YouTube(values['url'], on_progress_callback=progressUpdate)
                window['video_info'].update(
                    "Title: " + str(video.title) + "\n" +
                    "Author: " + str(video.author) + "\n" +
                    "Views: " + str(video.views) + "\n" +
                    "Length: " + str(video.length) + "\n" +
                    "Published: " + str(video.publish_date)
                )
                formattedStreams = formatStreams(video.streams)
                window['stream_list'].update(formattedStreams)
                window['progress_text'].update('')
                window.refresh()

            except:
                window['progress_text'].update("Failed to get info", text_color='red')

    elif event == 'download_button':
        try:
            items = len(values['stream_list'])
            for stream in values['stream_list']:
                currentItem += 1
                index = formattedStreams.index(stream)
                prefix = None
                videoStream = video.streams[index]
                if os.path.exists(values['output_dir'] + '/' + videoStream.default_filename):
                    prefix = str(currentItem) + '-'
                    
                videoStream.download(values['output_dir'], None, prefix)

            window['progress_text'].update("Downloaded 100% ({}/{})".format(items, items))

        except:
            window['progress_text'].update("Failed to download", text_color='red')

    if values['stream_list'] != []:
        window['download_button'].update(disabled=False)

    elif values['stream_list'] == []:
        window['download_button'].update(disabled=True)

window.close()