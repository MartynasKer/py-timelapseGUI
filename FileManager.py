import os
import Configuration
import threading
import datetime
import time

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
        for dirpath, dirnames, files in os.walk(path):
            for file_enumerator in files:
                if file_enumerator.endswith(".mp4") and not file_enumerator.endswith("h.mp4"):
                    print(file_enumerator)
                    oldest_file = os.path.join(dirpath, file_enumerator)
        
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
                        print("failed to delete large file")

        







    def ManageDirectory(self):
        
        while True:
            time.sleep(1)
         
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
                        os.remove(file_to_delete)
                    except:
                        print("failed to delete file: " + file_to_delete)
                        self.DirEvent.clear()
                    print("deleting: " + file_to_delete)
                    
                else:
                    self.selector.RefreshList()
                    self.DirEvent.clear()

            



             



