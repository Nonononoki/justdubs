# -*- coding: UTF-8 -*-

# Author: Nho Quy "Nonononoki" Dinh
# License: GPL v.2 https://www.gnu.org/copyleft/gpl.html

import sys
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs
import urllib
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

def main_menu():

	item_all = xbmcgui.ListItem(label='All Anime')			  
	url = get_url(action='list_all')
	is_folder = True
	xbmcplugin.addDirectoryItem(HANDLE, url, item_all, is_folder)
	
	item_alphabetical = xbmcgui.ListItem(label='Anime By First Letter')			  
	url = get_url(action='list_alphabetical')
	is_folder = True
	xbmcplugin.addDirectoryItem(HANDLE, url, item_alphabetical, is_folder)
	
	item_genre = xbmcgui.ListItem(label='Anime By Genre')			  
	url = get_url(action='list_genre')
	is_folder = True
	xbmcplugin.addDirectoryItem(HANDLE, url, item_genre, is_folder)
	
	item_new = xbmcgui.ListItem(label='New Anime')			  
	url = get_url(action='list_new')
	is_folder = True
	xbmcplugin.addDirectoryItem(HANDLE, url, item_new, is_folder)
	
	item_search = xbmcgui.ListItem(label='Search')			  
	url = get_url(action='list_search')
	is_folder = True
	xbmcplugin.addDirectoryItem(HANDLE, url, item_search, is_folder)
		
	xbmcplugin.endOfDirectory(HANDLE)


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
		url = get_url(action='list_episodes', url= BASE + urls[i])
		is_folder = True
		xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
		
	xbmcplugin.endOfDirectory(HANDLE)

def list_alphabetical():

	response = HTTP.request('GET', ALL_URL, headers=HEADER)
	webHTML = response.data
	#print(WebHTML);
	
	div = common.parseDOM(webHTML, "ul", attrs = { "class": "tabs--primary nav nav-tabs" })
	print repr(div)
	
	urls = common.parseDOM(div, "a", ret = "href")
	des = common.parseDOM(div, "a")
	
	print repr(urls)
	print repr(des)
	 	
	for i in range(len(urls)):
		list_item = xbmcgui.ListItem(label=HTMLParser.HTMLParser().unescape(des[i]))			  
		url = get_url(action='list_alphabetical2', url= BASE + urls[i])
		is_folder = True
		xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
		
	xbmcplugin.endOfDirectory(HANDLE)

def list_alphabetical2(url):

	url = unquote(url) 
	response = HTTP.request('GET', url, headers=HEADER)
	webHTML = response.data
	#print(WebHTML);
	
	div = common.parseDOM(webHTML, "div", attrs = { "class": "views-fluid-grid" })
	print repr(div)
	
	urls = common.parseDOM(div, "a", ret = "href")
	des = common.parseDOM(div, "a")
	
	print repr(urls)
	print repr(des)
	 	
	for i in range(len(urls)):
		#ignore images with links
		if des[i].find("<img") < 0:
			list_item = xbmcgui.ListItem(label=HTMLParser.HTMLParser().unescape(des[i]))			  
			url = get_url(action='list_episodes', url= BASE + urls[i])
			is_folder = True
			xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
		
	xbmcplugin.endOfDirectory(HANDLE)

def list_genre():
	response = HTTP.request('GET', 'https://justdubs.org/more-genre', headers=HEADER)
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
		url = get_url(action='list_genre2', url= BASE + urls[i])
		is_folder = True
		xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
		
	xbmcplugin.endOfDirectory(HANDLE)

def list_genre2(url):
	url = unquote(url) 
	response = HTTP.request('GET', url, headers=HEADER)
	webHTML = response.data
	#print(WebHTML);
	
	div = common.parseDOM(webHTML, "div", attrs = { "class": "table-responsive" })
	print repr(div)
	
	urls = common.parseDOM(div, "a", ret = "href")
	des = common.parseDOM(div, "a")
	
	print repr(urls)
	print repr(des)
	 	
	for i in range(len(urls)):
		#ignore images with links
		if des[i].find("<img") < 0:
			list_item = xbmcgui.ListItem(label=HTMLParser.HTMLParser().unescape(des[i]))			  
			url = get_url(action='list_episodes', url= BASE + urls[i])
			is_folder = True
			xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
			
	add_next_pager(webHTML, "li", "class", "pager-next", 'list_genre2', BASE)		
	xbmcplugin.endOfDirectory(HANDLE)
	
def list_new(url = 'https://justdubs.org/latest-dubbed-anime'):
	
	response = HTTP.request('GET', url, headers=HEADER)
	webHTML = response.data
	#print(WebHTML);
	
	div = common.parseDOM(webHTML, "div", attrs = { "class": "table-responsive" })
	print repr(div)
	
	urls = common.parseDOM(div, "a", ret = "href")
	des = common.parseDOM(div, "a")
	
	print repr(urls)
	print repr(des)
	 	
	for i in range(len(urls)):
		if des[i].find("<img") < 0:
			list_item = xbmcgui.ListItem(label=HTMLParser.HTMLParser().unescape(des[i]))			  
			url = get_url(action='list_episodes', url= BASE + urls[i])
			is_folder = True
			xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
		
	add_next_pager(webHTML, "li", "class", "next", 'list_new', BASE)	
	xbmcplugin.endOfDirectory(HANDLE)

def list_search():
	kb = xbmc.Keyboard('', 'What Anime are you looking for?')
	kb.doModal()
	if (kb.isConfirmed()):
		search1 = 'https://justdubs.org/search/node/type%3Aanime_movies%2Canime_series%20%22'
		search2 = '%22'
		url = search1 + urllib.quote(kb.getText(), safe='') + search2
		print url
		response = HTTP.request('GET', url, headers=HEADER)
		webHTML = response.data
		div = common.parseDOM(webHTML, "ol", attrs = { "class": "search-results node-results" })
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
	
	else: 
		main_menu()

def list_episodes(url):

	print('started list_episodes')
	url = unquote(url) 
	print(url)
	
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
		name = HTMLParser.HTMLParser().unescape(des[i])
		list_item = xbmcgui.ListItem(label=name)
		list_item.setArt({'thumb': thumb, 'fanart': thumb})
		list_item.setInfo('video', {'plot': txt})
		
		url = get_url(action='list_streams', url=urls[i], name=name)
		is_folder = True
		xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
		
	xbmcplugin.endOfDirectory(HANDLE)

def list_streams(url, name):

	url = unquote(url)
	print('stream_url: ' + url)
	
	response = HTTP.request('GET', url, headers=HEADER)
	WebHTML = response.data
	#print(WebHTML);
	
	urls = common.parseDOM(WebHTML, "iframe", ret = 'src')
	print repr(urls)
	
	for i in range(len(urls)):
		list_item = xbmcgui.ListItem(label=get_domain_name(urls[i]))
		cmd = 'XBMC.RunPlugin({})'.format(get_url(action='download_video', url=urls[i], name=name))
		#list_item.addContextMenuItems([('Download', "download_video(url = %s, name = %s)"  % (urls[i], name))])
		list_item.addContextMenuItems([('Download', cmd)])
		url = get_url(action='play_video', url=urls[i])
		is_folder = True
		xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
		
	xbmcplugin.endOfDirectory(HANDLE) 
	
	
def add_next_pager(html, el, attr, value, action, base):
	
	div = common.parseDOM(html, el, attrs = { attr: value })
	print repr(div)
	
	url = common.parseDOM(div, "a", ret = "href")
	
	if(len(url) > 0):
		url = url[0]
		print(base + url)
			
		list_item = xbmcgui.ListItem("Load more...")			  
		url = get_url(action=action, url= base + url)
		is_folder = True
		xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder) 


def play_video(url):

	url = unquote(url)
	print('video_url: ' + url)
	
	play_item = xbmcgui.ListItem(path=url)
	vid_url = play_item.getfilename()
	stream_url = resolveurl.resolve(url)
	print('direct link: ' + stream_url)
	xbmc.Player().play(stream_url) 
	

def download_video(url, name):

	url = unquote(url)
	print('download ' + url + ": " + name)
	
	url = resolveurl.resolve(url)
	addon = xbmcaddon.Addon()
	dl = addon.getSetting('download')
	print(dl)
		
	if(len(dl) <= 0):
		xbmcgui.Dialog().ok('Download folder not set', 'Please set the download path in the addon settings') #
	else:
		download = dl + name
		#xbmc.translatePath(download)
		print(download)
		
		xbmcvfs.mkdir(download)
		dl_file = dl + name + "\\video.mp4"
		
		url = url.split('|')[0]
		
		print(url)
		#url = "https://www.adobe.com/support/products/enterprise/knowledgecenter/media/c4611_sample_explain.pdf" #test
		download_helper(url, dl_file, name)
	
def download_helper(url, dest, name):
    dp = xbmcgui.DialogProgressBG()
    dp.create("Downloading...", name)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: dl_hook(nb,bs,fs,url,dp, name))

def dl_hook(numblocks, blocksize, filesize, url=None,dp=None, name=''):
	try:
		percent = min((numblocks*blocksize*100)/filesize, 100)
		print percent
		dp.update(percent)
	except:
		dp.close()
		xbmcgui.Dialog().ok("Download failed", name)

def get_url(**kwargs):
	return '{0}?{1}'.format(ADDON_URL, urlencode(kwargs))
	

def get_domain_name(url):
	return url.split("://")[1].split("/")[0]


def router(parameters):

	params = dict(parse_qsl(parameters))

	if params:
		if params['action'] == 'list_all':
			list_all()
		elif params['action'] == 'list_alphabetical':
			list_alphabetical()
		elif params['action'] == 'list_alphabetical2':
			list_alphabetical2(params['url'])
		elif params['action'] == 'list_genre':
			list_genre()
		elif params['action'] == 'list_genre2':
			list_genre2(params['url'])
		elif params['action'] == 'list_new':
			if 'url' in params:
				list_new(params['url'])
			else:
				list_new()
		elif params['action'] == 'list_search':
			list_search()
		elif params['action'] == 'download_video':
			download_video(params['url'], params['name'])
		elif params['action'] == 'list_episodes':
			list_episodes(params['url'])
		elif params['action'] == 'list_streams':
			list_streams(params['url'], params['name'])
		elif params['action'] == 'play_video':
			play_video(params['url'])
		else:
			main_menu()
	else:
		main_menu()


if __name__ == '__main__':
	router(sys.argv[2][1:])
	