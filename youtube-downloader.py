from os import path
from pytube import YouTube, Stream
import PySimpleGUI as sg

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


def progress_update(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_done = total_size - bytes_remaining
    percent = round(bytes_done / total_size * 100)
    window['progress_text'].update(f"Downloading... {percent}% ({current_item}/{items})", text_color='white')
    progress_bar.update(bytes_done, total_size)


def format_streams(streams: list[Stream]):
    formatted_streams = []
    for stream in streams:
        formatted_stream = []
        if stream.includes_video_track:
            formatted_stream.append("Video")
            formatted_stream.append(stream.subtype)
            formatted_stream.append(stream.resolution)
            formatted_stream.append(str(stream.fps) + " FPS")
            if stream.filesize < 1024 ** 2:
                formatted_stream.append(str(round(stream.filesize / 1024, 2)) + " KB")
            elif stream.filesize < 1024 ** 3:
                formatted_stream.append(str(round(stream.filesize / (1024 ** 2), 2)) + " MB")
            else:
                formatted_stream.append(str(round(stream.filesize / (1024 ** 3), 2)) + " GB")
            formatted_stream.append(stream.video_codec)
            if stream.includes_audio_track:
                formatted_stream.insert(1, "Audio")
        elif not stream.includes_video_track:
            formatted_stream.append("Audio")
            formatted_stream.append(stream.subtype)
            formatted_stream.append(stream.abr)
            if stream.filesize < 1024 ** 2:
                formatted_stream.append(str(round(stream.filesize / 1024, 2)) + " KB")
            elif stream.filesize < 1024 ** 3:
                formatted_stream.append(str(round(stream.filesize / (1024 ** 2), 2)) + " MB")
            else:
                formatted_stream.append(str(round(stream.filesize / (1024 ** 3), 2)) + " GB")
            formatted_stream.append(stream.audio_codec)
        formatted_streams.append(', '.join(formatted_stream))
    return formatted_streams


window = sg.Window("YouTube Downloader", layout)
progress_bar = window['progress_bar']
current_item = 0
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
                video = YouTube(values['url'], on_progress_callback=progress_update)
                window['video_info'].update(
                    f"Title: {str(video.title)}\n"
                    + f"Author: {str(video.author)}\n"
                    + f"Views: {str(video.views)}\n"
                    + f"Length: {str(video.length)}\n"
                    + f"Published: {str(video.publish_date)}"
                )
                formatted_streams = format_streams(video.streams)
                window['stream_list'].update(formatted_streams)
                window['progress_text'].update('', text_color='white')
                window.refresh()
            except Exception as exception:
                window['progress_text'].update(f"Failed to get info. {exception}", text_color='red')
    elif event == 'download_button':
        try:
            items = len(values['stream_list'])
            for stream in values['stream_list']:
                current_item += 1
                index = formatted_streams.index(stream)
                prefix = None
                video_stream = video.streams[index]
                if path.exists(f"{values['output_dir']}/{video_stream.default_filename}"):
                    prefix = str(current_item) + '-'
                video_stream.download(values['output_dir'], None, prefix)
            window['progress_text'].update(f"Downloaded 100% ({items}/{items})", text_color='white')
        except Exception as exception:
            window['progress_text'].update(f"Failed to download. {exception}", text_color='red')
    if values['stream_list'] != []:
        window['download_button'].update(disabled=False)
    elif values['stream_list'] == []:
        window['download_button'].update(disabled=True)
window.close()
