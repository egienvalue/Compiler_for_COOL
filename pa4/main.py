#!/usr/bin/python

import sys
import pprint
import copy
import os
import traceback

ast_lines = []
class_list = []
ast = []
class_map_print_flag = 0
#type_filename = "my_" + (sys.argv[1])[:-4] + "-type"
type_filename =  (sys.argv[1])[:-4] + "-type"
fout = open(type_filename, 'w')
class_map = {"Object":[], "Int":[], "String":[], "Bool":[], "IO":[]}
imp_map = \
{"Object":[("Object","abort"),("Object","copy"),("Object","type_name")],\
   "Int" :[("Object","abort"),("Object","copy"),("Object","type_name")],\
"String" :[("Object","abort"),("Object","copy"),("Object","type_name"), \
           ("String","concat"),("String","length"),("String", "substr")],\
   "Bool":[("Object","abort"),("Object","copy"),("Object","type_name")],\
     "IO":[("Object","abort"),("Object","copy"),("Object","type_name"),\
           ("IO","in_int"),("IO","in_string"),("IO","out_int"),("IO","out_string")]
}
parent_map = {"Int":"Object", "String":"Object", "Bool":"Object"}
# define multiple classes
class Expression(object):
    global class_map_print_flag
    line_num = None
    exp_type = "No_TYPE"

    def s(self):
        ret = str(self.line_num) + "\n"
        if (class_map_print_flag == 1):
            ret += str(self.exp_type) + "\n"
        return ret

    def __init__(self, _line_num):
        self.line_num = _line_num

    def __repr__(self):
        return str(self)

class Integer(Expression):
    int_val = None

    def __init__(self, _line_num, _int_val):
        Expression.__init__(self, _line_num)
        self.int_val = _int_val
        self.exp_type = "Int"

    def __str__(self):
        ret = self.s()
        ret += "integer\n" 
        ret += str(self.int_val)+ "\n"
        return ret
    def __repr__(self):
        ret = self.s()
        ret += "integer\n" 
        ret += str(self.int_val)+ "\n"
        return ret

class String(Expression):
    str_val = None

    def __init__(self, _line_num, _str_val):
        Expression.__init__(self, _line_num)
        self.str_val = _str_val
        self.exp_type = "String"

    def __str__(self):
        ret = self.s()
        ret += "string\n" 
        ret += str(self.str_val) + "\n"
        return ret
    def __repr__(self):
        ret = self.s()
        ret += "string\n" 
        ret += str(self.str_val) + "\n"
        return ret


class TrueExp(Expression):
    def __init__(self, _line_num):
        Expression.__init__(self, _line_num)
        self.exp_type = "Bool"

    def __str__(self):
        ret = self.s()
        ret += "true\n"
        return ret

class FalseExp(Expression):
    def __init__(self, _line_num):
        Expression.__init__(self, _line_num)
        self.exp_type = "Bool"

    def __str__(self):
        ret = self.s()
        ret += "false\n"
        return ret

class IdentifierExp(Expression):
    ident = None
    def __init__(self, _line_num, _ident):
        Expression.__init__(self,_line_num)
        self.ident = _ident

    def __str__(self):
        ret = self.s()
        ret += "identifier\n" 
        ret += str(self.ident)
        return ret

class New(Expression):
    ident = None

    def __init__(self, _line_num, _ident):
        Expression.__init__(self, _line_num)
        self.ident = _ident
        self.exp_type = _ident.ident

    def __str__(self):
        ret = self.s()
        ret += "new\n"
        ret += str(self.ident)
        return ret

class Assign(Expression):
    ident = None
    exp = None

    def __init__(self, _line_num, _ident, _exp):
        Expression.__init__(self, _line_num)
        self.ident = _ident
        self.exp = _exp

    def __str__(self):
        ret = self.s()
        ret += "assign\n"
        ret += str(self.ident)
        ret += str(self.exp)

        return ret

# edit by Jun
class Let(Expression):
    binding_list = []
    exp = None

    def __init__(self, _line_num, _binding_list, _exp):
        Expression.__init__(self, _line_num)
        self.binding_list = _binding_list
        self.exp = _exp

    def __str__(self):
        ret = self.s()
        ret += "let\n"
        ret += str(len(self.binding_list)) + "\n"
        for binding in self.binding_list :
            ret += str(binding)
        ret += str(self.exp)
        return ret

# edit by Jun
class Binding(Expression):
    var_ident = None
    type_ident = None
    initialization = None
    value_exp = None

    def __init__(self, _var_ident, _type_ident, _initialization, _value_exp):
        self.var_ident = _var_ident
        self.type_ident = _type_ident
        self.initialization = _initialization
        self.value_exp = _value_exp
    
    def __str__(self):
        if self.initialization:
            ret = "let_binding_init\n"
        else :
            ret = "let_binding_no_init\n"
        ret += str(self.var_ident)
        ret += str(self.type_ident)
        if self.initialization:
            ret += str(self.value_exp)
        return ret

# edit by Jun
class Case(Expression):
    exp = None
    element_list = []
    
    def __init__(self, _line_num, _exp, _element_list):
        Expression.__init__(self, _line_num)
        self.exp = _exp
        self.element_list = _element_list

    def __str__(self):
        ret = self.s()
        ret += "case\n"
        ret += str(self.exp)
        ret += str(len(self.element_list)) + "\n"
        for element in self.element_list:
            ret += str(element)
        return ret

# edit by Jun
class Case_element(Expression):
    var_ident = None
    type_ident = None
    body_exp = None

    def __init__(self, _var_ident, _type_ident, _body_exp):
        self.var_ident = _var_ident
        self.type_ident = _type_ident
        self.body_exp = _body_exp
    
    def __str__(self):
        ret = str(self.var_ident)
        ret += str(self.type_ident)
        ret += str(self.body_exp)
        return ret

class Dynamic_Dispatch(Expression):
    exp = None
    method_ident = None
    args = None

    def __init__(self, _line_num, _exp, _method_ident, _args):
        Expression.__init__(self, _line_num)

        self.exp = _exp
        self.method_ident = _method_ident
        self.args = _args

    def __str__(self):
        ret = self.s()
        ret += "dynamic_dispatch\n"
        ret += str(self.exp)
        ret += str(self.method_ident)
        ret += str(len(self.args)) + "\n"
    	for arg in self.args:
	        ret += str(arg)
        return ret

class Static_Dispatch(Expression):
    exp = None
    type_ident = None
    method_ident = None
    args = None

    def __init__(self, _line_num, _exp, _type_ident, _method_ident, _args):
        Expression.__init__(self, _line_num)
        self.exp = _exp
        self.type_ident = _type_ident
        self.method_ident = _method_ident
        self.args = _args

    def __str__(self):
        ret = self.s()
        ret += "static_dispatch\n"
        ret += str(self.exp)
        ret += str(self.type_ident)
        ret += str(self.method_ident)
        ret += str(len(self.args)) + "\n"
        for arg in self.args:
            ret += str(arg)

        return ret

class Self_Dispatch(Expression):
    method_ident = None
    args = None

    def __init__(self, _line_num, _method_ident, _args):
        Expression.__init__(self, _line_num)
        self.method_ident = _method_ident
        self.args = _args

    def __str__(self):
        ret = self.s()
        ret += "self_dispatch\n"
        ret += str(self.method_ident)
        ret += str(len(self.args)) + "\n"
        for arg in self.args:
            ret += str(arg)
        return ret

class If(Expression):
    predicate = None
    then_body = None
    else_body = None

    def __init__ (self, _line_num, _predicate, _then_body, _else_body):
        Expression.__init__(self, _line_num)
        self.predicate = _predicate
        self.then_body = _then_body
        self.else_body = _else_body

    def __str__(self):
        ret = self.s()
        ret += "if\n"
        ret += str(self.predicate)
        ret += str(self.then_body)
        ret += str(self.else_body)

        return ret

class While(Expression):
    predicate = None
    body = None

    def __init__(self, _line_num, _predicate, _body):
        Expression.__init__(self, _line_num)
        self.predicate = _predicate
        self.body = _body

    def __str__(self):
        ret = self.s()
        ret += "while\n"
        ret += str(self.predicate)
        ret += str(self.body)

        return ret

class Block(Expression):
    exp_list = None
    def __init__(self, _line_num, _exp_list):
        Expression.__init__(self, _line_num)
        self.exp_list = _exp_list

    def __str__(self):
        ret = self.s()
        ret += "block\n"
        ret += str(len(self.exp_list)) + "\n"
        for exp in self.exp_list:
            ret += str(exp)

        return ret

class Isvoid(Expression):
    exp = None
    def __init__(self, _line_num, _exp):
        Expression.__init__(self, _line_num)
        self.exp = _exp

    def __str__(self):
        ret = self.s()
        ret += "isvoid\n"
        ret += str(self.exp)

        return ret

class Plus(Expression):
    lhs = None
    rhs = None

    def __init__(self, _line_num, _lhs, _rhs):
        Expression.__init__(self, _line_num)
        self.lhs = _lhs
        self.rhs = _rhs

    def __str__(self):
        ret = self.s()
        ret += "plus\n"
        ret += str(self.lhs)
        ret += str(self.rhs)

        return ret

class Minus(Expression):
    lhs = None
    rhs = None

    def __init__(self, _line_num, _lhs, _rhs):
        Expression.__init__(self, _line_num)
        self.lhs = _lhs
        self.rhs = _rhs

    def __str__(self):
        ret = self.s()
        ret += "minus\n"
        ret += str(self.lhs)
        ret += str(self.rhs)

        return ret

class Times(Expression):
    lhs = None
    rhs = None

    def __init__(self, _line_num, _lhs, _rhs):
        Expression.__init__(self, _line_num)
        self.lhs = _lhs
        self.rhs = _rhs

    def __str__(self):
        ret = self.s()
        ret += "times\n"
        ret += str(self.lhs)
        ret += str(self.rhs)

        return ret

class Divide(Expression):
    lhs = None
    rhs = None

    def __init__(self, _line_num, _lhs, _rhs):
        Expression.__init__(self, _line_num)
        self.lhs = _lhs
        self.rhs = _rhs

    def __str__(self):
        ret = self.s()
        ret += "divide\n"
        ret += str(self.lhs)
        ret += str(self.rhs)

        return ret

class Lt(Expression):
    lhs = None
    rhs = None

    def __init__(self, _line_num, _lhs, _rhs):
        Expression.__init__(self, _line_num)
        self.lhs = _lhs
        self.rhs = _rhs

    def __str__(self):
        ret = self.s()
        ret += "lt\n"
        ret += str(self.lhs)
        ret += str(self.rhs)

        return ret

class Le(Expression):
    lhs = None
    rhs = None

    def __init__(self, _line_num, _lhs, _rhs):
        Expression.__init__(self, _line_num)
        self.lhs = _lhs
        self.rhs = _rhs

    def __str__(self):
        ret = self.s()
        ret += "le\n"
        ret += str(self.lhs)
        ret += str(self.rhs)

        return ret

class Eq(Expression):
    lhs = None
    rhs = None

    def __init__(self, _line_num, _lhs, _rhs):
        Expression.__init__(self, _line_num)
        self.lhs = _lhs
        self.rhs = _rhs

    def __str__(self):
        ret = self.s()
        ret += "eq\n"
        ret += str(self.lhs)
        ret += str(self.rhs)

        return ret

class Not(Expression):
    exp = None

    def __init__(self, _line_num, _exp):
        Expression.__init__(self, _line_num)
        self.exp = _exp

    def __str__(self):
        ret = self.s()
        ret += "not\n"
        ret += str(self.exp)

        return ret

class Negate(Expression):
    exp = None

    def __init__(self, _line_num, _exp):
        Expression.__init__(self, _line_num)
        self.exp = _exp

    def __str__(self):
        ret = self.s()
        ret += "negate\n"
        ret += str(self.exp)

        return ret

class Formal(object):
    formal_name = None
    formal_type = None

    def __init__(self, _formal_name, _formal_type):
        self.formal_name = _formal_name
        self.formal_type = _formal_type

    def __str__(self):
        ret = str(self.formal_name)
        ret += str(self.formal_type)

        return ret

    def __repr__(self):
        return str(self)

class Attribute(object):
    attr_name = None
    attr_type = None
    initialization = None
    exp = None

    def __init__(self, _attr_name, _attr_type, _initialization, _exp):
        self.attr_name = _attr_name
        self.attr_type = _attr_type
        self.initialization = _initialization
        self.exp = _exp

    def __str__(self):
        ret = ""
        if self.initialization:
            ret += "attribute_init\n"
        else:
            ret += "attribute_no_init\n"

        ret += str(self.attr_name)
        ret += str(self.attr_type)

        if self.initialization:
            ret += str(self.exp)

        return ret

class Identifier(object):
    line_num = None
    ident = None
    def __init__(self, _line_num, _ident):
        self.line_num = _line_num
        self.ident = _ident

    def __str__(self):
        ret = str(self.line_num) + "\n" + str(self.ident) + "\n"
        return ret

    def __repr__(self):
        return str(self)

class Method(object):
    method_name = None
    formals = []
    method_type = None
    body_exp = None

    def __init__(self, _method_name, _formals, _method_type, _body_exp):
        self.method_name = _method_name
        self.formals = _formals
        self.method_type = _method_type
        self.body_exp = _body_exp

    def __str__(self):
        ret = "method\n"
        ret += str(self.method_name)
        ret += str(len(self.formals)) + "\n"
        for formal in self.formals:
            ret += str(formal)
        ret += str(self.method_type)
        ret += str(self.body_exp)

        return ret

    def __repr__(self):
        return str(self)

class Class(object):
    name_iden = None
    inherits_iden = None
    methods = []
    attributes = []
    features = []

    def __init__(self, _name_iden, _inherits_iden, _attributes, _methods,_features):
        self.name_iden = _name_iden
        self.inherits_iden = _inherits_iden
        self.attributes = _attributes
        self.methods = _methods
        self.features = _features

    def __str__(self):
        ret = str(self.name_iden)
        if self.inherits_iden != None:
            ret += "inherits\n" + str(self.inherits_iden)
        else:
            ret += "no_inherits\n"
        ret += str(len(self.features)) + "\n"
        for feature in self.features:
            ret += str(feature)

        return ret

    def __repr__(self):
        return str(self)


# print section
def get_line():
    global ast_lines
    if ast_lines == []:
        return
    return ast_lines.pop(0)

def read_identifier():
    line_no = get_line()
    ident_name = get_line()

    return Identifier(line_no, ident_name)

def read_formal():
    formal_name = read_identifier()
    formal_type = read_identifier()

    return Formal(formal_name, formal_type)

def read_binding():
    binding_kind = get_line()
    if binding_kind == "let_binding_init" :
        binding_var_ident = read_identifier()
        binding_type_ident = read_identifier()
        binding_value_exp = read_exp()
        return Binding(binding_var_ident,binding_type_ident, True, \
                binding_value_exp)
    elif binding_kind == "let_binding_no_init":
        binding_var_ident = read_identifier()
        binding_type_ident = read_identifier() 
        return Binding(binding_var_ident,binding_type_ident,False, None)

def read_case_elem():
    case_elem_var = read_identifier()
    case_elem_type = read_identifier()
    case_elem_body = read_exp()
    return Case_element(case_elem_var,case_elem_type,case_elem_body)

def read_exp():
    line_number = get_line()
    exp_name = get_line()

    if exp_name == 'assign':
        assignee = read_identifier()
        rhs = read_exp()
        return Assign(line_number, assignee, rhs)

# edit by Jun
    elif exp_name == 'let':
        num_bindings = int(get_line())
        binding_list = []
        for i in range(num_bindings):
            binding_list.append(read_binding())
        let_body = read_exp()
        return Let(line_number, binding_list, let_body)
      
# edit by Jun
    elif exp_name == 'case':
        case_exp = read_exp()
        num_case_elem = int(get_line())
        case_elem_list = []
        for i in range(num_case_elem):
           case_elem_list.append(read_case_elem())
        return Case(line_number, case_exp, case_elem_list)


    elif exp_name == 'dynamic_dispatch':
        obj_name = read_exp()
        method_name = read_identifier()
        num_args = int(get_line())
        args = []
        for i in range(num_args):
            args.append(read_exp())

        return Dynamic_Dispatch(line_number, obj_name, method_name, args)

    elif exp_name == 'static_dispatch':
        obj_name = read_exp()
        type_name = read_identifier()
        method_name = read_identifier()
        num_args = int(get_line())
        args = []
        for i in range(num_args):
            args.append(read_exp())

        return Static_Dispatch(line_number, obj_name, type_name, method_name, args)

    elif exp_name == 'self_dispatch':
        method_name = read_identifier()
        num_args = int(get_line())
        args = []
        for i in range(num_args):
            args.append(read_exp())

        return Self_Dispatch(line_number, method_name, args)

    elif exp_name == 'if':
        predicate = read_exp()
        then_body = read_exp()
        else_body = read_exp()

        return  If(line_number, predicate, then_body, else_body)

    elif exp_name == 'while':
        predicate = read_exp()
        body_exp = read_exp()

        return While(line_number,predicate, body_exp)

    elif exp_name == 'block':
        num_exps = int(get_line())
        exps = []
        for i in range(num_exps):
            exps.append(read_exp())

        return Block(line_number, exps)

    elif exp_name == 'new':
        return New(line_number, read_identifier())


    elif exp_name == 'isvoid':
        return Isvoid(line_number, read_exp())

    elif exp_name == 'plus':
        return Plus(line_number, read_exp(), read_exp())

    elif exp_name == 'minus':
        return Minus(line_number, read_exp(), read_exp())

    elif exp_name == 'times':
        return Times(line_number, read_exp(), read_exp())

    elif exp_name == 'divide':
        return Divide(line_number, read_exp(), read_exp())

    elif exp_name == 'lt':
        return Lt(line_number, read_exp(), read_exp())

    elif exp_name == 'le':
        return Le(line_number, read_exp(), read_exp())

    elif exp_name == 'eq':
        return Eq(line_number, read_exp(), read_exp())

    elif exp_name == 'not':
        return Not(line_number, read_exp())

    elif exp_name == 'negate':
        return Negate(line_number, read_exp())

    elif exp_name == 'integer':
        return Integer(line_number, int(get_line()))

    elif exp_name == 'string':
        return String(line_number, get_line())

    elif exp_name == 'identifier':
        return IdentifierExp(line_number, read_identifier())

    elif exp_name == 'true':
        return TrueExp(line_number)

    elif exp_name =='false':
        return FalseExp(line_number)

def read_feature():
    feature_kind = get_line()

    if feature_kind == 'attribute_no_init':
        feature_name = read_identifier()
        feature_type = read_identifier()
        return Attribute(feature_name, feature_type, False, None)

    elif feature_kind == 'attribute_init':
        feature_name = read_identifier()
        feature_type = read_identifier()
        feature_init = read_exp()
        return Attribute(feature_name, feature_type, True, feature_init)

    elif feature_kind == 'method':
        feature_name = read_identifier()
        formal_list = []
        num_formals = int(get_line())
        for i in range(num_formals):
            formal_list.append(read_formal())
        feature_type = read_identifier()
        feature_body = read_exp()

        return Method(feature_name, formal_list, feature_type, feature_body)

def read_class():
    class_info = read_identifier()

    check_inherits = get_line()

    parent = None
    if check_inherits == 'inherits':
        parent = read_identifier()

    num_features = int(get_line())
    attr_list = []
    method_list = []

    feature_list = []

    for i in range(num_features):
        feature_list.append(read_feature())
    for feature in feature_list:
        if isinstance(feature, Attribute):
            attr_list.append(feature)
        elif isinstance(feature,Method):
            method_list.append(feature)
    return Class(class_info, parent, attr_list, method_list, feature_list)

def read_ast():
    num_classes = int(get_line())

    for i in range(num_classes):
        class_list.append(read_class())

    return class_list
  



#def print_parent_method (overriden_method_list, cls, class_list, num_method):
#    
#    method_count = 0
#    if (cls.inherits_iden == None):
#
#        for method in cls.methods:
#            if method not in [x.method_name for x in overriden_method_list] :
#                method_count += 1
#        print num_method + method_count
#        for method in cls.methods:
#            if method not in overriden_method_list :
#                print method.method_name
#                print str(len(method.formals))
#                for formal in method.formals:
#                    print formal.formal_name
#    elif (cls.inherits_iden != None and cls.inherits_iden.ident not in
#            ["IO","Object", "Int", "String", "Bool"]) :
#        for method in cls.methods:
#            if method not in [x.method_name for x in overriden_method_list] :
#                method_count += 1
#        for method in cls.methods:
#            if check_overriden(method, filter(lambda x :
#            x.name_iden.ident==cls.inherits_iden.ident, class_list)[0],
#            class_list) :
#                overriden_method_list.append(method)
#
#        print_method(overriden_method_list, filter(lambda x :
#            x.name_iden.ident==cls.inherits_iden.ident, class_list)[0],
#            class_list, method_count)
#
#    for method in overriden_method_list:
#        print method_name
#        print str(len(method.formals))
#        for formal in method.formals:
#            print formal.formal_name
#    for method in cls.methods:
#        if method not in overriden_method_list:
#            print method_name
#            print str(len(method.formals))
#            for formal in method.formals:
#                print formal.formal_name
#
#
#def print_method(overriden_method_list, cls, class_list, num_method):
#    method_count = 0
#    if (cls.inherits_iden == None):
#        for method in cls.methods:
#            if method not in [x.method_name for x in overriden_method_list] :
#                method_count += 1
#        print num_method + method_count
#        for method in cls.methods:
#            if method not in overriden_method_list :
#                print method.method_name
#                print str(len(method.formals))
#                for formal in method.formals:
#                    print formal.formal_name
#    elif (cls.inherits_iden != None and cls.inherits_iden.ident not in
#            ["IO","Object", "Int", "String", "Bool"]) :
#        for method in cls.methods:
#            if method not in [x.method_name for x in overriden_method_list] :
#                method_count += 1
#        for method in cls.methods:
#            if check_overriden(method, filter(lambda x :
#            x.name_iden.ident==cls.inherits_iden.ident, class_list)[0],
#            class_list) :
#                overriden_method_list.append(method)
#
#        print_method(overriden_method_list, filter(lambda x :
#            x.name_iden.ident==cls.inherits_iden.ident, class_list)[0],
#            class_list, method_count)
#
#    for method in overriden_method_list:
#        print method_name
#        print str(len(method.formals))
#        for formal in method.formals:
#            print formal.formal_name
#    for method in cls.methods:
#        if method not in overriden_method_list:
#            print method_name
#            print str(len(method.formals))
#            for formal in method.formals:
#                print formal.formal_name
      
#overriden_methods = (method_name, method object, Class object)

def print_internal_method():
    ret = "abort\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "internal\n"
    ret += "Object.abort\n"
    ret += "copy\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "SELF_TYPE\n"
    ret += "internal\n"
    ret += "Object.copy\n"
    ret += "type_name\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "String\n"
    ret += "internal\n"
    ret += "Object.type_name\n"
    print str.strip(ret)
    return ret

def print_internal_IO_method():
    ret = "in_int\n"
    ret += "0\n"
    ret += "IO\n"
    ret += "0\n"
    ret += "Int\n"
    ret += "internal\n"
    ret += "IO.in_int\n"
    ret += "in_string\n"
    ret += "0\n"
    ret += "IO\n"
    ret += "0\n"
    ret += "String\n"
    ret += "internal\n"
    ret += "IO.in_string\n"
    ret += "out_int\n"
    ret += "1\n"
    ret += "x\n"
    ret += "IO\n"
    ret += "0\n"
    ret += "SELF_TYPE\n"
    ret += "internal\n"
    ret += "IO.out_int\n"
    ret += "out_string\n"
    ret += "1\n"
    ret += "x\n"
    ret += "IO\n"
    ret += "0\n"
    ret += "SELF_TYPE\n"
    ret += "internal\n"
    ret += "IO.out_string\n"
    print str.strip(ret)
    return ret

def print_Object_method():
    ret = "Object\n"
    ret += "3\n"
    ret += "abort\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "internal\n"
    ret += "Object.abort\n"
    ret += "copy\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "SELF_TYPE\n"
    ret += "internal\n"
    ret += "Object.copy\n"
    ret += "type_name\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "String\n"
    ret += "internal\n"
    ret += "Object.type_name\n"
    print str.strip(ret)
    return ret

def print_String_method():
    ret = "String\n"
    ret += "6\n"
    ret += "abort\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "internal\n"
    ret += "Object.abort\n"
    ret += "copy\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "SELF_TYPE\n"
    ret += "internal\n"
    ret += "Object.copy\n"
    ret += "type_name\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "String\n"
    ret += "internal\n"
    ret += "Object.type_name\n"
    ret += "concat\n"
    ret += "1\n"
    ret += "s\n"
    ret += "String\n"
    ret += "0\n"
    ret += "String\n"
    ret += "internal\n"
    ret += "String.concat\n"
    ret += "length\n"
    ret += "0\n"
    ret += "String\n"
    ret += "0\n"
    ret += "Int\n"
    ret += "internal\n"
    ret += "String.length\n"
    ret += "substr\n"
    ret += "2\n"
    ret += "i\n"
    ret += "l\n"
    ret += "String\n"
    ret += "0\n"
    ret += "String\n"
    ret += "internal\n"
    ret += "String.substr\n"
    print str.strip(ret)
    return ret

def print_Bool_method():
    ret = "Bool\n"
    ret += "3\n"
    ret += "abort\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "internal\n"
    ret += "Object.abort\n"
    ret += "copy\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "SELF_TYPE\n"
    ret += "internal\n"
    ret += "Object.copy\n"
    ret += "type_name\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "String\n"
    ret += "internal\n"
    ret += "Object.type_name\n"
    print str.strip(ret)
    return ret

def print_IO_method():
    ret = "IO\n"
    ret += "7\n"
    ret += "abort\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "internal\n"
    ret += "Object.abort\n"
    ret += "copy\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "SELF_TYPE\n"
    ret += "internal\n"
    ret += "Object.copy\n"
    ret += "type_name\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "String\n"
    ret += "internal\n"
    ret += "Object.type_name\n"
    ret += "in_int\n"
    ret += "0\n"
    ret += "IO\n"
    ret += "0\n"
    ret += "Int\n"
    ret += "internal\n"
    ret += "IO.in_int\n"
    ret += "in_string\n"
    ret += "0\n"
    ret += "IO\n"
    ret += "0\n"
    ret += "String\n"
    ret += "internal\n"
    ret += "IO.in_string\n"
    ret += "out_int\n"
    ret += "1\n"
    ret += "x\n"
    ret += "IO\n"
    ret += "0\n"
    ret += "SELF_TYPE\n"
    ret += "internal\n"
    ret += "IO.out_int\n"
    ret += "out_string\n"
    ret += "1\n"
    ret += "x\n"
    ret += "IO\n"
    ret += "0\n"
    ret += "SELF_TYPE\n"
    ret += "internal\n"
    ret += "IO.out_string\n"
    print str.strip(ret)
    return ret

def print_Int_method():
    ret = "Int\n"
    ret += "3\n"
    ret += "abort\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "internal\n"
    ret += "Object.abort\n"
    ret += "copy\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "SELF_TYPE\n"
    ret += "internal\n"
    ret += "Object.copy\n"
    ret += "type_name\n"
    ret += "0\n"
    ret += "Object\n"
    ret += "0\n"
    ret += "String\n"
    ret += "internal\n"
    ret += "Object.type_name\n"
    print str.strip(ret)
    return ret
 
def check_overriden(method, cls, class_list):
    method_name_list = [x.method_name.ident for x in cls.methods]
    if (method.method_name.ident in method_name_list):
        return True
    if (cls.inherits_iden == None):
        return False
    if (cls.inherits_iden != None) :
        return check_overriden(method,filter(lambda x :
            x.name_iden.ident==cls.inherits_iden.ident,
            class_list)[0],class_list)

def print_methods(overriden_methods, cls, class_list, num_method) :
   
    if cls.inherits_iden == None or cls.inherits_iden.ident in ["IO","String","Int","Object","Bool"]:
        if cls.inherits_iden != None :
            print str(num_method + len(cls.methods)+4)
            fout.write(str(num_method + len(cls.methods)+4) + "\n")
            fout.write(print_internal_method())
            fout.write(print_internal_IO_method())
        else:
            print str(num_method + len(cls.methods))
            fout.write(str(num_method + len(cls.methods)) + "\n")
            fout.write(print_internal_method())

        for method in cls.methods:
            print str(method.method_name.ident)
            fout.write(str(method.method_name.ident)+"\n")
            filtered_method = filter(lambda x : x[0] ==
                    method.method_name.ident, overriden_methods)
            if filtered_method != []:
                print str(len(filtered_method[0][1].formals))
                fout.write(str(len(filtered_method[0][1].formals))+ "\n")
                for formal in filtered_method[0][1].formals:
                    print str(formal.formal_name.ident)
                    fout.write(str(formal.formal_name.ident)+"\n")
                print str(filtered_method[0][2].name_iden.ident)
                fout.write(str(filtered_method[0][2].name_iden.ident) + "\n")
                print str(filtered_method[0][1].body_exp).rstrip()
                fout.write(str(filtered_method[0][1].body_exp))
            else:
                print str(len(method.formals))
                fout.write(str(len(method.formals))+"\n")
                for formal in method.formals:
                    print str(formal.formal_name.ident)
                    fout.write(str(formal.formal_name.ident)+"\n")
                print str(cls.name_iden.ident)
                fout.write(str(cls.name_iden.ident)+"\n")
                print str(method.body_exp).rstrip()
                fout.write(str(method.body_exp))
    else:
        printed_method_count = 0
        printed_method_list = []
        multi_overriden_methods = []
        parent_cls = filter(lambda x : x.name_iden.ident == cls.inherits_iden.ident,
                        class_list)
        for method in cls.methods:
            if not check_overriden(method, parent_cls[0], class_list):
                printed_method_count += 1
                printed_method_list.append(method)
            else:
                multi_overriden_methods.append(method)
        old_overriden_methods = overriden_methods
        for method in multi_overriden_methods:
            filtered_method = filter(lambda x : x[0] == \
                    method.method_name.ident, overriden_methods)
            if filtered_method == []:
                temp = (method.method_name.ident, method, cls)
                overriden_methods.append(temp)
        
        print_methods(overriden_methods, parent_cls[0], class_list, printed_method_count+num_method)

        for method in printed_method_list:
            print str(method.method_name.ident)
            fout.write(str(method.method_name.ident)+"\n")
            filtered_method = filter(lambda x : x[0] ==
                    method.method_name.ident, old_overriden_methods)
            if filtered_method != []:
                print str(len(filtered_method[0][1].formals))
                fout.write(str(len(filtered_method[0][1].formals))+"\n")
                for formal in filtered_method[0][1].formals:
                    print str(formal.formal_name.ident)
                    fout.write(str(formal.formal_name.ident)+"\n")
                print str(filtered_method[0][2].name_iden.ident)
                fout.write(str(filtered_method[0][2].name_iden.ident)+"\n")
                print str(filtered_method[0][1].body_exp).rstrip()
                fout.write(str(filtered_method[0][1].body_exp))
            else:
                print str(len(method.formals))
                fout.write(str(len(method.formals))+"\n")
                for formal in method.formals:
                    print str(formal.formal_name.ident)
                    fout.write(str(formal.formal_name.ident)+"\n")
                print str(cls.name_iden.ident)
                fout.write(str(cls.name_iden.ident)+"\n")
                print str(method.body_exp).rstrip()
                fout.write(str(method.body_exp))
        
def print_imp_map1(ast):
    print "implementation_map"
    fout.write("implementation_map\n")
    class_list = [c for c in ast]
    class_tuple_list = [(c.name_iden.ident, c) for c in ast]
    class_tuple_list += [("IO",None), ("Object",None), ("Int", None), ("String",
        None), ("Bool",None)]
    class_tuple_list = set(class_tuple_list)
    class_tuple_list = sorted(class_tuple_list, key = lambda x : x[0]) 
    print str(len(class_tuple_list))
    fout.write(str(len(class_tuple_list))+"\n")
    for class_tuple in class_tuple_list :
        if class_tuple[1] != None :
            print str(class_tuple[0])
            fout.write(str(class_tuple[0])+"\n")
            print_methods([], class_tuple[1], class_list,3)
        else:
            if class_tuple[0]=="IO":
                fout.write(print_IO_method())
            elif class_tuple[0]=="Int":
                fout.write(print_Int_method())
            elif class_tuple[0]=="Bool":
                fout.write(print_Bool_method())
            elif class_tuple[0]=="String":
                fout.write(print_String_method())
            elif class_tuple[0]=="Object":
                fout.write(print_Object_method())

def print_parent_map1(ast):
    #print "parent_map"
    fout.write("parent_map\n")
    class_list = [c for c in ast]
    class_tuple_list = [(c.name_iden.ident, c) for c in ast]
    class_tuple_list += [("IO",None), ("Int", None), ("String",
        None), ("Bool",None)]
    class_tuple_list = set(class_tuple_list)
    class_tuple_list = sorted(class_tuple_list, key = lambda x : x[0])
    #print len(class_tuple_list)
    fout.write(str(len(class_tuple_list))+"\n")
    for class_tuple in class_tuple_list :
        if class_tuple[1] == None :
            #print class_tuple[0] + "\n" + "Object"
            fout.write(class_tuple[0] + "\n" + "Object\n")
        else :
            if class_tuple[1].inherits_iden == None:
                #print class_tuple[0] + "\n" + "Object"
                fout.write(class_tuple[0] + "\n" + "Object\n")
            else:
                #print class_tuple[0] + "\n" + class_tuple[1].inherits_iden.ident
                fout.write(class_tuple[0] + "\n" +\
                        class_tuple[1].inherits_iden.ident + "\n")

def print_class_attribute(cls, class_list,num_attr):
    if (cls.inherits_iden != None and cls.inherits_iden.ident not in \
	["IO","Object", "Int", "String", "Bool"]) :
        print_class_attribute(filter(lambda x :
            x.name_iden.ident==cls.inherits_iden.ident, class_list)[0], class_list,
            num_attr + len(cls.attributes))
    else :
        print num_attr
        fout.write(str(num_attr)+"\n")
    for attribute in cls.attributes :
                if attribute.initialization :
                    print "initializer\n" + attribute.attr_name.ident + "\n"\
                            + attribute.attr_type.ident
                    fout.write("initializer\n" + attribute.attr_name.ident + "\n"\
                            + attribute.attr_type.ident+"\n")
		    fout.write(str(attribute.exp))
                else:
                    print "no_initializer\n" + attribute.attr_name.ident + "\n"\
                            + attribute.attr_type.ident
                    fout.write("no_initializer\n" + attribute.attr_name.ident + "\n"\
                            + attribute.attr_type.ident+"\n")

def print_class_map1(ast):
    print "class_map"
    fout.write("class_map\n")
    class_list = [c for c in ast]
    class_tuple_list = [(c.name_iden.ident, c) for c in ast]
    class_tuple_list += [("IO",None), ("Object",None), ("Int", None), ("String",
        None), ("Bool",None)]
    class_tuple_list = set(class_tuple_list)
    class_tuple_list = sorted(class_tuple_list, key = lambda x : x[0]) 
    print str(len(class_tuple_list))
    fout.write(str(len(class_tuple_list))+"\n")
    for class_tuple in class_tuple_list :
        print str(class_tuple[0])
        fout.write(str(class_tuple[0])+"\n")
        if class_tuple[1] == None :
            print "0"
            fout.write("0\n")
        else :
           print_class_attribute(class_tuple[1], class_list, len(class_tuple[1].attributes))

         

def tc(current_cls, astnode, symbol_table = {}):
    global ast
    global modified_ast
    global internal_ast
    if isinstance(astnode, Class):
        # check redefined Object
        if astnode.name_iden.ident in ["Object","Int","String","Bool","SELF_TYPE", "IO"]:
            raise Exception("ERROR: "+astnode.name_iden.line_num+": Type-Check: class "+astnode.name_iden.ident+" redefined")

        # check main method exist
        if astnode.name_iden.ident == "Main":
            if "main" not in [x[1] for x in imp_map["Main"]] :
                raise Exception("ERROR: 0: Type-Check: Class Main " + \
                                "method main not found")
            cls_name = [x[0] for x in imp_map["Main"] if x[1] == "main"][0]
            cls_instance = [_cls for _cls in ast if _cls.name_iden.ident == \
                    cls_name][0]
            method_instance = [_method for _method in cls_instance.methods if \
                                _method.method_name.ident == "main"][0]
            if method_instance.formals != []:
                raise Exception("ERROR: 0: Type-Check: class Main method main with 0 parameters not found")
                

        # check method redefined
        for i, method in enumerate(astnode.methods):
            for j, target_method in enumerate(astnode.methods):
                if i!=j and method.method_name.ident == \
                            target_method.method_name.ident:
                    raise Exception("ERROR: " + \
                            target_method.method_name.line_num + \
                            ":"+"Type-Check: Class "+ \
                            astnode.name_iden.ident + "redifines method")
        # check attribute redefined
        check_list = []
        for attribute in class_map[astnode.name_iden.ident]:
            if attribute.attr_name.ident in check_list:
                raise Exception("ERROR: "+attribute.attr_name.line_num+\
                        ": Type-Check: class "+astnode.name_iden.ident+\
                        " redefines attribute "+attribute.attr_name.ident)
            else :
                check_list.append(attribute.attr_name.ident)
 
        # check every attibute
        if astnode.attributes != [] :
            for attribute in class_map[astnode.name_iden.ident]:
                tc(current_cls,attribute,symbol_table)
                if attribute.attr_name.ident in symbol_table:
                    symbol_table[attribute.attr_name.ident].append((attribute.attr_name.ident,attribute.attr_type.ident))
                else:
                    symbol_table[attribute.attr_name.ident]=[(attribute.attr_name.ident,attribute.attr_type.ident)] 

        #for attribute in astnode.attributes:
        #    tc(current_cls,attribute,symbol_table)
        #for attribute in class_map[astnode.name_iden.ident]:
        #    if attribute.attr_name.ident in symbol_table:
        #        symbol_table[attribute.attr_name.ident].append((attribute.attr_name.ident,attribute.attr_type.ident))
        #    else:
        #        symbol_table[attribute.attr_name.ident]=[(attribute.attr_name.ident,attribute.attr_type.ident)] 

        if astnode.methods != [] :
            for method in astnode.methods:
                tc(current_cls,method,symbol_table)

    elif isinstance(astnode, Method):

        if astnode.method_type.ident not in class_map.keys()+["SELF_TYPE"]:
            raise Exception("ERROR: "+astnode.method_name.line_num+\
                    ": Type-Check: class has method "+\
                    astnode.method_name.ident + \
                    " with unknown return type " + astnode.method_type.ident)
        ## check duplicate formal
        check_list = []
        for formal in astnode.formals:
            if formal.formal_type.ident not in class_map.keys():
                raise Exception("ERROR: "+formal.formal_type.line_num+\
                        ": Type-Check: class has method "+ \
                        astnode.method_name.ident+ \
                        " with formal parameter of unknown type "+ \
                        formal.formal_type.ident)

            if formal.formal_name.ident == "self":
                raise Exception("ERROR: "+formal.formal_name.line_num+\
                ": Type-Check: class has method "+astnode.method_name.ident+\
                " with formal parameter named self")
            if formal.formal_name.ident in check_list:
                raise Exception("ERROR: "+ formal.formal_name.line_num+\
                        ": Type-Check: class "+formal.formal_name.ident+\
                        " duplicate formal "+formal.formal_name.ident)
            else :
                check_list.append(formal.formal_name.ident)

        for formal in astnode.formals:
            if formal.formal_name.ident in symbol_table:
	        symbol_table[formal.formal_name.ident].append \
                        ((formal.formal_name.ident, formal.formal_type.ident))
            else:
	        symbol_table[formal.formal_name.ident] = \
                        [(formal.formal_name.ident, formal.formal_type.ident)]
        
        method_body_type = tc(current_cls,astnode.body_exp,symbol_table)
        if method_body_type == "SELF_TYPE" and astnode.method_type.ident !=\
        "SELF_TYPE":
            method_body_type = current_cls.name_iden.ident
        if astnode.method_type.ident != \
                find_common_ancestor(method_body_type,astnode.method_type.ident):
            raise Exception("ERROR: "+astnode.method_type.line_num+\
                    ": Type-Check: "+method_body_type+" does not conform to "+\
                    astnode.method_type.ident+" in "+ astnode.method_name.ident)
        


    elif isinstance(astnode, Attribute):
        
        if astnode.attr_name.ident == "self":
            raise Exception("ERROR: "+astnode.attr_name.line_num + \
            ": Type-Check: class has an attribute named self")
        if astnode.exp != None :
            t1 = tc(current_cls,astnode.exp, symbol_table)
            if t1 == "SELF_TYPE":
                t1 = current_cls.name_iden.ident
                if astnode.attr_type.ident != find_common_ancestor(t1,astnode.attr_type.ident):
                    raise Exception("ERROR: "+astnode.exp.line_num+\
                            ": Type-Check: "+t1+\
                            " does not conform to "+astnode.attr_type.ident+\
                            " in initialized attribute")
        
    elif isinstance(astnode, Let):

        for i in range(len(astnode.binding_list)):
            if astnode.binding_list[i].initialization:
                binding_type = tc(current_cls,astnode.binding_list[i].value_exp,symbol_table)
                #TODO
        for binding in astnode.binding_list:
            if binding.var_ident.ident == "self":
                raise Exception("ERROR: "+binding.var_ident.line_num+\
                        ": Type-Check: binding self in a let is not allowed")
            if binding.var_ident.ident in symbol_table:
                symbol_table[binding.var_ident.ident].append((binding.var_ident.ident,binding.type_ident.ident))
            else:
                symbol_table[binding.var_ident.ident]=[(binding.var_ident.ident,binding.type_ident.ident)]
            if binding.initialization:
                binding_type = \
                tc(current_cls,binding.value_exp,symbol_table)
                #TODO self check
                if binding.type_ident.ident != \
                        find_common_ancestor(binding.type_ident.ident,
                                binding_type):
                            raise Exception("ERROR: "+
                                    binding.var_ident.line_num + ": Let")

	t1 = tc(current_cls, astnode.exp, symbol_table )
        for binding in astnode.binding_list:	
	    symbol_table[binding.var_ident.ident].pop()

	astnode.exp_type = t1
	return t1

    elif isinstance(astnode, String):
        astnode.exp_type = "String"
	return "String"

    elif isinstance(astnode, Integer):
        astnode.exp_type = "Int"
	return "Int"

    elif isinstance(astnode, Identifier):
        if astnode.ident == "self":
            #astnode.exp_type = "SELF_TYPE"
            return "SELF_TYPE"

	if astnode.ident not in symbol_table:
	    raise Exception ("ERROR: "+astnode.line_num+"Unbound identifier " + astnode.ident + "\n")
	else:
            #astnode.exp_type = symbol_table[astnode.ident][-1][1]
	    return symbol_table[astnode.ident][-1][1]

    elif isinstance(astnode, (Plus, Minus, Times, Divide)):

	t1 = tc(current_cls,astnode.lhs, symbol_table)
	t2 = tc(current_cls,astnode.rhs, symbol_table)
	if (t1 == "Int" and t2 == "Int"):
	    astnode.exp_type = "Int"
	    return "Int"
	else:
	    raise Exception ("ERROR: "+astnode.line_num+" Adding \n")

    elif isinstance(astnode, (Le, Eq, Lt)):

        t1 = tc(current_cls,astnode.lhs, symbol_table)
        t2 = tc(current_cls,astnode.rhs, symbol_table)
        if t1 in ["Bool","Int","String"] and (t1 != t2):
            raise Exception ("ERROR: "+astnode.line_num+" cannot compare "+t1 + "with" + t2 + "\n")
        astnode.exp_type = "Bool"
        return "Bool"         


    elif isinstance(astnode, TrueExp):
        astnode.exp_type = "Bool"
        return "Bool" 

    elif isinstance(astnode, FalseExp):
        astnode.exp_type = "Bool"
        return "Bool"    
    elif isinstance(astnode, Assign):

        assign_ident_type = tc(current_cls,astnode.ident, symbol_table)
        assign_exp_type = tc(current_cls,astnode.exp, symbol_table)
        if astnode.ident.ident == "self":
            raise Exception("ERROR: "+astnode.line_num+": Type-Check: cannot assign to self")
        if assign_ident_type != find_common_ancestor(assign_ident_type,
                assign_exp_type): 
            raise Exception("ERROR: "+astnode.line_num+\
                    ": Type-Check: "+assign_exp_type+" does not conform to "+\
                    assign_ident_type+\
                    " in assignment")
        astnode.exp_type = assign_exp_type
        return astnode.exp_type

    elif isinstance(astnode, New):

        if astnode.ident.ident == "SELF_TYPE":
            astnode.exp_type = "SELF_TYPE"
        else :
            astnode.exp_type = astnode.ident.ident
        return astnode.exp_type

    elif isinstance(astnode, If):

        node_topo = []
        predicate_type = tc(current_cls, astnode.predicate, symbol_table)
        then_body_type = tc(current_cls,astnode.then_body, symbol_table)
        else_body_type = tc(current_cls,astnode.else_body, symbol_table)
        if predicate_type != "Bool":
            raise Exception("ERROR: "+astnode.line_num+\
                    ": Type-Check: conditional has type "+predicate_type+" instead of Bool")
        if then_body_type == "SELF_TYPE" and else_body_type == "SELF_TYPE":
            astnode.exp_type = "SELF_TYPE"
            return astnode.exp_type

        if then_body_type == "SELF_TYPE":
            then_body_type = current_cls.name_iden.ident
        if else_body_type == "SELF_TYPE":
            else_body_type = current_cls.name_iden.ident
        astnode.exp_type = find_common_ancestor(then_body_type, else_body_type)
        return astnode.exp_type


    elif isinstance(astnode, Block):

        for i in range(len(astnode.exp_list)):
            block_exp_type = tc(current_cls,astnode.exp_list[i], symbol_table)
        astnode.exp_type = block_exp_type
        return block_exp_type

    elif isinstance(astnode, While):

        predicate_type = tc(current_cls,astnode.predicate, symbol_table)
        body_type = tc(current_cls,astnode.body, symbol_table)
        if predicate_type != "Bool":
            raise Exception("ERROR: "+astnode.line_num+ \
                    ": Type-Check: conditional has type "+predicate_type+ \
                    "instead of Bool")
        astnode.exp_type = "Object"
        return "Object"
        
    elif isinstance(astnode, Isvoid):

        tc(current_cls,astnode.exp, symbol_table)
        astnode.exp_type = "Bool"
        return "Bool"
    elif isinstance(astnode, IdentifierExp):
        t1 = tc(current_cls,astnode.ident, symbol_table)
        astnode.exp_type = t1
        return t1

    elif isinstance(astnode, Not):

        exp_type = tc(current_cls,astnode.exp, symbol_table)
        if exp_type != "Bool":
            raise Exception("ERROR: "+astnode.line_num+ \
                    ": Type-Check: Not has type "+exp_type+ \
                    "instead of Bool")
        astnode.exp_type = "Bool"
        return "Bool"
    elif isinstance(astnode, Negate):

        exp_type = tc(current_cls,astnode.exp, symbol_table)
        if exp_type != "Int":
            raise Exception("ERROR: "+astnode.line_num+ \
                    ": Type-Check: Negate has type "+exp_type+ \
                    "instead of Int")
        astnode.exp_type = "Int"
        return "Int"
    elif isinstance(astnode, Dynamic_Dispatch):
        d_dispatch_exp_type = tc(current_cls,astnode.exp, symbol_table)
        if d_dispatch_exp_type == "SELF_TYPE":
            d_dispatch_exp_type_new = current_cls.name_iden.ident
        else:
            d_dispatch_exp_type_new = d_dispatch_exp_type
        t = []
        for arg in astnode.args:
            temp = tc(current_cls,arg,symbol_table)
            if temp == "SELF_TYPE":
                temp = current_cls.name_iden.ident
            t.append(temp)

        method_tuple = [x for x in imp_map[d_dispatch_exp_type_new] if\
                x[1]==astnode.method_ident.ident]
        method_tuple = method_tuple[0]
        cls_instance = [_cls for _cls in ast+internal_ast if _cls.name_iden.ident == \
                    method_tuple[0]]
        cls_instance = cls_instance[0]
        method_instance = [_method for _method in cls_instance.methods if \
                                _method.method_name.ident ==\
                                method_tuple[1]][0]
        t_prime = [formal.formal_type.ident for formal in method_instance.formals]

        for i in range(len(t)):
            if t_prime[i] != find_common_ancestor(t_prime[i],t[i]):
                raise Exception("ERROR: "+astnode.line_num+\
                        ": Type-Check: argument #"+str(i+1)+" type "+t[i]+\
                        " does not conform to formal type "+t_prime[i])
        if isinstance(method_instance.body_exp, str):
            astnode.exp_type = method_instance.method_type.ident
            return astnode.exp_type
            #print astnode.exp_type
        else:
            #if method_instance.body_exp.exp_type == "No_TYPE":
            #    tc(cls_instance,cls_instance)
            if method_instance.method_type.ident == "SELF_TYPE":
                astnode.exp_type = d_dispatch_exp_type_new
                return astnode.exp_type
            else:
                astnode.exp_type = method_instance.method_type.ident
                return astnode.exp_type
    elif isinstance(astnode, Static_Dispatch):
        s_dispatch_exp_type = tc(current_cls,astnode.exp, symbol_table)
        if s_dispatch_exp_type == "SELF_TYPE":
            s_dispatch_exp_type_new = current_cls.name_iden.ident
        else:
            s_dispatch_exp_type_new = s_dispatch_exp_type
        t = []
        for arg in astnode.args:
            temp = tc(current_cls,arg,symbol_table)
            if temp == "SELF_TYPE":
                temp = current_cls.name_iden.ident
            t.append(temp)
        
        method_tuple = [x for x in imp_map[s_dispatch_exp_type_new] if\
                x[1]==astnode.method_ident.ident]
        method_tuple = method_tuple[0]
        cls_instance = [_cls for _cls in ast+internal_ast if _cls.name_iden.ident == \
                    method_tuple[0]]
        cls_instance = cls_instance[0]
        method_instance = [_method for _method in cls_instance.methods if \
                                _method.method_name.ident ==\
                                method_tuple[1]][0] 
        t_prime = [formal.formal_type.ident for formal in \
                 method_instance.formals]
        if len(t_prime)!= len(t):
            raise Exception("ERROR: "+astnode.line_num) 
            
        for i in range(len(t)):
            if t_prime[i] != find_common_ancestor(t_prime[i],t[i]):
                raise Exception("ERROR: "+astnode.line_num+\
                        ": Type-Check: argument #"+str(i+1)+" type "+t[i]+\
                        " does not conform to formal type "+t_prime[i])
        if astnode.type_ident.ident != \
                        find_common_ancestor(astnode.type_ident.ident,
                                s_dispatch_exp_type_new) :
            raise Exception("ERROR: "+astnode.line_num+": Type-Check: "+\
                    s_dispatch_exp_type_new+" does not conform to "+\
                    astnode.type_ident.ident+" in static dispatch") 

        if isinstance(method_instance.body_exp, str):
            astnode.exp_type = method_instance.method_type.ident
            return astnode.exp_type
            #print astnode.exp_type
        else:
            #if method_instance.body_exp.exp_type == "No_TYPE":
            #    tc(cls_instance,cls_instance)
            if method_instance.method_type.ident == "SELF_TYPE":
                astnode.exp_type = s_dispatch_exp_type_new
                return astnode.exp_type
            else:
                astnode.exp_type = method_instance.method_type.ident
                return astnode.exp_type

    elif isinstance(astnode, Self_Dispatch):
        t = []
        for arg in astnode.args:
            temp = tc(current_cls,arg,symbol_table)
            if temp == "SELF_TYPE":
                temp = current_cls.name_iden.ident
            t.append(temp)
        method_tuple = [x for x in\
                imp_map[current_cls.name_iden.ident] if\
                x[1]==astnode.method_ident.ident][0]
        cls_instance = [_cls for _cls in ast+internal_ast if _cls.name_iden.ident == \
                    method_tuple[0]][0]
        method_instance = [_method for _method in cls_instance.methods if \
                                _method.method_name.ident ==\
                                method_tuple[1]][0]

        t_prime = [formal.formal_type.ident for formal in \
                 method_instance.formals]
        for i in range(len(t)):
            if t_prime[i] != find_common_ancestor(t_prime[i],t[i]):
                raise Exception("ERROR: "+astnode.line_num+\
                        ": Type-Check: argument #"+str(i+1)+" type "+t[i]+\
                        " does not conform to formal type "+t_prime[i])

        astnode.exp_type = method_instance.method_type.ident
            #print astnode.exp_type
        return astnode.exp_type

    elif isinstance(astnode, Case):
        t_new = []
        t0 = tc(current_cls,astnode.exp,symbol_table)
        for i,case_element in enumerate(astnode.element_list):
            if case_element.type_ident.ident == "SELF_TYPE":
                raise Exception("ERROR: "+case_element.type_ident.line_num+\
                ": Type-Check: using SELF_TYPE as a case branch type is not allowed")
            for j, target_case_element in enumerate(astnode.element_list):
                if j!=i and target_case_element.type_ident.ident == \
                case_element.type_ident.ident:
                    raise Exception("ERROR: "+\
                            target_case_element.type_ident.line_num+\
                            ": Type-Check: case branch type "+ \
                            target_case_element.type_ident.ident+\
                            " is bound twice")
        for case_element in astnode.element_list:
            if case_element.var_ident.ident in symbol_table:
                symbol_table[case_element.var_ident.ident].append((case_element.var_ident.ident,case_element.type_ident.ident))
            else:
                symbol_table[case_element.var_ident.ident]=[(case_element.var_ident.ident,case_element.type_ident.ident)]
            case_element_body_type = tc(current_cls,case_element.body_exp,symbol_table)
            t_new.append(case_element_body_type)
            symbol_table[case_element.var_ident.ident].pop()

        while(len(t_new)>1):
            temp = find_common_ancestor(t_new.pop(),t_new.pop())
            t_new.append(temp)
        
        astnode.exp_type = t_new[0]
        return astnode.exp_type
            
    else:
    	raise Exception ("ERROR: Unkown Expression type!")

def produce_class_map(cls,ast):
    global class_map
    class_list = [c for c in ast]
    if cls.inherits_iden == None:
        class_map[cls.name_iden.ident]=cls.attributes
        return list(class_map[cls.name_iden.ident])
    elif cls.inherits_iden != None:
        parent_cls = filter(lambda x : x.name_iden.ident == cls.inherits_iden.ident,
                        class_list)[0]
        # recursive call
        produce_class_map(parent_cls, ast)
        class_map[cls.name_iden.ident] = \
        class_map[parent_map[cls.name_iden.ident]] + \
                                        cls.attributes
        return list(class_map[cls.name_iden.ident])

def produce_imp_map(cls, ast):
    global imp_map
    class_list = [c for c in ast]
    if cls.inherits_iden == None:
        imp_map[cls.name_iden.ident] = []
        for method in cls.methods :
            imp_map[cls.name_iden.ident].append((cls.name_iden.ident, \
                    method.method_name.ident))
        #imp_map[cls.name_iden.ident] = imp_map["Object"]+[]
        #parent_method_name_list = [method_tuple[1] for i,method_tuple in \
        #        enumerate(imp_map["Object"])]
        #for method in cls.methods:
        #    if method.method_name.ident in parent_method_name_list :
        #        i = parent_method_name_list.index(method.method_name.ident)
        #        imp_map[cls.name_iden.ident][i]=(cls.name_iden.ident,
        #                method.method_name.ident)
        #    else:
        #        imp_map[cls.name_iden.ident].append((cls.name_iden.ident, \
        #            method.method_name.ident))
        return list(imp_map[cls.name_iden.ident])
    elif cls.inherits_iden != None:
        parent_cls = filter(lambda x : x.name_iden.ident == cls.inherits_iden.ident,
                        class_list)[0]
        imp_map[cls.name_iden.ident] = produce_imp_map(parent_cls, ast)
        parent_method_name_list = [method_tuple[1] for i,method_tuple in \
                enumerate(imp_map[parent_cls.name_iden.ident])]

        for method in cls.methods:
            if method.method_name.ident in parent_method_name_list :
                i = parent_method_name_list.index(method.method_name.ident)
                imp_map[cls.name_iden.ident][i]=(cls.name_iden.ident,
                        method.method_name.ident)
            else:
                imp_map[cls.name_iden.ident].append((cls.name_iden.ident, \
                    method.method_name.ident))
        return list(imp_map[cls.name_iden.ident])
        #if cls.inherits_iden.ident != "IO":
        #    parent_cls = filter(lambda x : x.name_iden.ident == cls.inherits_iden.ident,
        #                class_list)[0]
        #    #recursive call
        #    imp_map[cls.name_iden.ident] = produce_imp_map(parent_cls, ast)
        #    parent_method_name_list = [method_tuple[1] for i,method_tuple in \
        #        enumerate(imp_map[cls.name_iden.ident])]
        #else:
        #    imp_map[cls.name_iden.ident] = imp_map["IO"] + []
        #    parent_method_name_list = [method_tuple[1] for i,method_tuple in \
        #        enumerate(imp_map["IO"])]

        for method in cls.methods:
            if method.method_name.ident in parent_method_name_list :
                i = parent_method_name_list.index(method.method_name.ident)
                imp_map[cls.name_iden.ident][i]=(cls.name_iden.ident,
                        method.method_name.ident)
            else:
                imp_map[cls.name_iden.ident].append((cls.name_iden.ident, \
                    method.method_name.ident))
        return list(imp_map[cls.name_iden.ident])


def find_common_ancestor(type1,type2):
            global parent_map
            temp = type1
            node_topo = []
            if temp != "SELF_TYPE" :
                while(parent_map.get(temp)!=None):
                    node_topo.append(temp)
                    temp = parent_map[temp]
            else:
                node_topo.append("SELF_TYPE")
                node_topo.append("Object")
       
            temp = type2
            if temp != "SELF_TYPE" :
                while(parent_map.get(temp)!=None):
                    if temp in node_topo:
                        return temp
                    temp = parent_map[temp]
            else:
                if temp in node_topo:
                    return temp
            # if not found
            return "Object"

def produce_parent_map(ast):
    global parent_map
    class_list = [c for c in ast]
    for cls in class_list:
        if cls.inherits_iden != None:
            parent_map[cls.name_iden.ident] = cls.inherits_iden.ident

def produce_internal_ast():
    name_iden = Identifier("0", "Object")
    inherits_iden = None
    method_names = {"abort":"Object","type_name":"String","copy":"SELF_TYPE"}
    methods = [] 
    method = Method(Identifier("0","abort"), [],Identifier("0","Object"),None)
    method.body_exp = "0" +"\n" +\
                          method.method_type.ident +\
                          "\ninternal\n"+name_iden.ident+"." +\
                          method.method_name.ident+"\n"
    methods.append(method)
    method = Method(Identifier("0","copy"), [],Identifier("0","SELF_TYPE"),None)
    method.body_exp = "0" +"\n" +\
                          method.method_type.ident +\
                          "\ninternal\n"+name_iden.ident+"." +\
                          method.method_name.ident+"\n"
    methods.append(method)
    method = Method(Identifier("0","type_name"), [],Identifier("0","String"),None)
    method.body_exp = "0" +"\n" +\
                          method.method_type.ident +\
                          "\ninternal\n"+name_iden.ident+"." +\
                          method.method_name.ident+"\n"
    methods.append(method)
    Object_class = Class(name_iden, inherits_iden, [],methods, methods+[])

    name_iden = Identifier("0", "IO")
    inherits_iden = Identifier("0","Object") 
    methods = []
    method = Method(Identifier("0","in_int"),
            [],Identifier("0","Int"),None)
    method.body_exp = "0" +"\n" +\
                          method.method_type.ident +\
                          "\ninternal\n"+name_iden.ident+"." +\
                          method.method_name.ident+"\n"
    methods.append(method)
    method = Method(Identifier("0","in_string"),
            [],Identifier("0","String"),None)
    method.body_exp = "0" +"\n" +\
                          method.method_type.ident +\
                          "\ninternal\n"+name_iden.ident+"." +\
                          method.method_name.ident+"\n"
    methods.append(method)
    method = Method(Identifier("0","out_int"),
            [Formal(Identifier("0","x"),Identifier("0","Int"))],Identifier("0","SELF_TYPE"),None)
    method.body_exp = "0" +"\n" +\
                          method.method_type.ident +\
                          "\ninternal\n"+name_iden.ident+"." +\
                          method.method_name.ident+"\n"
    methods.append(method)
    method = Method(Identifier("0","out_string"),
            [Formal(Identifier("0","x"),Identifier("0","String"))],Identifier("0","SELF_TYPE"),None)
    method.body_exp = "0" +"\n" +\
                          method.method_type.ident +\
                          "\ninternal\n"+name_iden.ident+"." +\
                          method.method_name.ident+"\n"
    methods.append(method)
    IO_class = Class(name_iden, inherits_iden, [],methods, methods+[])
    
    name_iden = Identifier("0", "Int")
    inherits_iden = Identifier("0","Object")
    methods = []
    Int_class = Class(name_iden, inherits_iden, [],methods, methods+[])

    name_iden = Identifier("0", "Bool")
    inherits_iden = Identifier("0","Object")
    methods = []
    Bool_class = Class(name_iden, inherits_iden, [],methods, methods+[])

    name_iden = Identifier("0", "String")
    inherits_iden = Identifier("0","Object")
    methods = []
    method = Method(Identifier("0","concat"),
            [Formal(Identifier("0","s"),Identifier("0","String"))],Identifier("0","String"),None)
    method.body_exp = "0" +"\n" +\
                          method.method_type.ident +\
                          "\ninternal\n"+name_iden.ident+"." +\
                          method.method_name.ident+"\n"
    methods.append(method)
    method = Method(Identifier("0","length"),
            [],Identifier("0","Int"),None)
    method.body_exp = "0" +"\n" +\
                          method.method_type.ident +\
                          "\ninternal\n"+name_iden.ident+"." +\
                          method.method_name.ident+"\n"
    methods.append(method)
    method = Method(Identifier("0","substr"),
            [Formal(Identifier("0","i"),Identifier("0","Int")), 
             Formal(Identifier("0","l"),Identifier("0","Int"))],Identifier("0","String"),None)
    method.body_exp = "0" +"\n" +\
                          method.method_type.ident +\
                          "\ninternal\n"+name_iden.ident+"." +\
                          method.method_name.ident+"\n"
    methods.append(method)
    String_class = Class(name_iden, inherits_iden, [],methods, methods+[])

    return [Object_class, Bool_class, IO_class, Int_class, String_class]


def print_imp_map(imp_map, ast):
    imp_map = sorted(imp_map.items())
    ret = "implementation_map\n"
    ret += str(len(imp_map)) + "\n"
    for cls,method_list in imp_map: 
        ret += cls + "\n"
        ret += str(len(method_list)) + "\n"
        for method_tuple in method_list :
            ret += method_tuple[1] + "\n"
            cls_instance = [_cls for _cls in ast if _cls.name_iden.ident == \
                    method_tuple[0]][0]
            method_instance = [_method for _method in cls_instance.methods if \
                                _method.method_name.ident == method_tuple[1]][0]
            ret += str(len(method_instance.formals)) + "\n"
            for formal in method_instance.formals :
                ret += formal.formal_name.ident + "\n"
            ret += method_tuple[0] + "\n"
            ret += str(method_instance.body_exp)
    fout.write(ret)
    return ret

def print_class_map(class_map, ast):
    class_map = sorted(class_map.items())
    ret = "class_map\n"
    ret += str(len(class_map)) + "\n"
    for cls, attribute_list in class_map:
        ret += cls + "\n"
        ret += str(len(attribute_list)) + "\n"
        for attribute in attribute_list :
            if attribute.initialization :
                    ret += "initializer\n" + attribute.attr_name.ident + "\n"+\
                            attribute.attr_type.ident + "\n"
                    ret += str(attribute.exp) 
            else:
                    ret += "no_initializer\n" + attribute.attr_name.ident + "\n"\
                            + attribute.attr_type.ident + "\n"
    fout.write(ret)

def print_parent_map(parent_map, ast):
    parent_map = sorted(parent_map.items())
    ret = "parent_map\n"
    ret += str(len(parent_map)) + "\n"
    for child, parent in parent_map:
        ret += child + "\n" + parent+"\n"
    fout.write(ret)

def main():
    global class_map_print_flag
    global ast_lines
    global class_map
    global imp_map
    global parent_map
    global ast
    global modified_ast
    global internal_ast
    if len(sys.argv) < 2:
        print("Specify .cl-ast input file.")
        exit()

    with open(sys.argv[1]) as f:
        ast_lines = [l[:-1] for l in f.readlines()]
    internal_ast = produce_internal_ast()
    ast = read_ast()

    modified_ast = copy.deepcopy(ast)
    for i,cls in enumerate(modified_ast):
        if cls.inherits_iden == None:
            modified_ast[i].inherits_iden = Identifier("0", "Object")
    modified_ast = modified_ast + internal_ast

    produce_parent_map(modified_ast)

    ### check if class is defined more than once
    for i, cls in enumerate(ast):
        if cls.name_iden.ident in ["Object"]:
            print "ERROR: "+cls.name_iden.line_num+": Type-Check: class Object redefined"
            exit()
        for j, target_cls in enumerate(ast):
            if i!=j and cls.name_iden.ident == target_cls.name_iden.ident:
                print "ERROR: " + target_cls.name_iden.line_num + ":"\
                    "Type-Check: Class defined multiple times:"\
                    + target_cls.name_iden.ident + "\n"
                exit()

    ## check class inherits from bool int string self_type
    for cls in ast:
        if cls.inherits_iden != None:
            if cls.inherits_iden.ident in ["Int","Bool","String", "SELF_TYPE"]:
                        print "ERROR: "+ cls.inherits_iden.line_num + \
                        ": Type-Check: class Main inherits from " + \
                        cls.inherits_iden.ident
                        exit()


    ### check if class inherits from nonexistent class

    class_names = set([c.name_iden.ident for c in ast])
    class_names.add("IO")
    class_names.add("Object")

    for cls in ast:
        if cls.inherits_iden != None :
            if (not cls.inherits_iden.ident in class_names):
                print "ERROR: " + cls.inherits_iden.line_num + " : "\
                    "Type-Check: Class inherits from non-existent class:"\
                    + cls.inherits_iden.ident
                exit()
    ### check the existance of Main class
    if "Main" not in [cls.name_iden.ident for cls in ast]:
        print "ERROR: 0: Type-Check: class Main not found"
        exit()
    
    ### check inherits circle
    def visit(current_cls):
        if current_cls.inherits_iden == None :
            return 0
        if current_cls.name_iden.ident in t_marked:
            print "ERROR: 0: Type-Check: inheritance cycle"
            exit(0)
        t_marked.append(current_cls.name_iden.ident)
        parent_cls = filter(lambda x : x.name_iden.ident == current_cls.inherits_iden.ident,
                        modified_ast)[0]
        visit(parent_cls)

    t_marked = []
    for cls in modified_ast:
        t_marked=[]
        visit(cls)

    ### 
    for cls in ast+internal_ast:
        produce_class_map(cls, ast+internal_ast)
    for cls in modified_ast:
        produce_imp_map(cls, modified_ast)

    try:
        for cls in ast:
            tc(cls,cls)
    except Exception as e:
        #exc_type, exc_obj, exc_tb = sys.exc_info()
        #fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #print(exc_type, fname, exc_tb.tb_lineno)
        #print(traceback.format_exc())
	print e.message
        exit()
    ### successful type checking, print AAST
    class_map_print_flag = 1 
    print_class_map(class_map, modified_ast)
    class_map_print_flag = 1
    print_imp_map(imp_map, ast+internal_ast)
    print_parent_map(parent_map, modified_ast)
    #print str(len(ast))
    fout.write(str(len(ast))+"\n")
    for cls in ast:
        #print cls
        fout.write(str(cls))
    
                

if __name__ == '__main__':
    main()
