import zapv2
import os

source = os.environ['source']
port = os.environ['port']
apiKey = os.environ['apiKey']
context_id = os.environ['context_id']
user_id = os.environ['user_id']
zap = zapv2.ZAPv2(apikey=apiKey, proxies={'http': source, 'https': source})

spider = 'http://'+port+'/JSON/spider/action/scanAsUser/?apikey='+apiKey+'&contextId='+context_id+'&userId='+user_id+'&url=&maxChildren=&recurse=&subtreeOnly='
zap.spider.scan(url=spider, apikey=apiKey)
while int(zap.spider.status()) < 100:
    print('Spider progress %: ' + zap.spider.status())
print('spider completed')
active = 'http://'+port+'/JSON/ascan/action/scanAsUser/?apikey='+apiKey+'&url=&contextId='+context_id+'&userId='+user_id+'&recurse=&scanPolicyName=&method=&postData='
zap.urlopen(active)
zap.ascan.scan(url=active, apikey=apiKey)
while int(zap.ascan.status()) < 100:
    print('ascan progress % ' + zap.ascan.status())
print('ascan completed')
f = open('/results/report.html', 'w')
f.write(zap.core.htmlreport(apikey=apiKey))
print("report completed")
