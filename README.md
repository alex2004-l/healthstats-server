## Homework 1 ASC - Les Stats Sportif

---

#### Alexandra Florentina Georgiana Lache, 332CD
---

Implementation
---

Some importants aspects for the design of my solution:
- Apart from the original files, I also created a separate file called `task.py` for my implementation of task objects.
- _TaskFactory_ : For modeling the jobs I created a task interface and implemented a class for each job using Factory desing. I chose this pattern for ensuring a uniform interface to all the tasks and for making it easy to maintain. Basically, when a thread runs a task from the queue, it will call task.func(), and each task's implementation is handled in the task.py file
- _DataFrames and DataIngestor_ : Initially, my aproach was for the tasks to work directly on dataframes. Later on, I thought it would be better design-wise to keep the pandas logic only in DataIngestor. So I added helper methods for processing the data and converting the results in dict() for easier conversion to the json format
- _Less duplicate code in routes.py_ : As I wrote the functions for the routes, my code from routes.py was becoming really repetitive, so I added a helper method for POST request to reduce code length and improve maintanability.
- _Threadpool_ : My threadpool has a event for shutdown management, a queue for yet unprocessed tasks and a dictionary for retaining the status of all the jobs.
- _TaskRunner_ : It hold a reference to its parent threadpool and to the task it is currently processing. It runs in a loop until the threadpool is shutdown and there are no more tasks to process. It is also responsible for writing the outputs of a task.


Challenges
---
- Using Pandas : As this was my first time using Pandas, it was an interesting experience. While I initially faced some challenges with dataframe manipulation, obtaining some malformed DataFrames, especially with the groupby function returning different objects, I eventually managed to get a hang of the process.
- Using Queue : Working with queue module was interesting. Discovering the timeout attribute and using it for permitting all the threads to finish after the threadpool shuts down might not be the most graceful method to handle this (I thought about using a get_no_wait() instead).
- The working of the logger : Discovering a method to use the logger created, and not the default logger of Flask was a little bit challenging.

What to improve
---

- Maybe thinking more thoughtfully the exceptions that might arise.

What I didn't do
---
- I didn't implement extra features.
- I didn't implement the unittesting.


Resources
---
- [about GIL and Python dictionaries](https://stackoverflow.com/questions/1312331/using-a-global-dictionary-with-threads-in-python) => I wasn't sure if dict() needed lock due to the GIL (the only link I saved)
- https://docs.python.org/3/library/
- https://stackoverflow.com
- https://www.w3schools.com/ => for syntax
- probably more, but I forgot to log them all

Git
-
1. https://github.com/alex2004-l/les-stats-sportif 



---