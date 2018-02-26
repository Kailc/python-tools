# coding=utf-8

import random
import string
import os
from Crypto.Cipher import AES
import base64
import getopt
import sys


# whitespace = ' \t\n\r\v\f'
# ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
# ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# ascii_letters = ascii_lowercase + ascii_uppercase
# digits = '0123456789'
# hexdigits = digits + 'abcdef' + 'ABCDEF'
# octdigits = '01234567'
# punctuation = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
# printable = digits + ascii_letters + punctuation + whitespace



def createpasswd(needlowercase = True, needuppercase = True, needdigits = True, needpunctuation = True, passwdlen = 10):
    chars_list = []
    chars = ''
    len = 0
    if needlowercase:
        chars_list = chars_list + random.sample(string.ascii_letters, 1)
        chars = chars + string.ascii_letters
        len = len + 1
    if needuppercase:
        chars_list = chars_list + random.sample(string.ascii_uppercase, 1)
        chars = chars + string.ascii_uppercase
        len = len + 1
    if needdigits:
        chars_list = chars_list + random.sample(string.digits, 1)
        chars = chars + string.digits
        len = len + 1
    if needpunctuation:
        chars_list = chars_list + random.sample(string.punctuation, 1)
        chars = chars + string.punctuation
        len = len + 1

    chars_list = chars_list + random.sample(chars, passwdlen - len)

    passwd = "".join(chars_list)
    chars_list = random.sample(passwd, passwdlen)
    passwd = "".join ( chars_list )

    return passwd

def createdict(sitename, username, dict_text = None):
    
    sitename = sitename.lower ().replace(' ', '')
    username = username.lower ().replace ( ' ', '' )
    load_dict = dict_text

    if isinstance(load_dict, dict) and load_dict != None and (sitename + ' ' + username) in load_dict:
        print ( 'Account already exists!\nSitename:' , sitename , '\nUsername:' , username , '\nPasswd:' ,
                load_dict[ sitename + ' ' + username ] )
        return load_dict

    passwd = createpasswd ()
    passwd_dict = {
        sitename + ' ' + username: passwd
    }

    if isinstance(load_dict, dict) and load_dict != None:
        for i in load_dict:
            passwd_dict[i] = load_dict[i]
        
    print ( 'Generate password success!\nSitename:', sitename, '\nUsername:', username, '\nPasswd:', passwd )
    return passwd_dict

def tobytesandpad16(text):
    while len(text) % 16 != 0:
        text += '\0'
    return str.encode ( text )

def pad16(text):
    while len(text) % 16 != 0:
        text += b' '
    return text


# mod = 0 encrypt
# mod = 1 decrypt

def encryptanddecrypt_aes(text, mod = 0, secret_key = 'abcdefghijklmnop'):
    if mod != 0 and mod != 1:
        print('mode error', mod)
        return None
    # print(tobytesandpad16(secret_key))
    aes = AES.new(tobytesandpad16(secret_key), AES.MODE_ECB)
    if mod == 0:
        return str(base64.encodebytes(aes.encrypt ( tobytesandpad16 ( text ) )), encoding='utf-8').replace('\0', '')
    else:
        return str(aes.decrypt(base64.decodebytes(text.encode(encoding='utf-8'))),encoding='utf-8').replace('\0', '')

def getcipher(fileame = 'xxxx'):
    text = None
    path = os.getcwd() + '\\' + fileame
    if os.name != 'nt':
        path = path.replace('\\', '/')
    if os.path.isfile(path):
        with open ( path , 'r' ) as f:
            text = f.read()
            f.close()
    return text

def storecipher(text = '', fileame = 'xxxx'):
    path = os.getcwd () + '\\' + fileame
    if os.name != 'nt':
        path = path.replace('\\', '/')
    with open ( path , 'w' ) as f:
        f.write ( text )
        f.close ()
    print('store in', path)

def usage():
    message ='''
gp(generatepassword), version 0.1

    '''
    print(message)
    sys.exit()
        
def getvalue():
    try:
        options, args = getopt.getopt(sys.argv[1:], 'hlUdpw:f:k:', ['help', 'lower', 'upper', 'digit', 'punctuation', 'passwdlen=', 'filename=', 'secret='])
    except getopt.GetoptError as e:
        print(e)
        sys.exit()
    needlowercase = False
    needuppercase = False
    needdigits = False
    needpunctuation = False
    passwdlen = 10
    filename = 'xxxx'
    secretkey = 'abcdefghijklmnop'
    sitename = ''
    username = ''
    for name, value in options:
        if name in ('-h', '--help'):
            usage()
        elif name in ('-l', '--lower'):
            needlowercase = True
        elif name in ('-U', '--upper'):
            needuppercase = True
        elif name in ('-d', '--digit'):
            needdigits = True
        elif name in ('-p', '--punctuation'):
            needpunctuation = True
        elif name in ('-w', '--passwdlen'):
            if not str(value).isdigit():
                print('passwdlen error!')
                sys.exit()
            passwdlen = int(value)
        elif name in ('-f', '--filename'):
            filename = str(value)
        elif name in ('-k', '--secret'):
            secretkey = str(value)
        elif name in ('-s', '--sitename'):
            sitename = str(value)
        elif name in ('-u', '--username'):
            username = str(value)
        else:
            print('Use the default value!')

    if sitename == '':
        print('There\'s no sitename!')
        sys.exit()
    if username == '':
        print('There\'s no username!''')
        sys.exit()
    return needlowercase, needuppercase, needdigits, needpunctuation, passwdlen, filename, secretkey, sitename, username

def main():
    needlowercase , needuppercase , needdigits , needpunctuation , passwdlen , filename , secretkey, sitename, username = getvalue()
    cleartext = None
    ciphertext = getcipher(filename)
    if ciphertext != None:
        cleartext = encryptanddecrypt_aes(ciphertext, mod=1, secret_key=secretkey)
        cleartext = eval(cleartext)

    storecipher(text=encryptanddecrypt_aes(str(createdict(sitename, username, cleartext)), mod=0, secret_key=secretkey))
    
if __name__ == '__main__':
    # getvalue()
    main()
