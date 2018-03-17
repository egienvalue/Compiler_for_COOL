class Expression(object):
    line_num = None
    exp_type = "No_TYPE"

    def s(self):
        ret = str(self.line_num) + "\n"
        ret += str(self.exp_type) + "\n"
        return ret

    def __init__(self, _line_num, _exp_type):
        self.line_num = _line_num
        self.exp_type = _exp_type

    def __repr__(self):
        return str(self)

class Internal(Expression):
    extra_detail = None

    def __init__(self, _line_num, _exp_type, _extra_detail):
        Expression.__init__(self, _line_num, _exp_type)
        self.extra_detail = _extra_detail

    def __str__(self):
        ret = self.s()
        ret += "internal\n"
        ret += self.extra_detail + "\n"
        return ret

class Integer(Expression):
    int_val = None

    def __init__(self, _line_num, _exp_type, _int_val):
        Expression.__init__(self, _line_num, _exp_type)
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

    def __init__(self, _line_num, _exp_type, _str_val):
        Expression.__init__(self, _line_num, _exp_type)
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
    def __init__(self, _line_num, _exp_type):
        Expression.__init__(self, _line_num, _exp_type)
        self.exp_type = "Bool"

    def __str__(self):
        ret = self.s()
        ret += "true\n"
        return ret

class FalseExp(Expression):
    def __init__(self, _line_num, _exp_type):
        Expression.__init__(self, _line_num, _exp_type)
        self.exp_type = "Bool"

    def __str__(self):
        ret = self.s()
        ret += "false\n"
        return ret

class IdentifierExp(Expression):
    ident = None
    def __init__(self, _line_num, _exp_type, _ident):
        Expression.__init__(self, _line_num, _exp_type)
        self.ident = _ident

    def __str__(self):
        ret = self.s()
        ret += "identifier\n" 
        ret += str(self.ident)
        return ret

class New(Expression):
    ident = None

    def __init__(self, _line_num, _exp_type, _ident):
        Expression.__init__(self, _line_num, _exp_type)
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

    def __init__(self, _line_num, _exp_type, _ident, _exp):
        Expression.__init__(self, _line_num, _exp_type)
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

    def __init__(self, _line_num, _exp_type, _binding_list, _exp):
        Expression.__init__(self, _line_num, _exp_type)
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
    
    def __init__(self, _line_num, _exp_type, _exp, _element_list):
        Expression.__init__(self, _line_num, _exp_type)
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

    def __init__(self, _line_num, _exp_type, _exp, _method_ident, _args):
        Expression.__init__(self, _line_num, _exp_type)

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

    def __init__(self, _line_num, _exp_type, _exp, _type_ident, _method_ident, _args):
        Expression.__init__(self, _line_num, _exp_type)
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

    def __init__(self, _line_num, _exp_type, _method_ident, _args):
        Expression.__init__(self, _line_num, _exp_type)
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

    def __init__ (self, _line_num, _exp_type, _predicate, _then_body, _else_body):
        Expression.__init__(self, _line_num, _exp_type)
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

    def __init__(self, _line_num, _exp_type, _predicate, _body):
        Expression.__init__(self, _line_num, _exp_type)
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
    def __init__(self, _line_num, _exp_type, _exp_list):
        Expression.__init__(self, _line_num, _exp_type)
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
    def __init__(self, _line_num, _exp_type, _exp):
        Expression.__init__(self, _line_num, _exp_type)
        self.exp = _exp

    def __str__(self):
        ret = self.s()
        ret += "isvoid\n"
        ret += str(self.exp)

        return ret

class Plus(Expression):
    lhs = None
    rhs = None

    def __init__(self, _line_num, _exp_type, _lhs, _rhs):
        Expression.__init__(self, _line_num, _exp_type)
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

    def __init__(self, _line_num, _exp_type, _lhs, _rhs):
        Expression.__init__(self, _line_num, _exp_type)
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

    def __init__(self, _line_num, _exp_type, _lhs, _rhs):
        Expression.__init__(self, _line_num, _exp_type)
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

    def __init__(self, _line_num, _exp_type, _lhs, _rhs):
        Expression.__init__(self, _line_num, _exp_type)
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

    def __init__(self, _line_num, _exp_type, _lhs, _rhs):
        Expression.__init__(self, _line_num, _exp_type)
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

    def __init__(self, _line_num, _exp_type, _lhs, _rhs):
        Expression.__init__(self, _line_num, _exp_type)
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

    def __init__(self, _line_num, _exp_type, _lhs, _rhs):
        Expression.__init__(self, _line_num, _exp_type)
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

    def __init__(self, _line_num, _exp_type, _exp):
        Expression.__init__(self, _line_num, _exp_type)
        self.exp = _exp

    def __str__(self):
        ret = self.s()
        ret += "not\n"
        ret += str(self.exp)

        return ret

class Negate(Expression):
    exp = None

    def __init__(self, _line_num, _exp_type, _exp):
        Expression.__init__(self, _line_num, _exp_type)
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

