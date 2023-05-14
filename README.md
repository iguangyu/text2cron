## A Python Library that converts human readable text to Cron Expression(Currently only supports Chinese)
## 可以将人类语言转换为cron表达式的Python库(目前仅支持中文)

### Installation
``` bash
pip install t2c
```

### usage
``` python
import t2c
# normal
cron_reg = t2c.Text2Cron('今天下午两点钟').cron()
# use openai api key
cron_gpt = t2c.Text2Cron('今天下午两点钟').gpt()
# print the cron expressions
# current time: 2023/5/15 00:25
print(cron_reg) # output: 0 14 15 5 ?
print(cron_gpt) # output: 0 14 * * *
```