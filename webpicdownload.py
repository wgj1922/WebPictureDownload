#coding=utf-8
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os, urllib, sys
from multiprocessing import Process

def getimg(imgurl, i):
    try:
        pic = requests.get(imgurl, timeout=10)
    except requests.exceptions.ConnectionError:
        print('[ERROR] Download this picture fail!!!')
        return
    file_path = '/Users/wanguojian/Desktop/test/' + str(i) + '.jpg'
    fp = open(file_path, 'wb')
    fp.write(pic.content)
    fp.close()
    file_size = os.path.getsize(file_path)

    if file_size < 10240:
        os.remove(file_path)

    print('Download[' + str(i) + '] : ' + imgurl + ' , size = ' + str(file_size))

def getimgurl(html, index):
    soup = BeautifulSoup(html, "lxml")
    imgsrc = soup.find_all("a", uigs='vieworipic')
    num = len(imgsrc)
    for i in range(num):
        imgurl = imgsrc[i].attrs['href']
        getimg(imgurl, index)

def getimgfromphantomis(orgi_sword, index):
    browser = webdriver.PhantomJS(executable_path='/usr/local/phantomis/bin/phantomjs', service_args=['--load-images=false'])
    
    searchWord = urllib.parse.quote(orgi_sword.encode('utf8'))

    for i in range(index, index+10):
        url = 'http://pic.sogou.com/d?query='+ searchWord +'&mode=1&did=1#did'+str(i)
        browser.get(url)
        browser.refresh() 
        html=browser.page_source
        getimgurl(html, i)

    browser.close()
    browser.quit()


def main():
    if len(sys.argv) <= 3:
        print('[Usage]webpicdownload.py query_word process_num pic_num')
        sys.exit()
        
    orgi_sword  = sys.argv[1]
    process_num = int(sys.argv[2])
    pic_num     = int(sys.argv[3])
    every_process_num = int(pic_num / process_num)
    
    process = []
    
    for i in range(0, every_process_num):
        process.append(i)
        process[i] = Process(target=getimgfromphantomis, args=(orgi_sword, every_process_num*i))
        process[i].start()
   
    for i in range(0, every_process_num):
        process[i].join()
    

if __name__ == '__main__':
    main()