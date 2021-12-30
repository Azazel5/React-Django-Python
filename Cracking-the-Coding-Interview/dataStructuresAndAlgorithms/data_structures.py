# from collections import deque -> you can use this as a stack too, just like a list


class Array:
    def __init__(self, size):
        self.items = [0] * size

    def __str__(self):
        return ', '.join([str(x) for x in self.items])

    def __getitem__(self, index):
        return self.items[index]

    def __setitem__(self, key, value):
        self.items[key] = value


class LinkedListNode:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedList:
    def __init__(self, dummy_value):
        self.dummy = LinkedListNode(dummy_value)

    def build_linked_list(self, numbers):
        ''' Builds a linked list from an array of numbers given a dummy head node '''
        index = 0
        curr = self.dummy

        while curr and index < len(numbers):
            node = LinkedListNode(numbers[index])
            curr.next = node
            curr = curr.next
            index += 1

    def get_nth_node(self, nth):
        index = 1
        curr = self.dummy.next

        while curr and index != nth:
            curr = curr.next
            index += 1

        return curr

    # Insertion: insert at front, after a particular node, and at the end
    def insert_front(self, value):
        dummy_next = self.dummy.next
        node_to_insert = LinkedListNode(value, dummy_next)
        self.dummy.next = node_to_insert

    def insert_after_node(self, existing_node, value):
        next_to_existing = existing_node.next
        existing_node.next = LinkedListNode(value, next_to_existing)

    def insertEnd(self, value):
        curr = self.dummy

        while curr.next:
            curr = curr.next

        curr.next = LinkedListNode(value)

    # Deletion: Delete a value (first occurrence), delete a value at index
    def delete_node_first(self, value):
        curr, prev = self.dummy.next, None

        while curr:
            if curr.value == value:
                break

            prev = curr
            curr = curr.next

        prev.next = curr.next
        curr = None

    def delete_node_at_index(self, index):
        node_to_delete, node_to_delete_prev = self.get_nth_node(
            index), self.get_nth_node(index - 1)
        node_to_delete_prev.next = node_to_delete.next
        node_to_delete = None

    def has_loop(self):
        ''' Detects a loop in the linkedList and returns the loop closing node '''
        setter = set()
        curr = self.dummy.next

        while curr:
            if curr not in setter:
                setter.add(curr)
                curr = curr.next
            else:
                return True, curr

        return False, 0

    def __str__(self):
        curr = self.dummy.next
        lis = []

        has_loop, _ = self.has_loop()

        if has_loop:
            return "I refuse to print; there's a loop in this damned list"
        else:
            while curr:
                lis.append(str(curr.value))
                curr = curr.next

            return '->'.join(lis)

# For  a stack implementation in python, either a list or a deque is fine
# Implement a stack using: LinkedList, Queue


class Stack1:
    ''' This stack can be initialized with a list or left empty '''

    def __init__(self, initializer=None):
        self.__list = LinkedList(0)

        if initializer:
            self.__list.build_linked_list(initializer)

    def push(self, value):
        self.__list.insertEnd(value)

    def peek(self):
        if self.get_size() == 0:
            return "Stack is empty"

        curr = self.__list.dummy.next

        while curr.next:
            curr = curr.next

        return curr.value

    def pop(self):
        ''' If the size is 0, there's nothing to pop. If it's one, pop and return the head node.
        Else, unlink the last node as usual '''

        size = self.get_size()

        curr, prev = self.__list.dummy.next, None
        return_value = None

        if size == 0:
            return

        elif size == 1:
            return_value = self.__list.dummy.next.value
            self.__list.dummy.next = None

        else:
            while curr.next:
                prev = curr
                curr = curr.next

            return_value = curr.value
            prev.next = None

            curr = None

        return return_value

    def is_empty(self):
        ''' Return True if the dummy node is the only node in the list; else, the linkedList has another
        node, which means the stack has at least one element '''

        return True if not self.__list.dummy.next else False

    def get_size(self):
        size = 0
        curr = self.__list.dummy.next

        while curr:
            size += 1
            curr = curr.next

        return size

