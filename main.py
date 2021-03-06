import ffmpeg, os, yt_dlp
from tkinter import *
from pytube import YouTube
from tkinter.filedialog import askdirectory

main = Tk()
main.title('YtDownloader')
main.resizable(False, False)

file = f'C:/Users/{os.getlogin()}/Downloads'

canvas = Canvas(main, width=1000, height=600, bg='#282828')
canvas.grid(rowspan=12)

statusbar = Label(main, text='Path: '+file, relief=SUNKEN, font='Verdana', bg='#282828', fg='#ffffff').grid(row=12, rowspan=3, column=0)

titlabel = Label(main, text='Insert a youtube link', font='Verdana', bg='#282828', fg='#ffffff').grid(row=1, column=0)

linkentry = Entry(main, width=50, bg='#b3b3b3')
linkentry.grid(row=2, column=0)

browselbl = Label(main, text='Select the folder where you want to save the file', font='Verdana', bg='#282828', fg='#ffffff').grid(row=3, column=0)
btntext = StringVar()
btntext.set('Browse')
browsebtn = Button(main, text=btntext.get(), font='Verdana', bg='#404040', fg='#ffffff', command=lambda:open_brws()).grid(row=4, column=0)

namelbl = Label(main, text='Declare a filename', font='Verdana', bg='#282828', fg='#ffffff').grid(row=5, column=0)
filentry = Entry(main, width=50, bg='#b3b3b3')
filentry.grid(row=6, column=0)

selec = StringVar()
selec.set('Select what you want to download')

dropdwn = OptionMenu(main, selec, 'Video', 'Audio', 'Video Only',)
dropdwn.grid(row=7, column=0)
dropdwn.config(bg='#282828', fg='#ffffff')
dropdwn['menu'].config(bg='#282828', fg='#ffffff')

mempr = StringVar()
mempr.set('Is it a members-only/private video?')

mempdwn = OptionMenu(main, mempr, 'Yes', 'No')
mempdwn.grid(row=8, column=0)
mempdwn.config(bg='#282828', fg='#ffffff')
mempdwn['menu'].config(bg='#282828', fg='#ffffff')

quality = StringVar()
quality.set('Select quality for the video')

dropmen = OptionMenu(main, quality, '144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p')
dropmen.grid(row=9, column=0)
dropmen.config(bg='#282828', fg='#ffffff')
dropmen['menu'].config(bg='#282828', fg='#ffffff')

confbtn = Button(main, text='Confirm',font='Verdana', bg='#404040', fg='#ffffff', command=lambda:callback(selec.get(), quality.get(), mempr.get())).grid(row=10, column=0)

def open_brws():
    global file
    file = askdirectory(parent=main, title='Select a folder')
    statusbar = Label(main, text='Path: '+file, relief=SUNKEN, font='Verdana', bg='#282828', fg='#ffffff').grid(row=12, column=0)

def callback(value, value1, value2):
        if value == 'Audio':
            if value2 == 'Yes':
                try:
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': f'{file}/{filentry.get()}.mp3',
                        'cookiefile': 'cookies.txt',
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([linkentry.get()])
                except:
                    print('Connection Error')
            else:
                try:
                    yt = YouTube(linkentry.get())
                except:
                    print('Connection Error')
                mp3file = yt.streams.get_audio_only().download(file, f'{filentry.get()}.mp3')
        elif value == 'Video':
            if value2 == 'Yes':
                try:
                    ydl_opts = {
                        'format': 'bestvideo+bestaudio',
                        'outtmpl': f'{file}/{filentry.get()}.mp4',
                        'cookiefile': 'cookies.txt',
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([linkentry.get()])
                except:
                    print('Connection Error')
            else:
                try:
                    yt = YouTube(linkentry.get())
                except:
                    print('Connection Error')

                v = ffmpeg.input(yt.streams.filter(resolution=value1).first().download(file, 'oiawjkldsnakdhnsak.mp4'))
                a = ffmpeg.input(yt.streams.get_audio_only().download(file, 'auhdwkljsahiluhnwsda.mp4'))

                r = ffmpeg.concat(v, a, v=1, a=1).output(f'{file}/{filentry.get()}.mp4').run()
                if os.path.exists(f'{file}/oiawjkldsnakdhnsak.mp4') and os.path.exists(f'{file}/auhdwkljsahiluhnwsda.mp4'):
                    os.remove(f'{file}/oiawjkldsnakdhnsak.mp4')
                    os.remove(f'{file}/auhdwkljsahiluhnwsda.mp4')
                else:
                    print('The files do not exist')
        elif value == 'Video Only':
            if value2 == 'Yes':
                try:
                    ydl_opts = {
                        'format': 'bestvideo',
                        'outtmpl': f'{file}/{filentry.get()}.mp4',
                        'cookiefile': 'cookies.txt',
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([linkentry.get()])
                except:
                    print('Connection Error')
            else:
                try:
                    yt = YouTube(linkentry.get())
                except:
                    print('Connection Error')
                mp4file = yt.streams.filter(resolution=value1).first().download(file, f'{filentry.get()}.mp4')
        else:
            print('Invalid')
        
        top = Toplevel()
        top.resizable(False, False)
        canvas2 = Canvas(top, width=500, height=200, bg='#282828')
        canvas2.grid(rowspan=2)
        if value == 'Audio':
            complete = Label(top, text=f'Download Completed!, saved to: {file}/{filentry.get()}.mp3', bg='#282828', fg='#ffffff').grid(row=0, column=0)
        else:
            complete = Label(top, text=f'Download Completed!, saved to: {file}/{filentry.get()}.mp4', bg='#282828', fg='#ffffff').grid(row=0, column=0)
main.mainloop()
