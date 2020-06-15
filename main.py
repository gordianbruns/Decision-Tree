''' File:       main.py
 *  Purpose:    Creates a decision tree and tests its accuracy
 *
 *  Input:      filename (optional)
 *  Output:     printed decision tree, accuracy test result
 *
 *  Usage:      python main.py [file]<String>(optional)
 *
 *  Note:       Default: titanic2.txt file
 *
'''

import sys      # for command line arguments
import math     # for mathematical functions (logarithm)
import random   # for randrange function
import copy     # for deepcopy
from tree import Tree, Node  # for Tree-class, Node-class

examples = dict()       # global variable; represents the labelled data


def main(argv):
    if len(sys.argv) > 2:
        print("Correct usage: python main.py [file]<String>(optional)")
    filename = "titanic2.txt"
    try:
        filename = sys.argv[1]
    except IndexError:
        pass
    read_file(filename)
    variables = extract_variables(examples)
    tree = decision_tree_learning(examples, variables, 0, 0)
    tree.get_root().print_tree()
    accuracy_test(examples)
'''  main  '''


''' Function:    read_file
 *  Purpose:     reads the file and creates a dictionary with the data
 *  Input args:  fname<String>
 *  Return val:  None
 *  Note:        changes the global variable examples
'''
def read_file(fname):       # reads the file
    global examples
    try:
        f = open(fname, "r")
    except IOError:
        exit("Error opening the file! Exiting ...")
    line = f.readline()
    if not line:
        exit("The file is empty! Exiting ...")
    example_l = line.split()
    example_t = tuple(example_l)
    examples[example_t[:-1]] = [0, 0]

    while True:
        line = f.readline()
        if not line:
            break
        example_list = line.split()
        example_tup = tuple(example_list)
        if example_tup[:-1] in examples.keys():
            if example_tup[-1] == "yes":
                examples[example_tup[:-1]][0] += 1
            else:
                examples[example_tup[:-1]][1] += 1
        else:
            if example_tup[-1] == "yes":
                examples[example_tup[:-1]] = [1, 0]
            else:
                examples[example_tup[:-1]] = [0, 1]
'''  read_file  '''


''' Function:    print_table
 *  Purpose:     prints the data as a table
 *  Input args:  None
 *  Return val:  None
'''
def print_table():        # prints the data
    for label in examples.keys():
        if examples[label] == [0, 0]:
            for i in label:
                print(i, end=" ")
            break
    print()
    for key, val in examples.items():
        if examples[key] != [0, 0]:
            print(key, ":", val)
'''  print_table  '''


''' Function:    extract_variables
 *  Purpose:     extracts all random variables of a given data set
 *  Input args:  data<dictionary>
 *  Return val:  variables<list> or False
 *  Note:        helper function
'''
def extract_variables(data):
    variables = 0
    for key in data.keys():
        if data[key] == [0, 0]:
            variables = key
    if variables != 0:
        return variables
    return False
'''  extract_variables  '''


''' Function:    index_of_var
 *  Purpose:     returns the index of a random variable
 *  Input args:  var<String>, data<dictionary>
 *  Return val:  i<int>changes the global variable examples
 *  Note:        helper function
'''
def index_of_var(var, data):      # calculates at what index the variable is
    for key in data.keys():
        if data[key] == [0, 0]:
            for i in range(len(key)):
                if key[i] == var:
                    return i
'''  index_of_var  '''


''' Function:    get_yes_no
 *  Purpose:     returns how many "yes" and "no" we have with a given attribute
 *  Input args:  var_index<int>, attribute<String>, data<dictionary>
 *  Return val:  yes_count<int>, no_count<int>
 *  Note:        helper function
'''
def get_yes_no(var_index, attribute, data):
    yes_count = 0
    no_count = 0
    visited = []
    if var_index == len(data.keys()) - 2:
        for val in data.values():
            yes_count += val[0]
            no_count += val[1]
        return yes_count, no_count
    for key in data.keys():
        if data[key] not in visited and key[var_index] == attribute:
            if data[key] != [0, 0]:
                visited.append(data[key])
                yes_count += data[key][0]
                no_count += data[key][1]
    return yes_count, no_count
'''  get_yes_no  '''


''' Function:    entropy_wrapper
 *  Purpose:     calculates the entropy of a single attribute
 *  Input args:  var_index<int>, attribute<String>, data<dictionary>
 *  Return val:  function call (b())
'''
def entropy_wrapper(var_index, attribute, data):
    yes_count, no_count = get_yes_no(var_index, attribute, data)
    return b(yes_count / (yes_count + no_count))
'''  entropy_wrapper  '''


''' Function:    entropy
 *  Purpose:     calculates the entropy of a random variable
 *  Input args:  var<String>, data<dictionary>
 *  Return val:  summ<double>
'''
def entropy(var, data):
    visited = []
    summ = 0
    index = index_of_var(var, data)
    for key in data.keys():
        if data[key] == [0, 0]:
            continue
        if key[index] not in visited:
            visited.append(key[index])
            entr = entropy_wrapper(index, key[index], data)
            summ += entr
    return summ
'''  entropy  '''


''' Function:    b
 *  Purpose:     calculates a value described in the textbook
 *  Input args:  q<double>
 *  Return val:  val<double>
'''
def b(q):
    if q == 0 or q == 1:
        return 0
    val = -(q * math.log(q, 2) + (1 - q) * math.log(1 - q, 2))
    return val
'''  b  '''


''' Function:    total_entropy
 *  Purpose:     calculates the entropy of a whole data set
 *  Input args:  data<dictionary>
 *  Return val:  function call (b())
 *  Note:        helper function
'''
def total_entropy(data):
    last = len(data.keys()) - 2
    yes_count, no_count = get_yes_no(last, "yes", data)
    return b(yes_count / (yes_count + no_count))
'''  total_entropy  '''


''' Function:    gain
 *  Purpose:     calculates the gain of a random variable
 *  Input args:  var_index<int>, data<dictionary>
 *  Return val:  difference of two function call values (total_entropy and remainder)
'''
def gain(var_index, data):
    return total_entropy(data) - remainder(var_index, data)
'''  gain  '''


''' Function:    remainder
 *  Purpose:     calculates the remainder based on the textbook's formula
 *  Input args:  var_index<int>, data<dictionary>
 *  Return val:  summ<double>
'''
def remainder(var_index, data):
    summ = 0
    last = len(data.keys()) - 2
    yes_total, no_total = get_yes_no(last, "yes", data)
    attributes = get_attributes(var_index, data)
    for attribute in attributes:
        yes_count, no_count = get_yes_no(var_index, attribute, data)
        summ += ((yes_count + no_count) / (yes_total + no_total)) * b(yes_count / (yes_count + no_count))
    return summ
'''  remainder  '''


''' Function:    importance
 *  Purpose:     returns a sorted list of tuples that consists of the random variables and their gains
 *  Input args:  data<dictionary>, attributes<list of random variables>
 *  Return val:  gains<list of tuples>
'''
def importance(data, attributes):
    gains = list()
    if len(attributes) != 0:
        for variable in range(len(attributes)):
            g = gain(variable, data)
            gains.append((attributes[variable], g))
        sort_tuple_list(gains)
        return gains
'''  importance  '''


''' Function:    sort_tuple_list
 *  Purpose:     sorts lists of tuples (the number/gain is the second value)
 *  Input args:  tuple_list<list of tuples>
 *  Return val:  None
 *  Note:        helper function; modifies the tuple list
'''
def sort_tuple_list(tuple_list):
    for i in range(1, len(tuple_list)):
        value = tuple_list[i]
        position = i
        while position > 0 and tuple_list[position - 1][1] > value[1]:
            tuple_list[position] = tuple_list[position - 1]
            position = position - 1
        tuple_list[position] = value
'''  sort_tuple_list  '''


''' Function:    plurality_value
 *  Purpose:     returns a subtree with a root whose value describes the plurality value as described in the textbook
 *  Input args:  data<dictionary>
 *  Return val:  Tree-object
'''
def plurality_value(data):
    yes = 0
    no = 0
    for key in data.keys():
        yes += data[key][0]
        no += data[key][1]
    if yes > no:
        return Tree(Node("yes"))
    elif yes < no:
        return Tree(Node("no"))
    else:
        return Tree(Node("no"))
'''  plurality_value  '''


''' Function:    same_classification_check
 *  Purpose:     checks whether given data has the same outcome each time
 *  Input args:  data<dictionary>
 *  Return val:  <boolean>, Tree-object (or None)
 *  Note:        helper function
'''
def same_classification_check(data):
    yes = 0
    no = 0
    for key in data.keys():
        yes += data[key][0]
        no += data[key][1]
    if yes == 0 and no > 0:
        return True, Tree(Node("no"))
    elif yes > 0 and no == 0:
        return True, Tree(Node("yes"))
    return False, None
'''  same_classification_check  '''


''' Function:    get_attributes
 *  Purpose:     returns all attributes of a random variable
 *  Input args:  var_index<int>, data<dictionary>
 *  Return val:  visited<list>
 *  Note:        helper function
'''
def get_attributes(var_index, data):
    visited = []
    for key in data.keys():
        if data[key] != [0, 0]:
            if key[var_index] not in visited:
                visited.append(key[var_index])
    return visited
'''  get_attributes  '''


''' Function:    get_examples_attributes
 *  Purpose:     returns a dictionary with the examples that contain a given attribute
 *  Input args:  var_index<int>, attribute<String>, data<dictionary>
 *  Return val:  new_dict<dictionary>
 *  Note:        helper function
'''
def get_examples_attribute(var_index, attribute, data):
    new_dict = dict()
    for key, val in data.items():
        if key[var_index] == attribute:
            new_dict[key] = val
        if data[key] == [0, 0]:
            new_dict[key] = [0, 0]
    return new_dict
'''  get_examples_attribute  '''


''' Function:    decision_tree_learning
 *  Purpose:     creates a decision tree recursively
 *  Input args:  data<dictionary>, attributes<list>, parent_examples<dictionary>, i<int>
 *  Return val:  Tree-object
 *  Note:        i is used to set the depth of each node; based on teh algorithm described in the textbook
'''
def decision_tree_learning(data, attributes, parent_examples, i):
    if len(data) == 0:
        return plurality_value(parent_examples)
    check, classification = same_classification_check(data)
    if check:
        return classification
    if len(list(attributes)) == 0:
        return plurality_value(data)
    a = importance(data, attributes)[0][0]      # a = the random variable with the highest gain out of the data
    node = Node(a)    # each node will have a tuple with attribute of parent node and node with the next random variable
    node.set_depth(i)       # sets the depth of each node (used to print the tree)
    i += 1
    tree = Tree(node)
    index = index_of_var(a, data)
    attributes1 = get_attributes(index, data)       # attributes1 = random variables
    if attributes1 is None:         # if there are no random variables left to look at, return the plurality value
        return plurality_value(data)
    for attribute in attributes1:
        exs = get_examples_attribute(index, attribute, data)
        temp = list(attributes)
        try:
            temp.remove(a)      # used to look at the data without a given random variable
        except Exception:
            pass
        variables = tuple(temp)
        subtree = decision_tree_learning(exs, variables, data, i)
        tree.get_root().add_child(subtree.get_root(), attribute)        # adds branch to the tree
    return tree
'''  decision_tree_learning  '''


''' Function:    in_data
 *  Purpose:     checks whether each attribute is in the given data
 *  Input args:  key<list>, variables<list>, data<dictionary>
 *  Return val:  result<list of booleans>
 *  Note:        helper function
'''
def in_data(key, variables, data):
    attributes = list()
    result = list()
    for i in range(len(variables)):
        attributes.append(get_attributes(i, data))
    for attribute in range(len(key)):
        for j in attributes:
            if key[attribute] in j:
                result.append(True)
    return result
'''  in_data  '''


''' Function:    test
 *  Purpose:     predicts whether a given key has "yes" or "no" as an output
 *  Input args:  key<list>, data<dictionary>
 *  Return val:  "yes" or "no"
'''
def test(key, data):
    variables = extract_variables(data)
    tree = decision_tree_learning(data, variables, 0, 0)
    node = (None, tree.get_root())
    check = in_data(key, variables, data)
    for i in range(len(check)):
        if check[i] is False:
            attributes = get_attributes(i, data)
            key[i] = attributes[0]              # sets an attribute to another attribute if it is not in the data
            break
    while True:
        copyy = node        # used to check whether we are stuck
        attribute_tuples = node[1].get_attributes()     # note that each attribute consists of the attribute of the
        for attribute in attribute_tuples:              # former random variable and the next node with a value as the
            if attribute[0] in key:                     # next random variable
                node = attribute
                break
        if node[1].get_value() == "yes":        # since there are also nodes for the "yes" and "no" outputs, we check
            return "yes"                        # whether it is such a node and return the value then
        elif node[1].get_value() == "no":
            return "no"
        if copyy == node:                   # handling of situations where we get stuck (such as having an attribute
            index = index_of_var(node[1].get_value(), data)     # that was not in the data set
            attributes = get_attributes(index, data)
            for attribute in range(len(attributes)):
                new_attribute = attributes[random.randrange(0, len(attributes))]        # chooses a new random attribute
                node[1].insert_attribute((new_attribute, node[1].get_attributes()[0][1]))
            if len(attributes) == 1 and attributes[0] == "yes":
                return "yes"
            elif len(attributes) == 1 and attributes[0] == "no":
                return "no"
            if node[0] is None:
                node = node[1].get_attributes()[0]
                print(node)
            if node[0] == "yes":
                return "yes"
            elif node[0] == "no":
                return "no"
'''  test  '''


''' Function:    pop_key
 *  Purpose:     takes out one line of the data set
 *  Input args:  key<list>, val<list>, data<dictionary>
 *  Return val:  data<dictionary>
 *  Note:        helper function; used to test accuracy
'''
def pop_key(key, val, data):
    if val == "yes":
        data[key][0] -= 1
    elif val == "no":
        data[key][1] -= 1
    if data[key] == [0, 0]:
        del data[key]
    return data
'''  pop_key  '''


''' Function:    accuracy_test
 *  Purpose:     tests the accuracy of a decision tree
 *  Input args:  data<dictionary>
 *  Return val:  None (prints how many it got correct)
'''
def accuracy_test(data):
    total = 0
    correct = 0
    for key in data.keys():
        copyy = copy.deepcopy(data)
        for i in range(data[key][0]):          # tests it for each "yes" value of a given key (if multiple values for
            temp = pop_key(key, "yes", copyy)  # the same key
            if test(key, temp) == "yes":
                correct += 1
            total += 1
        for j in range(data[key][1]):          # tests it for each "no" value of a given key
            temp = pop_key(key, "no", copyy)
            if test(key, temp) == "no":
                correct += 1
            total += 1
    print(correct, "out of", total, "correct")
'''  accuracy_test  '''


if __name__ == "__main__":
    main(sys.argv[:1])
