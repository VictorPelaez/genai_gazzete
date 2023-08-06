# -*- coding: utf-8 -*-
""" Utility functions"""

import configparser
import re


def readConfig():
  config = configparser.ConfigParser()
  config.read('genai_gazzete/config.ini')
  return config

def clear_article(text):
  text = re.sub(r'\\r\\n', ' ', text)
  text = re.sub(r'\W', ' ', text)
  text = re.sub(r'\s+', ' ', text, flags=re.I)
  return text.lower()

def remove_summaries(df):
  """
  Description: duplicated, empty summaries and non-specific ones
  """
  df.drop_duplicates(subset=['source', 'title'], keep='first', inplace=True)
  df.drop(df[df["summary"]=="empty"].index, inplace=True)
  df = df[df['summary'].apply(lambda s: ("llms" in s) | ("llm" in s) | ("generative ai" in s) | ("ai" in s))]  
  return df