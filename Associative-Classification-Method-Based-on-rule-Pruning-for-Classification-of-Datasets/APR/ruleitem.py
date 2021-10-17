import sys
sys.path.append('/.../CBA-master')
import ruleitem

class RuleItem:

    def __init__(self, condition_set, label, data):
        self.class_label = label
        self.condition_set = condition_set
        temp1 ,temp2 = self._find_count_for_support(data)
        self.support_count = temp2
        self.condition_support = temp1
        len_dataset = len(data)
        confidence = self._confidence()
        self.confidence = confidence
        support = self._support(len_dataset)
        self.support = support

    def _find_count_for_support(self, records):
        initial_value = 0
        support_count = condition_support = initial_value
        flag = 1
        increment = 1
        for case in records:
            
            for index in self.condition_set:
                if self.condition_set[index] == case[index]:
                    pass
                else:
                    flag = 0
                    break

            if(flag != 1):
                pass
            else:

                condition_support = condition_support + increment
                last_index = len(case) - 1

                if self.class_label != case[last_index]:
                    pass
                else:
                    support_count += 1

            flag = 1
        return condition_support, support_count

    def _support(self, size_of_records):
        rule_support_count = self.support_count
        size_of_dataset = size_of_records
        result = rule_support_count / size_of_dataset
        return result

    def _confidence(self):
        condition_support_count = self.condition_support
        rule_support_count = self.support_count
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
        for element in self.condition_set:
            cond_set_output += '(' + str(element) + ', ' + str(self.condition_set[element]) + '), '
        element = cond_set_output[:temp_index]
        cond_set_output = cond_set_output[:temp_index]
        cond_set_output = cond_set_output + square_bracket_close
        label = str(self.class_label)
        print(cond_set_output + arrow + '(class_label, ' + label+ closing_bracket)



