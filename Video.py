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







def SecondsFromMidnight():
    today_year = datetime.date.today().year
    today_month= datetime.date.today().month
    today_day= datetime.date.today().day
    delta_time= (time.time() - datetime.datetime(year=today_year, month=today_month, day= today_day).timestamp())
    return delta_time



def UpdateScreen(camFrame, panel1):
    
    ret, frame = cap.read()
      
            

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (640, 360))
    image = Image.fromarray(frame)
    image = ImageTk.PhotoImage(image)
    
        
    if camFrame == None:
        print(" 1initializing screen")
        
        
       
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
    print("lol")
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
            time.sleep(Record_timer)
            if recording:
                if not out.isOpened():
                    out, current_recording_path=VideoWriter(str(datetime.date.today()))
                
                 
                ret, frame = cap.read()
                
                out.write(frame)
                
            
           
                


            if stopEverything.is_set():
                out.release()
                cap.release()
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
    Preview_window = GUI.VideoPreview(gui_thread)
    View_window = GUI.VideoView(gui_thread)

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


    cap = cv2.VideoCapture(0)
    
    cap.set(3, config.resolution()[0])
    cap.set(4, config.resolution()[1])

    
    
    PreviewThread = threading.Thread(target=PreviewLoop)
    RecThread = threading.Thread(target=RecLoop)
    TimerThread = threading.Thread(target=TimerLoop)

    #to stop the threads if main window closes
    
    TimerThread.daemon =True
    PreviewThread.daemon = True
    RecThread.daemon = True
    View_window.viewer.run()
    fileManager.run()
    PreviewThread.start()
    TimerThread.start()
    YtUploader.run()
    FbUploader.run()
    RecThread.start()
    

    gui_thread.mainloop()

    #to stop recording and save the file before closing
    stopEverything.set()
    
    #wait for things to go off
    time.sleep(1)
    print("closing")
    
        
















