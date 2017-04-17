#!/usr/bin/env python3

'''
  StaticWebParser (for fun)
'''
__author__  = "Breogan COSTA"
__version__ = "1.0"
__email__   = "xbcovelo (at) gmail (dot) com, breo (at) cern (dot) ch"

import logging
from staticwebparser.StaticWebParser import *
from unittest import TestCase
import requests
import json
import unittest
import sys



class StaticWebHTMLParserTests(unittest.TestCase):
  result_mock = ""
  
  def test_parseHTML(self):
    logging.info(" [TEST] Running test_parseHTML")
    HTML_test_case = ""
    with open("tests-resources/StaticWebExample_2017-02.html", 'r', encoding='utf-8') as file:
      file.seek(0)
      HTML_test_case = file.read()
    if HTML_test_case == "":
      logging.error(" TEST: HTML code NOT loaded, not possible to continue test")
      return None
    parser = StaticWebHTMLParser()
    self.result_mock = parser.parseHTML(HTML_test_case)
    self.assertFalse(self.result_mock == [])
    
  def exposeLocalHTMLREST(self):
    StaticWebRESTExposer(self.result_mock)
  
  def test_daemon_runing(self):
    logging.info(" [TEST] Running test_runing")
    games_result = requests.get("http://localhost:8080/games/")
    self.assertTrue("[200]" in str(games_result))
  
  def test_games_GET(self):
    logging.info(" [TEST] Running test_games_GET")
    games_result = requests.get("http://localhost:8080/games/")
    orig = str(json.dumps(self.result_mock, sort_keys=False, indent=2) + "\n")
    logging.debug("Original \n", orig)
    result = str(games_result.text)
    logging.debug("Result\n",result)
    ''' Next is to avoid non-printable characters issues with answer and some 
        random inversions in the ('title','score') pair with results: some times 
         the output of json.dumps returns the result inverting the order to
        ('score','title'), that's why I do .replace("\",","\"")
    '''
    for line in result.splitlines():
      line_str = str(line).replace("  ","").replace("\",","\"")
      if not line_str in orig:
        logging.debug("line \"{}\" in orig ".format(line_str))
        logging.debug("\tLINE in ORIG: ", line_str in orig,"\n")
      self.assertTrue(line_str in orig)
    
  def test_games_GET_one(self,game):
    logging.info(" [TEST] Running test_games_GET_one for case {}".format(game))
    games_result = requests.get("http://localhost:8080/games/"+game)
    orig = str(json.dumps(self.result_mock, sort_keys=False, indent=2) + "\n")
    logging.debug("Original \n", orig)
    result = str(games_result.text)
    ''' Next is to avoid non-printable characters issues with answer and some 
        random inversions in the ('title','score') pair with results: some times 
         the output of json.dumps returns the result inverting the order to
        ('score','title'), that's why I do .replace("\",","\"")
    '''
    for line in result.splitlines():
      line_str = str(line).replace("  ","").replace("\",","\"")
      if not line_str in orig:
        logging.debug("line \"{}\" in orig ".format(line_str))
        logging.debug("\tLINE in ORIG: ", line_str in orig,"\n")
      self.assertTrue(line_str in orig)

def main():
  if sys.argv[len(sys.argv)-1] != "stop":
    logging.basicConfig(level=logging.INFO)
    
    tests = StaticWebHTMLParserTests()
    tests.test_parseHTML()
    tests.exposeLocalHTMLREST()
    tests.test_daemon_runing()
    tests.test_games_GET()
    tests.test_games_GET_one("Nioh")
    tests.test_games_GET_one("nioh")
    tests.test_games_GET_one("yakuza_0")
  else:
    print('Stopping ', sys.argv[len(sys.argv)-2])
  
if __name__ == "__main__":
  main()
  
