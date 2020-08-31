#!/usr/bin/env python3

import re
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse, urljoin
import numpy as np
import colorama

# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def fetch(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    # print(response.content.decode())
    soup = BeautifulSoup(response.text, 'html.parser')

    assets = []
    for img in soup.findAll('img'):
        assets.append(img.get('src'))
    print("\n")
    links = []
    for link in soup.find_all(attrs={'href': re.compile("http")}):
        links.append(link.get('href'))
    print("\n")
    
    return(assets,links)

def getWebsiteAssets(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
        # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        # print(href)
        if not is_valid(href):
        # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                # print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        # print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    # return urls
    # return internal_urls

if __name__ == "__main__":
    site = 'https://bgr.in'
    getWebsiteAssets(site)
    print("\n")
    for site_url in internal_urls:
        assets,links = fetch(site_url)
        print(f"{GREEN}The assets of the url {site_url} are: {RESET} \n")
        print(*assets, sep='\n')
        print("\n")