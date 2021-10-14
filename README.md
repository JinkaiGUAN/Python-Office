# Python-Office
This repository will store small projects using python. 

In this branch, I will upload some data structure achievement using Python. Also simple Algorithm will be shown here.

## Content
- [0-Git](https://github.com/JinkaiGUAN/Python-Office/tree/DataStructure/0-Git): This folder store some widely used `git` command. 

- [1-Stack_Queues_Deques](https://github.com/JinkaiGUAN/Python-Office/tree/DataStructure/1-Stack_Queues_Deques): The basic data structure achieved in this folder are as follows:
  - stacks: This folder achieved LIFO(last input first output) stacks. Now it only has array-based one.
  - queues: This folder achieved FIFO(first input first output) stacks. Noe it only has array-based one.

  - deque： We won't achieve this basic data structure since its a built-in data structure. you can use the following code to get it in Python
  
  ```python
  from collections import deque
  ```
- [2-LinkedList](https://github.com/JinkaiGUAN/Python-Office/tree/DataStructure/2-LinkedList): We are going to use linked list to build other kinds of data structure. The content are as follows,
  - singly_linkedlist: We achieved stack and queue using singly likedlist, which the time complexity in the wrost case can be `O(1)`, and the space complexity is `O(n)`, where n is the number of elements that the data structure stores.
  - circularly_linkedlist: Using singly linkedlist to develop circular Queue.
  - doubly_linkedlist: Develop the base doubly linked list.
  - positional_list_ADT: Inherent the doubly linked list to build a new list that using position to get the element.

- 3-Trees： Non-linear data structure.
    - Edge: An edge of tree T is a pair of nodes (u, v) such that u is the parent of v, or vice versa.
    - Path: A path of T is a sequence of nodes such that any two o=consecutive nodes in the sequence from an edge
    - **Ordered Trees**: A tree is ordered if there is a meaningful linear order among the children of each node; that is, we purposefully identify the children of a node as being the first, second, third, and so on. Such an order is usually visualized by arranging siblings left to right, according to their order.

