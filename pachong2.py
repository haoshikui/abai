# -*- coding:utf-8 -*-
import requests
import lxml
from bs4 import BeautifulSoup
import threading
from urllib.parse import urljoin
import hashlib
import sys


# 初始版本
# 异常处理代码较少


def downloadHTML(url, content):
    c = {}
    r = requests.get(url)
    if (200 != r.status_code):
        return None
    c['url'] = url
    c['HTML'] = r.text
    content.append(c)


def getMD5(src):
    MD5 = hashlib.md5()
    MD5.update(src.encode("utf8"))
    return MD5.hexdigest()


# root 爬取根节点
# threadNum 线程数量
def craw(root, threadNum):
    urlsToCraw = set()
    urlsHaveCrawed = set()
    urlsHash = set()

    urlsHash.add(getMD5(root))

    urlsToCraw.add(root)

    while (0 != len(urlsToCraw)):
        content = []
        th = []
        for i in list(range(threadNum)):
            if (0 == len(urlsToCraw)):
                break

            urlToCraw = urlsToCraw.pop()
            urlsHaveCrawed.add(urlToCraw)

            t = threading.Thread(target=downloadHTML, args=(urlToCraw, content))
            t.start()
            th.append(t)
        for t in th:
            t.join()

        for c in content:
            soup = BeautifulSoup(c['HTML'], 'lxml')

            links = soup.find_all('a')

            for link in links:
                newUrl = link.get('href')
                newFullUrl = urljoin(c['url'], newUrl)

                # 判断当前url是否属于当前网站
                if (-1 != newFullUrl.find(root)):

                    # 解决页面相同，参数不同的重复问题
                    # 例如： www.lueur.cn/example.jsp?id=1 www.lueur.cn/example.jsp?id=2
                    # 下面的方法使得只返回一个类似上面同类型的页面

                    src = ''
                    src += newFullUrl.split('?')[0]

                    if (len(newFullUrl.split('?')) > 1):
                        args = newFullUrl.split('?')[1]

                        args = args.split('&')
                        for arg in args:
                            if (len(arg.split('=')) > 1):
                                src += arg.split('=')[0]

                    if getMD5(src) not in urlsHash:
                        urlsHash.add(getMD5(src))
                        urlsToCraw.add(newFullUrl)

                        # for test
                        print('url', newFullUrl)

    return urlsHaveCrawed


def main():
    # reload(sys)
    # sys.setdefaultencoding("utf-8")
    temp = craw('http://www.tianmen.gov.cn', 5)


if __name__ == '__main__':
    main()