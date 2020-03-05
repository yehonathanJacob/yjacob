# Loan-Application-Risk-Quality-Prediction
This program builds a decision tree for categorical attributes and 2-class classification tasks. It builds a tree from a training dataset and classifies instances of the test set with the learned decision tree. 
Important methods and member for the class `DecisionTreeImpl`:

    1. private DecTreeNode root; 
    2. DecisionTreeImpl ( DataSet train ); 
    3. public String classify ( Instance instance ); 
    4. public void rootInfoGain ( DataSet train ); 
    5. public void printAccuracy (DataSet test)

`DecisionTreeImpl(DataSet train)` builds a decision tree using the training set train. 
`classify(Instance instance)` predicts the given instance’s class label using the previously-built decision tree. 
`rootInfoGain(DataSet train)` prints the information gain (one in each line) for all the attributes at the root based on the training set, train. The root of your tree should be stored in the member root that has been declared for you. RootInfoGain will only be called at the root node. It will not be called at other nodes when building your decision tree. 
`printAccuracy(DataSet test)` prints the classification accuracy for the instances in the test set, test, using the previously-learned decision tree.

## __Dataset__

A risk loan dataset, https://bigml.com/dashboard/dataset/577bdcd477920c1ba40009a6, is to be used to __predict the risk quality of a loan application__. There are 1,000 noisy instances using 10 categorical attributes, divided into three files called `examples1.txt`, `examples2.txt` and `examples3.txt`. Each instance is classified as either good (class label `G`) or bad (class label `B`), so this is a 2-class classification problem. Assume other datasets used for testing will also be 2-class classification tasks with categorical attributes. The 10 attributes and their possible values are shown in the table below:

 Attributes                     | Possible Values
 ------------------------------ | -----------------
 A1: Checking status 	          | x(no checking) n(x<0, negative) b(0<=x<200, bad) g(200<=x, good)
 A2: Saving status 	            | n(no known savings) b(x<100) m(100<=x<500) g(500<=x<=1000) w(1000<=x)
 A3: Credit history 	          | a(all paid) c(critical/other existing credit) d(delayed previously) e(existing paid) n(no credits) 
 A4: Housing 	r(rent)           | o(own) f(free)
 A5: Job                        |	h(high qualified/self-employed/management) s(skilled) n(unemployed) u(unskilled) 
 A6: Property magnitude         |	c(car) l(life insurance) r(real estate) n(no known property) 
 A7: Number of dependents       |	1, 2 
 A8: Number of existing credits |	1, 2, 3, 4 
 A9: Own telephones or not 	    | y(yes), n(no) 
 A10: Foreign workers or not    |	y(yes), n(no) 

In each file, there will be a header that gives information about the dataset; an example header and the first example in the dataset is shown below. First, there will be several lines starting with // that provide some description and comments about the dataset. Next, the line starting with %% will list all the class labels. Each line starting with ## will give the name of one attribute and all its possible values. We have written the dataset loading part for you according to this header, so do NOT change it. Following the header are the examples in the dataset, one example per line. The first example is shown below and corresponds to the feature vector (A1=x, A2=n, A3=e, A4=r, A5=h, A6=l, A7=1, A8=1, A9=y, A10=y) and its class is G. The class label for each instance is stored as a string in class `DataSet`.

    // Description of the data set 
    %%,G,B 
    ##,A1,x,n,b,g 
    ##,A2,n,b,m,g,w 
    ##,A3,a,c,d,e,n 
    ##,A4,r,o,f 
    ##,A5,h,s,n,u 
    ##,A6,c,l,r,n 
    ##,A7,1,2 
    ##,A8,1,2,3,4 
    ##,A9,y,n 
    ##,A10,y,n 
    x,n,e,r,h,l,1,1,y,y,G 
    …

## Implementation Details
### Data Types
There are four data types, called `Instance`, `DataSet`, `DecTreeNode` and `DecisionTreeImpl`. Their data members and methods are all commented in the provided code. `DecTreeNode` is a class with several fields, including class label, attribute, etc. For a node that is a leaf, set its attribute value to be null and its terminal Boolean to True.

### Building the Tree
The `DecisionTreeImpl(DataSet train)` builds a decision tree using the training data. The root of the final decision tree is assigned to the `root` class member. When calculating entropy, if the probability 𝑝𝑝 is zero, define 𝑝𝑝 log2 𝑝𝑝 = 0.  

Use information gain to decide which attribute is the best at a non-leaf node. If ties occur when determining the majority class, choose the one with the smallest index in `List<String> labels`. If ties occur when choosing the best attribute, choose the one with the smallest index in `List<String> attributes`. 

### Classification
`public String classify(Instance instance)` takes an instance (also called an example) as its input and computes the classification output (as a string) using the previously-built decision tree.

### Printing and Information Gain at the Root
```Java
public void rootInfoGain(DataSet train) 
```
For each attribute print the output one line at a time: first the name of the attribute and then the information gain achieved by selecting that attribute at the root. The output order of the attributes and associated information gain values _must_ be the _same_ as the order that the attributes appear in the training set’s header. Print your results with 5 decimal places using

```Java
System.out.format("%.5f\n", arg)  
```  
```Java
public void printAccuracy(DataSet test) 
```
Print out the accuracy with 5 decimal places.

### Testing
Using training and testing datasets with the command line format: 

    java <modeFlag> <trainFile> <testFile>

where `trainFile` and `testFile` are the names of the training and testing datasets, respectively. `modeFlag` is an integer from 0 to 3, controlling what the program will output. The requirements for each value of modeFlag are described in the following table:

    0: Print the information gain for each attribute at the root node based on the training set 
    1: Create a decision tree from the training set and print the tree 
    2: Create a decision tree from the training set and print the classification for each example in the test set 
    3: Create a decision tree from the training set and print the accuracy of the classification for the test set 

Here is an example command line: 

    java 0 examples1.txt examples2.txt  

The format of `rootInfoGain` (`modeFlag == 0`) looks like

    A1 0.11111 
    A2 0.11111 
    …
    A10 0.11111  

The format of  `printAccuracy` (`modeFlag == 3`) looks like

    0.12345  

As an example of what the output should be for each of the four modes, there has provided the correct outputs in `Sample Outputs` when using `examples1.txt` as the training set and `examples2.txt` as the test set.
