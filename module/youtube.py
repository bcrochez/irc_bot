# -*-coding:UTF-8 -*

from html.parser import HTMLParser
import urllib.request
#from bs4 import BeautifulSoup

class YoutubeParser(HTMLParser):
    def reset(self):
        HTMLParser.reset(self)
        self.title = "No video"
        self.views = "0"
        self.date = ""
        self.in_div = False
        self.in_date = False
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for attr in attrs:
                name, value = attr
                if name == 'class' and value == 'watch-view-count':
                    self.in_div = True
                    return
        if tag == 'span':
            for k, v in attrs:
                if k == 'id' and v == 'eow-title':
                    for k,v in attrs:
                        if k == 'title':
                            self.title = v;
                            return
        if tag == 'strong':
            for k, v in attrs:
                if k  == 'class' and v == "watch-time-text":
                    self.in_date = True
        
    def handle_endtag(self, tag):
        if tag == 'div':
            if self.in_div:
                self.in_div = False
        if tag == 'strong':
            if self.in_date:
                self.in_date = False
        
    def handle_data(self, data):
        if self.in_div:
            self.views = data
        if self.in_date:
            self.date = data
       
yt_parser = YoutubeParser() 
print("---- youtube module loaded ----")

def get_title_and_views(url):
    yt_parser.reset()
    try:
        html = urllib.request.urlopen(url).read().decode()
        yt_parser.feed(html)
    except:
        print("*** erreur url youtube ***")
    if yt_parser.views.split('\xa0')[-1] == "vues":
        yt_parser.views = yt_parser.views.split('\xa0')[0]
    return yt_parser.title, yt_parser.views, yt_parser.date
    
#def get_title_and_views_0(url):
#    try:
#        html = urllib.request.urlopen(url).read()
#    except:
#        print("impossible d'accéder à l'url")
#    soup = BeautifulSoup(html)
#    title = get_title(soup)
#    views = get_views(soup)
#    return title, views

def get_title(soup):
    try:
        tmp = soup.title.string.split("-")
        return "-".join(tmp[0:-1]).rstrip()
    except:
        return ""

def get_views(soup):
    try:
        return soup.find_all("div", class_="watch-view-count")[0].string#.replace("\xa0", " ")
    except:
        return '0'