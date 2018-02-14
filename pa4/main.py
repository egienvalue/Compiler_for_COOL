#!/usr/bin/python

import sys
import pprint

ast_lines = []
class_list = []

# define multiple classes
class Expression(object):
    line_num = None
    exp_type = "No_TYPE"

    def s(self):
        ret = self.line_num + "\n"
        ret += self.exp_type + "\n"
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
        ret += "Integer\n" + str(self.int_val + "\n")
        return ret

class String(Expression):
    str_val = None

    def __init__(self, _line_num, _str_val):
        Expression.__init__(self, _line_num)
        self.str_val = _str_val
        self.exp_type = "String"

    def __str__(self):
        ret = self.s()
        ret += "String\n" + self.str_val + "\n"
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
        Expression.__init__(sel,_line_num)
        self.ident = _ident

    def __str__(self):
        ret = self.s()
        ret += "identifier\n" + str(self.ident)
        return ret

class New(Expression):
    ident = None

    def __init__(self, _line_num, _ident):
        Expression.__init__(self, _line_num)
        self.ident = _ident
        self.exp_type = _ident.ident

    def __str__(self):
        ret = self.s()
        ret += "new\n" + str(self.ident)
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
        ret += self.ident.line_num + "\n"
        ret += self.ident.ident + "\n"
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
        for element in element_list:
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
        Expression.__init__(self, _line_num, _predicate, _then_body, _else_body)
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
        for exp in exp_list:
            ret += str(exp)

        return ret

class Isvoid(Expression):
    exp = None
    def __init__(self, _line_num, _exp):
        Expression.__init__(self, _exp)
        self.exp = _exp

    def __str__(self):
        ret = self.s()
        ret += "isvoid\n"
        ret += str(exp)

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

        return ret\

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

    def __init__(self, formal_name, _formal_type):
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
            ret += "Attribute_no_init\n"

        ret += str(self.attr_name)
        ret += str(self.attr_type)

        if self.initialization:
            ret += str(self.exp)

        return ret

class identifier(object):
    line_num = None
    ident = None
    def __init__(self, _line_num, _ident):
        self.line_num = _line_num
        self.ident = _ident

    def __str__(self):
        ret = self.line_num + "\n" + self.ident + "\n"
        return ret

    def __repr__(self):
        return str(self)
class Method(object):
    method_name = ""
    formals = []
    method_type = ""
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
    return ast_lines.pop(0)

def read_identifier():
    line_no = get_line()
    ident_name = get_line()

    return identifier(line_no, ident_name)

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

def read_exp():
    line_number = get_line()
    exp_name = get_line()

    if exp_name == 'assign':
        assignee = read_identifier()
        rhs = read_exp()

        return Assign(exp_name, assignee, rhs)

    elif exp_name == 'dynamic_dispatch':
        obj_name = read_exp()
        method_name = read_identifier()
        num_args = int(get_line())
        args = []
        for i in range(num_args):
            args.append(read_exp())

        return Dynamic_Dispatch(exp_name, obj_name, method_name, args)

    elif exp_name == 'static dispatch':
        obj_name = read_exp()
        type_name = read_identifier()
        args = []
        for i in range(num_args):
            args.append(read_exp())

        return Static_Dispatch(exp_name, obj_name, type_name, method_name, args)

    elif exp_name == 'self_dispatch':
        method_name = read_identifier()
        num_args = int(get_line())
        args = []
        for i in range(num_args):
            args.append(read_exp())

        return Self_Dispatch(exp_name, method_name, args)

    elif exp_name == 'if':
        predicate = read_exp()
        then_body = read_exp()
        else_body = read_exp()

        return  If(exp_name, predicate, then_body, else_body)

    elif exp_name == 'while':
        predicate = read_exp()
        body_exp = read_exp()

        return While(exp_name,predicate, body_exp)

    elif exp_name == 'block':
        num_exps = int(get_line())
        exps = []
        for i in range(num_exps):
            exps.append(read_exp())

        return Block(exp_name, exps)

    elif exp_name == 'new':
        return New(exp_name, read_identifier())


    elif exp_name == 'isvoid':
        return (exp_name, read_exp())

    elif exp_name == 'plus':
        return Plus(exp_name, read_exp(), read_exp())

    elif exp_name == 'minus':
        return Minus(exp_name, read_exp(), read_exp())

    elif exp_name == 'times':
        return Times(exp_name, read_exp(), read_exp())

    elif exp_name == 'divide':
        return Divide(exp_name, read_exp(), read_exp())

    elif exp_name == 'lt':
        return Lt(exp_name, read_exp(), read_exp())

    elif exp_name == 'le':
        return Le(exp_name, read_exp(), read_exp())

    elif exp_name == 'eq':
        return Eq(exp_name, read_exp(), read_exp())

    elif exp_name == 'not':
        return Not(exp_name, read_exp())

    elif exp_name == 'negate':
        return Negate(exp_name, read_exp())

    elif exp_name == 'integer':
        return (exp_name, int(get_line()))

    elif exp_name == 'string':
        return (exp_name, get_line())

    elif exp_name == 'identifier':
        return (exp_name, read_identifier())

    elif exp_name == 'true':
        return (exp_name)

    elif exp_name =='false':
        return (exp_name)

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

def main():
    global ast_lines
    if len(sys.argv) < 2:
        print("Specify .cl-ast input file.")
        exit()

    with open(sys.argv[1]) as f:
        ast_lines = [l.rstrip() for l in f.readlines()]

    ast = read_ast()

    ### check if class is defined more than once
    for i, cls in enumerate(ast):
        for j, target_cls in enumerate(ast):
            if i!=j and cls.name_iden.ident == target_cls.name_iden.ident:
                print "ERROR: " + cls.name_iden.line_num + ":"\
                    "Type-Check: Class defined multiple times:"\
                    + cls.name_iden.ident + "\n"
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
                    + cls.inherits_iden.ident + "\n"
                exit()


    ### successful type checking, print AAST
    print str(len(ast))
    for cls in ast:
        print cls

if __name__ == '__main__':
    main()
