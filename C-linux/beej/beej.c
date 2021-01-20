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
#include <poll.h>

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

// If you wanna create the same programs instead for UDP, then you'll simply supply SOCK_DGRAM as
// an argument. There'll be no need for listen or accept functions since these are unconnected
// dgram sockets. Again, data sent through UDP connections aren't guaranteed to arrive on the other
// end. At the same time, you can also create connected datagram sockets.

/* "Advanced" techniques 
 * ---------------------
 * Remember that many functions inherently block. Some of the ones you've used which block are accept
 * or read. When you first make a socket, it's set to block thanks to the kernel: to not block, you
 * must use fcntl.
 * Using the poll function is a great way of checking what file descriptors are available for IO 
 * operations. However, note that this function is horribly slow when there are a huge number of
 * connections. How does the poll call work? The OS will block until one of the events defined on the
 * struct pollfd array occurs. 
 */

void poll_example()
{
    struct pollfd pdfs[1];

    // Remember that 0 is standard input
    pdfs[0].fd = 0;
    pdfs[0].events = POLLIN;
    int num_events = poll(pdfs, 1, 2500);

    if (num_events == 0)
        printf("Poll timed out\n");

    else
    {
        int pollin_happened = pdfs[0].revents & POLLIN;

        if (pollin_happened)
            printf("File descriptor %d is ready for reading\n", pdfs[0].fd);
        else
            printf("Unexpected event occurred: %d\n", pdfs[0].revents);
    }
}

// The select function also gives a similar functionality to poll. If you wanna keep listening to
// connections while reading from already available connections, either of these functions are
// great choices. Select works by having sets of file descriptrs and a timeout struct: if you set
// the timeout struct fields to 0, select times out immediately and polls all file descriptors in
// the sets. If you set it to NULL, it will block and wait until the first file descriptor is
// ready.

void multiperson_chat_using_select(char *port)
{
    fd_set master;
    fd_set read_fds;
    int fdmax;
    int listener;
    int newfd;

    struct sockaddr_storage remoteaddr;
    socklen_t addrlen;
    char buf[256];
    int nbytes;

    char remoteIP[INET6_ADDRSTRLEN];
    int yes = 1;
    int i, j, rv;

    struct addrinfo hints, *res, *ptr;
    FD_ZERO(&master);
    FD_ZERO(&read_fds);

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET6;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE;

    if ((rv = getaddrinfo(NULL, port, &hints, &res)) == -1)
    {
        fprintf(stderr, "selectserver: %s\n", gai_strerror(rv));
        exit(1);
    }

    for (ptr = res; ptr != NULL; ptr = ptr->ai_next)
    {
        listener = socket(ptr->ai_family, ptr->ai_socktype, ptr->ai_protocol);

        if (listener < 0)
            continue;

        setsockopt(listener, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int));

        if (bind(listener, ptr->ai_addr, ptr->ai_addrlen) < 0)
        {
            close(listener);
            perror("bind()");
            exit(1);
        }

        break;
    }

    if (ptr == NULL)
    {
        fprintf(stderr, "selectserver: failed to bind\n");
        exit(1);
    }

    freeaddrinfo(res);

    if (listen(listener, 10) == -1)
    {
        perror("listen()");
        exit(1);
    }

    FD_SET(listener, &master);
    fdmax = listener;

    for (;;)
    {
        read_fds = master;

        // A good strategy is to keep track of the maximum file descriptor, so you can pass in that
        // fd + 1 as the first argument to select. Here we don't care about writable/exceptable fds,
        // and we're setting the time to NULL so it will block until the first one becomes availble
        if (select(fdmax + 1, &read_fds, NULL, NULL, NULL) == -1)
        {
            perror("select");
            exit(1);
        }

        for (i = 0; i <= fdmax; i++)
        {

            // If going inside the if block, the read_fd is ready for reading
            if (FD_ISSET(i, &read_fds))
            {
                if (i == listener)
                {
                    addrlen = sizeof(remoteaddr);
                    newfd = accept(listener, (struct sockaddr *)&remoteaddr, &addrlen);

                    if (newfd == -1)
                        perror("accept");
                }

                else
                {
                    FD_SET(newfd, &master);

                    if (newfd > fdmax)
                        fdmax = newfd;

                    printf("selectserver: new connection from %s on "
                           "socket %d\n",
                           inet_ntop(remoteaddr.ss_family,
                                     get_in_addr((struct sockaddr *)&remoteaddr), remoteIP, INET6_ADDRSTRLEN),
                           newfd);
                }
            }
            else
            {
                if ((nbytes = recv(i, buf, sizeof buf, 0)) <= 0)
                {
                    if (nbytes == 0)
                        printf("selectserver: socket %d hung up\n", i);

                    else
                        perror("recv");

                    close(i);
                    FD_CLR(i, &master);
                }

                // Successfully read some data from a client, so we'll send it to everyone
                else
                {
                    for (j = 0; j <= fdmax; j++)
                    {
                        if (FD_ISSET(j, &master))
                        {
                            if (j != listener && j != i)
                            {
                                if (send(j, buf, nbytes, 0) == -1)
                                    perror("send");
                            }
                        }
                    }
                }
            }
        }
    }
}

// Damn, that was a hell of a function. The reason why there are two sets of file descriptors is
// that the call to select changes them, so you must save the master safely elsewhere.
// On a different note, the call to any read/recv may be split up into portions because there's a
// limit. To handle these instances, you have to understand how data serialization works. Beej
// recommends finding a library or two which does this encoding/decoding process for you. For example,
// the functions you know and love, htonl, ntohl, ....

// If you're constructing your own packets, store binary integers in network byte order. Check if
// on every call to recv, you've reached the number of bytes read (until the byte size specified on
// the header). Once you're done, you've read the entire packet. If the packets got merged i.e. you
// read past one and a little bit of the second packet in one read call. For that, you're gonna have to
// do a bit of subtraction, remove that first packet from the buffer, and move the second packet to the
// front of the buffer, so the next recv call can build upon it. This moving up and down of the buffer
// can be implemented relatively easily with a circular buffer.

// Broadcasting can be used to send data to multiple hosts at the same time by setting the socket
// option to be SO_BROADCAST (when you set it to be reuseable). So what exactly is the destination
// address in this case? For the chat server program you wrote, you basically looped through the list
// of connected clients, and sent them messages one at a time, but this is different. Here, you have
// two options: send data to subnet broadcast address or to global broadcast address.

/* General tips section */

// Signals tend to cause blocked system calls, such as accept or select to return -1 and set errno.
// Handle this by creating a custom signal handler using sigaction.

// If you want a timeout on reading/writing operations, use select, which allows you to specify
// whatever timeouts you want for either sets of file descriptors.

// A return value of 0 on a recv means that the remote side has closed the connection.

// If you wanna compress/encrypt, the strategy is to compress first, then encrypt.

/* The rest of the book is Beej's own man pages, specifically geared towards networking */

int main(int argc, char *argv[])
{
    return 0;
}
