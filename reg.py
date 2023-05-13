import requests, json, time, random, string
from smsactivate.api import SMSActivateAPI

token = input('[*] Enter your braindeepjet api : (Enter L if you want to load it from previous config) :')  # get your token from https://braindeepjet.ga/  or  https://imwhodifferent.t.me/      |   token = 'b0k6UWErDv9e38ewLJjcHEI15e8ZdEdaBVpflnY'
if token == 'L' :
    try :
        with open('api_cache.txt') as b_api :
            b_api_lines = b_api.readlines()
            for line in b_api_lines :
                if 'b_api' in line :
                    token = line.strip().split('=')[1]
            print(f'### sms token : {token}')
            time.sleep(2)
    except FileNotFoundError :
        time.sleep(2)
        token = input('[*] not found . Enter your braindeepjet api manually : ')

        with open('api_cache.txt', 'w') as new_api :
            new_api.write(f'b_api={token}')
            new_api.close()

else :
    with open('api_cache.txt', 'w') as new_api :
        new_api.write(f'b_api={token}')
        new_api.close()


proxy_type = input('[*] proxy_type :   1:proxy_list  2:proxy_url ?')
if proxy_type == '2' :
    proxy_typy2_url = input('[*] Enter proxy url : ')
    proxy_type2_reset = input('[*] Enter proxy \"switch ip\" url : ')
    
acc_by_one_number = input('[*] how many account to create by one phone_number ? : ')
what_api = input('[*] choose your sms api :   1 - smshub    2 - sms-activate : ')
if what_api == '2' :
    sa = SMSActivateAPI(input('[*] Enter SMS-Activate api : '))
    sa.debug_mode = True
elif what_api == '1' :
    pass
    
try :
    with open('config.txt') as config :
        config_lines = config.readlines()
        for line in config_lines :
            if 'smstoken' in line :
                smstoken = line.strip().split('=')[1]
        print(f'### sms token : {smstoken}')
        time.sleep(2)
except :
    time.sleep(2)
    print('\n### put your sms token in config file in this format :   smstoken=exampletoken')
    time.sleep(500000)
        
        

country_ = int(input('[*] Enter code of country to create number(greece = 129) :'))
operator_ = input('[*] Enter operator (one of greece operator = q):')

if what_api == '1' :
    get_number_url = f'https://smshub.org/stubs/handler_api.php?api_key={smstoken}&action=getNumber&service=ig&operator={operator_}&country={country_}'
    get_status_url = f'https://smshub.org/stubs/handler_api.php?api_key={smstoken}&action=getStatus&id='
    





usernames = list(filter(None, open('usernames.txt').read().strip().split('\n')))
proxies = list(filter(None, open('proxies.txt').read().strip().split('\n')))

if proxy_type == '1' :
    if int(len(proxies)/int(acc_by_one_number)) < 1 :
        time.sleep(2)
        print(f'\nput at last {acc_by_one_number} proxy in proxies.txt')
        time.sleep(500000)
    
if proxy_type == '1' :
    try_for_account = int(len(proxies)/int(acc_by_one_number))
elif proxy_type == '2' :
    try_for_account = 10000
    
for p in range(try_for_account) :



    print('\ncreating new number ...')
    time.sleep(5)
    if what_api == '2':
        number = sa.getNumber(service='ig', operator=operator_, country=country_, verification="false")
        print('\n' + str(number))
    elif what_api == '1' :
        number_text = requests.get(get_number_url).text
        print('\n' + number_text)
        
    for t in range(int(acc_by_one_number)) :
        try :
            if continue_with_on_num == False :
                continue_with_on_num = True
                break
        except :
            pass
        if proxy_type == '1' :
            proxy = proxies[t]
        elif proxy_type == '2' :
            requests.get(proxy_type2_reset)
            proxy = proxy_typy2_url
            
        username = random.choice(usernames).lower()
        username1 = username + username[-1] + username[-1] + str(random.randint(10, 95)) + username[:3]
        username2 = username + '_' + username[-4:] + str(random.randint(100, 950))
        username3 = username + username[-4:] + '_' + str(random.randint(1990, 2008)) + random.choice(string.ascii_letters).lower() + random.choice(string.ascii_letters).lower()
        username4 = username + username[-4:] + str(random.randint(1990, 2008)) +  '_' + random.choice(string.ascii_letters).lower() + random.choice(string.ascii_letters).lower()
        username5 = username + username[:4] + str(random.randint(1990, 2008)) +  '_' + random.choice(string.ascii_letters).lower() + random.choice(string.ascii_letters).lower()
        username6 = username + username[:4] + random.choice(string.ascii_letters).lower() + random.choice(string.ascii_letters).lower() + random.choice(string.ascii_letters).lower() + str(random.randint(985, 999))
        username = random.choice([username1, username2, username3, username4, username5, username6])
        
        (username)
        
        
        sms_has_sent = False
        if ('http' in proxy) == False :
            this_proxy = 'http://' + proxy
        else :
            this_proxy = proxy
            
            
        phone_created_time = time.time()
        if what_api == '2' :
            try :
                phone_number = number['phone']
            except :
                print(number)
                break
        else :
            try :
                number = number_text.split(':')[2]
                activation_code = number_text.split(':')[1]
                phone_number = number
            except :
                print(number_text)
                break
        
        respond_1 = requests.get(f'https://braindeepjet.ga/create_account?token={token}&phone_number={phone_number}&proxy={this_proxy}&username={username}').json()
        try :
            
            session_code = respond_1['session_code'] 
        except :
            
            print(respond_1)
            if what_api == '2':
                sa.setStatus(id=number['activation_id'], status=8)
            else :
                requests.get(f'https://smshub.org/stubs/handler_api.php?api_key={smstoken}&action=setStatus&status=8&id={activation_code}')
            print('number set status : 8')
            continue
        

        print(f'session_code : {session_code}')
        time.sleep(2)
        print(f'getting registaration data ...')
        if respond_1.get('message') == 'started creating account' :
            mloop = True
            while mloop :
                
                time.sleep(7)
                get_status = requests.get(f'https://braindeepjet.ga/get_status?token={token}&session_code={session_code}').text
                if get_status == 'submit sms code':
                    check_sms = True
                    while check_sms :
                        print('checking sms api for code...')
                        if time.time() - phone_created_time > 60 :

                            print('### refused phone number .')
                            if what_api == '2' :
                                sa.setStatus(id=number['activation_id'], status=8)
                            else :
                                requests.get(f'https://smshub.org/stubs/handler_api.php?api_key={smstoken}&action=setStatus&status=8&id={activation_code}')
                            check_sms = False
                            mloop = False
                            continue_with_on_num = False
                        else :
                            time.sleep(3)
                            if what_api == '2' :
                                status = sa.getStatus(number['activation_id'])
                            elif what_api == '1' :
                                status = requests.get(get_status_url + activation_code).text
                            if 'STATUS_OK' in status :
                                sms = status.split(':')[-1]
                                print(f'received sms from instagram : {sms}')
                                time.sleep(2)
                                print('creating ...')
                                send_sms = requests.get(f'https://braindeepjet.ga/submit_sms?token={token}&session_code={session_code}&sms={sms}')
                                sms_has_sent = True
                                check_sms = False
                                mloop = False
                            else :
                                pass
                else :
                    if ('creating account...' in get_status) == False :
                        print(get_status)
                        print('### refused phone number X')
                        if what_api == '2' :
                            sa.setStatus(id=number['activation_id'], status=8)
                        else :
                            requests.get(f'https://smshub.org/stubs/handler_api.php?api_key={smstoken}&action=setStatus&status=8&id={activation_code}')
                                
                        continue_with_on_num = False  
                        mloop = False
        else :
            print(respond_1)
                
        if sms_has_sent == True :
            checking_result = time.time()
            while True :
                time.sleep(2)
                if time.time() - checking_result  > 60 :
                    break
                if '|||' in requests.get(f'https://braindeepjet.ga/get_status?token={token}&session_code={session_code}').text :
                    accounts_file = open(f'accounts.txt', 'a')
                    accounts_file.write(requests.get(f'https://braindeepjet.ga/get_status?token={token}&session_code={session_code}').text + '\n')
                    accounts_file.close()
                    print('### account created\n')
                    if what_api == '2' :
                        sa.setStatus(id=number['activation_id'], status=3)
                    else :
                        requests.get(f'https://smshub.org/stubs/handler_api.php?api_key={smstoken}&action=setStatus&status=3&id={activation_code}')
                    break
        
