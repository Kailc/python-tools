# coding=utf-8

import random
import string
import os
import json

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

def createjson(sitename, username):

    sitename = sitename.lower ().replace(' ', '')
    username = username.lower ().replace ( ' ' , '' )
    path = os.getcwd() + '\\xxxx'
    load_dict = {}
    if os.name != 'nt':
        path = path.replace('\\', '/')
    if os.path.isfile(path):
        with open ( path , 'r' ) as f:
            load_dict = json.load ( f )
            f.close ()
            if (sitename + ' ' + username) in load_dict:
                print ( 'Sitename:' , sitename , '\nUsername:' , username , '\nPasswd:' ,
                        load_dict[ sitename + ' ' + username ] )
                return


    passwd = createpasswd ()
    passwd_dict = {
        sitename + ' ' + username: passwd
    }

    for i in load_dict:
        passwd_dict[i] = load_dict[i]

    with open (path, 'w') as f:
        json.dump(passwd_dict, f, indent=4)
        f.close()
    print ( 'Sitename:' , sitename , '\nUsername:' , username , '\nPasswd:' , passwd )


def main():
    createjson ( 'sitename' , 'username' )

if __name__ == '__main__':
    main()
