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
import pandas as pd
from skimage.transform import resize

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
        except Exception as e:
            tune_search = wiki.search(self.title)
            print(f"Tune search:\n {tune_search}")
            print("[ERROR] Page not read! See below errors:")
            print(e)
            return tune_search
        return self.page
    def get_images_links(self):
        self.links_images = self.page.images
        self.links_images = sorted([i for i in self.links_images if i.endswith('.jpg') or i.endswith('.png')])
        return self.links_images
        # page.split('\n')