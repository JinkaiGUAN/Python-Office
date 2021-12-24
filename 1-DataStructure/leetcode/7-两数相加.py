# Definition for singly-linked list.
from typing import List


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        head = ListNode()
        curr = head
        carry_bit = 0

        ######## Fist method
        # while l1 and l2:
        #     target = l1.val + l2.val + carry_bit
        #     if target // 10:
        #         carry_bit, target = 1, target % 10
        #     else:
        #         carry_bit, target = 0, target
        #     new_node = ListNode(target)
        #     curr.next = new_node
        #     curr = new_node
            
        #     l1, l2 = l1.next, l2.next
            
        # # continue the job if two linkedlists do not have the same length
        # next_node = l1 if not l2 else l2
        # while next_node:
        #     target = next_node.val + carry_bit
        #     if target // 10:
        #         carry_bit, target = 1, target % 10
        #     else:
        #         carry_bit, target = 0, target
        #     new_node = ListNode(target)
        #     curr.next = new_node
        #     curr = new_node
        #     next_node = next_node.next
        #################


        ########### Second method

        while l1 or l2:
            # continule the loop until there is no elements in the l1 or l2
            n1 = l1.val if l1 else 0
            n2 = l2.val if l2 else 0
            sum = n1 + n2 + carry_bit
            new_node = ListNode(sum % 10)
            curr.next = new_node
            curr = new_node

            # calculate the carray bit
            carry_bit = sum // 10

            # update the linklist
            if l1: l1 = l1.next
            if l2: l2 = l2.next
        
        curr.next = ListNode(carry_bit) if not carry_bit == 0 else None

        return head.next

