urls = ['https://www.bbc.com/news','https://www.abc.net.au/news/']

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
    timestamp = pd.Timestamp.now()
    df_scan = df_scan.append({'url':url,'datetime':timestamp},ignore_index=True)
    df_new_images = pd.DataFrame({'image_url':img_list,'scanned':False})
    df_img = df_img.append(df_new_images.loc[~(df_new_images.image_url.isin(df_img.image_url))],ignore_index=True)
    df_appearance = df_appearance.append(pd.DataFrame({'url':url,'datetime':timestamp,'image_url': img_list}),ignore_index=True)
    

def scan_for_faces(img):
    try:
        time.sleep(3)
        this_image = image(img)
        faces = this_image.get_image_faces()
        print("Image: " + img)
        print("Number of faces: " + str(len(faces)))
        return true
    except:
        return false

df_img.loc[~df_img.scanned,'scanned'] = df_img.loc[~df_img.scanned].map(scan_for_faces)

'''for img in img_list:
    this_image = image(img)
    faces = this_image.get_image_faces()
    print("Image: " + img)
    print("Number of faces: " + str(len(faces)))
    time.sleep(3)'''
    




    
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