# -*- coding: UTF-8 -*-

# Author: Nho Quy "Nonononoki" Dinh
# License: GPL v.2 https://www.gnu.org/copyleft/gpl.html

import sys
import xbmcgui
import xbmcplugin
import urllib3
import re
import resolveurl
import HTMLParser
from urllib import unquote, urlencode
from urlparse import parse_qsl

import CommonFunctions
common = CommonFunctions
common.plugin = "JustDubs"

ADDON_URL = sys.argv[0]
HANDLE = int(sys.argv[1])

HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
	   
BASE = 'https://justdubs.org'
ALL_URL = 'https://justdubs.org/anime-list'	  

HTTP = urllib3.PoolManager()

def list_all():

	response = HTTP.request('GET', ALL_URL, headers=HEADER)
	webHTML = response.data
	#print(WebHTML);
	
	div = common.parseDOM(webHTML, "div", attrs = { "class": "view-content" })
	print repr(div)
	
	urls = common.parseDOM(div, "a", ret = "href")
	des = common.parseDOM(div, "a")
	
	print repr(urls)
	print repr(des)
	 	
	for i in range(len(urls)):
		list_item = xbmcgui.ListItem(label=HTMLParser.HTMLParser().unescape(des[i]))			  
		url = get_url(action='list_episodes', url=urls[i])
		is_folder = True
		xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
		
	xbmcplugin.endOfDirectory(HANDLE)
	

def list_episodes(url):

	print('started list_episodes')
	url = BASE + unquote(url) 
	
	response = HTTP.request('GET', url, headers=HEADER)
	WebHTML = response.data
	#print(WebHTML);
	
	div = common.parseDOM(WebHTML, "div", attrs = { "class": "list-group col-xs-12" })
	print repr(div)
	
	urls = common.parseDOM(div, "a", ret = "href")
	des = common.parseDOM(div, "div", attrs = { "class": "col-xs-7 col-sm-8" })
	thumb = common.parseDOM(WebHTML, "img", attrs = { "class": "img-responsive" }, ret = 'src')[0]
	txtDiv = common.parseDOM(WebHTML, "div", attrs = { "class": "field field-name-field-plot field-type-text-with-summary field-label-hidden" })[0]
	txt = common.parseDOM(txtDiv, "p")[0];
	
	print repr(urls)
	print repr(des)
	
	for i in range(len(urls)):
		list_item = xbmcgui.ListItem(label=HTMLParser.HTMLParser().unescape(des[i]))
		list_item.setArt({'thumb': thumb, 'icon': thumb, 'fanart': thumb})
		list_item.setInfo('video', {'plot': txt})
		
		url = get_url(action='list_streams', url=urls[i])
		is_folder = True
		xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
		
	xbmcplugin.endOfDirectory(HANDLE)

def list_streams(url):

	url = unquote(url)
	print('stream_url: ' + url)
	
	response = HTTP.request('GET', url, headers=HEADER)
	WebHTML = response.data
	#print(WebHTML);
	
	urls = common.parseDOM(WebHTML, "iframe", ret = 'src')
	print repr(urls)
	
	for i in range(len(urls)):
		list_item = xbmcgui.ListItem(label=get_domain_name(urls[i]))
		url = get_url(action='play_video', url=urls[i])
		is_folder = True
		xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
		
	xbmcplugin.endOfDirectory(HANDLE)


def play_video(url):

	url = unquote(url)
	print('video_url: ' + url)
	
	play_item = xbmcgui.ListItem(path=url)
	vid_url = play_item.getfilename()
	stream_url = resolveurl.resolve(url)
	print('direct link: ' + stream_url)
	xbmc.Player().play(stream_url) 


def get_url(**kwargs):
	return '{0}?{1}'.format(ADDON_URL, urlencode(kwargs))
	

def get_domain_name(url):
	return url.split("://")[1].split("/")[0]

def router(parameters):

	params = dict(parse_qsl(parameters))

	if params:
		if params['action'] == 'list_episodes':
			list_episodes(params['url'])
		elif params['action'] == 'list_streams':
			list_streams(params['url'])
		elif params['action'] == 'play_video':
			play_video(params['url'])
		else:
			list_all()
	else:
		list_all()


if __name__ == '__main__':
	router(sys.argv[2][1:])
	