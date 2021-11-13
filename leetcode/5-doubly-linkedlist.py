"""We start the linkedlist from 0."""


class Node:
    def __init__(self, val, next = None) -> None:
        self.val = val
        self.prev = None
        self.next = None


class MyLinkedList:

    def __init__(self):
        self.size = 0
        self.head, self.tailer = Node(0), Node(0) # sentinel nodes as pseudo-head and pseudo-tail
        self.head.next = self.tailer
        self.tailer.prev = self.head

    def get(self, index: int) -> int:
        if self.size == 0:
            return -1

        ind = 0

        curr_node = self.head.next
        while curr_node:
            if ind == index:
                return curr_node.val
            ind += 1
            curr_node = curr_node.next
        
        return -1 # beyond the elemnt bumber we have

    def addAtHead(self, val: int) -> None:
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        self.addAtIndex(self.size, val)

    def addAtIndex(self, index: int, val: int) -> None:
        new_node = Node(val)

        curr_node = self.head.next
        ind = 0
        while curr_node:
            if ind == index:
                # connect the new node
                new_node.next = curr_node
                new_node.prev = curr_node.prev

                # disable the old connections
                curr_node.prev.next = new_node
                curr_node.prev = new_node

                # update the size
                self.size += 1
                break
            
            # update the index and current node
            ind += 1
            curr_node = curr_node.next

    def deleteAtIndex(self, index: int) -> None:
        curr_node = self.head.next
        ind = 0

        while curr_node:
            if ind == index:
                # prev and next node conect
                curr_node.prev.next = curr_node.next
                curr_node.next.prev = curr_node.prev

                # disable the current node
                curr_node.next, curr_node.prev = None, None

                self.size -= 1
                break

            ind += 1
            curr_node = curr_node.next

    def printLinkedList(self):
        
        curr_node = self.head.next

        while curr_node.next.next: # if we get the previous node of the tailer, terminate
            print(str(curr_node.val) + ' -> ', end='')
            curr_node = curr_node.next
        print(str(curr_node.val))
        print("done")


linkedList =  MyLinkedList();
linkedList.addAtHead(1)
linkedList.addAtTail(3)
linkedList.printLinkedList()
linkedList.addAtIndex(0,2)  #//链表变为 2-> 1 -> 3   1-> 2-> 3
linkedList.printLinkedList()
print(linkedList.get(1))            #//返回1
linkedList.deleteAtIndex(1)  #//现在链表是2-> 3
linkedList.printLinkedList()
print(linkedList.get(1))
