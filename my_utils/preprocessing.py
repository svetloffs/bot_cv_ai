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
from tqdm import tqdm
from my_utils.wiki import WikiArticle
import os

def check_question(item, regex_search=True):
    mashrooms_dict = mr.mashrooms_dict
    # item = mashrooms_dict[-1]['rus']
    df_mashrooms = pd.DataFrame(mashrooms_dict)
    result = df_mashrooms[df_mashrooms['rus'].str.contains(item, regex=regex_search)]
    # return result['rus'].tolist()
    return result.to_dict(orient='records')

def read_and_write(path, i):
    os.makedirs("./temp_img", exist_ok=True)
    img = skimage.io.imread(path)
    H, W = img.shape[:2]
    print(f"[INFO] Image shape: {img.shape}")
    
    scale_H = 256/H
    scale_W = 256/W
    scale_H, scale_W
    if H <= W:
        img_re = resize(img, (int(H*scale_H), int(W*scale_H)), anti_aliasing=True)
    if H > W:
        img_re = resize(img, (int(H*scale_W), int(W*scale_W)), anti_aliasing=True)
    img = np.array(img_re*255, dtype=np.uint8)
    print(f"[INFO] Image Re-shape: {img.shape}")
    skimage.io.imsave(f'./temp_img/{i}.jpg', img)
    return img

def read_wiki_images(links_images, show_image=False):
    if isinstance(links_images, list):
        plt.rcParams['figure.figsize'] = (3,3)
        if len(links_images) > 3:
            cols = 3
            rows = len(links_images) // cols
        else:
            cols = len(links_images)
            rows = 1
        for i, path in tqdm(enumerate(links_images)):
            img = read_and_write(path, i)
            if show_image:
                plt.imshow(img);
                plt.show()
        # return img
    else:
        img  = read_and_write(links_images)
        if show_image:
            plt.rcParams['figure.figsize'] = (3,3)
            plt.imshow(img);
            plt.show()
        # return img

def check_question_handle(message):
    return [i['rus'] for i in check_question(message)]

def check_status(message):
    return [i['eat'] for i in check_question(message)]

def wiki_article_info(item, language='ru', show_image=False):
    print('WikiArticle - Get text:', item)
    page = WikiArticle(item, language)
    print(f"[wiki_article_info] - Answer Wiki type: {type(page)}")
    # if isinstance(page, dict):
    #     return page
    # page = WikiArticle('World', 'ru')
    # page = WikiArticle('Волоконница звёздчатоспоровая', 'ru')
    try:
        article = page.get_article_wiki()
        img_links = page.get_images_links()
        url = article.url
    except:
        return page.get_article_wiki()
    print(f"Images: {img_links}")
    print(f"URL page: {article.url}")
    # print(f"Categories: {article.categories}")
    content = [i for i in article.content.split('\n') if i!='']
    sections_article = [i for i in article.content.split('\n') if i!='' and i.startswith("==")]
    img_wiki = read_wiki_images(img_links, show_image=show_image)
    answer = {"article": article, "content": content, "sections_article": sections_article, "img_wiki":img_wiki}
    title = answer['content'][0].split('\n')
    # pprint(title)
    body = answer['content'][1:]
    body_blocks_title = {j:i for j, i in enumerate(body) if i.startswith('==')}
    body_blocks_content = {j:i for j, i in enumerate(body) if not i.startswith('==')}
    A = np.array(list(body_blocks_title.keys()))
    B = np.array(list(body_blocks_content.keys()))
    body_content = []
    info_wiki = {}
    for i in range(len(A)+1):
        try:
            res = B[np.where((B[:] >= A[i]) & (B[:] < A[i+1]))].tolist()
            body_content = [body_blocks_content[j] for j in res]
            info_wiki[body_blocks_title[A[i]].strip().replace('=','').strip()] = body_content
            body_content = []
        except Exception as e:
            continue
    pprint(list(info_wiki.keys()))
    return title, url, info_wiki