import os
import Configuration
import threading
import datetime

MB_TO_B= 1024*1024








class FileManager():
    def __init__(self, Selector):
        print("file manager intilialized")
        self.config = Configuration.Configurations()
        self.Settings = self.config.fileSettings
        self.MaxDirSize = int(self.Settings['max_space'])
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
                if file_enumerator.endswith(".avi"):
                    print(file_enumerator)
                    date_part = file_enumerator[:10]
                    date = datetime.datetime.strptime(date_part, "%Y-%m-%d")
                    if date <= oldest_date:
                        if date == oldest_date:
                            if oldest_enumerator == None or int(file_enumerator[11:-4]) < oldest_enumerator:
                                oldest_enumerator = int(file_enumerator[11:-4])
                                oldest_date=date
                                oldest_file= os.path.join(dirpath, file_enumerator)
                            if file_enumerator.__len__() == 14:
                                oldest_enumerator = 0
                                oldest_date=date
                                oldest_file= os.path.join(dirpath, file_enumerator)

                        else:
                            oldest_enumerator = None
                            oldest_date = date
                            oldest_file = os.path.join(dirpath, file_enumerator)
        
        return oldest_file
    
    def run(self):
        self.thread = threading.Thread(target=self.ManageDirectory)
        self.thread.daemon = True
        self.thread.start()

        
                
                
        







    def ManageDirectory(self):
        
        while True:
            
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

            



             



