import configparser
import os.path



class Configurations():
    def __init__(self):
        
        config = configparser.ConfigParser()
        self.con = config
        self.con.read("config.ini")
        self.camSettings = self.con['CamSettings']
        self.fileSettings = self.con['FileManagerSettings']
        self.youtubeSettings = self.con['YoutubeSettings']
        self.facebookSettings= self.con['FacebookSettings']
        self.UISettings=self.con['UISettings']
        self.thumbnail_with_time=self.UISettings.getboolean('thumbnail_name_with_time')
        self.timestamp=self.UISettings['live_timestamp_text']
    def resolution(self):
        return int(self.camSettings['Resolution_width']), int(self.camSettings['Resolution_height'])
    
    

    def folderPath(self):
        path = self.fileSettings['folder_path']
        if os.path.isdir(path):
            return path
        else:
            return str("")

    def TimelapseTimer(self):
        return int(self.camSettings['timelapse_timer'])
    
    def VideoLength(self):
        video_length = self.camSettings['recording_length']
        if int(video_length) > 86400:
            return 86400
        else:
            return int(video_length)
        

    def VideoStartTime(self):
        start_time = self.camSettings['video_auto_start_time']
        if int(start_time) > 86400:
            return int(86400)
        else:
            return int(start_time)


    def autoStart(self):
        return bool(self.camSettings['video_auto_start'])


    def Fps(self):
        return int(self.camSettings['fps'])





if __name__ =="__main__":
    config = Configurations()
    print(config.resolution())
    print(config.VideoStartTime())
    print(config.folderPath())

