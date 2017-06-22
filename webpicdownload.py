#coding=utf-8
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os, urllib

def getimg(imgurl, i):
    try:
        pic= requests.get(imgurl, timeout=10)
    except requests.exceptions.ConnectionError:
        print('[ERROR] Download this picture fail!!!')
        return
    file_path = '/Users/wanguojian/Desktop/test/' + str(i) + '.jpg'
    fp = open(file_path,'wb')
    fp.write(pic.content)    
    fp.close()
    file_size = os.path.getsize(file_path)
    
    if file_size < 10240 :
        os.remove(file_path)
        
    print('Download[' + str(i) + '] : ' + imgurl + ' , size = ' + str(file_size))
    

 
def getimgurl(html, index):
    soup = BeautifulSoup(html, "lxml")    
    imgsrc = soup.find_all("a", uigs='vieworipic')
    num = len(imgsrc)
    for i in range(num):
        imgurl = imgsrc[i].attrs['href']
        getimg(imgurl, index)

     
def main():
    browser = webdriver.PhantomJS(executable_path='/usr/local/phantomis/bin/phantomjs', service_args=['--load-images=false'])
    s = 'lovely cat'
    searchWord = urllib.parse.quote(s.encode('utf8'))  
    
    for i in range(0, 10):
        url = 'http://pic.sogou.com/d?query='+ searchWord +'&mode=1&did=1#did'+str(i) 
        browser.get(url) 
        browser.refresh()       
        html=browser.page_source
        getimgurl(html, i)
        
    browser.close()
    browser.quit()
    
main()