from collections import Counter

"""
1.1 Is Unique: Implement an algorithm to determine if a string has all unique characters. What if you
cannot use additional data structures? 
"""

def string_uniqueness_simple(s):
    return len(s) == len(set(s))

def string_uniqueness_hard(s):
    same_found = None 
    sorted_string = sorted(s)
    for i in range(len(sorted_string) - 1):
        if sorted_string[i] == sorted_string[i+1]:
            return False 

    return True 

"""
1.2 Check Permutation: Given two strings, write a method to decide if one is a permutation of the
other.
"""

def permutation(s1, s2):
    return sorted(s1) == sorted(s2)

"""
1.3 URLify: Write a method to replace all spaces in a string with '%20: You may assume that the string
has sufficient space at the end to hold the additional characters, and that you are given the "true"
length of the string. (Note: If implementing in Java, please use a character array so that you can
perform this operation in place.)
EXAMPLE
Input: "Mr John Smith ", 13
Output: "Mr%20John%20Smith"
"""

def URLify(s, length):
    s = s.strip()
    return s.replace(' ', '%20')

"""
1.4 Palindrome Permutation: Given a string, write a function to check if it is a permutation of a palindrome. A palindrome is a word or phrase that is the same forwards and backwards. A permutation
is a rearrangement of letters. The palindrome does not need to be limited to just dictionary words.
EXAMPLE
Input: Tact Coa
Output: True (permutations: "taco cat". "atco cta". etc.) 
"""

def palindrome_permutation(s):
    str_count = Counter(s)
    odd_count = 0
    for key, val in str_count.items():
        if odd_count > 1:
            return False 

        if val % 2 != 0:
            odd_count += 1

    return True 

"""
1.5 One Away: There are three types of edits that can be performed on strings: insert a character,
remove a character, or replace a character. Given two strings, write a function to check if they are
one edit (or zero edits) away.
EXAMPLE
pale, ple -> true
pales. pale -> true
pale. bale -> true
pale. bake -> false 
"""

def one_away(s1, s2):
    if abs(len(s1) - len(s2)) > 1:
        return False 

    s1_mapping = {}
    for i, s in enumerate(s1):
        s1_mapping[s] = i 

    unequal_chars = 0
    for s in s2:
        if not s in s1_mapping:
            unequal_chars += 1

    return True if unequal_chars <= 1 else False

"""
1.6 String Compression: Implement a method to perform basic string compression using the counts
of repeated characters. For example, the string aabcccccaaa would become a2b1c5a3. If the
"compressed" string would not become smaller than the original string, your method should return
the original string. You can assume the string has only uppercase and lowercase letters (a - z). 
"""

def string_compression(s):
    convert = []
    running_count = 0
    for i in range(len(s)):
        running_count += 1
        if i == len(s) - 1 or s[i] != s[i+1]:
            convert.append(s[i] + str(running_count))
            running_count = 0

    convert_str = ''.join(convert)
    return convert_str if len(convert_str) < len(s) else s 

"""
1.7 Rotate Matrix: Given an image represented by an NxN matrix, where each pixel in the image is 4
bytes, write a method to rotate the image by 90 degrees. (an you do this in place? 
"""

def rotate_matrix(matrix):
    matrix.reverse()
    for row in range(len(matrix)):
        for column in range(row):
            matrix[row][column], matrix[column][row] = matrix[column][row], matrix[row][column]

    return matrix 

"""
1.8 Zero Matrix: Write an algorithm such that if an element in an MxN matrix is 0, its entire row and
column are set to O. 
"""

def zero_matrix(matrix):
    mapping = {}
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            if matrix[row][column] == 0:
                mapping[row] = column
        
    for row in mapping.keys():
        for j in range(len(matrix[0])):
            matrix[row][j] = 0

    for column in mapping.values():
        for j in range(len(matrix)):
            matrix[j][column] = 0

    return matrix 

"""
1.9 String Rotation: Assume you have a method isSubstring which checks if one word is a substring
of another. Given two strings, s1 and s2, write code to check if s2 is a rotation of s1 using only one
call to isSubstring (e.g., "waterbottle" is a rotation of"erbottlewat"). 
"""

def isSubstring(s1, s2):
    return s2 in s1 

def string_rotation(s1, s2):
    if len(s1) == len(s2):
        return isSubstring(s1 + s1, s2)

    return False 

