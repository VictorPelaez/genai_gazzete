# -*- coding: utf-8 -*-
""" Utility functions"""

import configparser
import re

def readConfig():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def clear_article(text):
  text = re.sub(r'\\r\\n', ' ', text)
  text = re.sub(r'\W', ' ', text)
  text = re.sub(r'\s+', ' ', text, flags=re.I)
  return text.lower()
