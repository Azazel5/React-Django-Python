#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <string.h>
#include <arpa/inet.h>

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
 * 
 * Besides IP addresses and subnet/netmasks, we also have the port number to think about. A good 
 * analogy in the book is that an IP address is the address of a hotel and the port number is a room
 * number. 
 * 
 * In regards to byte ordering, most machines utilize the intuitive big-endian ordering of storing 
 * the bigger-ends first; it is also called network byte order. Some machines, ones with intel 
 * chips, utilize little-endian on the other hand. The conversion functions you have encountered so 
 * far (htons, htonl) etc are functions which standardize the process of conversion and are ordered
 * in this way: htons, htonl (host to network short/long)| ntohs, ntohl (network to host short/long)
 * 
 * struct addrinfo is what's used while making connections, as you've seen. After filling it up, you 
 * can even call getaddrinfo() to get a linked list with all the struct variables filled out with 
 * useful stuff. In the ai_family field, you can set it to IP version unspecified as well. Since it 
 * is a linked list, there are many results to choose from, but the first one should suit most of your
 * needs. 
 */

// struct sockaddr
// {
//     unsigned short sa_family;
//     char sa_data[14];
// };

// This struct is kinda annoying so programmers created another useful struct which can be casted to
// sockaddr last minute. This new struct is sockaddr_in (for IPV4). Here the sin_port should be in
// network byte order, so use htons.

// struct in_addr
// {
//     uint32_t s_addr;
// };

// struct sockaddr_in
// {
//     short int sin_family;
//     unsigned short int sin_port;
//     struct in_addr sin_addr;
//     unsigned char sin_zero[8];
// };

// Another struct sockaddr_storage is designed to be big enough to hold both IPV4 and IPV6, if you're
// unsure what kind of address you're gonna get. Then you can cast it to whatever you want.
// When working with IP addresses, you can use inet_pton which converts an IP to dots and strings
// and saves it to the sockaddr_in struct. If you want the IP in presentable format, use the
// inet_ntop function (ntop = network to presentation/pton = presentation to network).
// These inet functions only work on numeric IP addresses and not hostnames. If you actually wanna
// do nameserver DNS lookup, use getaddrinfo.

/*
 * Start using getaddrinfo to set up the necessary struct as it streamlines the process quite a lot. 
 * int getaddrinfo(const char *node, // e.g. "www.example.com" or IP
    const char *service, // e.g. "http" or port number
    const struct addrinfo *hints,
    struct addrinfo **res);

 * Through this you can supply hostname or IP, whatever works, as it will do the DNS lookup for you.
 * If you're a server, you'll call this function without the node argument and use the AI_PASSIVE 
 * argument for ai_flags, which fills in your local IP address for you (or you can put a specific 
 * address if you have one). The resultant linked list should be freed, as it is allocated by the 
 * function call. 
 */

// If you have a particular port you wanna connect to, pass that into the second argument
void getaddressinfo_example(char *host_name)
{
    struct addrinfo addr, *res, *ptr;

    // This call to memset clears the struct to make sure that the struct is empty
    memset(&addr, 0, sizeof(addr));

    addr.ai_family = AF_UNSPEC;
    addr.ai_socktype = SOCK_STREAM;
    int err;

    if ((err = getaddrinfo(host_name, NULL, &addr, &res)) != 0)
    {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(err));
        return;
    }

    for (ptr = res; ptr != NULL; ptr = ptr->ai_next)
    {
        void *addr;

        // IPV4
        if (ptr->ai_family == AF_INET)
        {
            struct sockaddr_in *p_addr = (struct sockaddr_in *)(ptr->ai_addr);
            printf("The port number is: %hu\n", p_addr->sin_port);
            addr = &p_addr->sin_addr;
        }

        // IPV6
        else
        {
            struct sockaddr_in6 *p_addr = (struct sockaddr_in6 *)(ptr->ai_addr);
            printf("The port number is: %hu\n", p_addr->sin6_port);
            addr = &p_addr->sin6_addr;
        }

        char ip_address[INET_ADDRSTRLEN];
        inet_ntop(ptr->ai_family, addr, ip_address, sizeof(ip_address));
        printf("IP address of host is: %s\n", ip_address);
    }
}

// In the call to socket, you have filled out the fields individually so far. Start using the amazing
// getaddrinfo function. When using the connect function, add in the destination port and IP address
// in the format of sockaddr_in. Do the same thing as hinted above: instead of the old school way
// of filling out your own struct, simply call getaddrinfo and fill in the connect call with the info.
// Remember: accept returns a new file descriptor, ready for reading and writing, while the older
// one is busy listening to other connections. If you're only expecting one connection, close
// the listenening file descriptor.

int main(int argc, char *argv[])
{

    return 0;
}
