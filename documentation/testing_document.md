# Testing document

The testing was done mostly by automated tests that can be found and ran in tests.py by:
```
cd src
python3 tests.py
```
Some tests have 2 parts and test 1 was also tested and verified on paper. There are 5 tests in total and all test a different aspect of the code. Test 1 tests the trie data structure and tests 2-5 test the markov chain. Many of the tests have smaller tests within them, but all of those smaller tests contribute in some way to the main test defined here / in the code.

Test 1 is divided into two parts. The first part tests that the trie contains exactly the inserted sequences and nothing more. This part of the test was also tested on paper to assure that there are no errors. The second parts test that the trie preserves repeated insertions and doesn’t get rid of them. 

Test 2 is testing that the Markov chain rejects correctly false / unusable starting sequences i.e. the test is passed if the Markov chain raises an error. Test 2 is also divided into two parts. The first part tests that an error is raised if the starting context includes a state that does not occur in the training data and the second test tests that an error is raised if the individual states of the starting sequences do occur in the training data but the given starting combination does not. 

Test 3 tests that the generated sequences obey the training data i.e. there are no transitions that were not in the training data. In other words the Markov chain should stick to the training data and not make transitions out of nowhere. 

Test 4 tests that the long run distributions are as they should be by the given training data. In the test the training data creates a loop where 3 and 4 should appear more and 2 and 5 less. The tests check that the distribution of notes in the generated sequence matches the distribution of the training data and that the distribution of  transitions also match the training data. 

Test 5 tests that the Markov and trie work with other hashable objects as well as that was the way they were designed. Test 5 logically tests the exact same things as test 4, but the sequence that is being tested consists of different hashable types: string, range, binary and boolean to be exact. 

All of the tests are passed and accepted. 
