import requests, time, json, random, string, re

alll = string.ascii_letters + string.digits
session_name = "".join(random.sample(alll,random.randint(12, 12)))

api_token = input('[*] Enter your api : (Enter L if you want to load it from previous config) : ') 

if (api_token == 'L') or (api_token == 'l'):
    try :
        with open('api_cache.txt') as b_api :
            b_api_lines = b_api.readlines()
            for line in b_api_lines :
                if 'b_api' in line :
                    api_token = line.strip().split('=')[1]
            print(f'###token : {api_token}')
            time.sleep(2)
    except FileNotFoundError :
        time.sleep(2)
        api_token = input('[*] not found . Enter your api manually : ')

        with open('api_cache.txt', 'w') as new_api :
            new_api.write(f'b_api={api_token}')
            new_api.close()

else :
    with open('api_cache.txt', 'w') as new_api :
        new_api.write(f'b_api={api_token}')
        new_api.close()

pr_type = input('[*] Do you want to use 1-proxy + rotate url   2-proxy list : ')
if pr_type == '1' :
    rola_proxy_token = input('[*] Enter the proxy (http://ip:port) : ')
    rola_proxy_rotate = input('[*] Enter the url for rotate proxy : ')
elif pr_type == '2' :
    print('[*] proxy list selected')
    proxies_file = open('proxies.txt', 'r')
    proxies_list = proxies_file.readlines()
    pr_index = 0





this_time_country = int(input('[*] Enter code of country to create number(greece = 129) : '))
operator_ = input('[*] Enter operator (if you want random operator , enter \'any\'): ')

try :
    with open('config.txt') as config :
        config_lines = config.readlines()
        for line in config_lines :
            if 'smstoken' in line :
                smshub_token = line.strip().split('=')[1]
        print(f'### sms token : {smshub_token}')
        time.sleep(2)
except :
    time.sleep(2)
    print('\n### put your sms token in config file in this format :   smstoken=exampletoken')
    time.sleep(500000)

sms_api_type = input('select your sms_api  |  1-sms-activate  -  2-smshub : ')
if sms_api_type == '1' :
    from smsactivate.api import SMSActivateAPI
    sa = SMSActivateAPI(smshub_token)
    sa.debug_mode = True

time.sleep(2)

def sms_get_number(country, operator) :
    if sms_api_type == '2' :
        try :
            request_number = requests.get(f'https://smshub.org/stubs/handler_api.php?api_key={smshub_token}&action=getNumber&service=ig&operator={operator}&country={country}')
            if 'ACCESS_NUMBER:' in request_number.text :
                return {'number':request_number.text.split(':')[2], 'access_code':request_number.text.split(':')[1]}
            else :
                return request_number.text
        except :
            return False
    else :
        try :
            request_number = sa.getNumber(service='ig', operator=operator, country=country, verification="false")
            if request_number.get('phone') != None :
                return {'number':request_number.get('phone'), 'access_code':request_number.get('activation_id')}
            else :
                return str(request_number)
        except Exception as e:
            print(e)
            return False

def sms_status_three(access_code):
    if sms_api_type == '2' :
        try :
            return requests.get(f'https://smshub.org/stubs/handler_api.php?api_key={smshub_token}&action=setStatus&status=3&id={access_code}').text
        except :
            return False
    else :
        try :
            return sa.setStatus(id=access_code, status=3)
        except :
            return False

def sms_status_eight(access_code):
    if sms_api_type == '2' :
        try :
            return requests.get(f'https://smshub.org/stubs/handler_api.php?api_key={smshub_token}&action=setStatus&status=8&id={access_code}').text
        except :
            return False
    else :
        try :
            return sa.setStatus(id=access_code, status=8)
        except :
            return False

def sms_get_status(access_code) :
    if sms_api_type == '2' :
        try :
            return requests.get(f'https://smshub.org/stubs/handler_api.php?api_key={smshub_token}&action=getStatus&id={access_code}').text
        except :
            return False
    else :
        try :
            return sa.getStatus(access_code)
        except :
            return False

    
def get_proxy() :
    if pr_type == '1' :
        requests.get(rola_proxy_rotate)
        return rola_proxy_token
    else :
        global pr_index
        pr = proxies_list[pr_index - (len(proxies_list) * ((round(pr_index/len(proxies_list)))))].strip('\n')
        pr_index += 1
        return pr


def try_to_create(username123, proxy123) :
    timer2 = 0
    ase=True
    while ase :
        timer2 += 1.5
        time.sleep(1.5)
        print('\n###  creating number ...')
        try_to_create_number = sms_get_number(this_time_country, 'any')
        if type(try_to_create_number) == dict :
            created_number = try_to_create_number['number']
            created_number_accesscode = try_to_create_number['access_code']
            ase = False
        else :
            fake_accesscode = 55555555
            print(try_to_create_number)
            return (False, try_to_create_number, fake_accesscode)
        if timer2 > 20 :
            fake_accesscode = 55555555
            return (False, try_to_create_number, fake_accesscode)
    try :
        create_request = requests.get(f'https://braindeepjet.online/create_account?token={api_token}&phone_number={created_number}&proxy={proxy123}&username={username123}')
        if 'started creating account'  in create_request.text :
            return {'status':'True', 'session_code': json.loads(create_request.text.strip())['session_code'], 'created_number':created_number, 'created_number_accesscode':created_number_accesscode}
        else :
            return (create_request.text, created_number, created_number_accesscode)
    except Exception as e :
        print(e)
        return (False, created_number, created_number_accesscode)


def try_to_create_fixed_number(created_number, created_number_accesscode, username123, proxy123) :
    print('\n###  creating another number ...')
    try :
        create_request = requests.get(f'https://braindeepjet.online/create_account?token={api_token}&phone_number={created_number}&proxy={proxy123}&username={username123}')
        if 'started creating account'  in create_request.text :
            return {'status':'True', 'session_code': json.loads(create_request.text.strip())['session_code'], 'created_number':created_number, 'created_number_accesscode':created_number_accesscode}
        else :
            return (create_request.text, created_number, created_number_accesscode)
    except Exception as e :
        print(e)
        return (False, created_number, created_number_accesscode)


def try_to_submit_sms(session_code, sms) :
    try :
        return requests.get(f'https://braindeepjet.online/submit_sms?token={api_token}&session_code={session_code}&sms={sms}').text
    except :
        return False

def try_to_getstatus(session_code) :
    try :
        return requests.get(f'https://braindeepjet.online/get_status?token={api_token}&session_code={session_code}').text
    except :
        return False

    

usernames_t = list(filter(None, open('usernames.txt').read().strip().split('\n')))

how_many = int(input('[*] how many account do you want to be created by 1 single number ? (use maximum 3_4 because instagram will be sensitive to you : '))

while True :
    for att in range(how_many) :
        username = random.choice(usernames_t).lower()
        username1 = username + username[-1] + username[-1] + str(random.randint(10, 95)) + username[:3]
        username2 = username + '_' + username[-4:] + str(random.randint(100, 950))
        username3 = username + username[-4:] + '_' + str(random.randint(1990, 2008)) + random.choice(string.ascii_letters).lower() + random.choice(string.ascii_letters).lower()
        username4 = username + username[-4:] + str(random.randint(1990, 2008)) +  '_' + random.choice(string.ascii_letters).lower() + random.choice(string.ascii_letters).lower()
        username5 = username + username[:4] + str(random.randint(1990, 2008)) +  '_' + random.choice(string.ascii_letters).lower() + random.choice(string.ascii_letters).lower()
        username6 = username + username[:4] + random.choice(string.ascii_letters).lower() + random.choice(string.ascii_letters).lower() + random.choice(string.ascii_letters).lower() + str(random.randint(985, 999))
        username = random.choice([username1, username2, username3, username4, username5, username6])
        usern = username

        if att == 0 :
            first_attempt = try_to_create(usern, get_proxy())
            try :
                a_number = first_attempt["created_number"]
                a_accesscode = first_attempt["created_number_accesscode"]
            except :
                print('error :  maybe no number available  ,  try again after minutes')
                time.sleep(555555)
        else :
            first_attempt = try_to_create_fixed_number(a_number, a_accesscode, usern, get_proxy())

        print(first_attempt)
        sms_submited = False
        
        if type(first_attempt) == dict :
            timer = 0
            asew=True
            is_status_eight = False
            while asew :
                if timer >= 250 :
                    if att == 0 :
                        print(sms_status_eight(first_attempt["created_number_accesscode"]))
                        is_status_eight = True
                    asew = False
                    
                print('###  waiting for sms ...')
                time.sleep(2)
                timer += 2
                smsget = sms_get_status(first_attempt['created_number_accesscode'])
                if ('STATUS_OK' in smsget) and (is_status_eight == False):
                    print(sms_status_three(first_attempt['created_number_accesscode']))
                    try_to_submit_sms(first_attempt['session_code'], smsget.split(':')[1])
                    sms_submited = True
                    asew = False
                    print(f'###  sms submited : {smsget.split(":")[1]}')
                    time.sleep(1.5)
                    print(f'###  creating account ...')
                else :
                    pass

        else :
            sms_status_eight(first_attempt[2])
            break
        try :
            if sms_submited == True :
                t = 0
                acw = True
                while acw :
                    if t >= 120 :
                        print(f'###  unsuccessfull attempt : {try_to_getstatus(first_attempt["session_code"])}')
                        acw = False
                    time.sleep(1)
                    t += 1
                    gg = try_to_getstatus(first_attempt['session_code'])
                    if t == 6 :
                        print('### getting registration data ...')
                    if t == 10 :
                        print('### sending final requests ...')
                    if '||' in gg :
                        print(gg + '\n')
                        acw = False
                        accounts_file = open(f'accounts.txt', 'a')
                        accounts_file.write(gg + '\n')
                        accounts_file.close()
                        
                        json_cookie = open(f'{usern}.json', 'a')
                        try :
                            json_cookie.write(requests.get(f'https://braindeepjet.online/get_status?token={api_token}&session_code={first_attempt["session_code"]}&instagrapi=true').text)
                        except :
                            pass
                        json_cookie.close()
                        #accounts_file = open(f'accounts_{session_name}.txt', 'a')
                        #accounts_file.write(gg + '\n')
                        #accounts_file.close()

                        #accounts_file_detail = open(f'details0_{session_name}.txt', 'a')
                        uns = re.findall('(.*?)\|', gg)[0].split(':')[0]
                        ups = re.findall('(.*?)\|', gg)[0].split(':')[1]

                        #accounts_file_detail.write(f'{uns},{ups},{a_number}\n')
                        #accounts_file_detail.close()

                    else :
                        pass
                    
        except :
            pass
