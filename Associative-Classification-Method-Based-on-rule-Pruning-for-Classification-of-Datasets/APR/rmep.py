
import math


class Block:
    def __init__(self, data):
        self.data = data
        self.size = len(data)
        classes = set([x[1] for x in data])     # get distinct class labels in this table
        self.number_of_classes = len(set(classes))
        self.entropy = calculate_entropy(data)


# Calculate the entropy of dataset
# parameter data: the data table to be used
def calculate_entropy(data):
    size = 0
    for elem in data:
        size+=1
    classes_list = []
    for y in data:
        classes_list.append(y[1])
    classes_set = set(classes_list)
    class_count = {}
    for class_label in classes_set:
        class_count[class_label] = 0
    for case in data:
        class_count[case[1]] += 1      # count the number of data case of each class
    entropy = 0
    for c in classes_set:
        numerator = class_count[c]
        denominator = size
        p = numerator / denominator
        term_to_be_subtracted = p*math.log2(p)
        entropy -= term_to_be_subtracted         # calculate information entropy by its formula, where the base is 2
    return entropy



def entropy_gain(original_block, left_block, right_block):
    original_entropy = original_block.entropy
    entropy_to_be_subtracted = ((left_block.size / original_block.size) * left_block.entropy + (right_block.size / original_block.size) * right_block.entropy)
    gain = original_entropy - entropy_to_be_subtracted
            
    return gain

def calculate_delta(original_block, left_block, right_block):
    delta = math.log2(math.pow(3, original_block.number_of_classes) - 2) - \
            (original_block.number_of_classes * original_block.entropy -
             left_block.number_of_classes * left_block.entropy -
             right_block.number_of_classes * right_block.entropy)
    return delta

def calculate_gain_sup(original_block, delta):
    return math.log2(original_block.size - 1) / original_block.size + delta / original_block.size



def min_gain(original_block, left_block, right_block):

    delta = calculate_delta(original_block, left_block, right_block)
    gain_sup = calculate_gain_sup(original_block, delta)
    return gain_sup


# Identify the best acceptable value to split block
# block: a block of dataset
# Return value: a list of (boundary, entropy gain, left block, right block) or
def split(block):
    
    candidates = []
    for y in block.data:
        candidates.append(y[0])
    candidates = list(set(candidates))          # get different values in table
    candidates.sort()                           # sort ascending
    candidates = candidates[1:]                 # discard smallest, because by definition no value is smaller

    final_boundary_list = []       # wall is a list storing final boundary
    i=0
    while i<len(candidates):
        value = candidates[i]
        # split by value into 2 groups, below & above
        data_on_the_left = []
        data_on_the_right = []
        for data_case in block.data:
            if data_case[0] >= value:
                data_on_the_right.append(data_case)
            else:
                data_on_the_left.append(data_case)

        left_block = Block(data_on_the_left)
        right_block = Block(data_on_the_right)

        gain = entropy_gain(block, left_block, right_block)
        threshold = min_gain(block, left_block, right_block)

        # minimum threshold is met, the value is an acceptable candidate
        if gain<threshold:
            pass
        else:
            final_boundary_list.append([value, gain, left_block, right_block])
        i+=1
    
    if not final_boundary_list:
        return None

    else:    # has candidate
        final_boundary_list.sort(key=lambda wall: wall[1], reverse=True)   # sort descending by "gain"
        return final_boundary_list[0]      # return best candidate with max entropy gain
    


# Top-down recursive partition of a data block, append boundary into "walls"
# block: a data block
def partition(block):
    walls_array = []

    # inner recursive function, accumulate the partitioning values
    # sub_block: just a data block
    def recursive_split(sub_block):
        is_returned = split(sub_block)
        if not is_returned:
            return 
        else:
            walls_array.append(is_returned[0])
            recursive_split(is_returned[2])
            recursive_split(is_returned[3])
        

    recursive_split(block)      # call inner function
    walls_array.sort()                # sort boundaries descending
    return walls_array


# just for test
if __name__ == '__main__':
    import random

    test_data = []
    for i in range(100):
        test_data.append([random.random(), random.choice(range(0, 2))])
        test_data.append([random.random() + 1, random.choice(range(2, 4))])
        test_data.append([random.random() + 2, random.choice(range(4, 6))])
        test_data.append([random.random() + 3, random.choice(range(6, 8))])

    test_block = Block(test_data)
    test_walls = partition(test_block)
    print(test_walls)
