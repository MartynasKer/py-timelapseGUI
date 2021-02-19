import os
import Configuration
import threading
import datetime
import time
import AppPath

MB_TO_B= 1024*1024


class FileManager():
    def __init__(self, Selector, YtUploader, FbUploader):
        print("file manager intilialized")
        self.config = Configuration.Configurations()
        self.YtUploader=YtUploader
        self.FbUploader=FbUploader
        self.Settings = self.config.fileSettings
        self.MaxDirSize = int(self.Settings['max_space'])
        self.DeleteH= self.Settings.getboolean('delete_high_res_files')
        self.Dir = self.config.folderPath()
        self.DirEvent = threading.Event()
        self.selector = Selector
        self.deleteRetryCounter=0

    def dirSize(self, path):
        size = 0
        for dirpath, dirnames, files in os.walk(path):
            for file_enumerator in files:
                file = os.path.join(dirpath, file_enumerator)
                size+= os.path.getsize(file)

        return size

    


    def ScanForOldestFile(self, path):
        oldest_date = datetime.datetime.max
        oldest_enumerator = None 
        oldest_file=str("")
        Files = [] 
        for dirpath, dirnames, files in os.walk(path):
            for file_enumerator in files:
                if file_enumerator.endswith(".mp4"):  
                    Files.append(os.path.join(dirpath, file_enumerator))
        Files.sort(key=os.path.getctime)
        return Files[0]
        
        return oldest_file
    
    def run(self):
        self.thread = threading.Thread(target=self.ManageDirectory)
        self.thread.daemon = True
        self.thread.start()

        
                
    def DeleteLargeFiles(self, path):
        for dirpath, dirnames, files in os.walk(path):
            for file_enumerator in files:
                if file_enumerator.endswith("h.mp4"):
                    try:
                        os.remove(os.path.join(dirpath, file_enumerator))
                    except:
                        pass

        







    def ManageDirectory(self):
        
        while True:
            time.sleep(5)
         
            if self.DeleteH:
                if self.FbUploader.uploaded.is_set() or not self.FbUploader.upload:
                
                
                    if self.YtUploader.uploaded.is_set() or not self.YtUploader.upload:
                    
                        self.DeleteLargeFiles(self.Dir)
                        self.YtUploader.uploaded.clear()
                        self.FbUploader.uploaded.clear()
                


            if self.DirEvent.is_set():
            
                if self.dirSize(self.Dir) >= self.MaxDirSize * MB_TO_B:
                    
                    file_to_delete = self.ScanForOldestFile(self.Dir)
                    try:
                        print("deleting: " + file_to_delete)
                        os.remove(file_to_delete)
                    except Exception as e:
                        print("failed to delete file: " + file_to_delete)
                        print(e)
                        self.deleteRetryCounter += 1
                    
                    if self.deleteRetryCounter >= 3:
                        self.selector.RefreshList()
                        self.DirEvent.clear()
                else:
                    self.selector.RefreshList()
                    self.DirEvent.clear()

            



             



