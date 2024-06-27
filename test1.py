import csv

import requests
from lxml import etree

#得到每一页的html
def get_url(i):
    base_url = 'https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset='
    url = base_url + str(i)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    return html

#在每一页中获取每个歌单链接
def get_link(html,j):

    base_url2 = '/html/body/div[3]/div/ul/li[' + str(j) + ']/p[1]/a'
    tt = html.xpath(base_url2)

    if len(tt) == 0:
        tt = html.xpath('/html/body/div[3]/div/ul/li[' + str(j) + ']/div/a')
    else:
        tt = html.xpath(base_url2)

    link = 'https://music.163.com'+ tt[0].get('href')

    url2 = link
    headers = {'user-agent':'Mozilla/5.0'}
    response2 = requests.get(url2,headers=headers)
    html2 = etree.HTML(response2.text)
    return html2

#进入链接里获取
def get_more(html2):

    # data = html2.xpath('//*[@id="auto-id-A7SXxz8nCYO7lVM"]/div[2]/div/div[2]/span')
    # print(data[0].text)
    #biaoti
    tt2 = html2.xpath('/html/body/div[3]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/h2')
    title = tt2[0].text
    print(title)

    #id
    id2 = html2.xpath('/html/body/div[3]/div[1]/div/div/div[1]/div[2]/div/div[2]/span[1]/a')
    id = id2[0].text
    print(id)

    #播放量
    bof = html2.xpath('/html/body/div[3]/div[1]/div/div/div[2]/div[1]/div[1]/strong')
    play = bof[0].text
    print(play)
    #简介
    brief = html2.xpath('/html/body/div[3]/div[1]/div/div/div[1]/div[2]/div/p/text()')
    print(brief)
    #标签
    tag1 = html2.xpath('/html/body/div[3]/div[1]/div/div/div[1]/div[2]/div/div[4]/a[1]/i/text()')
    print(tag1)
    tag2 = html2.xpath('/html/body/div[3]/div[1]/div/div/div[1]/div[2]/div/div[4]/a[2]/i/text()')
    print(tag2)
    tag3 = html2.xpath('/html/body/div[3]/div[1]/div/div/div[1]/div[2]/div/div[4]/a[3]/i/text()')
    print(tag3)
    tags = tag1 + tag2 + tag3
    print(tags)
    #收藏量
    like = html2.xpath('/html/body/div[3]/div[1]/div/div/div[1]/div[2]/div/div[3]/a[3]/i')
    collect = like[0].text
    print(collect)
    #日期
    data = html2.xpath('/html/body/div[3]/div[1]/div/div/div[1]/div[2]/div/div[2]/span[2]')
    data = data[0].text
    print(data)

    print('-----------------------------------------------------------')

    return title,id,play,brief,tags,collect,data

if __name__ == '__main__':

    f = open('datamusic.csv', 'w', encoding='utf-8',newline='')

    csv_writer = csv.writer(f)
    csv_writer.writerow(['titlesum', 'idsum', 'playsum', 'briefsum', 'tagsum', 'collectsum', 'datasum'])

    for i in range (0,630,35):
        for j in range(1,35):
            html = get_url(i)
            html2 = get_link(html,j)
            title,id,play,brief,tags,collect,data = get_more(html2)

            f = open('datamusic.csv','a',encoding='utf-8',newline='')

            csv_writer = csv.writer(f)

            csv_writer.writerow([title,id,play,brief,tags,collect,data])

