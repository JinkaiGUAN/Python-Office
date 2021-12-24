# Definition for a Node.
class Node:
    def __init__(self, val, prev, next, child):
        self.val = val
        self.prev = prev
        self.next = next
        self.child = child

class Solution:
    def flatten(self, head: Node) -> Node:
        def dfs(node: Node) -> Node:
            curr = node
            last = None # last node
            while curr:
                nxt = curr.next

                if curr.child:
                    child_last = dfs(curr.child)

                    # insert the child
                    curr.next = curr.next
                    curr.child.prev = curr

                    # If we have next node for this current node, we insert the child between current and next node.
                    if nxt:
                        child_last.next = nxt
                        nxt.prev = child_last
                    
                    # Deprecate the child for this node
                    curr.child = None
                    last = child_last
                else:
                    last = curr
                curr = nxt
            return last
        
        dfs(head)

        return head
        