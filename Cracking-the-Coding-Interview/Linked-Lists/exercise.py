class Node:
    def __init__(self, val):
        self.val = val 
        self.next = None 

class SinglyLinkedList:
    def __init__(self):
        self.head = None 

    def append_to_tail(self, val):
        my_node = Node(val)
        my_node.next = None 

        curr = self.head 
        if not curr:
            self.head = my_node
            self.head.next = None 
        else:
            while curr.next:
                curr = curr.next 

            curr.next = my_node
            return my_node
    
    def delete_node(self, val):
        if not self.head:
            return None 
        elif self.head.val == val:
            self.head = self.head.next 

        curr = self.head 
        while curr.next:
            if curr.next.val == val:
                curr.next = curr.next.next
                return head  

            curr = curr.next 

    def reverse_list(self):
        curr, prev = self.head, None 
        while curr:
            next_node = curr.next 
            curr.next = prev 
            prev = curr 
            curr = next_node

        self.head = prev 

    def print_list(self, head):
        curr = self.head 
        while curr:
            if curr.next:
                print(f'{curr.val}->', end="")
            else:
                print(curr.val)
            curr = curr.next 
 
"""
2.1 Remove Dups: Write code to remove duplicates from an unsorted linked list.
FOLLOW UP
How would you solve this problem if a temporary buffer is not allowed? 
"""

def remove_duplicates(head):
    curr = head 
    while curr:
        runner = curr 
        while runner.next:
            if runner.next.val == runner.val:
                runner.next = runner.next.next 
            else:
                runner = runner.next 
        curr = curr.next 

"""
2.2 Return Kth to Last: Implement an algorithm to find the kth to last element of a singly linked list. 
"""

def kth_to_last(head, k):
    # Find length of list and return the length - kth node 

    length, counter = 0, 0
    curr, iterator = head, head 
    
    while curr:
        length += 1
        curr = curr.next 

    if k < 1 or k > length:
        return head

    while length - k != counter:
        counter += 1
        iterator = iterator.next 
    
    return iterator

"""
2.3 Delete Middle Node: Implement an algorithm to delete a node in the middle (i.e., any node but
the first and last node, not necessarily the exact middle) of a singly linked list, given only access to
that node.
EXAMPLE
Input: the node c from the linked list a - >b- >c - >d - >e- >f
Result: nothing is returned, but the new linked list looks like a - >b- >d - >e- >f 
"""

def delete_middle_node(node):
    if not node or not node.next:
        return 

    next_node = node.next
    node.val = next_node.val 
    node.next = next_node.next 

"""
2.4 Partition: Write code to partition a linked list around a value x, such that all nodes less than x come
before all nodes greater than or equal to x. lf x is contained within the list, the values of x only need
to be after the elements less than x (see below). The partition element x can appear anywhere in the
"right partition"; it does not need to appear between the left and right partitions.
EXAMPLE
Input: 3 -> 5 -> 8 -> 5 - > 10 -> 2 -> 1 [partition = 5)
Output: 3 -> 1 -> 2 -> 10 -> 5 -> 5 -> 8 
"""

def partition(head, k):
    lesser = SinglyLinkedList()
    higher = SinglyLinkedList()
    while head:
        if head.val < k:
            lesser.append_to_tail(head.val)
        elif head.val >= k:
            higher.append_to_tail(head.val)

        head = head.next 

    curr = lesser.head 
    while curr.next:
        curr = curr.next 
    
    curr.next = higher.head 
    return lesser 

"""
2.S Sum Lists: You have two numbers represented by a linked list, where each node contains a single
digit. The digits are stored in reverse order, such that the 1 's digit is at the head of the list. Write a
function that adds the two numbers and returns the sum as a linked list.
EXAMPLE
Input: (7-) 1 -) 6) + (5 -) 9 -) 2).Thatis,617 + 295.
Output: 2 -) 1 -) 9. That is, 912.
FOLLOW UP
Suppose the digits are stored in forward order. Repeat the above problem.
EXAMPLE
Input: (6 -) 1 -) 7) + (2 -) 9 -) 5).Thatis,617 + 295.
Output: 9 -) 1 -) 2. That is, 912. 
"""

def sum_lists(list1, list2, backwards = None):
    if backwards:
        list1.reverse_list()
        list2.reverse_list()

    curr1, curr2, sum1, sum2 = list1.head, list2.head, [], []
    while curr1:
        sum1.append(str(curr1.val))
        curr1 = curr1.next 

    while curr2:
        sum2.append(str(curr2.val))
        curr2 = curr2.next 

    res = str(int(''.join(sum1)) + int(''.join(sum2)))
    ret = SinglyLinkedList()
    for i in res:
        ret.append_to_tail(int(i))

    return ret 
    
"""
2.6 Palindrome: Implement a function to check if a linked list is a palindrome. 
"""

def palindrome_linkedlist(head):
    # Use the runner method to find and reverse the latter half of the list and compare it
    # If both halves prove to be equal, it is a palindrome linked list

    slow = fast = head 
    while fast and fast.next:
        fast = fast.next.next 
        slow = slow.next 

    prev = None 
    while slow:
        slow_next = slow.next 
        slow.next = prev 
        prev = slow 
        slow = slow_next

    while prev:
        if prev.val != head.val:
            return False 

        prev = prev.next 
        head = head.next 

    return True 

"""
2.7 Intersection: Given two (singly) linked lists, determine if the two lists intersect. Return the intersecting node. Note that the intersection is defined based on reference, not value. That is, if the kth
node of the first linked list is the exact same node (by reference) as the jth node of the second
linked list, then they are intersecting. 
"""

def intersection_linkedlist(head1, head2):
    if not head1 or not head2:
        return None 

    curr1, curr2, = head1, head2 
    while curr1 != curr2:
        curr1 = head2 if not curr1 else curr1.next 
        curr2 = head1 if not curr2 else curr2.next 

    return curr1 
     
"""
2.8 Loop Detection: Given a circular linked list, implement an algorithm that returns the node at the
beginning of the loop.
DEFINITION
Circular linked list: A (corrupt) linked list in which a node's next pointer points to an earlier node, so
as to make a loop in the linked list.
"""

def loop_detector(head):
    slow, fast = head, head 

    # Check the meeting point of slow and fast inside the loop
    while fast and fast.next:
        slow = slow.next 
        fast = fast.next.next 
        if fast == slow:
            break 
    
    if not fast or not fast.next:
        return None 
    
    # Earlier meeting point and head node are equidistant from each other, so they will meet at the 
    # loop start when moves at the same pace
    slow = head
    while slow != fast:
        slow = slow.next 
        fast = fast.next 

    return slow 
