import requests, time, json, random, string, re

alll = string.ascii_letters + string.digits
session_name = "".join(random.sample(alll,random.randint(12, 12)))

api_token =  ''        # https://braindeepjet.ga/
smshub_token = ''      # https://smshub.org/en/main
rola_proxy_token = ''  # https://www.rola-ip.co/      

countries = {'15':'pl', '129':'gr'}

this_time_country = str(random.choice(list(countries.keys())))
this_time_proxy = random.choice([countries[this_time_country] , 'us'])
print(f'###  country : {this_time_country}  ,  proxy : {this_time_proxy}')
time.sleep(2)

def sms_get_number(country, operator) :
    try :
        request_number = requests.get(f'https://smshub.org/stubs/handler_api.php?api_key={smshub_token}&action=getNumber&service=ig&operator={operator}&country={country}')
        if 'ACCESS_NUMBER:' in request_number.text :
            return {'number':request_number.text.split(':')[2], 'access_code':request_number.text.split(':')[1]}
        else :
            return request_number.text
    except :
        return False

def sms_status_three(access_code):
    try :
        return requests.get(f'https://smshub.org/stubs/handler_api.php?api_key={smshub_token}&action=setStatus&status=3&id={access_code}').text
    except :
        return False

def sms_status_eight(access_code):
    try :
        return requests.get(f'https://smshub.org/stubs/handler_api.php?api_key={smshub_token}&action=setStatus&status=8&id={access_code}').text
    except :
        return False

def sms_get_status(access_code) :
    try :
        return requests.get(f'https://smshub.org/stubs/handler_api.php?api_key={smshub_token}&action=getStatus&id={access_code}').text
    except :
        return False
    
def get_proxy() :
    return 'http://' + requests.get(f'http://list.rola.info:8088/user_get_ip_list?token={rola_proxy_token}&type=4g&qty=1&country={this_time_proxy}&time=10&format=txt&protocol=http&filter= 1&area=us').text


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
        create_request = requests.get(f'https://braindeepjet.ga/create_account?token={api_token}&phone_number={created_number}&proxy={proxy123}&username={username123}')
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
        create_request = requests.get(f'https://braindeepjet.ga/create_account?token={api_token}&phone_number={created_number}&proxy={proxy123}&username={username123}')
        if 'started creating account'  in create_request.text :
            return {'status':'True', 'session_code': json.loads(create_request.text.strip())['session_code'], 'created_number':created_number, 'created_number_accesscode':created_number_accesscode}
        else :
            return (create_request.text, created_number, created_number_accesscode)
    except Exception as e :
        print(e)
        return (False, created_number, created_number_accesscode)


def try_to_submit_sms(session_code, sms) :
    try :
        return requests.get(f'https://braindeepjet.ga/submit_sms?token={api_token}&session_code={session_code}&sms={sms}').text
    except :
        return False

def try_to_getstatus(session_code) :
    try :
        return requests.get(f'https://braindeepjet.ga/get_status?token={api_token}&session_code={session_code}').text
    except :
        return False

    

usernames_t = list(filter(None, open('usernames.txt').read().strip().split('\n')))

how_many = int(input('how many account do you want to be created by 1 single number ? (use maximum 3_4 because instagram will be sensitive to you : '))

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
    if type(first_attempt) == dict :
        timer = 0
        asew=True
        while asew :
            if timer >= 55 :
                print(sms_status_eight(first_attempt["created_number_accesscode"]))
                asew = False

            print('###  waiting for sms ...')
            time.sleep(2)
            timer += 2
            smsget = sms_get_status(first_attempt['created_number_accesscode'])
            if 'STATUS_OK' in smsget :
                sms_status_three(first_attempt['created_number_accesscode'])
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
                if '||' in gg :
                    print(gg + '\n')
                    acw = False
                    accounts_file = open(f'accounts_{session_name}.txt', 'a')
                    accounts_file.write(gg + '\n')
                    accounts_file.close()

                    accounts_file_detail = open(f'details0_{session_name}.txt', 'a')
                    uns = re.findall('(.*?)\|', gg)[0].split(':')[0]
                    ups = re.findall('(.*?)\|', gg)[0].split(':')[1]

                    accounts_file_detail.write(f'{uns},{ups},{a_number},{this_time_proxy}\n')
                    accounts_file_detail.close()

                else :
                    pass
                
    except :
        pass
