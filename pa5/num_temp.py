from cool_classes import *

def numTemp_gen(exp) :
    ret = 1
    if isinstance(exp, Attribute):
        if exp.initialization == True:
            ret = numTemp_gen(exp.exp)
        return ret
    elif isinstance(exp, Method):
        return ret 
    
    elif isinstance(exp, Internal):
        ret = 1
        return ret

    elif isinstance(exp, Let):
        temp_for_binding = len(exp.binding_list) 
        temp_for_exp = numTemp_gen(exp.exp)
        temp_list = [numTemp_gen(binding.value_exp) for binding in exp.binding_list if
            binding.initialization == True]
        if temp_list == []:
            temp_for_binding_exp = 1
        else:
            temp_for_binding_exp = max(temp_list)
        #print temp_for_exp
        #print temp_for_binding_exp
        #print temp_for_binding
        ret = max(temp_for_exp, temp_for_binding_exp) + temp_for_binding
        return ret

    elif isinstance(exp, Binding):
        return ret 

    elif isinstance(exp, String):
        return ret

    elif isinstance(exp, Integer):
        return ret

    elif isinstance(exp, IdentifierExp):
        return ret

    elif isinstance(exp, (Plus, Minus, Times, Divide, Le, Eq, Lt)):
        ret = max(numTemp_gen(exp.lhs), 1+numTemp_gen(exp.rhs))
        return ret

    elif isinstance(exp, (TrueExp, FalseExp)):
        return ret
    
    elif isinstance(exp, Assign):
        ret = numTemp_gen(exp.exp)
        return ret

    elif isinstance(exp, New):
        return ret

    elif isinstance(exp, If):
        ret = max(numTemp_gen(exp.predicate), numTemp_gen(exp.then_body),\
                numTemp_gen(exp.else_body))
        return ret

    elif isinstance(exp, Block):
        numTemp_list = [numTemp_gen(expr) for expr in exp.exp_list]
        if numTemp_list == []:
            return ret
        ret = max(numTemp_list)
        return ret

    elif isinstance(exp, While):
        ret = max(numTemp_gen(exp.predicate), 1 + numTemp_gen(exp.body))
        return ret

    elif isinstance(exp, Isvoid):
        ret = numTemp_gen(exp.exp)
        return ret

    elif isinstance(exp, Not):
        ret = numTemp_gen(exp.exp)
        return ret
    elif isinstance(exp, Negate):
        ret = 1 + numTemp_gen(exp.exp)
        return ret
    elif isinstance(exp, Dynamic_Dispatch):
        numTemp_list = [numTemp_gen(arg) for arg in exp.args]
        numTemp_list.append(numTemp_gen(exp.exp))
        if numTemp_list == []:
            return ret
        ret = max(numTemp_list)
        return ret

    elif isinstance(exp, Static_Dispatch):
        numTemp_list = [numTemp_gen(arg) for arg in exp.args]
        numTemp_list.append(numTemp_gen(exp.exp))
        if numTemp_list == []:
            return ret
        ret = max(numTemp_list)
        return ret

    elif isinstance(exp, Self_Dispatch):
        numTemp_list = [numTemp_gen(arg) for arg in exp.args]
        if numTemp_list == []:
            return ret
        ret = max(numTemp_list)
        return ret

    elif isinstance(exp, Case):
        numTemp_list = [numTemp_gen(case_ele) for case_ele in exp.element_list]
        numTemp_list.append(numTemp_gen(exp.exp))
        if numTemp_list == []:
            ret = numTemp_gen(exp.exp)
            return ret 
        ret = max(numTemp_list)
        return ret

    elif isinstance(exp, Case_element):
        ret = 1 + numTemp_gen(exp.body_exp)
        return ret

    elif exp == None:
        #print "unhandled temp Expression"
        return ret

    else:
        return ret
