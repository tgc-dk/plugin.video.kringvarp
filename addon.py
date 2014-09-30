import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import urllib2
from BeautifulSoup import BeautifulSoup


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:
    # First the live feed
    url = 'http://217.172.83.186/fo/videohigher/playlist.m3u8'
    li = xbmcgui.ListItem('Watch Kringvarp Live', iconImage='DefaultVideo.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

    # Then a folder for programs
    url = build_url({'mode': 'programlist'})
    li = xbmcgui.ListItem('Sendingar', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'programlist':
    # Get a list of programs from kvf.fo and add a folder per program
    url = 'http://kvf.fo/podcast'
    source = urllib2.urlopen(url)
    # Turn the saved source into a BeautifulSoup object
    soup = BeautifulSoup(source, convertEntities=BeautifulSoup.HTML_ENTITIES)
    for span in soup.findAll('span', {'class': ['field-content']}):
        title = span.text
        # By replacing http by rss XBMC can figure out to do lists automaticly
        feedurl = span.find('a')['href'].replace('http', 'rss')
        li = xbmcgui.ListItem(title, iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=feedurl, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
