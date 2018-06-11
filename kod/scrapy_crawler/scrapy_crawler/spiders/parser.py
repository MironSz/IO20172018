# -*- coding: utf-8 -*-
from scrapy.selector import Selector
import re
from datetime import datetime,timedelta
import unittest

def strIsTime(dateStr):
    def fnormal(matchObj):
        d = int(matchObj.group(1))
        m = int(matchObj.group(2))
        y = int(matchObj.group(3))
        return datetime(year=y,month=m,day=d)
    def fyesterday(matchObj):
        curr  = datetime.now()
        h = matchObj.group(2)
        m = matchObj.group(3)
        ago = timedelta(days=1)
        result = curr.replace(hour=int(h),minute=int(m))
        return result - ago
    def fminutesAgo(matchObj):
        curr  = datetime.now()
        howManyMinutes = matchObj.group(1)
        ago = timedelta(minutes=int(howManyMinutes))
        return curr - ago
    def fhoursAgo(matchObj):
        curr  = datetime.now()
        howManyHours = matchObj.group(1)
        ago = timedelta(hours=int(howManyHours))
        return curr - ago
    def fdaysAgo(matchObj):
        curr  = datetime.now()
        howManyDays = matchObj.group(1)
        ago = timedelta(days=int(howManyDays))
        return curr - ago

    functions = [fnormal,fyesterday,fminutesAgo,fhoursAgo,fdaysAgo]

    patterns = ["(\d{2})-(\d{2})-(\d{4})",
                "(wczoraj|yesterday)\s*\((\d{1,2}):(\d{2})\)",
                "(\d{1,2})\s*min\.?\s*temu",
                "(\d{1,2})\s*h\s*temu",
                "(\d{1,2})\s*(dni|days)\s*temu"]

    for i in range(len(patterns)):
        matchObj = re.search(patterns[i], dateStr)
        if matchObj is not None:
            # print(patterns[i])
            return functions[i](matchObj)
    return datetime.now()


def extract_comment(body):
  #MAIN_COMMENT_CLASS = 'ZAGLdcz'
  #SUB_COMMENT_CLASS = '_1psQ5BP'
  selector = Selector(text = body)
  dclass = selector.xpath('//body/div/@class').extract()[0]
  print(dclass)

  comment = None
  time = None

  comment = selector.xpath('//p/span/span/text()').extract()[0]

  old_times = selector.xpath('//span[@class="_1a6MrkE"]/div/span/text()').extract()
  if old_times:
    time = old_times[0]

  new_times = selector.xpath('//div[@class="_3fn6S4H"]/following-sibling::span/text()').extract()
  if new_times:
    time = new_times[0]
      
  temp_time = selector.xpath('//span[@class="_2266F5s"]/span/text()').extract()
  if temp_time:
    time = temp_time[0]
    
  return {
    'domain': 'wiadomosci.wp.pl',
    'text': comment,
    'time': strIsTime(time)
  }

ex=['''
<div class="ZAGLdcz">
    <div class="_2tw1Q-l">
        <div class="_2vQ-kLI">
            <button class="_3SsZfIC _31biZiI">Zgłoś</button>
        </div>
    </div>
    <span class="LkfRSB8">AS</span>
    <span class="_1a6MrkE">
        <div>
            <div class="_3fn6S4H">
                <span class="">
                    <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 26 26">
                        <defs>
                            <style>
                                .svg-star {
                                    fill: #f3f3f3;
                                    stroke: #797979;
                                    stroke-linejoin: round;
                                    stroke-opacity: 0.4;
                                    stroke-width: 2px;
                                    fill-rule: evenodd;
                                }
                            </style>
                        </defs>
                        <path class="svg-star" d="M52,125l3.955,7.541L64,134.167l-5.6,6.286L59.415,149,52,145.342,44.584,149l1.016-8.546L40,134.167l8.044-1.625L52,125"
                            transform="translate(-39 -124)"></path>
                    </svg>
                </span>
            </div>
            <span>25 min. temu</span>
        </div>
    </span>
</div>
<p class="_2oI562d">
    <span>
        <span>DNO aż żal .</span>
    </span>
</p>
<div class="Keg2pKH">
    <button class="_1tk8-du">Odpowiedz</button>
    <div class="TQ8uVRx _3QTnqHE">
        <div class="_363wu-W" data-votes="21">
            <span class="">
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22">
                    <path d="M421,313h22v6H421v-6Zm8-8h6v22h-6V305Z" transform="translate(-421 -305)"></path>
                </svg>
            </span>
        </div>
        <div class="_2bWAj-M" data-votes="2">
            <span class="">
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="6" viewBox="0 0 22 6">
                    <rect width="22" height="6"></rect>
                </svg>
            </span>
        </div>
    </div>
</div>
''',
'''
<div class="_1psQ5BP">
    <div class="LOIrgd-">
        <button class="_3SsZfIC _31biZiI">Zgłoś</button>
    </div>
    <span class="_1Nau3q-">Pivi</span>
    <span class="_2266F5s">
        <span>2 min. temu</span>
    </span>
</div>
<p class="_2880t66">
    <span>
        <span>polsat należy do tvpis</span>
    </span>
</p>
<div class="_1Zbcq-m">
    <div class="TQ8uVRx _3rYkM0M _3QTnqHE">
        <div class="_363wu-W" data-votes="0">
            <span class="">
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22">
                    <path d="M421,313h22v6H421v-6Zm8-8h6v22h-6V305Z" transform="translate(-421 -305)"></path>
                </svg>
            </span>
        </div>
        <div class="_2bWAj-M" data-votes="0">
            <span class="">
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="6" viewBox="0 0 22 6">
                    <rect width="22" height="6"></rect>
                </svg>
            </span>
        </div>
    </div>
</div>
''','''
<div class="ZAGLdcz">
    <div class="_2tw1Q-l">
        <div class="_2vQ-kLI">
            <button class="_3SsZfIC _31biZiI">Zgłoś</button>
        </div>
    </div>
    <span class="LkfRSB8">iinternautkanternautka</span>
    <span class="_1a6MrkE">
        <div>
            <span>11-04-2018</span>
        </div>
    </span>
</div>
<p class="_2oI562d">
    <span>
        <span>O moj Boze jezeli 93% telewidzow nie wierzy w techniczne bzdury Macierewicza to po co oddawac tak drogi i cenny czas
            antenowy na takie bzdety!! Juz nie mozna na te konfabulacje patrzec ,wlaczam telewizor</span>
    </span>
    <span>
        <!-- react-text: 1037 -->...
        <!-- /react-text -->
        <!-- react-text: 1038 -->&nbsp;
        <!-- /react-text -->
        <span class="_1rh9-ML">Czytaj całość</span>
    </span>
</p>
<div class="Keg2pKH">
    <button class="_1tk8-du">Odpowiedz</button>
    <div class="TQ8uVRx _3QTnqHE">
        <div class="_363wu-W" data-votes="5">
            <span class="">
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22">
                    <path d="M421,313h22v6H421v-6Zm8-8h6v22h-6V305Z" transform="translate(-421 -305)"></path>
                </svg>
            </span>
        </div>
        <div class="_2bWAj-M" data-votes="0">
            <span class="">
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="6" viewBox="0 0 22 6">
                    <rect width="22" height="6"></rect>
                </svg>
            </span>
        </div>
    </div>
</div>
''']

class TestExtract(unittest.TestCase):
    def test_extract_comment(self):
        for body in ex:
            res = extract_comment(body)
            self.assertTrue(res['text'] is not None)
            self.assertTrue(res['domain'] is not None)
            forbidden = ['Czytaj Całość', 'Rozwiń Komentarz']
            for text in forbidden:
                for value in [res['text'], res['domain']]:
                    self.assertFalse(text in value)


# if __name__ == '__main__':
#     unittest.main()

TestExtract().test_extract_comment()

  