/*
 * Everything in UNIX is a file, whether you're talking about network connections, File IO, or even 
 * the terminal you work on. Even within the domain of network sockets, there exist two kinds of 
 * sockets, namely stream sockets and datagram sockets. Stream sockets are used in creating two way
 * connections and are used in telnet, HTTP request, etc. These stream sockets get this high level 
 * data transmission quality only because of TCP (Transmission Control Protocol).
 * You've heard about TCP/IP, where IP is simply the internet protocol; however, bear in mind that 
 * IP only cares about routing, while preserving actual data integrity falls under TCP's department.
 * 
 * Datagram sockets are used when trying to create connectionless sockets, which have lots of uses 
 * as well. While using these sockets, you have to either ignore or account for dropped packages
 * as there's no guarantee that everything will be sent and received (UDP). What's the advantage of 
 * this? Speed. 
 * 
 * There's a multiple level of data encapsulation in a network request: it would be something like,
 * ethernet -> IP -> UDP -> TFPTP -> data 
 *  In Unix:   Application Layer (telnet, ftp, etc.)
                Host-to-Host Transport Layer (TCP, UDP)
                Internet Layer (IP and routing)
                Network Access Layer (Ethernet, wi-fi, or whatever)
 */

/*
 * IP addresses V4 and V6
 * ----------------------
 * We were in the danger of running out of actual IP addresses, so IPV6 was intvented which represents
 * addresses in an evolved "dots and numbers" form. IP addresses are organized into network addresses
 * and hostn portions. The netmask is used to find the network address, through the use of bitwise
 * operations. 
 */