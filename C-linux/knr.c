#include <stdio.h>
#include <string.h>

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
int atoi(char s[])
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

double atof(char s[])
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

void free(char *p)
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

int main()
{
    return 0;
}