"""回文， 给定链表 半段回文"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:

    def isPalindrome(self, head: ListNode) -> bool:
        """There are two methods here.
        
        - Gain all values in the linkedlist and push them into an array, then using array to check 
            whether the linkedlist is palindrome or not.

        - Reverse the later half linkedlist, then check each element for each half linkedlist.
        """

        if head is None:
            return True

        # find the ending node of the first half linkedlist and reverse the later half linkedlist
        middle = self.end_of_fist_half(head)
        second_half_start = self.reverse_later_half(middle.next)

        # Check palindrome 
        result = True
        first_position = head
        second_position = second_half_start
        while result and second_position is not None:
            if first_position.val != second_position.val:
                result = False
            first_position, second_position = first_position.next, second_position.next

        # restore the original linkedlist
        middle.next = self.reverse_later_half(second_half_start)
        return result

    def end_of_fist_half(self, head: ListNode) -> ListNode:
        fast, slow = head, head

        while fast and slow and fast.next and fast.next.next:
            fast, slow = fast.next.next, slow.next
        return slow
    
    def reverse_later_half(self, head: ListNode) -> ListNode:
        prev, curr = None, head
        while curr is not None:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        return prev
            


        

