#!/usr/bin/env python3

'''
  StaticWebParser (for fun)
'''


__author__  = "Breogan COSTA"
__version__ = "1.0"
__email__   = "xbcovelo (at) gmail (dot) com, breo (at) cern (dot) ch"

import logging
from lxml import html
from lxml import etree
import requests
import json
from bottledaemon import daemon_run
from bottle import get, route, run

class StaticWebHTMLParser():
  SITE_URL = ''
  json_result = []
    
  def __init__(self, new_URL = None):
    logging.basicConfig(level=logging.INFO)
    logging.debug(' StaticWeb Parser Started')
    if new_URL != None:
      try:
        self.SITE_URL = new_URL
      except:
        logging.error(' Error setting parameter. Using default one')
        self.SITE_URL = "http://www.metacritic.com/game/playstation-4"
    else:
      self.SITE_URL = "http://www.metacritic.com/game/playstation-4"

  def parseHTML(self, HTML_content = None):
    result = ""
    tittles_html = ""
    try:
      if HTML_content != None:
        logging.debug(' Parsing given HTML')
        result = HTML_content
        page_content = html.fromstring(result)
      else:
        logging.info(' Parsing %s', self.SITE_URL)
        # we must make this example Website think that we are using a Web browser
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; '
          'Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like '
          'Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        result = requests.get(self.SITE_URL, headers=headers)
        page_content = html.fromstring(result.content)
      tittles_html = page_content.xpath('//h3[@class="product_title"]')
      scores = page_content.xpath(
        '//span[@class="metascore_w medium game positive"]/text()')
      if not tittles_html:
        logging.warning(" Parsed, but not found coincidences")
      i = 0
      for elem in tittles_html:
        string = str(elem).replace("\n","").replace("  ","")
        json_elem = {
          'title' : str(elem.text_content()),'score' : scores[i]}
        i = i+1
        self.json_result.append(json_elem)
    except:
      logging.error(' Parse ERROR. Returning empty list')
      return []
    return self.json_result


class StaticWebRESTExposer():
  
  json_values = []
  
  def __init__(self, site_json_values):
    logging.basicConfig(level=logging.INFO)
    self.json_values = site_json_values
    self.defineREST()
    self.exposeREST()
  
  def searchGame(self,title):
    for r in self.json_values:
      if str(r['title']).lower() == title.lower():
        logging.debug(' Found requested game info %s for %s', r, title)
        return r
    
  def defineREST(self):
    
    @get('/games/<title>')
    def show_game_info(title):
      logging.debug(' Looking for game info for %s', title)
      return json.dumps(self.searchGame( str(title).replace("_"," ") ),
                        sort_keys=False,
                        indent=2) + "\n"

    @get('/games')
    @get('/games/')
    def games():
      return json.dumps(self.json_values, sort_keys=False, indent=2) + "\n"
    
  def exposeREST(self): 
    try:
      ''' Alternative without bottledaemon
      run(host='localhost', port=8080, debug=True)
      '''
      logging.info(' Exposing REST through embedded server. Available in '
        'http://localhost:8080/games or http://localhost:8080/games/'
        '<TITLE_OF_GAME>\n   Access it (better) running:'
        '\n\tcurl -i -H "Accept: application/json" -H "Content-Type: '
        'application/json" -X GET [address]\n   or using a Web browser')
      daemon_run()
    except:
      logging.error(' Error starting Bottle server, already running? '
                    'Ignore this message in that case.')
  

