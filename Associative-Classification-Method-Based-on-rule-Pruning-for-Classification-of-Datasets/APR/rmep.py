
import math

class Block:
    def __init__(self, data):
        self.data = data
        self.size = len(data)
        classes = set([x[1] for x in data])     
        self.number_of_classes = len(set(classes))
        self.entropy = calculate_entropy(data)

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
        class_count[case[1]] += 1     
    entropy = 0
    for c in classes_set:
        numerator = class_count[c]
        denominator = size
        p = numerator / denominator
        term_to_be_subtracted = p*math.log2(p)
        entropy -= term_to_be_subtracted         
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



def split(block):
    
    candidates = []
    for y in block.data:
        candidates.append(y[0])
    candidates = list(set(candidates))          
    candidates.sort()                          
    candidates = candidates[1:]                
    final_boundary_list = []       
    i=0
    while i<len(candidates):
        value = candidates[i]
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

        if gain<threshold:
            pass
        else:
            final_boundary_list.append([value, gain, left_block, right_block])
        i+=1
    
    if not final_boundary_list:
        return 

    else:   
        final_boundary_list.sort(key=lambda wall: wall[1], reverse=True)   
        return final_boundary_list[0]      
    


def partition(block):
    walls_array = []
    def recursive_split(sub_block):
        is_returned = split(sub_block)
        if not is_returned:
            return 
        else:
            walls_array.append(is_returned[0])
            recursive_split(is_returned[2])
            recursive_split(is_returned[3])
    recursive_split(block)      
    walls_array.sort()                
    return walls_array


