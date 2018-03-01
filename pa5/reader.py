from cool_classes import *


def get_line():
    global cl_type_lines
    if cl_type_lines == []:
        return
    return cl_type_lines.pop(0)

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
    exp_type = get_line() # NEW
    exp_name = get_line()

    # NEW
    if exp_name == 'internal':
        extra_detail = get_line()
        return Internal(line_number, exp_type, extra_detail)

    elif exp_name == 'assign':
        assignee = read_identifier()
        rhs = read_exp()
        return Assign(line_number, exp_type, assignee, rhs)

# edit by Jun
    elif exp_name == 'let':
        num_bindings = int(get_line())
        binding_list = []
        for i in range(num_bindings):
            binding_list.append(read_binding())
        let_body = read_exp()
        return Let(line_number, exp_type, binding_list, let_body)
      
# edit by Jun
    elif exp_name == 'case':
        case_exp = read_exp()
        num_case_elem = int(get_line())
        case_elem_list = []
        for i in range(num_case_elem):
           case_elem_list.append(read_case_elem())
        return Case(line_number, exp_type, case_exp, case_elem_list)


    elif exp_name == 'dynamic_dispatch':
        obj_name = read_exp()
        method_name = read_identifier()
        num_args = int(get_line())
        args = []
        for i in range(num_args):
            args.append(read_exp())

        return Dynamic_Dispatch(line_number, exp_type, obj_name, method_name, args)

    elif exp_name == 'static_dispatch':
        obj_name = read_exp()
        type_name = read_identifier()
        method_name = read_identifier()
        num_args = int(get_line())
        args = []
        for i in range(num_args):
            args.append(read_exp())

        return Static_Dispatch(line_number, exp_type, obj_name, type_name, method_name, args)

    elif exp_name == 'self_dispatch':
        method_name = read_identifier()
        num_args = int(get_line())
        args = []
        for i in range(num_args):
            args.append(read_exp())

        return Self_Dispatch(line_number, exp_type, method_name, args)

    elif exp_name == 'if':
        predicate = read_exp()
        then_body = read_exp()
        else_body = read_exp()

        return  If(line_number, exp_type, predicate, then_body, else_body)

    elif exp_name == 'while':
        predicate = read_exp()
        body_exp = read_exp()

        return While(line_number, exp_type,predicate, body_exp)

    elif exp_name == 'block':
        num_exps = int(get_line())
        exps = []
        for i in range(num_exps):
            exps.append(read_exp())

        return Block(line_number, exp_type, exps)

    elif exp_name == 'new':
        return New(line_number, exp_type, read_identifier())


    elif exp_name == 'isvoid':
        return Isvoid(line_number, exp_type, read_exp())

    elif exp_name == 'plus':
        return Plus(line_number, exp_type, read_exp(), read_exp())

    elif exp_name == 'minus':
        return Minus(line_number, exp_type, read_exp(), read_exp())

    elif exp_name == 'times':
        return Times(line_number, exp_type, read_exp(), read_exp())

    elif exp_name == 'divide':
        return Divide(line_number, exp_type, read_exp(), read_exp())

    elif exp_name == 'lt':
        return Lt(line_number, exp_type, read_exp(), read_exp())

    elif exp_name == 'le':
        return Le(line_number, exp_type, read_exp(), read_exp())

    elif exp_name == 'eq':
        return Eq(line_number, exp_type, read_exp(), read_exp())

    elif exp_name == 'not':
        return Not(line_number, exp_type, read_exp())

    elif exp_name == 'negate':
        return Negate(line_number, exp_type, read_exp())

    elif exp_name == 'integer':
        return Integer(line_number, exp_type, int(get_line()))

    elif exp_name == 'string':
        return String(line_number, exp_type, get_line())

    elif exp_name == 'identifier':
        return IdentifierExp(line_number, exp_type, read_identifier())

    elif exp_name == 'true':
        return TrueExp(line_number, exp_type)

    elif exp_name =='false':
        return FalseExp(line_number, exp_type)

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


def read_class_map():
    class_map = {}
    num_classes = int(get_line())
    for i in range(num_classes):
        cls_name = get_line()
        class_map[cls_name] = []
        num_attr = int(get_line())
        for j in range(num_attr):
            attr_init = get_line()
            attr_name = Identifier("no_num",get_line())
            attr_type = Identifier("no_num",get_line())
            if attr_init == "no_initializer":
                attr_instance = Attribute(attr_name, attr_type, False, None)
                class_map[cls_name].append(attr_instance)
            elif attr_init == "initializer":
                attr_exp = read_exp()
                attr_instance = Attribute(attr_name, attr_type, True, attr_exp)
                class_map[cls_name].append(attr_instance)
    return class_map

def read_imp_map():
    imp_map = {}
    num_classes = int(get_line())
    for i in range(num_classes):
        cls_name = get_line()
        imp_map[cls_name] = []
        num_method = int(get_line())
        for j in range(num_method):
            method_name = Identifier("no_num",get_line())
            num_formal = int(get_line())
            formals = []
            for m in range(num_formal):
                formal_name = Identifier("no_num",get_line())
                formals.append(Formal(formal_name, Identifier("no_num","Formal_type")))
            src_class = get_line()
            method_body = read_exp()
            method_instance = Method(method_name, formals,
                    Identifier("no_num","Method_type"),
                                    method_body)
            imp_map[cls_name].append((src_class,method_instance))
    return imp_map 


def read_parent_map():
    parent_map = {}
    num = int(get_line())
    for i in range(num):
        child = get_line()
        parent = get_line()
        parent_map[child] = parent
    return parent_map

def read_aast():
    num_classes = int(get_line())
    class_list = []
    for i in range(num_classes):
        class_list.append(read_class())

    return class_list 


def read_type_file(filename):
    global cl_type_lines
    with open(filename) as f:
        cl_type_lines = [l[:-1] for l in f.readlines()]
    
    for i in range(3):
        read_type = get_line()
        if read_type == "class_map":
            class_map = read_class_map()
        elif read_type == "implementation_map":
            imp_map = read_imp_map()
        elif read_type == "parent_map":
            parent_map = read_parent_map()
        else:
            print "reader bug"
            exit()
    aast = read_aast()
    return class_map, imp_map, parent_map, aast
