#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <string.h>
#include <arpa/inet.h>
#include <errno.h>
#include <signal.h>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/wait.h>

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

// Another function (shutdown) exists, which provides finer control over how you're closing the sockets
// Shutdown makes it so that the socket is unavailable for further reads and writes; to actually close
// it, you must call close. Another function: getpeername, to get the other end of the connection.

/* Simple client-server program  */

// Server side
void sigchild_handler(int signo)
{
    // waitpid can overwrite errno, so you have to restore it

    int saved_errno = errno;
    while (waitpid(-1, NULL, WNOHANG) > 0)
        ;
    errno = saved_errno;
}

void *get_in_addr(struct sockaddr *sa)
{
    // Returning a pointer to the IP address, no matter whether it's IPV4 or IPV6

    if (sa->sa_family == AF_INET)
    {
        return &((struct sockaddr_in *)(sa))->sin_addr;
    }

    return &((struct sockaddr_in6 *)(sa))->sin6_addr;
}

int server_main(char *port)
{
    int sockfd, newfd;
    struct addrinfo hints, *res, *ptr;
    struct sockaddr_storage their_addr; // When there's ambiguity on the other end and you wanna
    socklen_t addr_len;                 // allocate enough space

    struct sigaction sa;
    int yes = 1;
    char s[INET_ADDRSTRLEN];
    int rv;

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE; // Use my own IP i.e. the server's IP

    if ((rv = getaddrinfo(NULL, port, &hints, &res)) != 0)
    {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
        return 1;
    }

    for (ptr = res; ptr != NULL; ptr = ptr->ai_next)
    {
        // Do all the things you wanna do on the first result
        if ((sockfd = socket(ptr->ai_family, ptr->ai_socktype, ptr->ai_protocol)) == -1)
        {
            perror("socket(): coudln't create socket");
            continue;
        }

        if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1)
        {
            perror("setsockopt: couldn't set options");
            exit(1);
        }

        if (bind(sockfd, ptr->ai_addr, ptr->ai_addrlen) == -1)
        {
            perror("bind(): coudln't bind the socket");
            continue;
        }

        break;
    }

    freeaddrinfo(res);

    if (ptr == NULL)
    {
        // The first pointer was NULL, so we aren't binded to anything
        fprintf(stderr, "server: failed to bind\n");
        exit(1);
    }

    if (listen(sockfd, 10) == -1)
    {
        perror("listen(): coudln't listen");
        exit(1);
    }

    // Signal handling part
    sa.sa_handler = sigchild_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART;

    if (sigaction(SIGCHLD, &sa, NULL) == -1)
    {
        perror("sigaction");
        exit(1);
    }

    printf("Everything's set; waiting for connections...\n");

    while (1)
    {
        // Save their address on the accept call
        socklen_t addrlen = sizeof(their_addr);
        newfd = accept(sockfd, (struct sockaddr *)&their_addr, &addrlen);

        if (newfd == -1)
        {
            perror("accpet()");
            exit(1);
        }

        if (inet_ntop(their_addr.ss_family, get_in_addr((struct sockaddr *)&their_addr), s, sizeof(s)) == NULL)
        {
            perror("inet_ntop(): message");
            exit(1);
        }

        printf("server: got connection from %s\n", s);

        // Shorthand for child process, as if fork == 0, then it is the child process
        if (!fork())
        {
            close(sockfd);

            if (send(newfd, "Hello World!", 13, 0) == -1)
                perror("send");

            close(newfd);
            exit(0);
        }

        // For parent process
        close(newfd);
    }

    return 0;
}

// Client side
int client_main(char *hostname, char *port)
{
    int sockfd, numbytes;
    char buf[100];
    struct addrinfo hints, *servinfo, *ptr;
    int rv;
    char s[INET_ADDRSTRLEN];

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    if ((rv = getaddrinfo(hostname, port, &hints, &servinfo)) != 0)
    {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
        return 1;
    }

    for (ptr = servinfo; ptr != NULL; ptr = ptr->ai_next)
    {
        if ((sockfd = socket(ptr->ai_family, ptr->ai_socktype, ptr->ai_protocol)) == -1)
        {
            perror("socket(): client couldn't create socket");
            continue;
        }

        if (connect(sockfd, ptr->ai_addr, ptr->ai_addrlen) == -1)
        {
            close(sockfd);
            perror("connect(): client socket couldn't connect to server socket");
            exit(1);
        }

        break;
    }

    if (ptr == NULL)
    {
        fprintf(stderr, "Client failed to connect\n");
        return -1;
    }

    if (inet_ntop(ptr->ai_family, get_in_addr((struct sockaddr *)&ptr->ai_addr), s, sizeof(s)) == NULL)
    {
        perror("inet_ntop(): message");
    }

    printf("client is connecting to %s\n", s);
    freeaddrinfo(servinfo);

    if ((numbytes = recv(sockfd, buf, 99, 0)) == -1)
    {
        perror("recv()");
        exit(1);
    }

    buf[numbytes] = '\0';
    printf("Client received message from server: %s\n", buf);
    close(sockfd);

    return 0;
}

int main(int argc, char *argv[])
{

    return 0;
}
