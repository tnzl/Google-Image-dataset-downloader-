from pathlib import Path
from os import listdir
import re
#!/usr/bin/env python3

import os
import requests
import tkinter as tk 
from tkinter import filedialog
from sys import exit



def set_text(text):
        e.delete(0,END)
        e.insert(0,text)
        return

def download_url(url, dest, overwrite=False, pbar=None, show_progress=False, chunk_size=1024*1024, timeout=4, retries=5):
    "Download `url` to `dest` unless it exists and not `overwrite`."
    if os.path.exists(dest) and not overwrite: return

    s = requests.Session()
    s.mount('http://',requests.adapters.HTTPAdapter(max_retries=retries))
    u = s.get(url, stream=True, timeout=timeout)
    try: file_size = int(u.headers["Content-Length"])
    except: show_progress = False

    with open(dest, 'wb') as f:
        nbytes = 0
        if show_progress: pbar = progress_bar(range(file_size), auto_update=False, leave=False, parent=pbar)
        try:
            for chunk in u.iter_content(chunk_size=chunk_size):
                nbytes += len(chunk)
                if show_progress: pbar.update(nbytes)
                f.write(chunk)
        except requests.exceptions.ConnectionError as e:
            fname = url.split('/')[-1]
            from fastai.datasets import Config
            data_dir = Config().data_path()
            timeout_txt =(f'\n Download of {url} has failed after {retries} retries\n'
                          f' Fix the download manually:\n'
                          f'$ mkdir -p {data_dir}\n'
                          f'$ cd {data_dir}\n'
                          f'$ wget -c {url}\n'
                          f'$ tar -zxvf {fname}\n\n'
                          f'And re-run your code once the download is successful\n')
            print(timeout_txt)
            import sys;sys.exit(1)

def download_image(url,dest, timeout=4):
    try: 
        r = download_url(url, dest, overwrite=True, show_progress=False, timeout=timeout)
        return 1
        

    except Exception as e: 
        show_dialog(f"Error {url} {e}")
        return 0

def _download_image_inner(dest, url, i, timeout=4):
    suffix = re.findall(r'\.\w+?(?=(?:\?|$))', url)
    suffix = suffix[0] if len(suffix)>0  else '.jpg'
    return download_image(url, dest/f"{i:08d}{suffix}", timeout=timeout)

def download_images(urls, dest, max_pics=1000, max_workers:int=8, timeout=4):
    "Download images listed in text file `urls` to path `dest`, at most `max_pics`"
    
    filename=str(urls)[str(urls).rfind('/')+1:]
    urls = open(urls).read().strip().split("\n")[:int(max_pics*12/10)]
    dest.mkdir(exist_ok=True)
    print(dest)
    c=0
    
    for i in range(len(urls)):    
        c=c+_download_image_inner(dest, urls[i], c, timeout=4)
        if c==max_pics:
            print(c, ' images downloaded of',filename,'.')
            break

    return 1

def start_downloading(urls_directory_path,dest_root=Path('/home/'),max_pics=1000):
        print('Starting download in: ',dest_root)

        url_files=listdir(urls_directory_path)
        for filename in url_files:
                dest=dest_root/str(filename)
                download_images(urls_directory_path/filename,dest=dest,max_pics=max_pics)
        print('Download complete!')

def browse1():
    print('URL browse button pressed.')

    global inp1
    
    inp1=filedialog.askdirectory()
    
    inp1_entry.delete(0)
    inp1_entry.insert(0,inp1)
    
    print('URL directory selected:',inp1)

def browse2():
    print('Save to browse button pressed.')

    global inp2

    inp2=Path(filedialog.askdirectory())
    
    inp2_entry.delete(0)
    inp2_entry.insert(0,inp2)

    print('Save database to ',inp2)
        
def next():
    'configure settings here no of images for each file and other'
    print('Next button pressed')

    global data_save_root
    global urls_directory_path
    global inp1
    global inp2

    urls_directory_path= Path(inp1)
    data_save_root= Path(inp2)
    
    print('From root:',urls_directory_path)
    print('Save root:',data_save_root)
    
    start_downloading(urls_directory_path,data_save_root,max_pics=2)

    
def set_global_variable():
    "this will set global variables from gui."

    window=tk.Tk()
    window.title("Google Image dataset downloader")
    window.geometry('450x450')
        
    inp1_entry= tk.Entry(window, textvariable=inp1).grid(row=1,column=1)
    inp1_button= tk.Button(window, text= 'Browse', command=browse1).grid(row=1,column=5)
    
    inp2_entry= tk.Entry(window, textvariable=inp2).grid(row=3,column=1)
    inp2_button= tk.Button(window, text= 'Browse', command= browse2).grid(row=3,column=5)
    
    next_button= tk.Button(window, text= 'Next', command= next).grid(row=6,column=5)
    window.mainloop()

    print('Dialog box created.')

inp1=''
inp2=''

urls_directory_path=Path('/home')
data_save_root=Path('/home')

#Setting up dialog box
window=tk.Tk()
window.title("Google Image dataset downloader")
window.geometry('300x120')

inp1_entry= tk.Entry(window, textvariable=inp1)
inp1_entry.grid(row=1,column=2)

inp1_button= tk.Button(window, text= 'Browse', command=browse1)
inp1_button.grid(row=1,column=3)

inp2_entry= tk.Entry(window, textvariable=inp2)
inp2_entry.grid(row=2,column=2)

inp2_button= tk.Button(window, text= 'Browse', command= browse2)
inp2_button.grid(row=2,column=3)
    
next_button= tk.Button(window, text= 'Next', command= next).grid(row=3,column=3)
window.mainloop()

print('Dialog box closed.')

exit()



