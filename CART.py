# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 16:09:14 2019

@author: Puranjay
"""


def test_split(index, value, dataset):
    """
    Function name: test_split
    This function splits the data into two halves on the basis of a given row
    Attributes: 
        index:index of the row under consideration through which the split is being made
        value: value of that row under consideration through which the split is being made
        dataset: the original dataset
    Return:
        left and right  tuples of the split
    
    """
    left, right = list(), list()
    for row in dataset:
        if row[index] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right
 
# Calculate the Gini index for a split dataset
def gini_index(groups, classes):
	"""
    Function_Name: gini_index
    will return the gini value for the split that we made
    Attributes:
        groups:A list with the two splits containing left and right values
        classes:Dependent variable values
    Returns:
        gini value for the split
    
    
    
    
    """
	n_instances = float(sum([len(group) for group in groups]))
	# refer to https://sefiks.com/2018/08/27/a-step-by-step-cart-decision-tree-example/ for formulae of gini
    
	gini = 0.0
	for group in groups:
		size = float(len(group))
		# avoid divide by zero
		if size == 0:
			continue
		score = 0.0
		# score the group based on the score for each class
		for class_val in classes:
			p = [row[-1] for row in group].count(class_val) / size
			score += p * p
		# weight the group score by its relative size
		gini += (1.0 - score) * (size / n_instances)
	return gini
 
# Select the best split point for a dataset
def get_split(dataset):
    """
    Function get_split():
        This split will call the above functions in a for loop for each row and then return the best split found at that node.
        Note: this is deciding the best data split for all the data just for the node under consideraton 
        It takes row of each attribute and then tries to split the data on the basis of that row and checks for the entropy or gini value.
        Please dont be lathargic and open the link i mentioned while understanding the code.
    Attributes:
        dataset: Actual dataset
    returns:
        a dictionary with the best split index,value at that index,the groups splitted
    """
    class_values = list(set(row[-1] for row in dataset))
    b_index, b_value, b_score, b_groups = 999, 999, 999, None
    for index in range(len(dataset[0])-1):
        for row in dataset:
            #print("value of index= ",index)
            groups = test_split(index, row[index], dataset)
            gini = gini_index(groups, class_values)
        if gini < b_score:
            b_index, b_value, b_score, b_groups = index, row[index], gini, groups
    return {'index':b_index, 'value':b_value, 'groups':b_groups}
 
# Create a terminal node value
def to_terminal(group):
    """
    Function name: to_terminal
    It returns the maximum from the count of outcomes ie if 0 are max then 0 or 1 if 1 are max
    
    
    """
    outcomes = [row[-1] for row in group]
   
    return max(set(outcomes), key=outcomes.count)
 
# Create child splits for a node or make terminal
def split(node, max_depth, min_size, depth):
    """
    Function_name:split()
    This function performs the actual split of nodes while recursively calling the above methods 
    and then each node split point is calculated and it is splitted.
    This function also checks for termination conditions which are:
        Maximum Tree Depth. This is the maximum number of nodes from the root node of the tree.
        Once a maximum depth of the tree is met, we must stop splitting adding new nodes.
        Deeper trees are more complex and are more likely to overfit the training data.
        
        Minimum Node Records. This is the minimum number of training patterns that a given node is responsible for.
        Once at or below this minimum, we must stop splitting and adding new nodes. 
        Nodes that account for too few training patterns are expected to be too specific and 
        are likely to overfit the training data.
        
        Third approach is when the dependent variables are uniform in the split then we already have the answer.If you dont understand this that means you didnt open the url.
        
        STEPS:
        1. Firstly, the two groups of data split by the node are extracted for use and deleted from the node. As we work on these groups 
           the node no longer requires access to these data.
        2. Next, we check if either left or right group of rows is empty and if so we create a terminal node using what records we do have.
        3. We then check if we have reached our maximum depth and if so we create a terminal node.
        4. We then process the left child, creating a terminal node if the group of rows is too small, 
           otherwise creating and adding the left node in a depth first fashion until the bottom of the tree is reached on this branch.
        5. The right side is then processed in the same manner, as we rise back up the constructed tree to the root.
    Arguments:
        node: node under consideration
        max_depth: max depth the tree must traverse to
        min_size: min no of rows  a child node must have in order to exist
        depth:current depth of the tree
        
    
    
    
    
    
    
    
    """
    #print("Loading ........")
    left, right = node['groups']
    del(node['groups'])
	# check for a no split
    if not left or not right:
        node['left'] = node['right'] = to_terminal(left + right)
        print("Nodes contain similar values")
        return
	# check for max depth
    if depth >= max_depth:
        node['left'], node['right'] = to_terminal(left), to_terminal(right)
        print("Node reached max depth")
        return
	# process left child
    if len(left) <= min_size:
        node['left'] = to_terminal(left)
        print("node left :",node['left']," Reached its min size")
    else:
        node['left'] = get_split(left)
        split(node['left'], max_depth, min_size, depth+1)
	# process right child
    if len(right) <= min_size:
        node['right'] = to_terminal(right)
        print("node right :",node['right']," Reached its min size")

    else:
        node['right'] = get_split(right)
        split(node['right'], max_depth, min_size, depth+1)
    #print("Loading ....")
 
# Build a decision tree
def build_tree(train, max_depth, min_size):
   """
   Function_Name: build_tree
   This function calls the get_split and split for the first time that is on the root
   Attributes:
       train: train dataset
       max_depth: maximum depth 
       min_size: min no of rows for node to exist
    Returns:
         root: first node of the tree
   
   
   
    
   """
   root = get_split(train)
   print(root)
   split(root, max_depth, min_size, 1)
   return root
 
# Print a decision tree
def print_tree(node, depth=0):
    # prints the tree
	if isinstance(node, dict):
		print('%s[X%d < %.3f]' % ((depth*' ', (node['index']+1), node['value'])))
		print_tree(node['left'], depth+1)
		print_tree(node['right'], depth+1)
        
	else:
		print('%s[%s]' % ((depth*' ', node)))
 
"""dataset = [[2.771244718,1.784783929,0],
	[1.728571309,1.169761413,0],
	[3.678319846,2.81281357,0],
	[3.961043357,2.61995032,0],
	[2.999208922,2.209014212,0],
	[7.497545867,3.162953546,1],
	[9.00220326,3.339047188,1],
	[7.444542326,0.476683375,1],
	[10.12493903,3.234550982,1],
	[6.642287351,3.319983761,1]]
"""
def call_cart(dataset):
    tree = build_tree(dataset, 500, 1)
    #print_tree(tree)
    for row in dataset:
        prediction = predict(tree, row)
        #print('Expected=%d, Got=%d' % (row[-1], prediction))
    return tree
"""
Method name:predict(node,row)
Usage: used for prediction of rows which are sent to the made tree
Parameters: 
    node: The tree which has been made
    row:the row from train data to be predicted


"""
def predict(node, row):
	if row[node['index']] < node['value']:
		if isinstance(node['left'], dict):
			return predict(node['left'], row)
		else:
			return node['left']
	else:
		if isinstance(node['right'], dict):
			return predict(node['right'], row)
		else:
			return node['right']
#tree=call_cart(dataset)