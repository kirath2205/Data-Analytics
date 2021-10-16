import ruleitem
import sys
import apr_cb_m1

class FrequentRuleitems:
    """
    A set of frequent k-ruleitems, just using set.
    """
    def __init__(self):
        self.frequent_ruleitems_set = set()

    # get size of set
    def get_size(self):
        counter=0
        for element in self.frequent_ruleitems_set:
            counter+=1
        return counter

    # add a new ruleitem into set
    def add(self, new_item):
        for element in self.frequent_ruleitems_set:
            if(element.class_label == new_item.class_label and element.cond_set == new_item.cond_set):
                return
            else:
                pass
        self.frequent_ruleitems_set.add(new_item)

    # append set of ruleitems
    def append(self, sets):
        for item in sets.frequent_ruleitems:
            self.add(item)

    # print out all frequent ruleitems
    def print(self):
        for item in self.frequent_ruleitems_set:
            item.print()


class Car:
    """
    Class Association Rules (Car). If some ruleitems has the same condset, the ruleitem with the highest confidence is
    chosen as the Possible Rule (PR). If there're more than one ruleitem with the same highest confidence, we randomly
    select one ruleitem.
    """
    def __init__(self):
        self.rules = set()
        self.rules_list=[]
        self.pruned_rules = set()

    # print out all rules
    def print_rule(self):
        for item in self.rules:
            item.print_rule()

    # print out all pruned rules
    def print_pruned_rule(self):
        for item in self.pruned_rules:
            item.print_rule()

    # add a new rule (frequent & accurate), save the ruleitem with the highest confidence when having the same condset
    def _add(self, rule_item, minsup, minconf):
        if rule_item.support >= minsup and rule_item.confidence >= minconf:
            if rule_item in self.rules:
                return
            for item in self.rules:
                if item.cond_set == rule_item.cond_set and item.confidence < rule_item.confidence:
                    # print("---",item.cond_set)
                    self.rules.remove(item)
                    self.rules.add(rule_item)

                    self.rules_list.remove(item)
                    self.rules_list.append(rule_item)
                    return
                elif item.cond_set == rule_item.cond_set and item.confidence >= rule_item.confidence:
                    return
            self.rules.add(rule_item)
            self.rules_list.append(rule_item)

    # convert frequent ruleitems into car
    def gen_rules(self, frequent_ruleitems, minimum_support, minimum_confidence):
        for item in frequent_ruleitems.frequent_ruleitems_set:
            self._add(item, minimum_support, minimum_confidence)

    # prune rules
    def prune_rules(self, dataset):
        for rule1 in self.rules:
            pruned_rule = prune(rule1, dataset)
            for rule2 in self.pruned_rules:
                if(rule2.cond_set == pruned_rule.cond_set and rule2.class_label == pruned_rule.class_label):
                    return
                else:
                    pass
            self.pruned_rules.add(pruned_rule)

    # union new car into rules list
    def append(self, car, minsup, minconf):
        for item in car.rules:
            self._add(item, minsup, minconf)


# try to prune rule
def prune(rule, dataset):
    
    minimum_rule_error = sys.maxsize
    pruned_rule = rule

    # prune rule recursively
    def find_prune_rule(current_rule):
        nonlocal minimum_rule_error
        nonlocal pruned_rule

        # calculate how many errors the rule r make in the dataset
        def errors_of_rule(rule):
            
            number_of_errors = 0
            for single_item in dataset:
                if apr_cb_m1.is_satisfy(single_item, rule):
                    continue
                else:
                    number_of_errors += 1
            return number_of_errors

        rule_error = errors_of_rule(current_rule)
        if rule_error >= minimum_rule_error:
            pass
        else:
            min_rule_error = rule_error
            pruned_rule = current_rule
        this_rule_cond_set = list(current_rule.cond_set)
        if len(this_rule_cond_set) < 2:
            pass
        else:
            for attribute in this_rule_cond_set:
                temporary_condition_set = dict(current_rule.cond_set)
                temporary_condition_set.pop(attribute)
                temporary_rule = ruleitem.RuleItem(temporary_condition_set, current_rule.class_label, dataset)
                temp_rule_error = errors_of_rule(temporary_rule)
                if temp_rule_error > min_rule_error:
                    pass
                else:
                    min_rule_error = temp_rule_error
                    pruned_rule = temporary_rule
                    if len(temporary_condition_set) < 2:
                        pass
                    else:
                        find_prune_rule(temporary_rule)

    find_prune_rule(rule)
    return pruned_rule


# invoked by candidate_gen, join two items to generate candidate
def join(first_item, second_item, dataset):
    if first_item.class_label==second_item.class_label:
        pass
    elif first_item.class_label != second_item.class_label:
        return None
   
    first_category = set(first_item.cond_set)
    second_category = set(second_item.cond_set)
    if first_category != second_category:
        pass
    else:
        return None
    intersection_of_first_category_and_second_category = first_category & second_category
    for element in intersection_of_first_category_and_second_category:
        if first_item.cond_set[element] == second_item.cond_set[element]:
            continue
        else:
            return None
    final_category = first_category | second_category
    new_condition_set = dict()
    for elem in final_category:
        if elem not in first_category:
            new_condition_set[elem] = second_item.cond_set[elem]
        else:
            new_condition_set[elem] = first_item.cond_set[elem]
    new_ruleitem = ruleitem.RuleItem(new_condition_set, first_item.class_label, dataset)
    return new_ruleitem


# similar to Apriori-gen in algorithm Apriori
def candidate_gen(recurrent_ruleitems, data):
    returned_frequent_ruleitems = FrequentRuleitems()

    for rule_item1 in recurrent_ruleitems.frequent_ruleitems_set:

        for rule_item2 in recurrent_ruleitems.frequent_ruleitems_set:
            new_rule_item = join(rule_item1, rule_item2, data)

            if new_rule_item!=None:
                returned_frequent_ruleitems.add(new_rule_item)

                if returned_frequent_ruleitems.get_size() >= 1000:      # not allow to store more than 1000 ruleitems
                    return returned_frequent_ruleitems
                    
                else:
                    pass

            else:
                continue

    return returned_frequent_ruleitems


# main method, implementation of CBA-RG algorithm
def rule_generator(dataset, minimum_support, minimum_confidence):
    frequent_rule_items = FrequentRuleitems()
    classification_association_rule = Car()
    i=0
    class_labels_list = []
    while i<len(dataset):
        class_labels_list.append(dataset[i][-1])
        i+=1
    class_labels_set = set(class_labels_list)
    col=0
    while col<len(dataset[0])-1:
        values_list = []
        for elem in dataset:
            values_list.append(elem[col])
        distinct_values_set = set(values_list)
        for val in distinct_values_set:
            condition_set = {col: val}
            for class_label in class_labels_set:
                one_rule_item = ruleitem.RuleItem(condition_set, class_label, dataset)
                if one_rule_item.support < minimum_support:
                    continue
                else:
                    frequent_rule_items.add(one_rule_item)
        col+=1
    classification_association_rule.gen_rules(frequent_rule_items, minimum_support, minimum_confidence)
    classification_association_rules = classification_association_rule

    end_classification_association_rules_no = 0
    present_classification_association_rules_no = len(classification_association_rules.rules)
    while frequent_rule_items.get_size()>0 and present_classification_association_rules_no<=2000 and (present_classification_association_rules_no-end_classification_association_rules_no)>=10:
        candidate_Rule = candidate_gen(frequent_rule_items, dataset)
        frequent_rule_items = FrequentRuleitems()
        classification_association_rule = Car()
        for element in candidate_Rule.frequent_ruleitems_set:
            if element.support<minimum_support:
                continue
            else:
                frequent_rule_items.add(element)
        classification_association_rule.gen_rules(frequent_rule_items, minimum_support, minimum_confidence)
        classification_association_rules.append(classification_association_rule, minimum_support, minimum_confidence)
        end_classification_association_rules_no = present_classification_association_rules_no
        present_classification_association_rules_no = len(classification_association_rule.rules)
    
    return classification_association_rules


# just for test
if __name__ == "__main__":
    dataset = [[1, 1, 1], [1, 1, 1], [1, 2, 1], [2, 2, 1], [2, 2, 1],
               [2, 2, 0], [2, 3, 0], [2, 3, 0], [1, 1, 0], [3, 2, 0]]
    minsup = 0.15
    minconf = 0.6
    cars = rule_generator(dataset, minsup, minconf)

    print("CARs:")
    cars.print_rule()

    print("prCARs:")
    cars.prune_rules(dataset)
    cars.print_pruned_rule()


    dataset = [[1, 1, 1,2], [1, 1, 2,2], [2, 1, 2,1], [1, 2, 2,1], [3, 1, 1,1],
               [1, 1, 1,2], [2, 2, 3,1], [1, 2, 3,1], [1, 2, 2,1], [1, 2, 2,2]]
    minsup = 0.2
    minconf = 0.65
    cars = rule_generator(dataset, minsup, minconf)

    print("CARs:")
    cars.print_rule()


    print("prCARs:")
    cars.prune_rules(dataset)
    cars.print_pruned_rule()
