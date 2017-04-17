#!/usr/bin/env python3

''' 
  Main module of the StaticWebParser (for fun)
'''

__author__  = "Breogan COSTA"
__version__ = "1.0"
__email__   = "xbcovelo (at) gmail (dot) com, breo (at) cern (dot) ch"

import logging
import atexit

from staticwebparser.StaticWebParser import *
#from mypackage.myothermodule import add

@atexit.register
def close():
    logging.info("Exiting main for StaticWebParser, closing bottle daemon.")
    

def main():
  logging.basicConfig(level=logging.INFO)
  parser = StaticWebHTMLParser()
  result = parser.parseHTML()
  if result == []:
    logging.error(' ERROR parsing page HTML code, it WILL NOT be resulst')
  rest   = StaticWebRESTExposer(result)


if __name__ == "__main__":
  main()

