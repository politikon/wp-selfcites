"""
WP self-cites

This (dirty) script parses a Wordpress export XML, tracing the links to posts of 
the same blog, and outputs a GEXF-formatted directed graph of the self-citations.
Examples: http://juanfont.eu/graph/test.html
          http://box.jisko.net/d/f59c0a02

Use it as you like. 

2013/12/04 - Juan Font - juanfontalonso@gmail.com
"""

import xml.etree.ElementTree as ET
from gexf import Gexf
import re

GEXF_OUTPUT_FILE='politikon.gexf'
INPUT_WP_XML='/home/juan/politikon.wordpress.2011.xml'

def get_post_links(content):
  if content:
    return re.findall("http://politikon.es/\d\d\d\d/\d\d/[\d\d/]*[\w*-]*/", content)
  else:
    return []

def get_color(author):
  if not author:
    return (255, 255, 255)
  if author=='rsenserrich':
    return (255,0,0)
  if author=='kikollaneras':
    return (119,0,119)
  if author=='jorgegalindo':
    return (0,0,255)
  if author=='jorgesanmiguel':
    return (255,128,0)
  if author=='pablosimon':
    return (255,255,0)
  if author=='juanfont':
    return (0,255,255)
  if author=='cives':
    return (0,255,0)
  if author=='ramonmateo':
    return (26,83,24)
  if author=='kantor':
    return (194,78,78)
  if author=='octavio-medina':
    return (93,0,0)
  return (255,255,255)


def main():
  gexf = Gexf("Politikon","Autoreferences graph")
  graph=gexf.addGraph("directed","static","a hello world graph")

  tree = ET.parse(INPUT_WP_XML)
  root = tree.getroot()

  orphan = []

  for item in root[0].findall('item'):
    if re.match("http://politikon.es/\d\d\d\d/\d\d/\d\d/([\w*-]*)/", item.find('link').text):    
      post_id = re.match("http://politikon.es/\d\d\d\d/\d\d/\d\d/([\w*-]*)/", item.find('link').text).group(1)
      post_link = item.find('link').text
      r,g,b = get_color(item.find('{http://purl.org/dc/elements/1.1/}creator').text)
      graph.addNode(id=str(post_id),label=str(post_link), r=str(r), g=str(g), b=str(b))
      links = get_post_links(item.find('{http://purl.org/rss/1.0/modules/content/}encoded').text)
      if links:
        for link in links:
          link_id = re.match("http://politikon.es/\d\d\d\d/\d\d/[\d\d/]*([\w*-]*)/", link).group(1)
          if link_id in orphan:
            orphan.remove(link_id)
          if graph.nodeExists(link_id):
            graph.addEdge(post_id+"->"+link_id, post_id, link_id)
      else:
        orphan.append(post_id)
        
  for o in orphan:
    del graph._nodes[o]
      
  output_file=open(GEXF_OUTPUT_FILE,"w")
  gexf.write(output_file)


if __name__ == "__main__":
  main()
