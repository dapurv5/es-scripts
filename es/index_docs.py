#!/usr/bin/env/python
#
# author: apurvverma@gatech.edu

"""
Simple indexer for indexing json documents in elasticsearch

An example of a simple query is

{
  "fields": ["codes", "pid"],
  "query": {
    "term": {
      "codes": "5770"
    },
    "term": {
      "codes": "3091"
    }
  }
}
"""

import argparse
import json
import numpy as np

from elasticsearch import Elasticsearch

def main(args):
  index_name = 'psim'
  es = Elasticsearch()
  
  # Delete index if already found one
  try:
    es.indices.delete(index = index_name)
  except Exception:
    pass
  
  # Setup fresh index and mapping
  es.indices.create(index=index_name, body = {
                        "mappings": {
                           "book": {
                             "_all" : {"enabled" : "false"},       
                             "properties": {
                                "codes": {"type": "string",
                                         "term_vector": "yes",
                                         "store": "true"},
                                "pid" : {"type" : "string"},
                                "embedding": {"type": "float",
                                              "store": "true"}
                             }     
                           }
                        }
                     })
     
  with open(args.input) as input_file:
    for line in input_file:
      json_doc = json.loads(line)
      #res = es.index(index=index_name, doc_type = 'book', id = int(json_doc['pid'], 16), body = json_doc)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Specify arguments')
  parser.add_argument('--input',help='path to input file to generate indexable documents from',required=True)
  parser.add_argument('--codes', help='codes file',required=True)
  parser.add_argument('--embeddings', help='embeddings file', required=True)
  parser.add_argument('--dim', help='dimensionality of the embedding vector', required=False)
  args = parser.parse_args()
  main(args)
