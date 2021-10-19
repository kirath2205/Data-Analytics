from read import read
from pre_processing import pre_process
from cba_rg import rule_generator
from cba_cb_m1 import classifier_builder_m1
import time
import random


def acc(apr,test):
    temp=[]
    actual=[x[-1] for x in test]
    count=0
    for i in range(len(test)):
        flag1=True
        for j in range(len(apr.rule_list)):
            flag=True
            for item in apr.rule_list[j].condition_set:
                if test[i][item]!=apr.rule_list[j].condition_set[item]:
                    flag=False
                    break
            if flag:
                temp.append(apr.rule_list[j].class_label)
                if temp[-1]==actual[i]:
                    count+=1
                flag1=False
                break

        if flag1:
            temp.append(apr.default_class)
            if temp[-1]==actual[i]:
                count+=1

    res=count/len(test)
    return res

# 10-fold cross-validations on CBA
def cross_validate(data_path, scheme_path,class_first=False, minimum_support=0.01, minimum_confidence=0.5):
    data, attributes, value_type = read(data_path, scheme_path)
    if not class_first:
        pass
    else:
        i=0
        while i<len(data):
            a=data[i].pop(0)
            data[i].append(a)
            i+=1
        popped_attribute=attributes.pop(0)
        attributes.append(popped_attribute)
        popped_value=value_type.pop(0)
        value_type.append(popped_value)
        # print(data[0])
    random.shuffle(data)
    dataset = pre_process(data, attributes, value_type)

    block_size = len(dataset) // 10
    split_point = []
    for i in range(10):
        split_point.append(i*block_size)
    split_point.append(len(dataset))

    cba_rg_total_runtime = 0
    cba_cb_total_runtime = 0
    total_car_number = 0
    total_classifier_rule_num = 0
    acc_total=0
    k=0
    while k<len(split_point)-1:
        print("\nRound %d:" % k)
        print("\n")

        training_dataset = dataset[:split_point[k]] + dataset[split_point[k+1]:]
        test_dataset = dataset[split_point[k]:split_point[k+1]]

        start_time = time.time()
        cars = rule_generator(training_dataset, minimum_support, minimum_confidence)
        end_time = time.time()
        cba_rg_runtime = end_time - start_time
        cba_rg_total_runtime += cba_rg_runtime

        start_time = time.time()
        classifier= classifier_builder_m1(cars, training_dataset)
        end_time = time.time()
        cba_cb_runtime = end_time - start_time
        cba_cb_total_runtime += cba_cb_runtime

        classifier.print()
        res=acc(classifier,test_dataset)
        acc_total+=res

        total_car_number += len(cars.rules)
        total_classifier_rule_num += len(classifier.rule_list)
        print()
        print("********************************************************************")
        print("Accuracy :",(res*100))
       
        print("Number of CARs : ",len(cars.rules))
        
        print("CBA-RG's run time : s" ,cba_rg_runtime)
        
        print("CBA-CB M1's run time :  s" ,cba_cb_runtime)
        
        print("No. of rules in classifier of CBA-CB: " ,len(classifier.rule_list))
        print("********************************************************************")
        print()
        k+=1

    print("Average CBA accuracy :",(acc_total/10*100))
   
    print("Average Number of CARs : ",(total_car_number / 10))
    
    print("Average CBA-RG's run time: " ,(cba_rg_total_runtime / 10))
    
    print("Average CBA-CB run time:  " ,(cba_cb_total_runtime / 10))
    
    print("Average No. of rules in classifier of CBA-CB: " ,(total_classifier_rule_num / 10))

    print()

# test entry goes here
if __name__ == "__main__":
    dataset = "iris"

    test_data_path = f'Dataset/{dataset}.data'
    test_scheme_path = f'Dataset/{dataset}.names'

    min_support=0.01
    min_conf=0.5
    is_class_first=False
    cross_validate(test_data_path, test_scheme_path,is_class_first,min_support,min_conf)
