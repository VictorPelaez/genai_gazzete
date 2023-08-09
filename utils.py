# -*- coding: utf-8 -*-
""" Utility functions"""

import configparser
import re
from newsapi import NewsApiClient


def get_news(fdate, n_articles=20):
  """
  Description: get n_articles news from newsapi client
  -
  -
  """

  config = configparser.ConfigParser()
  config.read('genai_gazzete/config.ini')
  d_config = dict(config.items('DEFAULT'))
  newsapi = NewsApiClient(api_key=d_config['api_key'])
  q_topics = 'generative ai genai llms'
  articles = newsapi.get_everything(q=q_topics,
                                    language='en',
                                    from_param=fdate,
                                    sort_by='relevancy',
                                    page_size=n_articles)
  return articles

def clear_article(text):
  text = re.sub(r'\\r\\n', ' ', text)
  text = re.sub(r'\W', ' ', text)
  text = re.sub(r'\s+', ' ', text, flags=re.I)
  return text.lower()

def format_summary(text):
  """
  Description: it function gives some text-format
  - Remove whitespaces
  - Replace some text
  - Modify upper-case in some cases
  
  """
  text = re.sub(r'\s([?.!"](?:\s|$))', r'\1', text) 
  text =  text.replace("ai", "AI")
  text =  text.replace("llm", "LLM").replace("llms", "LLMs")
  text =  text.replace("google", "Google").replace("amazon", "Amazon").replace("microsoft", "Microsoft")
  text = '. '.join(map(lambda s: s.strip().capitalize(), text.split('.')))
  return text

def remove_summaries(df, top=10):
  """
  Description: duplicated, empty summaries and non-specific ones
  and return top N articles
  """
  df.drop_duplicates(subset=['source', 'title'], keep='first', inplace=True)
  df.drop(df[df["summary"]=="empty"].index, inplace=True)
  df = df[df['summary'].apply(lambda s: ("llms" in s) | ("llm" in s) | ("generative ai" in s) | ("ai" in s))]  
  df = df.head(top).reset_index()
  return df