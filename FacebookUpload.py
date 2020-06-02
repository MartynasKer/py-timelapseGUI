import facebook
import os
import requests
import threading
import time
from Configuration import Configurations
from requests_toolbelt import MultipartEncoder


class FacebookUploader():
    def __init__(self):
        config=Configurations()
        self.settings=config.facebookSettings
        self.file_to_upload=""
        self.title=self.settings['post_title']
        self.description=self.settings['post_description']
        self.access_token=self.settings['access_token']
        self.page_id=self.settings['page_id']
        self.upload=self.settings.getboolean('upload_to_facebook')
        print(self.upload)
        self.UploadEvent = threading.Event()
        

    def UploadThread(self):
        while True:
            time.sleep(1)
            
            if self.file_to_upload.__len__()>0 and self.UploadEvent.is_set() and self.upload:
                print("uploading to facebook")
                if(os.path.exists(self.file_to_upload)):
                    put_video(self.file_to_upload, self.page_id, self.access_token, self.description, self.title)
                self.file_to_upload = ""
                self.UploadEvent.clear()
                
    



    def run(self):
        self.thread=threading.Thread(target=self.UploadThread)
        self.thread.daemon= True
        self.thread.start()









#get_api connection
def get_api(cfg):
  graph = facebook.GraphAPI(cfg['access_token'])
  resp = graph.get_object('me/accounts')
  page_access_token = None
  for page in resp['data']:
    if page['id'] == cfg['page_id']:
      page_access_token = page['access_token']
  graph = facebook.GraphAPI(page_access_token)
  return graph

#post video
def put_video(video_url, page_id, access_token, description, title):
    video_file_name=title
    local_video_file=video_url
    path = "{0}/videos".format(page_id)
    fb_url = "https://graph-video.facebook.com/{0}?access_token={1}".format(
             path, access_token)
    print (fb_url)
    # multipart chunked uploads
    m = MultipartEncoder(
        fields={'description': description,
                'title': title,
                'comment':'postvideo',
                'source': (video_file_name, open(local_video_file, 'rb'))}
    )
    r = requests.post(fb_url, headers={'Content-Type': m.content_type}, data=m) 
    if r.status_code == 200:
        j_res = r.json()
        facebook_video_id = j_res.get('id')
        print ("facebook_video_id = {0}".format(facebook_video_id))
    else:
        print ("Facebook upload error: {0}".format(r.text))

def put_unpublishedvideo(video_url, page_id, access_token,description, title):
    video_file_name=title
    local_video_file=video_url
    path = "{0}/videos".format(page_id)
    fb_url = "https://graph-video.facebook.com/{0}?access_token={1}".format(
             path, access_token)
    print (fb_url)
    # multipart chunked uploads
    m = MultipartEncoder(
        fields={'description': description,
                'title': title,
                'comment':'postvideo',
                'published':'false',
                'source': (video_file_name, open(local_video_file, 'rb'))}
    )
    r = requests.post(fb_url, headers={'Content-Type': m.content_type}, data=m) 
    if r.status_code == 200:
        j_res = r.json()
        facebook_video_id = j_res.get('id')
        print ("facebook_video_id = {0}".format(facebook_video_id))
    else:
        print ("Facebook upload error: {0}".format(r.text))