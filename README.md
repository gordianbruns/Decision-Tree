README
------------------
Gordian Bruns

CS365

Lab C - Decision Trees
------------------

I. File List
 - main.py  # contains read_file, print_table, entropy, gain, remainder, importance, plurality_value, decision_tree_learning, test, accuracy_test, and a bunch of helper functions
 - tree.py  # contains Tree-class and Node-class (print_tree)

Note that all files must be in the same directory.


II. Usage

The program takes one optional command line argument:

   - filename

It is set to printing the decision tree and printing the accuracy of the computed decision tree of titanic2.txt, if you do not give a command line argument.
If you do, it will do the same thing, but with the data set of the file you entered.

To run the program you must be in the directory of the files and type the following into the command line:

python main.py <filename> (optional)

Note that the file must exist, otherwise, it is going to exit.
