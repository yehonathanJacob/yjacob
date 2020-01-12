Welcome to Aidoc's coding interview!

During the interview you will write code to solve problems.
It's OK to search Google for syntax and language structures, it's not OK to search directly for the answers to our
questions.


All answers are meant to be programmed in python with good division to classes / functions, with readable and concise
code.

1.1. Write a class that unifies several input iterators into one, while always returning the smallest element among all
of the next elements of its iterator members. If there is a tie - take the one from the iterator with the lowest index
(e.g. if there is a tie between iterator #1 and iterator #3, take iterator #1).

The class interface should be the following:

Class MyStream:

    def __init__(self, iterator_list):
        """
        iterator_list is a list of iterators, each having a .__next__() method that returns an integer, or raises a
        StopIteration exception if the stream is empty.
        """

    def __next__(self):
        """
        Returns the minimal element among all next elements of the iterators in iterator_list
        """

Examples:

* If the two iterators are two input lists [1, 4, 6] and [2, 3, 7] - the output iterator should give:
[1, 2, 3, 4, 6, 7]

* If there are three input lists as the input iterators, and their values are:
[1, 5, 2]
[4, 3, 6]
[2, 6, 1]
The output should be:
[1, 2, 4, 3, 5, 2, 6, 6, 1]

1.2. Write your code in the way that you would write it if it was:
* Written to be used in production
* Shared among a team of software engineers
* Planned to be scaled as the product grows for much larger amounts of data

Including, but not limited to, clean code, good design, an effective test suite, and more.


Good luck!
