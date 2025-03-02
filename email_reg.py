import re, requests, time , random

kopeechka_token = '2aa7bcdhhlsshjfnls34jhfad7e40ba77745'
braindeepjet_token = '2ajbjsa7bcd8b43dkknk98dv7e40ba7llns745'
proxies_list = open('proxies.txt').readlines()   # http://ip:port   or   http://user:pass@ip:port

usernames_list = open('usernames.txt').readlines()


def cancel_email(mail_id, kopeechka_token):
    try :
        rq = requests.get(f'https://api.kopeechka.store/mailbox-cancel?id={mail_id}&token={kopeechka_token}&api=2.0'); print(rq)
        return '1'
    except :
        return '0'

#while True :
for i in range(1, len(proxies_list)):
    http_proxy = proxies_list[i].strip('\n')

    name1 = random.choice(usernames_list).strip('\n').lower() 
    name2 = random.choice(usernames_list).strip('\n').lower()
    username_sel = name1 + random.choice(['', name1[-1]*2]) + random.choice(['', '_', '_._']) + name2[:random.choice([3, -2])] + str(random.randint(10, 99))

    print(username_sel)

    try :
        xx= requests.get(f'https://api.kopeechka.store/mailbox-get-email?site=instagram.com&mail_type=outlook.com&token={kopeechka_token}&type=json&api=2.0').json(); print(xx); newm=xx['mail']; mail_id = xx['id']
        crt = requests.get(f'https://braindeepjet.online/create_account?token={braindeepjet_token}&email={newm}&proxy={http_proxy}&username={username_sel}').text


    except :
        continue; cancel_email(mail_id)

    if not 'creating account' in crt :
        continue; cancel_email(mail_id)

    sess_id = re.findall('\d{6,}', crt)[0]

    for i in range(1, 19):
        time.sleep(3)
        rct = requests.get(f'https://braindeepjet.online/get_status?token={braindeepjet_token}&session_code={sess_id}').text
        if 'submit sms' in rct :
            sms_state = True
            break
        else:
            sms_state = False
            if not 'creating account' in rct:
                break

    if sms_state == False:
        print(rct)
        continue; cancel_email(mail_id)

    for j in range(1, 160):
        time.sleep(1)
        try :
            resp = requests.get(f'https://api.kopeechka.store/mailbox-get-message?id={mail_id}&token={kopeechka_token}&type=json&api=2.0').text
            code_digit = re.findall('\d{6}', resp)[0]
            break
        except:
            pass

    try :
        nc = code_digit
    except Exception as e:
        print(f'didnt receive code after 90 sec\n{e}')
        continue; cancel_email(mail_id)

    print(requests.get(f'https://braindeepjet.online/submit_sms?token={braindeepjet_token}&session_code={sess_id}&sms={code_digit}').text)

    for i in range(1, 45):
        time.sleep(3)
        rf = requests.get(f'https://braindeepjet.online/get_status?token={braindeepjet_token}&session_code={sess_id}').text
        print(rf.encode())
        if not 'creating account (sms has been submited)' in rf:
            print(rf.encode())
            if 'earer' in rf:
                with open('accounts.txt', 'a') as accs:
                    accs.write(rf+'\n')
            break



