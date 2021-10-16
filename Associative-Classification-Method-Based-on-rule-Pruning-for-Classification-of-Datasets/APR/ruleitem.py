import sys
sys.path.append('/.../CBA-master')
import ruleitem

class RuleItem:

    def __init__(self, cond_set, class_label, dataset):
        self.cond_set = cond_set
        self.class_label = class_label
        self.cond_sup_count, self.rule_sup_count = self._get_sup_count(dataset)
        self.support = self._get_support(len(dataset))
        self.confidence = self._get_confidence()

    def _get_sup_count(self, records):
        initial_value = 0
        rule_sup_count = cond_sup_count = initial_value
        flag = 1
        increment = 1
        for case in records:
            
            for index in self.cond_set:
                if self.cond_set[index] == case[index]:
                    pass
                else:
                    flag = 0
                    break

            if(flag != 1):
                pass
            else:

                cond_sup_count = cond_sup_count + increment
                last_index = len(case) - 1

                if self.class_label != case[last_index]:
                    pass
                else:
                    rule_sup_count += 1

            flag = 1
        return cond_sup_count, rule_sup_count

    def _get_support(self, size_of_records):
        rule_support_count = self.rule_sup_count
        size_of_dataset = size_of_records
        result = rule_support_count / size_of_dataset
        return result

    def _get_confidence(self):
        condition_support_count = self.cond_sup_count
        rule_support_count = self.rule_sup_count
        initial_value = 0
        if(condition_support_count == 0):
            return 0
            
        answer = rule_support_count / condition_support_count

        if(condition_support_count == initial_value):
            return initial_value
            
        elif(condition_support_count != initial_value):
            return answer

    # print out rule
    def print_rule(self):
        temp_index = -2
        cond_set_output = '['
        square_bracket_close = ']'
        arrow = ' -> '
        closing_bracket = ')'
        for element in self.cond_set:
            cond_set_output += '(' + str(element) + ', ' + str(self.cond_set[element]) + '), '
        element = cond_set_output[:temp_index]
        cond_set_output = cond_set_output[:temp_index]
        cond_set_output = cond_set_output + square_bracket_close
        label = str(self.class_label)
        print(cond_set_output + arrow + '(class_label, ' + label+ closing_bracket)



# just for test
if __name__ == '__main__':
    cond_set = {0: 1, 1: 1}
    class_label = 1
    dataset = [[1, 1, 1], [1, 1, 1], [1, 2, 1], [2, 2, 1], [2, 2, 1],
               [2, 2, 0], [2, 3, 0], [2, 3, 0], [1, 1, 0], [3, 2, 0]]
    rule_item = ruleitem.RuleItem(cond_set, class_label, dataset)
    rule_item.print()
    rule_item.print_rule()
    print('Condition support count =', rule_item.cond_sup_count)   # should be 3
    print('rulesupCount =', rule_item.rule_sup_count)   # should be 2
    print('support =', rule_item.support)               # should be 0.2
    print('confidence =', rule_item.confidence)         # should be 0.667
