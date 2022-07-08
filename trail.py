import zapv2
import time

target = 'https://demo.testfire.net'
apiKey = '1s6ns5olm3jnqi2t5f8dfsqge1'

zap = zapv2.ZAPv2(apikey=apiKey, proxies={'http': 'http://localhost:8081', 'https': 'http://localhost:8081'})

zap.urlopen(target)

zap.spider.scan(url=target, apikey=apiKey)
time.sleep(5)
while int(zap.spider.status()) < 100:
    # Poll the status until it completes
    print('Spider progress %: ' + zap.spider.status())
    time.sleep(5)
print('spider completed')
zap.spider.scan(url=target, maxchildren=5, recurse=True, subtreeonly=False, apikey=apiKey)

while int(zap.pscan.records_to_scan) > 0:
    print('pscan records : ' + zap.pscan.records_to_scan)
    time.sleep(5)
print('pscan completed')

zap.ascan.scan(url=target, apikey=apiKey)
time.sleep(5)

while int(zap.ascan.status()) < 100:
    print('ascan progress % ' + zap.ascan.status())
    time.sleep(5)
print('ascan completed')

f = open('report.html', 'w')
f.write(zap.core.htmlreport(apikey=apiKey))
f = open('report.html', 'r')
print(f.read())

