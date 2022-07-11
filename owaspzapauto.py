import zapv2
import urllib.parse

class OwaspZAP():

    def __init__(self, config):
        self.config = config
        self.user = config['user']
        self.username = config['username']
        self.password = config['password']
        self.login_url = config['loginurl']
        self.context = config['context_name']
        self.context_id = config['context_id']
        self.zap = zapv2.ZAPv2(apikey=apiKey, proxies={'http': config['zapserver'], 'https': config['zapserver']})

        #zap.urlopen(target)

        if(config['type'] == 'Passive'):
            self.invokepassivescan()
        if (config['type'] == 'Active'):
            self.set_logged_in_indicator()
            if(config['authtype'] == 'Form'):
                self.set_form_based_auth()
            self.set_include_in_context(config['exclude_url'], config['include_url'])
            self.activescan()
        if (config['type'] == 'Spider'):
            user_id_response = self.set_user_auth_config()
            self.start_spider(user_id_response)
        pass

    def invokepassivescan(self):
        print("test")
        pass

    def set_include_in_context(self):

        self.zap.context.set_context_in_scope(self.context)
        print('Configured include and exclude regex(s) in context')

    def set_logged_in_indicator(self):
        logged_in_regex = '<a id="AccountLink" href="/login.jsp" class="focus" >ONLINE BANKING LOGIN</a>'
        self.zap.authentication.set_logged_in_indicator(self.context_id, logged_in_regex)
        print('Configured logged in indicator regex: ')

    def set_form_based_auth(self):

        login_request_data = 'username={%username%}&password={%password%}'
        form_based_config = 'loginUrl=' + urllib.parse.quote(self.login_url) + '&loginRequestData=' + urllib.parse.quote(
            login_request_data)
        self.zap.authentication.set_authentication_method(self.context_id, 'formBasedAuthentication', form_based_config)
        print('Configured form based authentication')

    def set_user_auth_config(self):

        user_id = self.zap.users.new_user(self.context_id, self.user)
        user_auth_config = 'username=' + urllib.parse.quote(self.username) + '&password=' + urllib.parse.quote(self.password)
        self.zap.users.set_authentication_credentials(self.context_id, user_id, user_auth_config)
        self.zap.users.set_user_enabled(self.context_id, user_id, 'true')
        self.zap.forcedUser.set_forced_user(self.context_id, user_id)
        self.zap.forcedUser.set_forced_user_mode_enabled('true')
        print('User Auth Configured')
        return user_id

    def start_spider(self, user_id):
        self.zap.spider.scan_as_user(self.context_id, user_id, target_url, recurse='true')
        print('Started Scanning with Authentication')

    def activescan(self):
        print('activescan')


if __name__ == '__main__':
    target = 'https://demo.testfire.net'
    apiKey = 'j9782ud4rme7p4bghnrmj6ul0v'


    target_url = 'https://demo.testfire.net'

    config = {}

    config['context_name'] = 'test'
    config['zapserver'] = 'http://localhost:8080'
    config['type'] = "Active"
    config['target'] = target
    config['apikey'] = apiKey
    config['exclude_url'] = 'https://demo.testfire.net/login.jsp'
    config['include_url'] = 'https://demo.testfire.net'
    config['user'] = 'admin'
    config['username'] = 'admin'
    config['password'] = 'admin'
    config['authtype'] = 'Form' #chose other forms
    config['loginurl'] = 'https://demo.testfire.net/login.jsp'
    config['context_id'] = '2'

owaspzapauto = OwaspZAP(config)






    #user_id_response = owaspzapauto.set_user_auth_config()
