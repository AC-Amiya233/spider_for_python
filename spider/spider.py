from urllib import request

import re
import ssl

class Spider :
    #for test
    url = 'https://www.manhuagui.com/rank/'

    root_pattern = '<tr>([\w\W]*?)</tr>'

    general_rank_pattern = '<td class="rank-no">([\w\W]*?)</td>'
    number_pattern = '>([\d]*?)<'

    general_title_pattern = '<td class="rank-title"><h5>([\w\W]*?)</h5>([\w\W]*?)</td>'
    word_pattern = '>([\w\W]*?)<'

    score_pattern = '<td class="rank-score">([1-9]\d*\.?\d*)</td>'

    def __fetch_content(self) :
        accepted = request.urlopen(self.url)
        htmls = accepted.read()
        content = str(htmls, encoding='utf-8')
        return content

    def __analysis(self, content) :
        list = []
        root_html = re.findall(Spider.root_pattern, content)
        flag = True
        for html in root_html :
            if (flag) :
                flag = False
                continue
            rank = re.findall(Spider.general_rank_pattern, html)
            rank = re.findall(Spider.number_pattern, rank[0])
            name = re.findall(Spider.general_title_pattern, html)
            state = re.findall(Spider.word_pattern, name[0][1])
            name = re.findall(Spider.word_pattern, name[0][0])
            score = re.findall(Spider.score_pattern, html)
            record = {'rank' : rank[0], 'name' : name[0], 'state' : state[0], 'score' : score[0]}
            list.append(record)
            # print(record)
        return list

    def __refine(self, data) :
        pass

    def __sort(self, data) :
        data = sorted(data, key = self.__sort_seed, reverse = True)
        return data

    def __sort_seed(self, info) :
        return float(info['score'])

    def __show(self, data):
        for info in data :
            print('Rank: %-5s, Name: %-40s, State: %-5s, Score: %-5s' % (info['rank'], info['name'], info['state'], info['score']))

    def go(self) :
        content = self.__fetch_content()
        list = self.__analysis(content)
        self.__show(list)

    def go_with_temperature(self) :
        content = self.__fetch_content()
        list = self.__analysis(content)
        list = self.__sort(list)
        self.__show(list)

# run the spider
spider = Spider()
# spider.go()
spider.go_with_temperature()