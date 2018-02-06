# -*- coding: utf-8 -*-
import time
import sys
import os
from random import randint
from urllib.request import Request, urlopen
from urllib.request import URLError, HTTPError


# Downloading entire Web Document (Raw Page Content)
def download_page(url):
    version = (3, 0)
    cur_version = sys.version_info
    if cur_version >= version:  # If the Current Version of Python is 3.0 or above
        import urllib.request  # urllib library for Extracting web pages
        try:
            headers = {}
            headers[
                'User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:  # If the Current Version of Python is 2.x
        import urllib2
        try:
            headers = {}
            headers[
                'User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except:
            return "Page Not found"


# Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:  # If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"', start_line + 1)
        end_content = s.find(',"ow"', start_content + 1)
        content_raw = str(s[start_content + 6:end_content - 1])
        return content_raw, end_content


# Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    i = 0
    items = []
    while True:
        i += 1
        if i > 103:
            items = []
            break
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append(item)  # Append all the links in the list named 'Links'
            time.sleep(0.1)  # Timer could be used to slow down the request for image downloads
            page = page[end_content:]
    return items


def image_search(search_keyword):
    t0 = time.time()

    items = [] # Download Image Links
    iteration = "Searching for: " + str(search_keyword)
    print (iteration)
    print ("Evaluating...")
    search = search_keyword.replace(' ', '%20')

    color_param = ''
    url = 'https://www.google.com/search?q=' + search + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch' + color_param + '&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
    raw_html = (download_page(url))
    time.sleep(0.1)
    items = _images_get_all_items(raw_html)
    print ("Total Image Links = " + str(len(items)))

    t1 = time.time()
    total_time = t1 - t0
    print("Total time taken: " + str(total_time) + " Seconds")
    fatal_error = 0
    error = 0 #skipping the URL if there is any error

    if len(items) > 25:
        maximum = 25
    else:
        maximum = len(items)

    while True:
        if len(items) <= 1:
            fatal_error=1
            break
        k = randint(1,maximum)
        print("Trying downloading image number "+str(k))
        try:
            req = Request(items[k], headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            response = urlopen(req, None, 15)
            image_name = str(items[k][(items[k].rfind('/'))+1:])
            if '?' in image_name:
                image_name = image_name[:image_name.find('?')]
            if ".jpg" in image_name or ".png" in image_name or ".jpeg" in image_name or ".svg" in image_name:
                output_file = open("img/"+image_name, 'wb')
            else:
                output_file = open("img/"+image_name+".jpg", 'wb')
                image_name = image_name + ".jpg"

            data = response.read()
            output_file.write(data)
            response.close()
            error = 0

        except IOError:
            print("IOError on image " + str(k))
            error = 1
        except HTTPError:
            print("HTTPError" + str(k))
            error = 1
        except URLError:
            print("URLError " + str(k))
            error = 1
        if error == 0:
            break
    if fatal_error == 1:
        print("\n")
        print("No images with this keyword")
        return False
    else:
        output_file.close()
        print("\n")
        print("Succesfully downloaded image number "+str(k)+", "+image_name)
        return image_name

if __name__ == "__main__":
    print('better run reply.py')
