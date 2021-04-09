from os import path
import PySimpleGUI as sg
from pytube import YouTube, Stream

sg.theme('Black')

layout = [
    [
        sg.Column([
            [sg.Text("Video URL", key='url_title')], 
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
            [sg.Listbox(values=[], key='stream_list', size=(54, 16), enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)], 
            [sg.Button("Download", key='download_button', disabled=True)]
        ], vertical_alignment='top')
    ],
    [
        sg.Column([
            [sg.Text(key='progress_text', size=(80, 1))], 
            [sg.ProgressBar(max_value=1000, key='progress_bar', size=(74, 20))]
        ], justification='center')
    ]
]

def ProgressUpdate(stream, chunk, bytesRemaining):
    totalSize = stream.filesize
    bytesDone = totalSize - bytesRemaining
    percent = round(bytesDone / totalSize * 100)
    window['progress_text'].update(f"Downloading... {percent}% ({currentItem}/{items})", text_color='white')
    progressBar.update(bytesDone, totalSize)

def FormatStreams(streams: list[Stream]):
    formattedStreams = []
    for stream in streams:
        formattedStream = []
        if stream.includes_video_track:
            formattedStream.append("Video")
            formattedStream.append(stream.subtype)
            formattedStream.append(stream.resolution)
            formattedStream.append(str(stream.fps) + " FPS")
            if stream.filesize < 1024 ** 2:
                formattedStream.append(str(round(stream.filesize / 1024, 2)) + " KB")

            elif stream.filesize < 1024 ** 3:
                formattedStream.append(str(round(stream.filesize / (1024 ** 2), 2)) + " MB")

            else:
                formattedStream.append(str(round(stream.filesize / (1024 ** 3), 2)) + " GB")

            formattedStream.append(stream.video_codec)
        
            if stream.includes_audio_track:
                formattedStream.insert(1, "Audio")

        elif not stream.includes_video_track:
            formattedStream.append("Audio")
            formattedStream.append(stream.subtype)
            formattedStream.append(stream.abr)
            if stream.filesize < 1024 ** 2:
                formattedStream.append(str(round(stream.filesize / 1024, 2)) + " KB")

            elif stream.filesize < 1024 ** 3:
                formattedStream.append(str(round(stream.filesize / (1024 ** 2), 2)) + " MB")

            else:
                formattedStream.append(str(round(stream.filesize / (1024 ** 3), 2)) + " GB")

            formattedStream.append(stream.audio_codec)

        formattedStreams.append(', '.join(formattedStream))
    
    return formattedStreams

window = sg.Window("YouTube Downloader", layout)
progressBar = window['progress_bar']
currentItem = 0
while True:
    window.refresh()
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    elif event == 'next_button':
        if not path.exists(values['output_dir']):
            window['output_dir_text'].update("Invalid folder", text_color='red')

        if values['url'] == '' or values['url'] is None:
            window['url_text'].update("Invalid URL", text_color='red')

        elif path.exists(values['output_dir']):
            window['output_dir_text'].update('')
            window['url_text'].update('')
            try:
                window['progress_text'].update("Getting info...", text_color='white')
                window.refresh()
                video = YouTube(values['url'], on_progress_callback=ProgressUpdate)
                window['video_info'].update(
                    f"Title: {str(video.title)}\n" +
                    f"Author: {str(video.author)}\n" +
                    f"Views: {str(video.views)}\n" +
                    f"Length: {str(video.length)}\n" +
                    f"Published: {str(video.publish_date)}"
                )
                formattedStreams = FormatStreams(video.streams)
                window['stream_list'].update(formattedStreams)
                window['progress_text'].update('', text_color='white')
                window.refresh()

            except Exception as exception:
                window['progress_text'].update(f"Failed to get info. {exception}", text_color='red')

    elif event == 'download_button':
        try:
            items = len(values['stream_list'])
            for stream in values['stream_list']:
                currentItem += 1
                index = formattedStreams.index(stream)
                prefix = None
                videoStream = video.streams[index]
                if path.exists(f"{values['output_dir']}/{videoStream.default_filename}"):
                    prefix = str(currentItem) + '-'
                    
                videoStream.download(values['output_dir'], None, prefix)

            window['progress_text'].update(f"Downloaded 100% ({items}/{items})", text_color='white')

        except:
            window['progress_text'].update("Failed to download", text_color='red')

    if values['stream_list'] != []:
        window['download_button'].update(disabled=False)

    elif values['stream_list'] == []:
        window['download_button'].update(disabled=True)

window.close()