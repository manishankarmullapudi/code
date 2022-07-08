import time
import zapv2
import urllib.parse
from pprint import pprint
target = 'https://demo.testfire.net'
apiKey = '1s6ns5olm3jnqi2t5f8dfsqge1'

zap = zapv2.ZAPv2(apikey=apiKey, proxies={'http': 'http://localhost:8081', 'https': 'http://localhost:8081'})

zap.urlopen(target)

context_id = 2
apikey = '1s6ns5olm3jnqi2t5f8dfsqge1'
context_name = 'login'
target_url = 'https://demo.testfire.net'

# By default ZAP API client will connect to port 8080
# zap = ZAPv2(apikey=apikey)


# Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
# zap = zapv2.ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8081', 'https': 'http://127.0.0.1:8081'})


def set_include_in_context():
    exclude_url = 'https://demo.testfire.net/login.jsp'
    include_url = 'https://demo.testfire.net'
    zap.context.include_in_context(context_name, include_url)
    zap.context.exclude_from_context(context_name, exclude_url)
    print('Configured include and exclude regex(s) in context')


def set_logged_in_indicator():
    logged_in_regex = '<a id="AccountLink" href="/login.jsp" class="focus" >ONLINE BANKING LOGIN</a>'
    zap.authentication.set_logged_in_indicator(context_id, logged_in_regex)
    print('Configured logged in indicator regex: ')


def set_form_based_auth():
    login_url = 'https://demo.testfire.net/login.jsp'
    login_request_data = 'username={%username%}&password={%password%}'
    form_based_config = 'loginUrl=' + urllib.parse.quote(login_url) + '&loginRequestData=' + urllib.parse.quote(
        login_request_data)
    zap.authentication.set_authentication_method(context_id, 'formBasedAuthentication', form_based_config)
    print('Configured form based authentication')


def set_user_auth_config():
    user = 'admin'
    username = 'admin'
    password = 'admin'

    user_id = zap.users.new_user(context_id, user)
    user_auth_config = 'username=' + urllib.parse.quote(username) + '&password=' + urllib.parse.quote(password)
    zap.users.set_authentication_credentials(context_id, user_id, user_auth_config)
    zap.users.set_user_enabled(context_id, user_id, 'true')
    zap.forcedUser.set_forced_user(context_id, user_id)
    zap.forcedUser.set_forced_user_mode_enabled('true')
    print('User Auth Configured')
    return user_id


def start_spider(user_id):
    zap.spider.scan_as_user(context_id, user_id, target_url, recurse='true')
    print('Started Scanning with Authentication')

set_include_in_context()
set_form_based_auth()
set_logged_in_indicator()
user_id_response = set_user_auth_config()
start_spider(user_id_response)

print('Spidering target {}'.format(target))
# The scan returns a scan id to support concurrent scanning
scanID = zap.spider.scan(target)
while int(zap.spider.status(scanID)) < 100:
    # Poll the status until it completes
    print('Spider progress %: {}'.format(zap.spider.status(scanID)))
    time.sleep(1)

print('Spider has completed!')
# Prints the URLs the spider has crawled
print('\n'.join(map(str, zap.spider.results(scanID))))
# If required post process the spider results

print('Active Scanning target {}'.format(target))
scanID = zap.ascan.scan(target)
while int(zap.ascan.status(scanID)) < 100:
    # Loop until the scanner has finished
    print('Scan progress %: {}'.format(zap.ascan.status(scanID)))
    time.sleep(5)

print('Active Scan completed')
# Print vulnerabilities found by the scanning
print('Hosts: {}'.format(', '.join(zap.core.hosts)))
print('Alerts: ')
pprint(zap.core.alerts(baseurl=target))

with open('report.html', 'w') as f:f.write(zap.core.htmlreport(apikey=apiKey))
print("report done")