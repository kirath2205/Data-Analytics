
import sys


def is_satisfy(datacase, rule):

    for item in rule.condition_set:
        if datacase[item] == rule.condition_set[item]:
            continue
        return 
    last_index = len(datacase)-1
    if datacase[last_index] != rule.class_label:
        return False
    return True

class Classifier:

    def __init__(self):
        self.rule_list = list()
        self.default_class = None
        self._error_list = list()
        self._default_class_list = list()

  
    def insert(self, rule, dataset):
        
        self.rule_list.append(rule)

        
        col = []
        for row in dataset:
            col.append(row[-1])
        labels = set(col)
        max_count = 0
        current_default = None
        for l in labels:
            label_count = col.count(l)
            if label_count >= max_count:
                current_default = l
        self._default_class_list.append(current_default)

        
        self._calc_error(dataset)

  
    def _calc_error(self, dataset):
        if len(dataset) <= 0:
            self._error_list.append(sys.maxsize)
            return
        else:
            error_number = 0

            for case in dataset:
                is_cover = False
                for rule in self.rule_list:
                    if is_satisfy(case, rule):
                        is_cover = True
                        break
                if not is_cover:
                    error_number += 1

            class_column = [x[-1] for x in dataset]
            error_number += len(class_column) - class_column.count(self._default_class_list[-1])
            self._error_list.append(error_number)


    def drop_rules(self):
       
        index = self._error_list.index(min(self._error_list))
        self.rule_list = self.rule_list[:(index+1)]
        self._error_list = None

        
        self.default_class = self._default_class_list[index]
        self._default_class_list = None

   
    def print(self):
        for r in self.rule_list:
            r.print_rule()
        print("default_class:", self.default_class)

def SortRuleList(arr):

    lenArr = len(arr)

    if lenArr > 1:

        mid = lenArr//2

        right = arr[mid:]
        left = arr[:mid]

        SortRuleList(right)
        SortRuleList(left)
        
        index2 = index3 = index1 = 0

        while index2 < len(right) and index1 < len(left):

            a , b = left[index1] , right[index2]

            confidence_a = a.confidence
            confidence_b = b.confidence
            confidence_difference = confidence_a - confidence_b
            
            if confidence_difference > 0:
                index1 += 1
                arr[index3] = left[index1-1]
                

            elif confidence_difference == 0:
                support_a = a.support
                support_b = b.support
                support_difference = support_a - support_b

                if support_difference > 0:
                    arr[index3] = left[index1]
                    index1 += 1

                elif support_difference == 0:
                    if len(a.condition_set) > len(b.condition_set):
                        index1 += 1
                        arr[index3] = left[index1-1]
                        
                    else:
                        index2 += 1
                        arr[index3] = right[index2-1]

                else:
                    index2 += 1
                    arr[index3] = right[index2-1]
                    
            else:
                index2 += 1
                arr[index3] = right[index2-1]
                

            index3 += 1

        while index1 < len(left):
            index3 += 1
            index1 += 1
            arr[index3-1] = left[index1-1]
            

        while index2 < len(right):
            index3 += 1
            index2 += 1
            arr[index3-1] = right[index2-1]
    else:
        pass




def classifier_builder_m1(cars, dataset):
    
    
    classifier = Classifier()
    rule_list = list(cars.rules)

   
    SortRuleList(rule_list)

    
    cars_list=rule_list

    for rule in cars_list:
       
        temp = []
        marked = False
        for index1 in range(len(dataset)):
            
            is_satisfy_value = is_satisfy(dataset[index1], rule)
            if is_satisfy_value is not None:
                temp.append(index1)
                if is_satisfy_value:
                    marked = True
        if marked:
            temp_dataset = list(dataset)
            for index in temp:
                temp_dataset[index] = []
            while [] in temp_dataset:
                temp_dataset.remove([])
            dataset = temp_dataset
            classifier.insert(rule, dataset)

    classifier.drop_rules()
    return classifier

