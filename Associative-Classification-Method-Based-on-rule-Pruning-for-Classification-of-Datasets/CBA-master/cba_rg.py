import ruleitem


class FrequentRuleitems:
    """
    A set of frequent k-ruleitems, just using set.
    """
    def __init__(self):
        self.frequent_ruleitems_set = set()

    # get size of set
    def get_size(self):
        return len(self.frequent_ruleitems_set)

    # add a new ruleitem into set
    def add(self, rule_item):
        is_existed = False
        for item in self.frequent_ruleitems_set:
            if item.class_label == rule_item.class_label:
                if item.condition_set == rule_item.condition_set:
                    is_existed = True
                    break
        if not is_existed:
            self.frequent_ruleitems_set.add(rule_item)

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
                if item.condition_set == rule_item.condition_set and item.confidence < rule_item.confidence:
                    # print("---",item.condition_set)
                    self.rules.remove(item)
                    self.rules.add(rule_item)
                    return
                elif item.condition_set == rule_item.condition_set and item.confidence >= rule_item.confidence:
                    return
            self.rules.add(rule_item)

    # convert frequent ruleitems into car
    def gen_rules(self, frequent_ruleitems, minsup, minconf):
        for item in frequent_ruleitems.frequent_ruleitems_set:
            self._add(item, minsup, minconf)

    # prune rules
    def prune_rules(self, dataset):
        for rule in self.rules:
            pruned_rule = prune(rule, dataset)
            # print("pruned rule:",pruned_rule.condition_set)
            is_existed = False
            for rule in self.pruned_rules:
                if rule.class_label == pruned_rule.class_label:
                    if rule.condition_set == pruned_rule.condition_set:
                        is_existed = True
                        break

            if not is_existed:
                self.pruned_rules.add(pruned_rule)

    # union new car into rules list
    def append(self, car, minsup, minconf):
        for item in car.rules:
            self._add(item, minsup, minconf)


# try to prune rule
def prune(rule, dataset):
    import sys
    min_rule_error = sys.maxsize
    pruned_rule = rule

    # prune rule recursively
    def find_prune_rule(this_rule):
        nonlocal min_rule_error
        nonlocal pruned_rule

        # calculate how many errors the rule r make in the dataset
        def errors_of_rule(r):
            import cba_cb_m1

            errors_number = 0
            for case in dataset:
                if cba_cb_m1.is_satisfy(case, r) == False:
                    errors_number += 1
            return errors_number

        rule_error = errors_of_rule(this_rule)
        if rule_error < min_rule_error:
            min_rule_error = rule_error
            pruned_rule = this_rule
        this_rule_cond_set = list(this_rule.condition_set)
        if len(this_rule_cond_set) >= 2:
            for attribute in this_rule_cond_set:
                temp_cond_set = dict(this_rule.condition_set)
                temp_cond_set.pop(attribute)
                temp_rule = ruleitem.RuleItem(temp_cond_set, this_rule.class_label, dataset)
                temp_rule_error = errors_of_rule(temp_rule)
                if temp_rule_error <= min_rule_error:
                    min_rule_error = temp_rule_error
                    pruned_rule = temp_rule
                    if len(temp_cond_set) >= 2:
                        find_prune_rule(temp_rule)

    find_prune_rule(rule)
    return pruned_rule


# invoked by candidate_gen, join two items to generate candidate
def join(first_item, second_item, dataset):
    if first_item.class_label==second_item.class_label:
        pass
    elif first_item.class_label != second_item.class_label:
        return None
   
    first_category = set(first_item.condition_set)
    second_category = set(second_item.condition_set)
    if first_category != second_category:
        pass
    else:
        return None
    intersection_of_first_category_and_second_category = first_category & second_category
    for element in intersection_of_first_category_and_second_category:
        if first_item.condition_set[element] == second_item.condition_set[element]:
            continue
        else:
            return None
    final_category = first_category | second_category
    new_condition_set = dict()
    for elem in final_category:
        if elem not in first_category:
            new_condition_set[elem] = second_item.condition_set[elem]
        else:
            new_condition_set[elem] = first_item.condition_set[elem]
    new_ruleitem = ruleitem.RuleItem(new_condition_set, first_item.class_label, dataset)
    return new_ruleitem

# similar to Apriori-gen in algorithm Apriori
def candidate_gen(frequent_ruleitems, dataset):
    returned_frequent_ruleitems = FrequentRuleitems()
    threshold_number_rule_items = 1000
    for item_one in frequent_ruleitems.frequent_ruleitems_set:
        for item_two in frequent_ruleitems.frequent_ruleitems_set:
            new_ruleitem = join(item_one, item_two, dataset)
            if new_ruleitem:
                returned_frequent_ruleitems.add(new_ruleitem)
                if returned_frequent_ruleitems.get_size() >= threshold_number_rule_items:      # not allow to store more than 1000 ruleitems
                    return returned_frequent_ruleitems
    return returned_frequent_ruleitems


# main method, implementation of CBA-RG algorithm
def rule_generator(dataset, minimum_support, minimum_confidence):
    frequent_ruleitems = FrequentRuleitems()
    classification_association_rule = Car()

    # get large 1-ruleitems and generate rules
    i=0
    class_labels_list = []
    while i<len(dataset):
        class_labels_list.append(dataset[i][-1])
        i+=1
    class_labels_set = set(class_labels_list)
    col=0
    while col<len(dataset[0])-1:
        distinct_values_set = set([x[col] for x in dataset])
        #print("distinct values:",distinct_value)
        for value in distinct_values_set:
            condition_set = {col: value}
            for number_of_classes in class_labels_set:
                rule_item = ruleitem.RuleItem(condition_set, number_of_classes, dataset)
                if rule_item.support >= minimum_support:
                    frequent_ruleitems.add(rule_item)
        col+=1

    classification_association_rule.gen_rules(frequent_ruleitems, minimum_support, minimum_confidence)
    cars = classification_association_rule

    last_cars_number = 0
    current_cars_number = len(cars.rules)

    while frequent_ruleitems.get_size() > 0 and current_cars_number <= 1000 :
        #print("******")
        candidate = candidate_gen(frequent_ruleitems, dataset)
        frequent_ruleitems = FrequentRuleitems()
        car = Car()
        for item in candidate.frequent_ruleitems_set:
            if item.support >= minimum_support:
                frequent_ruleitems.add(item)
        car.gen_rules(frequent_ruleitems, minimum_support, minimum_confidence)
        cars.append(car, minimum_support, minimum_confidence)
        #cars.prune_rules(dataset)
        last_cars_number = current_cars_number
        current_cars_number = len(cars.rules)

    return cars



