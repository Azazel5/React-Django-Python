"""
3.1 Three in One: Describe how you could use a single array to implement three stacks. 
"""

class ThreeInOneStack:
    def __init__(self, stack_size):
        self.number_stacks = 3 
        self.stack_size = stack_size 
        self.stacks = [0] * (self.number_stacks * stack_size)
        self.sizes = [0] * self.number_stacks

    def push(self, stack_number, value):
        if self.isFull(stack_number):
            raise Exception(f"Stack {stack_number} is full!") 

        self.sizes[stack_number] += 1
        self.stacks[self.jump_to_stack(stack_number)] = value 

    def pop(self, stack_number):
        if self.isEmpty(stack_number):
            raise Exception(f"Stack {stack_number} is empty!")

        index_start = self.jump_to_stack(stack_number)
        top_value = self.stacks.pop(index_start)
        self.sizes[stack_number] -= 1
        return top_value


    def peek(self, stack_number):
        if self.isEmpty(stack_number):
            raise Exception(f"Stack {stack_number} is empty!")

        return self.stacks[self.jump_to_stack(stack_number)]

    def isFull(self, stack_number):            
        return self.sizes[stack_number] == self.stack_size

    def isEmpty(self, stack_number):
        return self.sizes[stack_number] == 0

    def jump_to_stack(self, stack_number):
        offset = stack_number * self.stack_size 
        filled_items = self.sizes[stack_number]
        return offset + filled_items - 1

"""
3.2 Stack Min: How would you design a stack which, in addition to push and pop, has a function min
which returns the minimum element? Push, pop and min should all operate in 0(1) time. 
"""

class MinStack:
    def __init__(self):
        self.stack = []
        self.min = []

    def push(self, value):
        if not self.min or value < self.min[-1]:
            self.min.append(value)

        self.stack.append(value)

    def pop(self):
        popped = self.stack.pop()
        if popped == self.min[-1]:
            self.min.pop()
        return popped 

    def peek(self, arr):
        return arr[-1]

"""
3.3 Stack of Plates: Imagine a (literal) stack of plates. If the stack gets too high, it might topple.
Therefore, in real life, we would likely start a new stack when the previous stack exceeds some
threshold. Implement a data structure SetOfStacks that mimics this. SetOfStacks should be
composed of several stacks and should create a new stack once the previous one exceeds capacity.
SetOfStacks. push () and SetOfStacks. pop () should behave identically to a single stack
(that is, pop ( ) should return the same values as it would if there were just a single stack).
FOLLOW UP
Implement a function popAt (int index) which performs a pop operation on a specific sub-stack.
"""

class StackOfPlates:
    def __init__(self, stack_size):
        self.stack_o_stacks = [[0]* stack_size]
        self.stack_size = stack_size
        self.stack_pointer = 0
        self.indexes = [0]

    def push(self, value):
        if self.is_full(self.stack_pointer):
            self.stack_pointer += 1 
            self.stack_o_stacks.append([0]* self.stack_size)
            self.indexes.append(0)
        
        self.indexes[self.stack_pointer] += 1
        self.stack_o_stacks[self.stack_pointer][self.indexes[self.stack_pointer]-1] = value

    def pop(self):
        if self.is_empty(self.stack_pointer):
            self.indexes.pop(self.stack_pointer)
            self.stack_o_stacks.pop(self.stack_pointer)
            self.stack_pointer -= 1

        elif self.indexes[self.stack_pointer] == 1:
            self.indexes.pop(self.stack_pointer)
            popped = self.stack_o_stacks.pop(self.stack_pointer)[0]
            self.stack_pointer -= 1
            return popped

        popped = self.stack_o_stacks[self.stack_pointer].pop(self.indexes[self.stack_pointer] - 1)
        self.indexes[self.stack_pointer] -= 1
        return popped

    def is_empty(self, stack_number):
        if stack_number >= 0:
            return self.indexes[stack_number] == 0
        else:
            raise Exception("Cannot pop a totally empty StackOfPlates") 

    def is_full(self, stack_number):
        return self.indexes[stack_number] == self.stack_size

"""
3.4 Queue via Stacks: Implement a MyQueue class which implements a queue using two stacks. 
"""



    