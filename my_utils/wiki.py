from my_utils import mashrooms as mr
import wikipedia as wiki
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import requests
from io import BytesIO
import skimage
from pprint import pprint
import numpy as np

def read_wiki_images(url, show_image=False):
    if isinstance(url, list):
        if len(url)>3:
            cols = 3
            rows = len(url)//cols
        else:
            cols = len(url)
            rows = 1
    else:
        rows = 1
        cols = 1
    img = skimage.io.imread(url)
    if show_image:
        plt.rcParams['figure.figsize'] = (3,3)
        plt.imshow(img);
        plt.show()
        
class WikiArticle(object):
    def __init__(self, title = '', language = 'ru'):
        self.title = title
        self.lang = language
        wiki.set_lang(self.lang)
    def set_lang(self):
        wiki.set_lang(self.lang)
    
    def get_article_wiki(self):
        try:
            self.page = wiki.WikipediaPage(self.title)
            return self.page
        except Exception as e:
            print("[ERROR] Page not read! See below errors:")
            print(e)
    def get_images_links(self):
        self.links_images = self.page.images
        self.links_images = [i for i in self.links_images if i.endswith('.jpg') or i.endswith('.png')]
        return self.links_images
        # page.split('\n')

