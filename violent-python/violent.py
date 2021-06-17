#####################################################################
# Chapter 1
#####################################################################
import nmap
import crypt
import zipfile
import optparse
from socket import *
from threading import Thread, Semaphore


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
    parser = optparse.OptionParser('usage %prog –H' +
                                   '<target host> -p <target port>')

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