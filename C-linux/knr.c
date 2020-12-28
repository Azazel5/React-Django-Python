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
int atoi(char s[]) {
    // Note - s[i] - '0' gives the ASCII character value for the char stored in s[i]
    int n = 0;
    for(int i = 0; s[i] >= '0' && s[i] <= '9'; i++) 
        n = 10 * n + s[i] - '0';
    
    return n;
}

// 1 is true and 0 is false; if assigning variables of different types, the "less spacious" type is 
// converted to the more spacious one. If the assigning is happenening the other way round, the excess
// portions are simply discarded: for example - float to int, the decimal portions are discarded.

// A nice little shortcut for setting one value equal to another and then incrementing the earlier value is
// a[i++] = b[j], where both are arrays 

char *squeeze(char *s, int c) {
    // Simply moves all c elements to the end and terminates the array

    int i, j;
    int length = strlen(s);

    for(i = j = 0; i < length; i++) {
        if(s[i] != c) 
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

double atof(char s[]) {
    // Converts a string to a double
    double val, power;
    int i, sign;
    for(i = 0; s[i] == ' ' || s[i] == '\n' || s[i] == '\t'; i++) {

    }
}

int main()
{

    return 0;
}