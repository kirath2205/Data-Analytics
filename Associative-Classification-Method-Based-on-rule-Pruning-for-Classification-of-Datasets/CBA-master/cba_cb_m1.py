
import cba_rg
from functools import cmp_to_key
import sys
import time

def is_satisfy(datacase, rule):

    for item in rule.cond_set:
        if datacase[item] != rule.cond_set[item]:
            return None
    if datacase[-1] == rule.class_label:
        return True
    else:
        return False

class Classifier:

    def __init__(self):
        self.rule_list = list()
        self.default_class = None
        self._error_list = list()
        self._default_class_list = list()

    # inserting a rule into rule_list
    def insert(self, rule, dataset):
        # appending the rule to rule list
        self.rule_list.append(rule)

        # setting a default class for current rule
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

        # calculating the total number of errors of C
        self._calc_error(dataset)

    # calculate the total error
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
        # finding the rule with lowest error rate
        index = self._error_list.index(min(self._error_list))
        self.rule_list = self.rule_list[:(index+1)]
        self._error_list = None

        # assigning the default class
        self.default_class = self._default_class_list[index]
        self._default_class_list = None

    # print the default class and rules
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
        
        j = k = i = 0

        while j < len(right) and i < len(left):

            b = right[j]
            a = left[i]

            conf_a = a.confidence
            conf_b = b.confidence
            conf_diff = conf_a - conf_b
            
            if conf_diff > 0:
                arr[k] = left[i]
                i += 1

            elif conf_diff == 0:
                sup_a = a.support
                sup_b = b.support
                sup_diff = sup_a - sup_b

                if sup_diff > 0:
                    arr[k] = left[i]
                    i += 1

                elif sup_diff == 0:
                    if len(a.cond_set) > len(b.cond_set):
                        arr[k] = left[i]
                        i += 1
                        
                    else:
                        arr[k] = right[j]
                        j += 1
                else:
                    arr[k] = right[j]
                    j += 1
            else:
                arr[k] = right[j]
                j += 1

            k += 1

        while i < len(left):
            arr[k] = left[i]
            k += 1
            i += 1

        while j < len(right):
            arr[k] = right[j]
            k += 1
            j += 1
    else:
        pass

# def rule_compare(a, b):
#     if a.confidence < b.confidence:
#         return 1
#     elif a.confidence < b.confidence:
#         if a.support < b.support:
#             return 1
#         elif a.support == b.support:
#             if len(a.cond_set) < len(b.cond_set):
#                 return 1
#             else:
#                 return -1
#         else:
#             return -1
#     else:
#         return -1

# following the pseudo code given in KDD paper
def classifier_builder_m1(cars, dataset):
    
    # creating the classifier
    classifier = Classifier()
    rule_list = list(cars.rules)

    # sorting rules based on the “>” condition
    SortRuleList(rule_list)

    # rule_list.sort(key=cmp_to_key(rule_compare))
    
    cars_list=rule_list

    for rule in cars_list:
        # temporary list to store rule IDs
        temp = []
        marked = False
        for i in range(len(dataset)):
            # checking if the dataset row satisfies the current rule
            is_satisfy_value = is_satisfy(dataset[i], rule)
            if is_satisfy_value is not None:
                temp.append(i)
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

    # dropping all rules after the rule with the lowest error value
    classifier.drop_rules()
    return classifier


if __name__ == '__main__':
    dataset = [[1, 1, 1,2], [1, 1, 2,2], [2, 1, 2,1], [1, 2, 2,1], [3, 1, 1,1],
               [1, 1, 1,2], [2, 2, 3,1], [1, 2, 3,1], [1, 2, 2,1], [1, 2, 2,2]]
    minsup = 0.2
    minconf = 0.6
    cars = cba_rg.rule_generator(dataset, minsup, minconf)
    classifier = classifier_builder_m1(cars, dataset)
    classifier.print()

    print()
    dataset = [[1, 1, 1,2], [1, 1, 2,2], [2, 1, 2,1], [1, 2, 2,1], [3, 1, 1,1],
               [1, 1, 1,2], [2, 2, 3,1], [1, 2, 3,1], [1, 2, 2,1], [1, 2, 2,2]]
    cars.prune_rules(dataset)
    cars.rules = cars.pruned_rules
    classifier = classifier_builder_m1(cars, dataset)
