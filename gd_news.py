urls = ['https://www.bbc.com/news','https://www.abc.net.au/news']

https://www.alexa.com/topsites/category/Top/News

new york times
CNN
washington post
MSNBC
fox news
cnbc
reuters
bloomberg
wsj.com
usatoday.com
nypost.com
usnews.com

chron.com
dw.com

guardian
the age
sydney morning herald

indiatimes.com
hindustantimes.com
indianexpress.com


from selenium import webdriver
driver = webdriver.Chrome()

#import time

from lib.image_scraper import *
from lib.image import *

#import urllib.request
import time

import pandas as pd


try:
    df_scan = pd.read_parquet('data/scans.parquet')
    df_img = pd.read_parquet('data/images.parquet')
    df_appearance = pd.read_parquet('data/appearances.parquet')
    df_faces = pd.read_parquet('data/faces.parquet')
except:
    df_scan = pd.DataFrame({})
    df_img = pd.DataFrame(columns=['image_url','scanned'])
    df_appearance = pd.DataFrame({})
    df_faces = pd.DataFrame({})

for url in urls:
    img_scraper = image_scraper(url,driver)
    img_list = img_scraper.image_list()
    timestamp = pd.Timestamp.now().round('s')
    df_scan = df_scan.append({'url':url,'datetime':timestamp},ignore_index=True)
    df_new_images = pd.DataFrame({'image_url':img_list,'scanned':False})
    df_img = df_img.append(df_new_images.loc[~(df_new_images.image_url.isin(df_img.image_url))],ignore_index=True)
    df_appearance = df_appearance.append(pd.DataFrame({'url':url,'datetime':timestamp,'image_url': img_list}),ignore_index=True)
    

def scan_for_faces(img):
    print("Scanning " + img + " for faces.") 
    global df_faces
    try:
        time.sleep(3)
        print("Creating image")
        this_image = image(img)
        print("Getting faces")
        faces = this_image.get_image_faces()
        print("Image: " + img)
        print("Number of faces: " + str(len(faces)))
        df_faces = df_faces.append(pd.DataFrame({
            'img':img,
            'left':[f.left for f in faces],
            'top':[f.top for f in faces],
            'width':[f.width for f in faces],
            'height':[f.height for f in faces],
            'age':[f.age for f in faces],
            'gender':[f.gender for f in faces],
            'smile':[f.smile for f in faces],
            'emotion':[f.emotion for f in faces]            
        }))
        return True
    except:
        return False

df_img.loc[df_img.scanned == False,'scanned'] = df_img.loc[df_img.scanned == False,'image_url'].map(scan_for_faces)

df_scan.to_parquet('data/scans.parquet')
df_img.to_parquet('data/images.parquet')
df_appearance.to_parquet('data/appearances.parquet')
df_faces.to_parquet('data/faces.parquet')




    
#https://azure.microsoft.com/en-au/pricing/details/cognitive-services/face-api/

#Todo:
#Self-lookup to check you're not doubling up on pictures
#Table for occurences
#Table for images (de-duped).
#Call Azure Face API at spaced intervals (once per 3 seconds).


'''
    Load existing images, scans and faces.
    Load images from urls.
    Filter to get list of images which haven't been scanned.
    
    


'''