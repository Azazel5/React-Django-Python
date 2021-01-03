#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/stat.h>
#include <sys/dir.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>

/*
 * Just to be clear, a call by reference is passing a pointer to the function. Array arguments are 
 * always call by reference.  
 * Just like \n, other useful characters may be \t (tab), \b (backspace), \" (double quote), or 
 * \\ (single backslash). 
*/

void format_specifiers()
{
    // The 4 and 6 in the beginning specifies the minimum number of spaces
    // before printing while the decimal point is how many decimal points to include.
    printf("%4.0f and %6.1f\n", 6.00002356, 1.2453455);
}

// It is bad practice to have random numbers floating around in your program, so
// always use the define keyword to set up constants. Note: no semicolon needed at
// the end of a define declaration.

void copy_file()
{
    // Copy file using getchar() and putchar()
    // getchar returns an int, so we define c as an int to capture that value
    int c;
    while ((c = getchar()) != EOF)
    {
        putchar(c);
    }
}

void count_char()
{
    long nc = 1;
    while (getchar() != EOF)
        nc++;
    printf("%ld\n", nc);
}

// "\n" is a string which contains only one character, so it contains 1 byte
// multivariable initialization exists i.e. a = b = c = 0;
// on big programs, giving reading #define(s) for values like 0 and 1, makes all the difference in
// readability

void count_dig_white_other()
{
    int c, nwhite, other;
    int ndigit[10];
    nwhite = other = 0;
    for (int i = 0; i < 10; i++)
        ndigit[i] = 0;

    while ((c = getchar()) != EOF)
    {
        if (c >= '0' && c <= '9')
            ++ndigit[c - '0'];
        else if (c == ' ' || c == '\n' || c == '\t')
            ++nwhite;
        else
            ++other;
    }

    printf("digits =");
    for (int i = 0; i < 10; i++)
        printf(" %d", ndigit[i]);
    printf("\nWhite space = %d, other = %d", nwhite, other);
}

int getline_(char s[], int lim)
{
    // helper for find_longest_line
    int c, i;
    for (i = 0; i < lim - 1 && (c = getchar()) != EOF && c != '\n'; ++i)
        s[i] = c;

    if (c == '\n')
    {
        s[i] = c;
        ++i;
    }

    s[i] = '0';
    return i;
}

void copy(char s1[], char s2[])
{
    // helper for find_longest_line
    int i = 0;
    while ((s2[i] = s1[i]) != '\n')
        ++i;
}

#define MAXLINE 1000
void find_longest_line()
{
    int len;
    int max = 0;
    char line[MAXLINE];
    char save[MAXLINE];
    while ((len = getline_(line, MAXLINE)) > 0)
    {
        if (len > max)
        {
            max = len;
            copy(line, save);
        }
    }

    if (max > 0)
        printf("%s", save);
}

/* the C compiler puts the character \0 at the end of char arrays to mark the end of the string 
 * if a program uses several files, and you need to use a global variable from another file, the 
 * extern keyword will be requried
 * You can specify qualifiers for ints, such as short, long, unsigned etc. Long constants are written like 
 * 123L. Any leading 0's means that it is an octal representation and 0x means hexadecimal.
 * Par exemple, decimal 31 can be written as 037 in octal or 0x1f in hexadecimal. 
 * Characters constants have different values in different character sets which can undergo numeric 
 * operations, just like any other numbers. 
*/

// Custom example of atoi
int atoi_(char s[])
{
    // Note - s[i] - '0' gives the ASCII character value for the char stored in s[i]
    int n = 0;
    for (int i = 0; s[i] >= '0' && s[i] <= '9'; i++)
        n = 10 * n + s[i] - '0';

    return n;
}

// 1 is true and 0 is false; if assigning variables of different types, the "less spacious" type is
// converted to the more spacious one. If the assigning is happenening the other way round, the excess
// portions are simply discarded: for example - float to int, the decimal portions are discarded.

// A nice little shortcut for setting one value equal to another and then incrementing the earlier value is
// a[i++] = b[j], where both are arrays

char *squeeze(char *s, int c)
{
    // Simply moves all c elements to the end and terminates the array

    int i, j;
    int length = strlen(s);

    for (i = j = 0; i < length; i++)
    {
        if (s[i] != c)
            s[j++] = s[i];
    }

    s[j] = '\0';
    return s;
}

/* Operators Refresher: &, |, ^ (exclusive or), << (left shift), >> (right shift), and ~ (complement)
 * Bitwise AND is often used to mask off some set of bits, while the OR turns the bits on ;)
 * x >> 2 will shift x by two positions to the right, or to the left if << is used; the excess positions
 * are filled by 0's. The complement is often used (converts 1's to 0's and vice versa) in situations like
 * x & ~077, which fills the last 6 bits of x to 0's. 
*/

// The (bool) ? statement1 : statement2 operator also works in C. Save the for loop variables for
// situations when you have several nested for loops; it may come in handy sometimes!
// Try to find smarter ways to write boolean statements: a mixture of &&, ||, and ! makes things
// unreadable.

double atof_(char s[])
{
    // Converts a string to a double
    double val, power;
    int i, sign;

    // Remember that you can save the variable above to just skip over any possible tabs, newline chars,
    // or empty spaces via the empty for loop
    for (i = 0; s[i] == ' ' || s[i] == '\n' || s[i] == '\t'; i++)
        ;

    sign = 1;
    if (s[i] == '+' || s[i] == '-')
        sign = (s[i++] == '+') ? 1 : -1;

    for (val = 0; s[i] >= '0' && s[i] <= '9'; i++)
        val = 10 * val + s[i] - '0';

    if (s[i] == '.')
        i++;

    for (power = 1; s[i] >= '0' && s[i] <= '9'; i++)
    {
        val = 10 * val + s[i] - '0';
        power *= 10;
    }

    return (sign * val / power);
}

// Function arguments are passed by value by default. So, they receive a private copy of the variable
// you passed into it. If you want it to affect the actual variable you passed, you must, instead, pass
// by reference i.e. pass the variable's address value.

// Thinking in terms of data structures is very useful; for example, think about a simple calculator
// application. Sure, you can brute force your approach, but a better, more efficient approach would
// be to create a stack, add the operands, and pop them after an operator comes in, and finish by
// pushing the result back into the stack.

// There exist functions for ungetting characters i.e. ungetch, which is the mirror image of getch.

#define BUFSIZE 100
char buf[BUFSIZE];
int bufptr = 0;

char getch()
{
    // Get a character from buffer

    return (bufptr > 0) ? buf[--bufptr] : getchar();
}

void ungetch(int c)
{
    // Push character back into buffer

    if (bufptr > BUFSIZE)
        printf("Too many characters\n");
    else
        buf[++bufptr] = c;
}

// Internal static variables can be private, permanant storage for functions, and don't just come into
// existence when the function is called. Static variables and functions only exists within that
// particular source file and cannot be used in other files, unlike extern variables.

// In the absence of explicit intialization, extern and static variables are intialized to 0, while
// local and register variables have garbage values.

// Macros are more powerful than simple #includes and #defines. You can even have macros with arguments,
// but they have their own issues. Nonetheless, they can be benefitial, so learning them is worthwhile.

// & gives the address of a variable, and * dereferences a pointer and outputs the value associated with
// the pointer. int * defined an int pointer i.e. if the pointer variable is dereferenced, it will be in
// the context of an int. Pointers can also be used in expressions, typically like a = *p + 2; On the
// other hand *(px + 1) has a slightly different meaning.

// To corroborate the earlier idea, let us take the idea of arrays, which are essentially pointers. If
// we have a pointer int *x = &a[0], x + 1 will point to the next element, x - i will point to i elements
// before x. Thus, *(x + 1) will refer to the contents of a[1]. By adding 1, it multiples by the size of the
// object the array is holding (in this case an int).

// The difference between a pointer and array is that pointers can be set to another variable, but
// arrays are constants, so they cannot be reset to another array.

// Pointers can also be set: pa = pb will set the pointer of a to the pointer of b now. A powerful
// usage of pointers is to make general functions (like swap()) and pass pointers to it. Now the function
// will alter the original variables themselves rather than the local copies swap() has to itself.

int strlen_(char *s)
{
    // Armed with this knowledge, we can create a version of strlen which relies on this pointer
    // incrementation like. A refreser once again: *s points to the first element in the char
    // array, so s++ will point to s[1], s[2], ... because of the for loop. The dereference simply
    // checks for the end of a string, so until it encounters that, we keep adding to length.

    int length;
    for (length = 0; *s != '\0'; s++)
        length++;

    return length;
}

// A rudimentary storage allocator using pointer arithmetic
#define ALLOCSIZE 1000 // Available space
static char allocbuf[ALLOCSIZE];
static char *allocptr = allocbuf; // This will point to the first index in allocbuf

char *alloc(int n)
{
    // this function should return a pointer to n characters. The function works by shifting
    // the buffer pointer by n units and returing a the old pointer back (as it is free now)

    if (allocptr + n <= allocbuf + ALLOCSIZE)
    {
        allocptr += n;
        return allocptr - n;
    }
    else
    {
        return NULL;
    }
}

void free_(char *p)
{
    if (p >= allocbuf && p < allocbuf + ALLOCSIZE)
        allocptr = p;
}

// You can use and increment at the same time as defined somewhere above, if you value conciseness
// a la *a++, which dereferences the pointer and increments the pointer after that.
// If you wanna define a 2D array in C, you can do something like int (*day_tab)[13] or day_tab[][13]
// Arrays of pointers can also be useful, and the book uses the example of sorting strings prove that
// So the example defines char *arr[100], where each arr[i] is a character pointer.

// What exactly is the difference between int a[10][10] and int *b[10]? The former is a true array with
// 100 cell, but b, however, allocates 10 pointers, which each point to an array of ints. Thus, the latter
// will allocate 110 items, 10*10 and 10 extra for the pointers themselves. The second version is
// more flexible in that each pointer may point to 10 elements, no elements, or anything in between in this case.

// This is a good time to introduce command line arguments, as argv is the kind of variable discussed
// above i.e. char *argv[]. Argv[0] is always the name of the program.

// Optional arguments should be specified in any order, and it's very convenient if users can join
// those arguments together.

/*
    #define MAXLINE 1000
    int main(int argc, char* argv[]) {
        char line[MAXLINE], *s;
        long lineno = 0;
        int except = 0, number = 0;
        
        while (--argc > 0 && (*++argv[0] == '-')) 
            for (s = argv[0] + 1; *s != '\0'; s++)
                switch (*s) {
                    case 'x':
                        except = 1;
                        break;
                    
                    case 'n':
                        number = 1;
                        break;
                    
                    default:
                        printf("find: illegal option %c\n", *s);
                        argc = 0;
                        break;
                }
        
        if (argc != 1) 
            printf("Usage: find -x -n pattern\n");
        else
            while (getline(line, MAXLINE) > 0) {
                lineno++;
                if ((index(line, *argv) >= 0) != except) {
                    if (number)
                        printf("%ld: ", lineno);
                    printf("%s", line);
                }
            }
    }

    Every time it encounters a situation where the first element of argv (which is a pointer to pointer) is
    a -, it checks the cases and sets the numbers. Command line utilities are created using these
    formats and are very useful. 
*/

// You can also pass functions as pointers to other functions. Notice that int (*comp) {} and int *comp {}
// have different meanings: the former means that comp is a pointer to a function that returns an int
// and the latter is that comp is a function which returns a pointer to an int.

// Keeping a bunch of related variables into one component ~ a structure, which is extremely useful. Use
// the dot operator to access variables inside the structs. Structures can be nested as well.

// An example payroll struct
struct date
{
    int month;
    int day;
    int year;
    char month_name[4];
};

struct person
{
    char name[100];
    char address[1000];
    long zipcode;
    long ss_number;
    double salary;
    struct date birth_information;
    struct date hire_date;
};

// Structures cannot be passed to or returned from functions, and we can only get the address of or
// the value of its members. However, "pointers to structures do not suffer from these limitations".
// If you instead have a pointer to a structure, you'll have to use struct_name->variable_name to
// access that variable. This is useful, as you won't have to declare all the arguments in the
// function where you passed the pointer.

// Defining an array of structs:
// struct c {
//  ...
// } keytab[100];
// Another way to write this: struct key keytab[100] -> defines an array keytab, which
// holds 100 key structs.

struct key
{
    char *keyword;
    int keycount;
} keytab[100];

int binary_search(char *word, struct key tab[], int n)
{
    // the second argument is how you pass in an array (and thus a pointer) of structs to a function
    int low = 0, mid = 0, high = n - 1, contd;
    while (low <= high)
    {
        mid = (low + high) / 2;
        if ((contd = strcmp(word, tab[mid].keyword)) < 0)
            high = mid - 1;
        else if (contd < 0)
            low = mid + 1;
        else
            return mid;
    }

    return -1;
}

// To find the size of a struct array, you can use the sizeof operator to divide each struct by
// the space occupied by the total array i.e. sizeof(keytab) / sizeof(key)

#define LETTER 'a'
#define DIGIT '0'

int type(int c)
{
    // Determines type of character, using the defines above: the defines themselves can be
    // anything that is a digit or letter
    if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'))
        return LETTER;
    else if (c >= '0' && c <= '9')
        return DIGIT;
    else
        return c;
}

int getword(char *w, int lim)
{
    int c, t;

    if (type(c = *w++ = getch()) != LETTER)
    {
        *w = '\0';
        return c;
    }

    while (--lim > 0)
    {
        t = type(c = *w++ = getch());
        if (t != LETTER && t != DIGIT)
        {
            ungetch(c);
            break;
        }
    }

    *(w - 1) = '\0';
    return LETTER;
}

void countCKeywords()
{
    int n, t;
    char word[20];

    while ((t = getword(word, 20)) != EOF)
        if (t == LETTER)
            if ((n = binary_search(word, keytab, 100)) >= 0)
                keytab[n].keycount++;

    for (n = 0; n < 100; n++)
        if (keytab[n].keycount > 0)
            printf("%4d %s\n", keytab[n].keycount, keytab[n].keyword);
}

// We could've also written the above function using pointers to the struct array, with minor modifications.
// The bianry search function would have to return pointers to each key struct element. In countCKeywords,
// the increment would have to be done like n->keycount++, assuming we made the changes to binary_search
// returns struct key *.

// When functions are returning a complicated type like struct key *binary(...), an alternate style which can
// be used is:
// struct key *
// binary(...)

// Structs can also refer to themselves. Let's take the problem of trying to count occurrences of all
// words in an input. We can use structs to implement binary trees to help us do that efficiently.
// We'll make it so that the left subtree will only contain words smaller than the word at the node
// and the right subtree will have the "greater" words.

// Self declarations on structs are also legal, but there's a catch: the declaration must be a
// pointer to the struct node for it to be okay.

#define MAXWORD 20

struct tnode
{
    char *word;
    int count;
    struct tnode *left;
    struct tnode *right;
};

char *strsave(char *s)
{
    char *p;

    if ((p = malloc(strlen(s) + 1)) != NULL)
        strcpy(p, s);

    return p;
}

// When you're allocating space for different data types, you must be mindful and use some
// extra space to satisfy all alignment restrictions. This is why casting is done on
// malloc/calloc calls.

struct tnode *talloc()
{
    return (struct tnode *)alloc(sizeof(struct tnode));
}

struct tnode *tree(struct tnode *p, char *w)
{
    int cond;
    if (p == NULL)
    {
        p = talloc();
        p->word = strsave(w);
        p->count = 1;
        p->left = p->right = NULL;
    }
    else if ((cond = strcmp(w, p->word)) == 0)
        p->word++;
    else if (cond < 0)
        p->left = tree(p->left, w);
    else
        p->right = tree(p->right, w);

    return p;
}

void treeprint(struct tnode *p)
{
    if (p != NULL)
    {
        treeprint(p->left);
        printf("%4d %s\n", p->count, p->word);
        treeprint(p->right);
    }
}

void wordFrequencyCounter()
{
    struct tnode *root;
    char word[MAXWORD];
    int t;

    root = NULL;
    while ((t = getword(word, MAXWORD)) != EOF)
        if (t == LETTER)
            root = tree(root, word);

    treeprint(root);
}

// Table lookup programs are pretty fundamental, as they're used heavily in areas hidden by
// high level packages or programming languages. Eg. the #define A 1 call will put A and 1
// in a table-like structure i.e. hashtable (dictionary for you python geeks out there).
// Implementing this will be simple:
// Hash the incoming name and use it to index into an array of pointers -> pointing to the description
// of the names.

#define HASHSIZE 100

struct nlist
{
    char *name;
    char *def;
    struct nlist *next;
} * hashtable[HASHSIZE];

int hashfunction(char *s)
{
    int hashval;
    for (hashval = 0; *s != '\0'; s++)
        hashval += *s;

    return hashval;
}

struct nlist *lookup(char *s)
{
    // Returns a pointer to the nlist entry if the name exists

    struct nlist *np;
    for (np = hashtable[hashfunction(s)]; np != NULL; np = np->next)
        if (strcmp(np->name, s) == 0)
            return np;

    return NULL;
}

/*
    Reading this book (and the intro to OS class) has taught me:
    
    1. Error checking is crucial. After any computation, always wrap your variables with a 
       quick error check
    2. Writing a quick paragraph detailing the steps you have to take for your function to 
       work is very valuable i.e. the software design doc. Imagine you're a professor writing a 
       project for your class. 
*/

struct nlist *install(char *name, char *def)
{
    struct nlist *np;
    int hashval;

    if ((np = lookup(name)) == NULL)
    {
        // No such record in the hash table
        np = (struct nlist *)alloc(sizeof(*np));
        if (np == NULL)
            return NULL;

        if ((np->name = strsave(name)) == NULL)
            return NULL;

        hashval = hashfunction(np->name);
        np->next = hashtable[hashval];
        hashtable[hashval] = np;
    }
    else
    {
        // Found the record, np now is the pointer to the record
        free(np->def);
    }

    // Free any previous definition, even if a name was found in the table, so it can be overwritten
    // by this call below
    if ((np->def = strsave(def)) == NULL)
        return NULL;

    return np;
}

// Symbol tables in compilers must know whether the text is a keyword, static, or external. The usual way
// this is done is define some masks which are bit positions, and turn them off or on using bitwise
// operations. Eg. flags |= EXTERNAL | STATIC to turn on or flags &= ~(EXTERNAL | STATIC).
// if ((flags & (EXTERNAL | STATIC)) == 0) -> will be true if both bits are off
// You could also define a set of bits within an int; the bits are adjacent and are 1 bit each.
// These are called fields.

struct
{
    unsigned is_keyword : 1;
    unsigned is_extern : 1;
    unsigned is_static : 1;
} flags;

// Unions are a type of structure that can hold variables of different types. The union is big enough
// to hold the variable of the "widest" type. Another useful tool we have got as C programmers
// is the typedef facility. The typedef occurs after the variable type i.e. typdef char *reverendDonkBonkers.

// Here's a good example, using the tree nodes shown earlier
typedef struct tnode_
{
    char *word;
    int count;
    struct tnode *left;
    struct tnode *right;
} TREENODE, *TREEPTR;

// Why do this? This will give you the structure and a pointer to the structure too. Using this,
// you'll be able to pass in the TREEPTR in the alloc call too: you'll get more flexibility and
// readability.

// The simplest you can get with IO is the getchar and putchar functions. Also, in the terminal, you
// can switch whether you want input to be read from the terminal or another file via the < operator.
// Also, you can use pipes i.e. | to provide IO from one program to another. Example - otherprog | prog
// will cause the input for prog to come from the output of otherprog. Similarly, we have the > command
// which writes the program output to a file instead of the terminal too.

// Since the cat utility simply reads a file, you can combine the output of multiple files into one single
// thing a la cat file1 file2 ... | lower > output, which creates a pipe: the output of all the files is
// sent to "lower" (as input), and the lower-case resultant is returned as output file.

/* Each format specifier in printf can have options added to it -
 * 1. Minus sign: left adjustment 
 * 2. Digit string: minimum field width
 * 3. Period: seperates field width with the next digit string, which is..
 * 4. The precision digit string: used for floats or doubles 
 * 5. Length modifier l: indicates that the data item is a long and not an int 
 * 
 * The conversion characters available:
 * d (decimal), o (unsigned octal), x (unsigned hexadecimal), u (unsigned decimal), 
 * c (single character), s (string), e (scientific notation), f (float or double),
 * g (e or f, whichever is shorter, and ignores non-significant zeroes) 
*/

// For scanf, you must specify the arguments as pointers to where the read input must reside.
// The conversion characters for scanf is similar to printf, but it has some differences,
// which can be checked via documentation.

// There are variables flavors of printf/scanf avaiable, such as sscanf or sprintf, which
// operate on strings instead of files.

// Opening a file, using high level IO, is as simple as an fopen call, which returns a
// struct pointer (internally implemented as a typedef) called FILE *. Note - opening an
// existing file for writing will discard all the previous contents. To read, the simplest way is
// to use the getc and putc functions. There are three files opened automatically in every C
// prgoram, which are stdin, stdout, and stderr. For formatted IO of files, use fprintf and
// fscanf.

/*
    ### An implementation of the cat utility in UNIX ###

    void filecopy(FILE *fp) {
        int c;

        while ((c = getc(fp)) != EOF)
            putc(c, stdout);
    }

    int main(int argc, char *argv[]) {
        FILE *fp;

        if (argc == 1)
            filecopy(stdin);

        else {
            while (--argc > 0)

                if ((fp = fopen(*++argv, "r")) == NULL) {
                    fprintf(stderr, "cat: can't open %s\n", *argv);
                    exit(1);

                } else {
                    filecopy(fp);
                    fclose(fp);
                }
        }

        exit(0);
    }
*/

// Standard IO also provides the fgets function, which reads the input line by line, into a buffer.
// fputs for putting in lines, as usual.

// The calloc function is just like the alloc written in the book, as it returns a pointer to
// enough space for n objects of the specified size -> cfree to free the pointer. Calloc
// initializes the memory to 0, whereas malloc doesn't.

// In any given UNIX system, everything is a file, even the user's terminal. All this communication
// is done via file descriptors. Whenever, the terminal runs a program in UNIX, three files are
// created, just just in C programs described above. In this case, the file descriptors 0, 1, and 2
// are opened, which correspond to stdin, stdout, and stderr respectively. IO redirection is done as
// usual with < and >.

// For low level IO, the open/read/write operations become an entry point to the OS, where everything is
// done in bytes.

// Note the byte count to read or write is arbitrary; however, some commonly used examples include 1
// (1 char at a time) or 512 (a physical blocksize on many devices). The latter is more efficient.
// For the open function, pass in 0 for read, 1 for write, and 2 for read/write access.

// An implementation of the UNIX utility cp, which copies one file to the other
#define BUFSIZE_ 512
#define PMODE 0644

void error(char *s1, char *s2)
{
    printf("%s %s\n", s1, s2);
    exit(1);
}

int main_cp(int argc, char *argv[])
{
    int f1, f2, f3, n;
    char buf[BUFSIZE_];

    if (argc != 3)
        error("Usage: cp from to", NULL);
    if ((f1 = open(argv[1], 0)) == -1)
        error("cp: can't open %s", argv[1]);
    if ((f2 = creat(argv[2], PMODE)) == -1)
        error("cp: can't create %s", argv[2]);

    while ((n = read(f1, buf, BUFSIZE_)) > 0)
        if (write(f2, buf, n) != n)
            error("cp: write error", NULL);

    exit(0);
}

// File IO is sequential, but you can access files at whatever position you desire using the lseek function.
// lseek(fd, offset, origin) - where origin can be 0, 1, 2 (start, current, or end of file)
// Since the FILE * is actually a struct, there's a wealth of information available about the file to you.
// This is the information about what it contains, rather about the file itself. For that we need the
// directory information.

// fsize, a special type of "ls" command, which also prints the file sizes.
// A directory is also a file! Ay yai yai UNIX!
// Use the dirent structure to get the inode number and the filename.

void directory(char *name)
{
    /* 
    struct dirent dirbuf;
    char *npb, *nep;
    int i, fd;

    npb = name + strlen(name);
    *npb++ = '/';
    if (npb + DIRSIZ + 2 >= name + BUFSIZE)
        return;
    if ((fd = open(name, 0)) == -1)
        return;
    while (read(fd, (char *) &dirbuf, sizeof(dirbuf)) > 0) {
        
        if (dirbuf.d_ino == 0)    *** 0 inode number means that the slot is unused ***
            continue;
        if ((strcmp(dirbuf.d_name, ".") == 0) || (strcmp(dirbuf.d_name, "..")) == 0)
            continue; *** If the directory is itself or its parent, skip ***
        
        for (i = 0, nep=npb; i < DIRSIZ; i++)
            *nep++ = dirbuf.d_name[i];

        *nep++ = '\0';
        fsize(name);
    }

    close(fd);
    *--npb = '\0'; 

    --- This function has been commented because my compiler cannot find DIRSIZ in <sys/dir.h> for some reason.
    */
}

void fsize(char *name)
{
    struct stat stbuf;

    if (stat(name, &stbuf) == -1)
    {
        fprintf(stderr, "fsize: can't find %s\n", name);
        return;
    }

    // If the file type is a directory
    if ((stbuf.st_mode & S_IFMT) == S_IFDIR)
        directory(name);

    printf("%8lld %s\n", stbuf.st_size, name);
}

int main__(int argc, char *argv[])
{
    char buf[256];

    if (argc == 1)
    {
        strcpy(buf, ".");
        fsize(buf);
    }
    else
        while (--argc > 0)
        {
            strcpy(buf, *++argv);
            fsize(buf);
        }

    return 0;
}

// Smart storage allocator
// This one will dynamically allocate memory instead of a compiled size array. Also, since other parts
// of the program may also request resources asynchronously, the space won't be continuous. Instead,
// we will get back blocks of data, one will point to the others. While freeing, we must check if the
// adjacent blocks are free as well, so we will be able to join those together.

// *** This memory allocator is pretty complicated; COME BACK TO THIS AFTER PRACTICING MORE C ***

typedef int ALIGN;
typedef union header
{
    struct
    {
        union header *ptr;
        unsigned size;
    } s;

    ALIGN x;
} HEADER;

static HEADER base;
static HEADER *allocptr_al = NULL;

void free_al(char *ap)
{
    register HEADER *p, *q;

    p = (HEADER *)ap - 1;
    for (q = allocptr_al; !(p > q && p < q->s.ptr); q = q->s.ptr)
        if (q >= q->s.ptr && (p > q || p < q->s.ptr))
            break;

    if (p + p->s.size == q->s.ptr)
    {
        p->s.size += q->s.ptr->s.size;
        p->s.ptr = q->s.ptr->s.ptr;
    }
    else
        p->s.ptr = q->s.ptr;

    if (q + q->s.size == p)
    {
        q->s.size += p->s.size;
        q->s.ptr = p->s.ptr;
    }
    else
        q->s.ptr = p;

    allocptr_al = q;
}

static HEADER *morecore(unsigned nu)
{
    // This function asks the OS for memory. Since that is very expensive, it is only done after
    // alloc passed it the number of units to allocate and rounds it up to a larger value.
    register char *cp;
    register HEADER *up;
    register int rnu;

    rnu = 128 * ((nu + 128 - 1) / 128); // 128 is the number of units to allocate at once
    cp = sbrk(rnu * sizeof(HEADER));

    if ((int)cp == -1)
        return NULL;

    up = (HEADER *)cp;
    up->s.size = rnu;
    free_al((char *)(up + 1));
    return allocptr_al;
}

char *alloc_al(unsigned nbytes)
{
    register HEADER *p, *q;
    register int nunits;

    nunits = 1 + (nbytes + sizeof(HEADER) - 1) / sizeof(HEADER);
    if ((q = allocptr_al) == NULL)
    {
        // No free list of blocks yet
        base.s.ptr = allocptr_al = q = &base;
        base.s.size = 0;
    }

    for (p = q->s.ptr;; q = p, p = p->s.ptr)
    {
        if (p->s.size >= nunits)
            q->s.ptr = p->s.ptr;
        else
        {
            p->s.size -= nunits;
            p += p->s.size;
            p->s.size = nunits;
        }

        allocptr_al = q;
        return (char *)(p + 1);
    }

    if (p == allocptr_al)
        if ((p = morecore(nunits)) == NULL)
            return NULL;
}

int main()
{
    return 0;
}