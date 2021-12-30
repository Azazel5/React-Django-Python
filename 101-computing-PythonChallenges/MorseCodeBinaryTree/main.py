# Morse Code Using a Binary Tree - www.101computing.net/morse-code-using-a-binary-tree/

# This library will only be used to draw the binary tree on the screen
from typing import Iterable
from tree import drawTree

# A class to implement a Node / Tree


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

# Convert Character (Find the chracter using a pre-order traversal of the Binary Tree


def getMorseCode(node, character, code):
    if node == None:
        return False
    elif node.value == character:
        return True
    else:
        if getMorseCode(node.left, character, code) == True:
            code.insert(0, ".")
            return True
        elif getMorseCode(node.right, character, code) == True:
            code.insert(0, "-")
            return True


# Let's initialise our binary tree:
tree = Node("START")  # The root node of our binary tree

# 1st Level
tree.left = Node("E")
tree.right = Node("T")

# 2nd Level
tree.left.left = Node("I")
tree.left.right = Node("A")
tree.right.left = Node("N")
tree.right.right = Node("M")

# 3rd Level
tree.left.left.left = Node("S")
tree.left.left.right = Node("U")
tree.left.right.left = Node("R")
tree.left.right.right = Node("W")

tree.right.left.left = Node("D")
tree.right.left.right = Node("K")
tree.right.right.left = Node("G")
tree.right.right.right = Node("O")

# 4th Level
tree.left.left.left.left = Node("H")
tree.left.left.left.right = Node("V")
tree.left.left.right.left = Node("F")
tree.left.left.right.right = Node("")
tree.left.right.left.left = Node("L")
tree.left.right.left.right = Node("")
tree.left.right.right.left = Node("P")
tree.left.right.right.right = Node("J")

tree.right.left.left.left = Node("B")
tree.right.left.left.right = Node("X")
tree.right.left.right.left = Node("C")
tree.right.left.right.right = Node("Y")
tree.right.right.left.left = Node("Z")
tree.right.right.left.right = Node("Q")
tree.right.right.right.left = Node("")
tree.right.right.right.right = Node("")

drawTree(tree)

# Message Input
message = input(
    "Enter a message to convert into Morse Code: (e.g. SOS)").upper()
morseCode = ""

# Convert the message, one character at a time!
for character in message:
    dotsdashes = []
    getMorseCode(tree, character, dotsdashes)
    code = "".join(dotsdashes)
    morseCode = morseCode + code + " "

print("The morse for {} is {}".format(message, morseCode))


def decodeMorseCodeHelper(root, word):
    iterator = root

    for w in word:
        if w == '.':
            iterator = iterator.left
        elif w == '-':
            iterator = iterator.right

    return iterator.value if word != '' else ' '


def decodeMorseCode(codedMessage):
    codedMessageList = codedMessage.split(' ')
    decoded = [decodeMorseCodeHelper(tree, word) for word in codedMessageList]
    return ''.join(decoded)


print("{} decoded: {}".format(morseCode, decodeMorseCode(morseCode)))
