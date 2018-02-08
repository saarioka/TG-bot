from lxml import html
import requests

page = requests.get('https://unisafka.fi/tty/')
tree = html.fromstring(page.content)
ruuat = []
ruuat += tree.xpath('')
ruuat += tree.xpath('//*[@id="food-wrapper"]/div/ul/li[1]/div[2]/span[1]/text()')
ruuat += tree.xpath('//*[@id="food-wrapper"]/div/ul/li[1]/div[2]/span[2]/text()')
for i in range (0,len(ruuat)):
    print(ruuat[i])