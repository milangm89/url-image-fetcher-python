#!/usr/bin/env python3

import re
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse, urljoin
import urllib.error
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
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(url, headers=headers)
        # print(response.content.decode())
        soup = BeautifulSoup(response.text, 'html.parser')
        assets = []
        for img in soup.findAll('img'):
            if not is_valid(img.get('src')):
                # not a valid URL
                continue
            assets.append(img.get('src'))
        print("\n")
        links = []
        for link in soup.find_all(attrs={'href': re.compile("http")}):
            if not is_valid(link.get('href')):
                # not a valid URL
                continue
            links.append(link.get('href'))
        print("\n")
        
        return(assets,links)
    except urllib.error.HTTPError as e:
        urlList.append( e )

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
                external_urls.add(href)
            continue
        urls.add(href)
        internal_urls.add(href)
    return urls

# def webassets_downloader(url):


if __name__ == "__main__":
    site = 'https://www.manoramaonline.com'
    getWebsiteAssets(site)
    print("\n")    
    for site_url in internal_urls:
        assets,links = fetch(site_url)
        print(f"{GREEN}Url: {site_url} \nAssets are as follows: {RESET} \n")
        print(*assets, sep='\n')
        print("[+] Total assets:", len(assets))
        print("\n")
        