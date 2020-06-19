import tkinter as tk
import tkinter.ttk as ttk
import Configuration
import os
from PIL import Image
from PIL import ImageTk
import datetime
from cv2 import cv2
import threading 
import time
import Video




class VideoPreview():
    def __init__(self, master):
        
        self.top=tk.Toplevel(master)
        self.top.title("recorder")
        self.preview_panel = tk.Frame(master=self.top, width=960, height=720, bg='black')
        self.frame_4 = tk.Frame(master=self.top)
        label_1 = tk.Label(self.frame_4)
        label_1.config(text='recording time:')
        label_1.pack(side='left')
            
       
        self.timer = tk.StringVar()
        
        timeLabel = tk.Label(master=self.frame_4, textvariable=self.timer)
        
        timeLabel.pack(side='left')
        
        self.frame_4.config(height='200', width='200')
        self.frame_4.pack(side='bottom')
        self.preview_panel.pack(side="top")

    

    def updateTime(self, time):
        self.timer.set(time)


class TimelapseVideo():
    def __init__(self):
        self.video=""
        
        self.name=""

class PreviewFrame():
    def __init__(self, frame, preview_processor):
        self.frame=tk.Label(frame,bg='black')
        self.frame.pack(side='right', expand=True, fill='both')
        self.showed=threading.Event()
        self.frameProcessor=preview_processor


    def ViewThread(self):
        
        while True:
            
            time.sleep(0.025)
            img = self.frameProcessor.ProcessedFrame
            self.frameProcessor.Processed.clear()
            self.frame.configure(image=img)
            self.frame.image=img
            
                
                


            
            
                

    def run(self):
        thread = threading.Thread(target=self.ViewThread)
        thread.daemon=True
        thread.start()





class VideoViewFrame():
    def __init__(self, frame, streamer, processor):
        self.view_frame=tk.Label(frame,bg='black')
        self.view_frame.pack(side='left', expand=True, fill='both')
        
        self.current_video_path=""
        self.frameProcessor=processor
        
        self.stream = streamer
        
        self.LoadEvent=threading.Event()
        self.frameCount=1
        
        
        
        
        
    def Load(self, path):
        
        self.loaded = True
        self.current_video_path=path
        self.stream.Load(path)
       
        

    def ViewThread(self):
        
        while True:
            time.sleep(0.025)
            img = self.frameProcessor.ProcessedFrame
            
            self.view_frame.configure(image=img)
            self.view_frame.image=img
                


            
            
                

    def run(self):
        thread = threading.Thread(target=self.ViewThread)
        thread.daemon=True
        thread.start()
    






def ScanForNewestFiles(path):
    Files = []
    for dirpath, dirnames, files in os.walk(path):
            for file_enumerator in files:
                if file_enumerator.endswith(".mp4") and not file_enumerator.endswith("h.mp4"):
                    
                    file = TimelapseVideo()
                    file.name = file_enumerator[:-4]
                    file.video = os.path.join(path, file_enumerator)
                    
                    
                    Files.append(file)

    Files.reverse()
    return Files
    




class Selector():
    def __init__(self, master, view_frame):
        self.view_frame= view_frame
        self.config = Configuration.Configurations()
        self.UIsettings = self.config.con['UISettings']
        self.thumnail_time=self.UIsettings['thumbnail_time']
        self.selector_frame= tk.Frame(master=master, bg='black')
        self.files =[]
        self.thumnails=[]
        self.current_pos = [0, 1, 2]
        
        for i in range(3):
            thumbnail = Thumbnail(self.selector_frame, self.view_frame)
            self.thumnails.append(thumbnail)
        self.thumnails.reverse()
        self.selector_frame.config(height='200', width='200')
        self.selector_frame.pack(expand='true', fill='both', ipadx='0', padx='0', pady='0', side='left')
        self.RefreshList()
        self.UpdateThumbnails()



    def UpdateThumbnails(self):
        
        if self.files.__len__() < 3:
            i_range = self.files.__len__()
        else:
            i_range = 3
        for i in range(i_range):
            file=self.files[self.current_pos[i]]
            
            print(file.video)
            video=cv2.VideoCapture(file.video)
            video.set(1, 1+ self.config.Fps()*int(self.thumnail_time))
            ret, frame = video.read()
            video.release()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (256, 200))
            image = Image.fromarray(frame)
            
            image = ImageTk.PhotoImage(image)
            self.thumnails[i].button.configure(image = image)
            self.thumnails[i].button.image=image
            
            self.thumnails[i].label.config(text=file.name)
            self.thumnails[i].video = file.video
            



    def ChangeSelection(self, incremention):
        if incremention > 0 and self.current_pos[2] < (self.files.__len__() - 1):
            for i in range(3):
                self.current_pos[i] += 1
                
        if incremention <0 and self.current_pos[0] > 0:
            for i in range(3):
                self.current_pos[i] -= 1
                
        self.UpdateThumbnails()

    
            
                





    def RefreshList(self):
        self.files=ScanForNewestFiles(self.config.folderPath())
        self.current_pos =[0,1,2]
        self.UpdateThumbnails()
        if self.files.__len__()>0:
            self.view_frame.Load(self.files[0].video)


        
    
    
        
        









class Thumbnail():
    


    def __init__(self, master, view_frame):
        self.view_frame = view_frame
        self.frame = tk.Frame(master=master,bg='black')
        self.video=""
        self.button = tk.Button(master=self.frame, command=lambda: self.buttonClick(),bg='black' )
        self.button.config(text='empty')
        self.button.pack(expand='false', fill='both', side='top')
        self.label = ttk.Label(master=self.frame)
        self.label.config(text='empty',foreground='#98a5fa',background='black')
        self.label.pack(side='top')
        self.frame.config(height='100', width='100')
        self.frame.pack(expand='true', fill='both', side='left')
    def buttonClick(self):
        self.view_frame.Load(self.video)
        
        
        


class VideoView():
    def __init__(self, master, streamer, processor, cam_processor):
        # build ui
        self.toplevel_1 = tk.Toplevel(master=master,bg='black')
        self.toplevel_1.title("Viewer")
        self.toplevel_1.attributes("-fullscreen", True)
        self.toplevel_1.bind("<Escape>", self.QuitFullscreen)
        self.toplevel_1.bind("<F7>", self.EnterFullscreen)
        frame_8 = tk.Frame(self.toplevel_1,bg='black')
        self.frame_10 = tk.Frame(master=frame_8,bg='black')
        self.frame_10.config(height='450', width='200')
        self.frame_10.pack(expand='true', fill='both', ipady='30', pady='0', side='top')
        frame_11 = tk.Frame(frame_8)
        frame_12 = tk.Frame(frame_11)
        button_10 = tk.Button(master=frame_12,command=lambda: self.selector_frame.ChangeSelection(1),bg='#98a5fa')
        self.img_arrowleft = tk.PhotoImage(file='arrow_left.png')
        button_10.config(image=self.img_arrowleft, text='button_10')
        button_10.pack(expand='true', side='top',fill='both')
        frame_12.config(height='200', width='100')
        frame_12.pack(anchor='n', expand='false', fill='y', ipadx='10', padx='0', side='left')
        
        self.viewer = VideoViewFrame(self.frame_10, streamer, processor)
        self.previewer= PreviewFrame(self.frame_10, cam_processor)
        self.selector_frame = Selector(frame_11, self.viewer)
        
        
        
        frame_14 = tk.Frame(frame_11)
        button_8 = tk.Button(master=frame_14,command=lambda: self.selector_frame.ChangeSelection(-1),bg='#98a5fa' )
        self.img_arrowright = tk.PhotoImage(file='arrow_right.png')
        button_8.config(image=self.img_arrowright, text='button_8',)
        button_8.pack(expand='true', pady='0', side='top', fill='both')
        frame_14.config(height='200', width='100')
        frame_14.pack(expand='false', fill='y', ipadx='10', side='right')
        frame_11.config(height='100', relief='raised', width='200')
        frame_11.pack(expand='true', fill='both', pady='0', side='bottom')
        frame_8.config(height='500', width='200')
        frame_8.pack(expand='true', fill='both', side='top')
        self.toplevel_1.config(height='200', takefocus=True, width='200')
        self.toplevel_1.geometry('640x480')


        




    def QuitFullscreen(self, event):
        self.toplevel_1.attributes("-fullscreen", False)

    def EnterFullscreen(self, event):
        self.toplevel_1.attributes("-fullscreen", True)

    
        




