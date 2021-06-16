import crypt
import socket
import zipfile
import optparse
from threading import Thread


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


main_zip()
