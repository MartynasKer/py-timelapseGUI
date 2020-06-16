import tkinter as tk
import tkinter.ttk as ttk
from cv2 import cv2
from PIL import ImageTk
from PIL import Image

import threading

import time 
import datetime
import Configuration
import FileManager
import os.path
import YoutubeUpload
import FacebookUpload
import GUI


    


class VideoStream():
    def __init__(self):
        self.path=None
        self.timer=0
        self.cap=cv2.VideoCapture(self.path)
        
        self.NewestFrame=cv2.imread("NoImage.png")
        

    def run(self):
        self.Thread=threading.Thread(target=self.Stream)
        self.Thread.daemon = True
        self.Thread.start()

    

    def Stream(self):
        while True:
            if self.cap.isOpened():
                ret, frame = self.cap.read()

                self.NewestFrame=frame
                
                time.sleep(self.timer)
       
        self.cap.release()


class TimelapseStream(VideoStream):
    def __init__(self):
        
        self.timer=0.03
        self.cap = cv2.VideoCapture()
        self.cap.release()
        
        self.path="timelapse"
        
        self.NewestFrame=cv2.resize(cv2.imread("NoImage.png"),(800,450) )
        
    
    def Load(self, path):
        self.cap=cv2.VideoCapture(path)

    

class Camera(VideoStream):
    def __init__(self):
        config = Configuration.Configurations()
        self.timer=0
        self.path="camera"
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, config.resolution()[0])
        self.cap.set(4, config.resolution()[1])
        
        self.NewestFrame=cv2.resize(cv2.imread("NoImage.png"),(800,450) )
        


class CamProcessor():
    def __init__(self, video_stream):
        self.ProcessedFrame=None
        self.Processed = threading.Event()
        self.stream=video_stream
        

    def run(self):
        self.thread= threading.Thread(target=self.Process)
        self.thread.daemon=True
        self.thread.start()

    def Process(self):
        
        while True:
           
            frame = self.stream.NewestFrame
            
            try:
                   
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (800, 450))
                image = Image.fromarray(frame)
                image = ImageTk.PhotoImage(image)
                self.ProcessedFrame=image
                    
                    
            except:
                print("failed to process image")

            


class FrameProcessor():
    def __init__(self, video_stream):
        self.ProcessedFrame=None
        self.Processed = threading.Event()
       
        self.stream=video_stream
        


    

    def run(self):
        self.thread= threading.Thread(target=self.Process)
        self.thread.daemon=True
        self.thread.start()

    def Process(self):
        
        while True:
    
            frame = self.stream.NewestFrame
            
            try:
                    
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                image = Image.fromarray(frame)
                image = ImageTk.PhotoImage(image)
                self.ProcessedFrame=image
                self.Processed.set()
                    
            except:
                pass



       







def SecondsFromMidnight():
    today_year = datetime.date.today().year
    today_month= datetime.date.today().month
    today_day= datetime.date.today().day
    delta_time= (time.time() - datetime.datetime(year=today_year, month=today_month, day= today_day).timestamp())
    return delta_time



def UpdateScreen(camFrame, panel1):
    
   
    image=VideoProcessor1.ProcessedFrame
        
    if camFrame == None:
        print("initializing screen")
        
        
       
        camFrame = tk.Label(master=panel1,image=image)
        camFrame.image = image
        camFrame.pack(side="top")
    else:
        camFrame.configure(image=image)
        camFrame.image = image
    return camFrame







    
  
    
    
    
def ButtonFunction():
    
    stopRec.set()
 
def VideoWriter(path):
    
    file_path = path+"h"
    return cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc(*'MP4V'), config.Fps(), config.resolution()), file_path

def SmallerResWriter(path):
    file_path = GenerateFilePath(os.path.join(config.folderPath(),path))
    return cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc(*'MP4V'), config.Fps(), (800,450)) 


def GenerateFilePath(path):
    path_enumerator = path + ".mp4"
    path_counter = 0
    while os.path.exists(path_enumerator):
        
        path_counter = path_counter + 1
        path_enumerator = path +"_"+str(path_counter)+".mp4"
    return path_enumerator

    


def RecLoop():
        current_recording_path=""
        out, current_recording_path = VideoWriter(str(datetime.date.today()))
        small_out = SmallerResWriter(str(datetime.date.today()))
        today= None
        recording = True
        
        while True:
            if Record_timer >0:
                time.sleep(Record_timer)
            else:
                time.sleep(1/config.Fps())

             
            if recording:
                if not out.isOpened() and not small_out.isOpened():
                    out, current_recording_path=VideoWriter(str(datetime.date.today()))
                    small_out = SmallerResWriter(str(datetime.date.today()))
                
                 
                frame = Cam.NewestFrame
                
                out.write(frame)
                frame =cv2.resize(frame, (800,450))
                small_out.write(frame)
            
           
                


            if stopEverything.is_set():
                out.release()
                small_out.release()
                return
            
            if int(SecondsFromMidnight()) >= int(config.VideoStartTime()) and not recording and today != datetime.date.today():
                today = datetime.date.today()
                if out.isOpened() and small_out.isOpened():
                    out.release()
                    small_out.release()
                fileManager.DirEvent.set()
                YtUploader.newest_file_path=current_recording_path
                YtUploader.uploadEvent.set()
                FbUploader.file_to_upload=current_recording_path
                FbUploader.UploadEvent.set()
                resetTimer.set()
                stopTimer.clear()
                time.sleep(1)
                recording = True

            


            if stopRec.is_set() and recording:
                print("ending recording")
                out.release()
                small_out.release()
                fileManager.DirEvent.set()
                YtUploader.newest_file_path=current_recording_path
                YtUploader.uploadEvent.set()
                FbUploader.file_to_upload=current_recording_path
                FbUploader.UploadEvent.set()
                resetTimer.set()
                stopTimer.set()
                recording = False
                stopRec.clear()
            
            
                


                

            

            
def TimerLoop():
    StartTime = time.time()
    while not stopEverything.is_set():
        time.sleep(0.1)
        if resetTimer.is_set():
                StartTime = time.time()
                resetTimer.clear()
                elapsed_time = int(time.time()) - int(StartTime)
            
                
        if not stopTimer.is_set():
            
            
            elapsed_time = int(time.time()) - int(StartTime)
            if elapsed_time >= config.VideoLength():
                stopRec.set()
            
        


        

if __name__ == "__main__":
    
    



    config = Configuration.Configurations()
    gui_thread= tk.Tk()
    Cam = Camera()
    
    VideoProcessor1 = CamProcessor(Cam)
    

    videoStreamer=TimelapseStream()
    VideoProcessor2 = FrameProcessor(videoStreamer)
    Cam.run()
    
    
    
    
    View_window = GUI.VideoView(gui_thread, videoStreamer, VideoProcessor2, VideoProcessor1)
    VideoProcessor1.run()
    videoStreamer.run()
    VideoProcessor2.run()
    
    stopRec = threading.Event()
    resetTimer = threading.Event()
    stopTimer =threading.Event()
    stopEverything = threading.Event()
    stopPreview = threading.Event()
    YtUploader=YoutubeUpload.YouTubeUploader()
    FbUploader = FacebookUpload.FacebookUploader()
    fileManager = FileManager.FileManager(View_window.selector_frame, YtUploader, FbUploader)
   

    
    
    
    
    
    
    Record_timer = config.TimelapseTimer()
    if not Record_timer > 0:
        Record_timer = 1/config.Fps()
    
    preview_timer = 0


    

    
    time.sleep(0.5)
    RecThread = threading.Thread(target=RecLoop)
    TimerThread = threading.Thread(target=TimerLoop)

    #to stop the threads if main window closes
    
    TimerThread.daemon =True
    
    RecThread.daemon = True
    View_window.viewer.run()
    View_window.previewer.run()
    fileManager.run()
    
    TimerThread.start()
    YtUploader.run()
    FbUploader.run()
    RecThread.start()
    

    gui_thread.mainloop()

    #to stop recording and save the file before closing
    stopEverything.set()
    Cam.cap.release()
    #wait for things to go off
    time.sleep(1)
    print("closing")
    
        
















