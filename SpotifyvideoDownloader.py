from youtube_search import YoutubeSearch
import pprint as p, io, time, json
import tkinter as tk
from PIL import Image, ImageTk
from urllib.request import urlopen
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tkinter import filedialog as fd
from pytube import YouTube
from threading import Thread
from tkinter import ttk

def download(song, dirname, choice):
        url = "https://youtube.com" + song['url_suffix']
        choice = ytdchoices.get()

        if(len(url)>1):
            yt = YouTube(url)
            if(choice == choices[0]):
                select = yt.streams.filter(progressive=True).first()

            elif(choice == choices[1]):
                select = yt.streams.filter(progressive=True,file_extension='mp4').last()

            elif(choice == choices[2]):
                select = yt.streams.filter(only_audio=True).first()
        
        select.download(dirname)

if __name__ == "__main__":

    #load in credentials and functions
    credentials = json.load(open('Authorization.json'))
    client_id = credentials['client_id']
    client_secret = credentials['client_secret']
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    dirname = ""
    isOn = False
    count = 0
    playlist = []

    def dispatchSearch():
        searchSpotify()
        dispatchDownload()

    def dispatchDownload():
        global count, playlist, dirname
        choice = ytdchoices.get()
        #for every song in the playlist, download the wanted one
        if count + 1 < len(playlist):
            count += 1
            YT = searchYT(playlist[count])
            if YT is not None:
                if len(YT) == 5:
                    x = 0
                    if isOn:
                        x = input('0 - 4 ? : ')
                    Thread(target = download, args = (YT[int(x)], dirname, choice, )).start()
                    CurrentOp.insert(count, '\n Downloading... \n' + YT[int(x)]['title'])
            root.after(1000,dispatchDownload)

    def searchYT(req):
        try:
            results = YoutubeSearch(req, max_results=5).to_dict()
        except:
            return None
        # returns a dictionary

        return results

    def searchSpotify():
        SpUrl = ytdEntry.get()
        username = "Test_1"
        playlist_id = SpUrl

        try:
            results = sp.user_playlist(username, playlist_id, 'tracks')
        except:
            raise ValueError("URI not found")
        for i in range(0, len(results['tracks']['items'])):
            r = results['tracks']['items'][i]['track']['name']
            playlist.append(r)
            DisPlay.insert(i, r)
        root.after(1000, dispatchDownload)
        
    
#tkinter functions

    def switch():
        global isOn
        if isOn:
            Automatic_Toggle.config(image = off)
            isOn = False
        else:
            Automatic_Toggle.config(image = on)
            isOn = True


    def select_dir():
        global dirname
        dirname = fd.askdirectory(
            title='download folder',
            initialdir='/'
            )
        
        if(len(dirname) > 1):
            locationError.config(text=dirname,fg="green")

        else:
            locationError.config(text="Please Choose Folder!!",fg="red")

    def displayRes(results):
        for i in range(0, len(results)):
            page = urlopen(results[i]['thumbnails'][0])
            img = io.BytesIO(page.read())
            imgProc = Image.open(img)
            imgtk = ImageTk.PhotoImage(imgProc)

            label = tk.Label(root, image = imgtk, width = 96, height = 54)
            label.place(x = 215, y = 40)  

#__start def screen__

    root = tk.Tk()
    root.title("Spotify_video_Downloader")
    root.geometry("1400x800")

    #__end def screen__


    #define needed attributes
    #Ytd Link Label
    SpUrl = tk.StringVar()
    ytdLabel = tk.Label(root,text="Enter Spotify URL",font=("Arial",15))
    ytdLabel.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 0, sticky = "nsew")

    #Entry Box
    ytdEntry = tk.Entry(root,width=50)
    ytdEntry.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 1, sticky = "nsew")

    #Error Msg
    ytdError = tk.Label(root,text="",fg="red",font=("Arial",10))
    ytdError.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 2,sticky = "nsew")

    #Asking save file label
    saveLabel = tk.Label(root,text="Video Directory",font=("Arial",15,"bold"))
    saveLabel.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 3, sticky = "nsew")

    #btn of save file
    saveEntry = tk.Button(root,width=10,bg="red",fg="white",text="Choose Path",command=select_dir)
    saveEntry.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 4, sticky = "nsew")

    #Error Msg location
    locationError = tk.Label(root,text="",fg="red",font=("Arial",10))
    locationError.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 5, sticky = "nsew")

    #Download Quality
    ytdQuality = tk.Label(root,text="Select Quality",font=("Arial",15))
    ytdQuality.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 6, sticky = "nsew")

    #combobox
    choices = ["720p","144p","Only Audio"]
    ytdchoices = ttk.Combobox(root,values=choices)
    ytdchoices.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 7, sticky = "nsew")

    #donwload btn
    downloadbtn = tk.Button(root,text="Donwload",width=10,bg="red",fg="white",command=dispatchSearch)
    downloadbtn.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, row = 8, sticky = "nsew")

    SwitchMessage = tk.Label(root,text="Enable Manual Check? (WIP)",fg="black",font=("Arial",15))
    SwitchMessage.grid(pady = 10, column = 1, row = 9, sticky = "nsew")

    on = ImageTk.PhotoImage(file = ("switch-on.jpeg"))
    off = ImageTk.PhotoImage(file = ("switch-off.jpeg"))
    Automatic_Toggle = tk.Button(root, image = off, bd = 0, command = switch)
    Automatic_Toggle.grid(pady = 5, ipady = 15, ipadx = 15, padx = 10, column = 1, sticky = "nsew")

    DisPlay = tk.Listbox(root, width = 60, height = 49)
    scroll = ttk.Scrollbar(root)
    scroll.config(command = DisPlay.yview)
    DisPlay.config(yscrollcommand = scroll.set)
    DisPlay.grid(column = 3, row = 0, sticky = "W", rowspan = 20)
    scroll.grid(column = 4, row = 0, sticky = "NSE", rowspan = 20)

    CurrentOp = tk.Listbox(root, width = 60, height = 49)
    scroll = ttk.Scrollbar(root)
    scroll.config(command = CurrentOp.yview)
    CurrentOp.config(yscrollcommand = scroll.set)
    CurrentOp.grid(column = 5, row = 0, sticky = "W", rowspan = 20)
    scroll.grid(column = 6, row = 0, sticky = "NSE", rowspan = 20)

    tk.mainloop()
