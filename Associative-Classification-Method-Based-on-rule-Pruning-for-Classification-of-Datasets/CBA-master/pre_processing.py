
import rmep



def get_mode(arr):
    mode = []
    arr_appear = {}
    for elem in arr:
        arr_appear[elem] = arr.count(elem)  
    if max(arr_appear.values()) != 1:       
        for key in arr_appear.keys():    
            if arr_appear[key] != max(arr_appear.values()):
                continue
            elif arr_appear[key] == max(arr_appear.values()):
                mode.append(key)
    else:
        return      
    return mode[0]  



def fill_missing_values(data, column_no):
    size=0
    for elem in data:
        size+=1
    column_data = []
    for y in data:
        column_data.append(y[column_no])
    question_mark = '?'
    while True:
        if question_mark in column_data:
            column_data.remove('?')
        else:
            break
    mode = get_mode(column_data)
    i=0
    while i<size:
        if data[i][column_no] != question_mark:
            continue
        else:
            data[i][column_no] = mode
        i+=1
    return data



def get_discretization_data(data_column, class_column):
    size=0
    for elem in data_column:
        size+=1
    result_list = []
    i=0
    while i<size:
        result_list.append([data_column[i], class_column[i]])
        i+=1
    return result_list



def replace_numerical(data, column_no, walls):
    size=0
    for elem in data:
        size+=1
    num_split_point=0
    for wall in walls:
        num_split_point+=1
    i=0
    while i<size:
        if data[i][column_no] > walls[num_split_point - 1]:
            data[i][column_no] = num_split_point + 1
            i+=1
            continue
        j=0
        while j<num_split_point:
            if data[i][column_no] > walls[j]:
                pass
            else:
                data[i][column_no] = j + 1
                break
            j+=1
        i+=1
    return data



def replace_categorical(data, column_no):
    size=0
    for elem in data:
        size+=1
    classes_list = []
    for y in data:
        classes_list.append(y[column_no])
    classes = set(classes_list)
    classes_no = {}
    for label in classes:
        classes_no[label] = 0
    j = 1
    for label in classes:
        classes_no[label] = j
        j += 1
    i=0
    while i<size:
        data[i][column_no] = classes_no[data[i][column_no]]
        i+=1
    return data, classes_no



def discard(data, discard_list):
    size=0
    for elem in data:
        size+=1
    length=0
    for elem in data[0]:
        length+=1
    data_result = []
    i=0
    while i<size:
        data_result.append([])
        j=0
        while j<length:
            if j in discard_list:
                continue
            else:
                data_result[i].append(data[i][j])
            j+=1
        i+=1
    return data_result



def pre_process(data, attribute, value_type):
    number_of_columns = 0
    for elem in data[0]:
        number_of_columns+=1
    size=0
    for elem in data:
        size+=1
    class_column = []
    for y in data:
        class_column.append(y[-1])
    discarded_values_list = []
    question_mark = "?"
    i=0
    while i < number_of_columns - 1:
        data_column = []
        for y in data:
            data_column.append(y[i])
        
        numerator = data_column.count(question_mark)
        denominator = size
        ratio_of_missing_values = numerator / denominator
        if ratio_of_missing_values>0 and ratio_of_missing_values<=0.5:
            data = fill_missing_values(data, i)
            data_column = []
            for y in data:
                data_column.append(y[i])
        elif ratio_of_missing_values > 0.5:
            discarded_values_list.append(i)
            continue
       
            

        

        if value_type[i] == 'categorical':
            returned_argument_1, returned_argument_2 = replace_categorical(data, i)
            data = returned_argument_1
            classes_no = returned_argument_2
            print(attribute[i] + ":", classes_no)   
        elif value_type[i] == 'numerical':
            discretization_data = get_discretization_data(data_column, class_column)
            block = rmep.Block(discretization_data)
            walls = rmep.partition(block)
            if len(walls)>0:
                pass
            elif len(walls)<0:
                pass
            else:
                minimum_value = min(data_column)
                maximum_value = max(data_column)
                first_value = maximum_value
                second_value = minimum_value
                num = 3
                step = (first_value - second_value) / num
                first_append = minimum_value+step
                second_append = minimum_value + 2 * step
                walls.append(first_append)
                walls.append(second_append)
            print(attribute[i] + ":", walls)        
            data = replace_numerical(data, i, walls)
        
        i+=1

    
    if len(discarded_values_list) > 0:
        data = discard(data, discarded_values_list)
        print("discard:", discarded_values_list)            
    return data



