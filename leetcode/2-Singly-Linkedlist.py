class Node:
    def __init__(self, value = None):
        self._val = value
        self._next = None

class MyLinkedList:

    def __init__(self):
        self._head = Node(0)

    def get(self, index: int) -> int:
        """index starts from 0."""
        if not self._head._next:
            return -1

        current_node = self._head._next
        current_index = 0
        while current_node:
            # Find the node with the corresponding index.
            if current_index == index:
                return current_node._val
    
            current_node = current_node._next
            current_index += 1
        
        return -1

    def __find_node_before_index__(self, index: int) -> Node:
        """ Take an example here, index = 0
        """
        if not self._head._next:
            return self._head
        current_node = self._head._next
        current_index = 0
        # Add a sepecial situation when index = 0
        if current_index == index:
            return self._head

        while current_node:
            # Find the node with the corresponding index.
            if (current_index + 1) == index: # and current_node._next:
                return current_node
    
            current_node = current_node._next
            current_index += 1
        
        return current_node._next

    def addAtHead(self, val: int) -> None:
        # If there is no elements in the linkedlist
        if not self._head._next:
            self._head._next = Node(val)
            return 
        
        # If there are some elements in the linkedlist
        new_node = Node(val)
        new_node._next = self._head._next
        self._head._next = new_node

    def addAtTail(self, val: int) -> None:
        # If there is no elements in the linkedlist
        if not self._head._next:
            self._head._next = Node(val)
            return
        
        # If there are some elements in the linkedlist
        new_node = Node(val)
        current_node = self._head._next
        while current_node:
            if not current_node._next:
                current_node._next = new_node
                break

            # Update the current node
            current_node = current_node._next

    def addAtIndex(self, index: int, val: int) -> None:
        # Get the previous node
        pre_node = self.__find_node_before_index__(index)
        # Create new node
        new_node = Node(val)
        # Update the linkedlist
        new_node._next = pre_node._next
        pre_node._next = new_node

    def deleteAtIndex(self, index: int) -> None:
        # Get the previous node
        pre_node = self.__find_node_before_index__(index)
        pre_node._next = pre_node._next._next

    def print_linkedlist(self):
        current_node = self._head._next
        while current_node:
            print(str(current_node._val) + ' -> ', end='')
            current_node = current_node._next
        print('')
        return 'False'


# Your MyLinkedList object will be instantiated and called as such:
obj = MyLinkedList()
# obj.addAtHead(7)
# obj.addAtHead(2)
# obj.addAtHead(1)
# obj.print_linkedlist()
# obj.addAtIndex(3, 0)

# obj.print_linkedlist()
# obj.deleteAtIndex(0)
# obj.print_linkedlist()

# obj.addAtIndex(0, 10)
# obj.print_linkedlist()
# obj.addAtIndex(0, 20)
# obj.addAtIndex(0, 30)
# obj.print_linkedlist()

obj.addAtTail(1)
obj.print_linkedlist()
print(obj.get(0))


# obj.addAtHead(1)
# obj.addAtTail(3)
# obj.print_linkedlist()
# obj.addAtIndex(1, 2)
# obj.print_linkedlist()
# print(obj.get(1))
# # obj.addAtHead(val)
# # obj.addAtTail(val)
# # obj.addAtIndex(index,val)
# obj.deleteAtIndex(1)
# obj.print_linkedlist()
# print(obj.get(1))

# MyLinkedList linkedList = new MyLinkedList();
# linkedList.addAtHead(1);
# linkedList.addAtTail(3);
# linkedList.addAtIndex(1,2);   //链表变为1-> 2-> 3
# linkedList.get(1);            //返回2
# linkedList.deleteAtIndex(1);  //现在链表是1-> 3
# linkedList.get(1);            //返回3
