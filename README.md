## A Python Library that converts human readable text to Cron Expression
## 可以将人类语言转换为cron表达式的Python库

### Installation
``` bash
pip install t2c
```

### usage
``` python
import t2c
# normal
cron_reg_zh = t2c.Text2Cron().cron('今天下午两点钟')
cron_reg_en = t2c.Text2Cron(language='en').cron('two minutes later')
# use openai api key
cron_gpt_zh = t2c.Text2Cron().gpt()
cron_gpt_en = t2c.Text2Cron(usegpt=True, api_key='openai_api_key', language='en').gpt('two minutes later')
# print the cron expressions
# current time: 2023/5/15 00:25
print(cron_reg_zh, cron_reg_en) # output: 0 14 15 5 ? , 27 0 15 5 ?
print(cron_gpt_zh, cron_gpt_en) # output: 0 1 1 */3 * , 0 1 1 */3 * 😭
```