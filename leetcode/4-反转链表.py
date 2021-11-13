# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        if not head or not head.next:
            return head
        # if ~head or ~head.next:
        #     return head
        
        rest = None
        curr = head
        while curr is not None:
            next_node = curr.next
            curr.next = rest
            rest = curr
            curr = next_node
            
        return rest