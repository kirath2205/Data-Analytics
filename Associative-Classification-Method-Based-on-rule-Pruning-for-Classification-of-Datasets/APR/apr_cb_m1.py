

from functools import cmp_to_key

def is_satisfy(records, item_rule):

    for item in item_rule.condition_set:
        if records[item] == item_rule.condition_set[item]:
            continue
        return 
    last_index = len(records)-1
    if records[last_index] != item_rule.class_label:
        return False
    return True

def cmp_method(item_1, item_2):
    len1=len(item_1.condition_set)
    len2=len(item_2.condition_set)
    if item_1.confidence < item_2.confidence:  
        return 1
    elif item_1.confidence == item_2.confidence:
        if (item_1.support < item_2.support):      
            return 1
        elif(item_1.support < item_2.support):
            return -1
        else:
            if len1 < len2: 
                return -1
            elif(len1>len2):
                return 1
            return 0
    return -1


class Classifier:
    def __init__(self):
        self.rule_list = list()
        self.default_class = None
        self._error_list = list()
        self._default_class_list = list()

    def insert(self, rule):
        self.rule_list.append(rule)

    # just print out all selected rules and default class in our classifier
    def print(self):
        for rule in self.rule_list:
            rule.print_rule()
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

def sort1(car):

    rule_list = list(car)
    rule_list.sort(key=cmp_to_key(cmp_method))
    return rule_list

def classifier_builder_m1(dataset,min_support,length,cars_list):
    classifier = Classifier()
    SortRuleList(cars_list)
    
    while cars_list:
        temp=[]
        rule=cars_list.pop(0)
        flag=False
        len_data = len(dataset)
        for i in range(len_data):
            is_satisfy_value=is_satisfy(dataset[i],rule)
            if is_satisfy_value is not None:
                temp.append(i)
                if is_satisfy_value:
                    flag=True

        if flag:
            temp_dataset=list(dataset)
            for index in temp:
                temp_dataset[index]=[]
            while [] in temp_dataset:
                temp_dataset.remove([])
            dataset=temp_dataset
            classifier.insert(rule)

            temp=list(cars_list)
            for i in range(len(cars_list)):
                cars_list[i].condition_support, cars_list[i].support_count = cars_list[i]._find_count_for_support(dataset)
                cars_list[i].confidenc , cars_list[i].support = cars_list[i]._confidence() , cars_list[i]._support(length)
                if cars_list[i].support<min_support:
                    temp[i]=[]

            while [] in temp:
                temp.remove([])
            cars_list=temp

        SortRuleList(cars_list)


    if len(dataset)>0:
        classes=set([x[-1] for x in dataset])
        temp=[x[-1] for x in dataset]
        counter=0
        choice=None
        for k in classes:
            s=temp.count(k)
            if s>counter:
                counter , choice =s , k
        classifier.default_class=choice
    else:
        classes=set([x.class_label for x in classifier.rule_list])
        temp=[x.class_label for x in classifier.rule_list]
        counter=0
        choice=None
        for k in classes:
            s=temp.count(k)
            if s>counter:
                counter,choice=s,k
        classifier.default_class=choice

    return classifier

def cmp_dict(array_1,array_2):
    partition_1=list(array_1.condition_set.keys())
    partition_2=list(array_2.condition_set.keys())
    for i in range(len(partition_1)):
        if(partition_1[i] == partition_2[i]):
            return 1
        elif(partition_1[i]>partition_2[i]):
            return 1
        return -1

def sort_dict(elements):
    rule_list = list(elements)
    rule_list.sort(key=cmp_to_key(cmp_dict))
    return rule_list


