import requests
import zapv2
source = 'http://localhost:8081'
apiKey = 'j9782ud4rme7p4bghnrmj6ul0v'
context_id = '2'
user_id = '19'
title = 'ZAP_test'
template = 'traditional-html'
zap = zapv2.ZAPv2(apikey=apiKey, proxies={'http': 'http://127.0.0.1:8081', 'https': 'http://127.0.0.1:8081'})

url_1 = '/JSON/spider/action/scanAsUser/?apikey='
url_2 = '&contextId='
url_3 = '&userId='
url_4 = '&url=&maxChildren=&recurse=&subtreeOnly='

url_5 = '/JSON/ascan/action/scanAsUser/?apikey='
url_6 = '&recurse=&scanPolicyName=&method=&postData='

url_7 = '/JSON/reports/action/generate/?apikey='
url_8 = '&title='
url_9 = '&template='
url_10 = '&theme=&description=&contexts=&sites=&sections=&includedConfidences=&includedRisks=&reportFileName=&reportFileNamePattern=&reportDir=&display=true'


spider_url = source + url_1 + apiKey + url_2 + context_id + url_3 + user_id + url_4
spider_run = requests.get(spider_url)
spider_run.json()
while int(zap.spider.status()) < 100:    
    print('Spider progress %: ' + zap.spider.status())
print('spider completed')
active_url = source + url_5 + apiKey + url_2 + context_id + url_3 + user_id + url_6
active_run = requests.get(active_url)
active_run.json()
while int(zap.ascan.status()) < 100:
    print('ascan progress % ' + zap.ascan.status())
print('ascan completed')
report_url = source + url_7 + apiKey + url_8 + title + url_9 + template + url_10
report_run = requests.get(report_url)
report_run.json()
