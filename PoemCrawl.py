import requests
from bs4 import BeautifulSoup
import sys
import re
import os
#wr_id limit is 1~241211
URL = "http://www.poemlove.co.kr/bbs/board.php?bo_table=tb01&wr_id="
hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')

#return Poem Title-writer
def ParsePoem(Num):
    req = requests.get(URL+str(Num))

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.select("#content table:nth-of-type(1) strong")

    title = result[0].string
    writer = result[1].string
    #print writer

    result = soup.find_all("span","ct")

    if not os.path.exists(writer):
        os.makedirs(writer)

    
    f = open(writer+"/"+title+".txt","wb")
    result = result[0]
    try:
        for i in range(99999999):
            try:
                a = hangul.sub('', result.contents[0].strip())
                a = a + '\r\n'
                f.write(a.encode('utf-8'))
            except:
                pass
            if len(result.contents) > 2:
                break
            try:
                result = result.contents[1]
            except:
                result = result.contents[0]
        for a in result.contents:
            try:
                a = hangul.sub('', a.strip())
                a = a + '\r\n'
                f.write(a.encode('utf-8'))
            except:
                pass
    except:
        print()
    f.close()
    return title

def main():
    print ("start")
    for i in range(35690, 75690):
        try:
            print (ParsePoem(i))
        except:
            continue
        if i % 100 == 0:
            ff = open('progress.txt', 'w')
            ff.write(str(i))
            ff.close()

if __name__ == '__main__':
    main()
