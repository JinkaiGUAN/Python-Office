
# Thread
## Two ways run a Python file based on CPython
- CPython parses and compiles the source text into bytecode.
- CPython runs the bytecode using a stack-based interpreter.
    -  CPython uses GIL to main coherence when running the programme.
    
## Needs to remember
- Python threads cannot run in parallel on multiple CPU cores because of the global interpreter lock.
- Python threads are still useful despite the GIL because they provide an easy way to do multiple things seemingly 
  at the same time.
  
- Use Python threads to make multiple system calls in parallel. This allows you to do blocking I/O at the same time 
  as computation.
  
## Questions:
- What's the thread?
- Using thread to complete the parallel task is reasonable or not?

# Using Lock to Prevent Data Races in Threads


# Using Queue to Fulfill the Parallelism

## Problems when using parallelism
- Need refactoring the code using lock. 

## What is the difference between `queue.Queue` and `collections.deque`
