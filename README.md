## A Python Library that converts human readable text to Cron Expression(Currently only supports Chinese)
## 可以将人类语言转换为cron表达式的Python库(目前仅支持中文)

### Installation
``` bash
pip install --upgrade openai
```

### useage
``` python
import t2c
# normal
cron_reg = t2c.Text2Cron('今天下午两点钟').cron()
# use openai api key
cron_gpt = t2c.Text2Cron('今天下午两点钟').gpt()
# print the cron expressions
print(cron_reg) # output: [4, 47, 14, 15, 5, '?', 2023]
print(cron_gpt) # output: 0 14 * * *
```