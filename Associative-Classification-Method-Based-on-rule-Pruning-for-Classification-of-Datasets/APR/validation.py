
from read import read
from pre_processing import pre_process
from apr_rg import rule_generator
from apr_cb_m1 import classifier_builder_m1
from apr_cb_m1 import is_satisfy
from functools import cmp_to_key
import time
import random
    
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



def find_accuracy(apr,test):
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

def cross_validate_m1_without_prune(data_path, scheme_path,class_first=False, minsup=0.1, minconf=0.6):
    data, attributes, value_type = read(data_path, scheme_path)
    if class_first:
        for i in range(len(data)):
            a=data[i].pop(0)
            data[i].append(a)
        a=attributes.pop(0)
        attributes.append(a)
        b=value_type.pop(0)
        value_type.append(b)

    random.shuffle(data)
    dataset = pre_process(data, attributes, value_type)

    block_size = int(len(dataset) / 10)
    split_point = [k * block_size for k in range(0, 10)]
    split_point.append(len(dataset))

    apr_rg_total_runtime = 0
    apr_cb_total_runtime = 0
    total_car_number = 0
    total_classifier_rule_num = 0
    error_total_rate = 0
    acc_total=0
    for k in range(len(split_point)-1):
        print("\nRound %d:" % k)

        training_dataset = dataset[:split_point[k]] + dataset[split_point[k+1]:]
        test_dataset = dataset[split_point[k]:split_point[k+1]]

        start_time = time.time()
        cars = rule_generator(training_dataset, minsup, minconf)
        end_time = time.time()
        apr_rg_runtime = end_time - start_time
        apr_rg_total_runtime += apr_rg_runtime

        arr=list(cars.rules_list)
        max=-1

        for i in range(len(arr)):
            if len(arr[i].condition_set)>max:
                max=len(arr[i].condition_set)
        T=[[] for i in range(max)]
        for i in range(len(arr)):
            T[len(arr[i].condition_set)-1].append(arr[i])
        u=[]
        for i in range(len(T)):
            T[i]=sort_dict(T[i])

            for j in T[i]:
                u.append(j)
        apr_rg_total_runtime += apr_rg_runtime

        start_time = time.time()
        print("-------------------------------------------------------------------------")
        classifier= classifier_builder_m1(training_dataset,minsup,len(training_dataset),u)


        end_time = time.time()
        apr_cb_runtime = (end_time - start_time)/10
        apr_cb_total_runtime += apr_cb_runtime

        classifier.print()
        res=find_accuracy(classifier,test_dataset)
        acc_total+=res

        total_car_number += len(cars.rules)
        total_classifier_rule_num += len(classifier.rule_list)
        print()
        print("-------------------------------------------------------------------------")
        print()
        print("No. of rules in classifier of apr: " ,len(classifier.rule_list))
        print()
        print("No. of CARs : ",len(cars.rules_list))
        print()
        print("accuracy : ",(res*100),'%')
        print()
        print("apr-RG's run time : " ,str(round(apr_rg_runtime, 5)),'seconds')
        print()
        print("apr-CB run time :  " ,str(round(apr_cb_runtime, 5)),'seconds')
        print()
        print("-------------------------------------------------------------------------")
    print()
    print('Average Statistics')
    print()
    print("-------------------------------------------------------------------------")
    print()
    print("Average No. of CARs : ",(total_car_number / 10))
    print()
    print("Average No. of rules in classifier of apr: " ,(total_classifier_rule_num / 10))
    print()
    print("Average APR's accuracy :",(acc_total/10*100),'%')
    print()
    print("Average apr-RG's run time : " ,str(round((apr_rg_total_runtime / 10), 5)),'seconds')
    print()
    print("Average apr-CB run time :  " , str(round((apr_cb_total_runtime / 10), 5)),'seconds')
    print()

    print("-------------------------------------------------------------------------")



if __name__ == "__main__":
    # using the relative path, all data sets are stored in datasets directory
    test_data_path = 'Dataset/iris.data'
    test_scheme_path = 'Dataset/iris.names'

    # just choose one mode to experiment by removing one line comment and running
    min_support=0.01
    min_conf=0.5
    is_class_first=False
    cross_validate_m1_without_prune(test_data_path, test_scheme_path,is_class_first,min_support,min_conf)
