import re
import json
import requests
import pendulum
import cn2an

class Text2Cron(object):
    now = pendulum.now()
    current_datetime = f"{now.hour}时{now.minute}分"
    re_dict = {
        ' ': '',
        '号': '日',
        "日": "天",
        "星期": "周",
        "礼拜": "周",
        "小时": "时",
        "钟头": "时",
        "点钟": "时",
        "点": "时",
        "小时": "时",
        "分钟": "分",
        "个半": ".5",
        "天半": ".5天",
        "半时":"30分",
        "半个时":"30分",
        "半个小时":"30分",
        "半":"30分",
        "一刻": "15分",
        "minute": "分",
        "这时候": current_datetime,
        "这个时候": current_datetime
    }
    period = r'(每个?|下[^午]|这个?)?'
    day = r'(今.|明[天]?|后[天]?|周[天1234567]?|月\d+天|[天周月年])?'
    aopm = r'(早.|上.|中.|下.|晚.)?'
    hour = r'(\d+)?' + r'[点时：:]?'
    minute = r'([0-5]?[0-9]|半|一刻)?'
    
    full_pattern = period + day + aopm + hour + minute 
    short_term = r'(\d+\.?5?)?个?([分时天周月年])之?后'
    day_pattern = r'周(\d|天)|月(\d+)天|(今.)|(明.)|(大*后.)'
    
    
    def __init__(self, text: str, usegpt = False) -> None:
        self.text = text
        # print(self.full_pattern)
        if not usegpt:
            text = text.replace('\n','')
            for key, value in self.re_dict.items():
                text = text.replace(key, value)
            self.text = cn2an.transform(text)
        
    def __to_cron(self) -> list:
        l, isshort = self.__find_util(self.text)
        if isshort:
            digit = float(l[0])
            offset = {
                '年': self.now.add(years=int(digit)), 
                '月': self.now.add(months=int(digit)),
                '周': self.now.add(weeks=digit),
                '天': self.now.add(days=digit),
                '时': self.now.add(hours=digit),
                '分': self.now.add(minutes=digit)
            }
            self.now = offset[l[1]]
            return [
                0, self.now.minute, self.now.hour, 
                self.now.day, self.now.month, '?', self.now.year,
            ]
        else:
            period, day, aopm, hour, minute = l
            everyday = False
            # period_matches = re.search(self.period_pattern, period)
            day_matches = re.search(self.day_pattern, day)
            if day_matches is not None:
                matches = day_matches.groups()
                date_day, offset_days = matches[0:2], matches[2::]
                if date_day != (None, None):
                    self.now = self.now.replace(day=int(date_day[1])) \
                        if date_day[0] is None else self.now.next(
                            int(date_day[0]) if date_day[0] != '天' else 0)
                else:
                    a,b,c = offset_days
                    self.now = self.now.add(
                        days=0 if a is not None else 1 \
                            if b is not None else c.count('大') + 2 \
                                if c is not None else 0)
            if period != '':
                if '每' in period:
                    if '天' in day:
                        everyday = True
                    # TODO
            if hour != '' and 0<= int(hour) < 24:
                hour = int(hour)
                if '晚' in aopm or '下' in aopm and hour <= 12:
                    if hour == 12:
                        self.now = self.now.replace(hour=0)
                        self.now.add(days=1)
                    else:
                        self.now = self.now.replace(hour=(12 + hour % 12))
                else:
                    self.now = self.now.replace(hour=int(hour))
            self.now = self.now.replace(minute=int(minute) if minute != '' else 0)
            self.now = self.now.replace(second=0)
            return [
                self.now.minute, self.now.hour, 
                self.now.day if not everyday else '*', 
                self.now.month if not everyday else '*',
                '?',
            ]

    def show_args(self):
        l, _ = self.__find_util(self.text)
        return l

    def cron(self) -> str:
        cron_list = self.__to_cron()
        return ' '.join([str(i) for i in cron_list])
    
    
    def __find_util(self, text: str) -> list[tuple, bool]:
        long_term = max(re.findall(pattern=self.full_pattern, string=text),
            key=lambda tup: sum(1 for val in tup if val != ''))
        short_term = re.findall(pattern=self.short_term, string=text)
        short_term = () if len(short_term) == 0 else short_term[0]
        if sum(1 for val in short_term if val != '') == 2:
            return short_term, True
        term = max([long_term, short_term],
            key=lambda tup: sum(1 for val in tup if val != ''))
        return term, term == short_term

    def gpt(self, apikey: str) -> str:        
        try:
            import openai
            openai.api_key = apikey
            res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                    "role": "system",
                    "content": "You are a helpful webapp that provides users with cron expressions"
                },{
                    "role": "user",
                    "content": f"Write a cron expression for the following and please just output the answer, say nothing else and don't explain 'current time is {self.now.to_datetime_string} {self.text}'"
                }]
            )
            return res.choices[0].message.content
        except ImportError as e:
            print('You need to install openai module to use gpt\npip install openai')
        


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='task tool argparse')
    parser.add_argument('--time', '-t', type=str, default=None, help="安排的任务时间")
    parser.add_argument('--cron', '-c', type=str, default=None, help="解析cron")
    parser.add_argument('--gpt', '-g', type=str, default=None, help="使用gpt")
    
    args = parser.parse_args()
    text = args.time
    if args.gpt is not None:
        res = Text2Cron(text, usegpt=True, apikey='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').gpt()
    else: 
        res = Text2Cron(text).cron()
        print(res)

    if args.cron is not None:
        print('= cron表达式如下 =')
        cron_exp = ' '.join([str(c) for c in res])
        res = requests.get('http://cron.ciding.cc/getCornTimes?cronExpression='+cron_exp+'&time=5')
        print('\n'.join(json.loads(res.text)['datas']))

    # import pendulum
    now = pendulum.now()
    now.add()

