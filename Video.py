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
        self.stop =threading.Event()
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
        
        self.timer=0.01
        self.cap = cv2.VideoCapture()
        self.cap.release()
        self.path="timelapse"
        self.stop =threading.Event()
        self.NewestFrame=cv2.imread("NoImage.png")
        
    
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
        self.stop =threading.Event()
        self.NewestFrame=cv2.imread("NoImage.png")
        


    
            


class FrameProcessor():
    def __init__(self, video_stream):
        self.ProcessedFrame=None
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
                time.sleep(0.05)
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







    
  
    
    


def PreviewLoop():
    CameraFrame = None
    
    
    while not stopPreview.is_set():
        time.sleep(preview_timer) 
        if stopPreview.is_set():
            print("stopping")
            return
        CameraFrame = UpdateScreen(camFrame=CameraFrame, panel1=Preview_window.preview_panel)
    return
            
     
def ButtonFunction():
    
    stopRec.set()
 
def VideoWriter(path):
    
    file_path = GenerateFilePath(os.path.join(config.folderPath(),path))
    return cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc(*'XVID'), config.Fps(), config.resolution()), file_path

def GenerateFilePath(path):
    path_enumerator = path + ".avi"
    path_counter = 0
    while os.path.exists(path_enumerator):
        
        path_counter = path_counter + 1
        path_enumerator = path +"_"+str(path_counter)+".avi"
    return path_enumerator

    


def RecLoop():
        current_recording_path=""
        out, current_recording_path = VideoWriter(str(datetime.date.today()))
        
        today= None
        recording = True
        
        while True:
            time.sleep(Record_timer+0.04)
            if recording:
                if not out.isOpened():
                    out, current_recording_path=VideoWriter(str(datetime.date.today()))
                
                 
                frame = Cam.NewestFrame
                
                out.write(frame)
                
            
           
                


            if stopEverything.is_set():
                out.release()

                return
            
            if int(SecondsFromMidnight()) >= int(config.VideoStartTime()) and not recording and today != datetime.date.today():
                today = datetime.date.today()
                if out.isOpened():
                    out.release()
                fileManager.DirEvent.set()
                YtUploader.newest_file_path=current_recording_path
                YtUploader.uploadEvent.set()
                FbUploader.file_to_upload=current_recording_path
                FbUploader.UploadEvent.set()
                resetTimer.set()
                stopTimer.clear()
                recording = True

            


            if stopRec.is_set() and recording:
                print("ending recording")
                out.release()
                fileManager.DirEvent.set()
                YtUploader.newest_file_path=current_recording_path
                YtUploader.uploadEvent.set()
                FbUploader.file_to_upload=current_recording_path
                FbUploader.UploadEvent.set()
                resetTimer.set()
                stopTimer.set()
                recording = False
                stopRec.clear()
            
            
                


                

def TimerUpdate(updateString):
    Preview_window.updateTime(updateString)                

            
def TimerLoop():
    StartTime = time.time()
    while not stopEverything.is_set():
        time.sleep(0.1)
        if resetTimer.is_set():
                StartTime = time.time()
                resetTimer.clear()
                elapsed_time = int(time.time()) - int(StartTime)
            
                TimerUpdate(str(datetime.timedelta(seconds=elapsed_time)))
        if not stopTimer.is_set():
            
            
            elapsed_time = int(time.time()) - int(StartTime)
            if elapsed_time >= config.VideoLength():
                stopRec.set()
            TimerUpdate(str(datetime.timedelta(seconds=elapsed_time)))
        


        

if __name__ == "__main__":
    
    



    config = Configuration.Configurations()
    gui_thread= tk.Tk()
    Cam = Camera()
    
    VideoProcessor1 = FrameProcessor(Cam)
    

    videoStreamer=TimelapseStream()
    VideoProcessor2 = FrameProcessor(videoStreamer)
    Cam.run()
    
    
    
    Preview_window = GUI.VideoPreview(gui_thread)
    View_window = GUI.VideoView(gui_thread, videoStreamer, VideoProcessor2, VideoProcessor1)
    VideoProcessor1.run()
    videoStreamer.run()
    VideoProcessor2.run()
    
    stopRec = threading.Event()
    resetTimer = threading.Event()
    stopTimer =threading.Event()
    stopEverything = threading.Event()
    stopPreview = threading.Event()
    fileManager = FileManager.FileManager(View_window.selector_frame)
    YtUploader=YoutubeUpload.YouTubeUploader()
    FbUploader = FacebookUpload.FacebookUploader()

    
    
    
    button_1 = tk.Button(master=Preview_window.frame_4, command=lambda: ButtonFunction())
    button_1.config(text='stop recording')
    button_1.pack(side='top')
    
    
    Record_timer = config.TimelapseTimer()
    preview_timer = 0


    

    
    
    PreviewThread = threading.Thread(target=PreviewLoop)
    RecThread = threading.Thread(target=RecLoop)
    TimerThread = threading.Thread(target=TimerLoop)

    #to stop the threads if main window closes
    
    TimerThread.daemon =True
    PreviewThread.daemon = True
    RecThread.daemon = True
    View_window.viewer.run()
    View_window.previewer.run()
    fileManager.run()
    PreviewThread.start()
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
    
        
















