# n-katalog request

import requests as r

from bs4 import BeautifulSoup as bs

def get_info(URL):
    hs = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
      "accept-language": "ru-RU,ru;q=0.7",
      "cache-control": "max-age=0",
      "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Brave\";v=\"115\", \"Chromium\";v=\"115\"",
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": "\"Windows\"",
      "sec-fetch-dest": "document",
      "sec-fetch-mode": "navigate",
      "sec-fetch-site": "cross-site",
      "sec-fetch-user": "?1",
      "sec-gpc": "1",
      "upgrade-insecure-requests": "1"
  }
    req = r.get(URL, headers=hs)
    html = req.text
    
    
    soup = bs(html, "lxml")
    price = soup.find("span",itemprop="lowPrice").get_text()
    title = soup.find("h1", itemprop='name').get_text()

    return {
        'name': title,
        'price': price,
        'link': URL
    }