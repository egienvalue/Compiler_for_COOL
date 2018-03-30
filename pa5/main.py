import sys
import reader as rd
from asm_classes import *
from cool_classes import *
from num_temp import *
self_reg = R(12)
acc_reg = R(13)
temp_reg = R(14)
self_reg_d = R(12,"d")
acc_reg_d = R(13, "d")
temp_reg_d = R(14, "d")

tab_6 = "{:<24}".format("")
tab_3 = "{:<12}".format("")

rax = RAX()
eax = EAX()
rbx = RBX() 
rcx = RCX() 
rdx = RDX()
rsi = RSI() 
rdi = RDI()
edi = EDI()
rbp = RBP() 
rsp = RSP()
r8  = R(8)
r9  = R(9)
r10 = R(10) 
r11 = R(11)
r15 = R(15)

int_context_offset = 24

# use these variables to keep tracking info
label = 0
#string_map = {"the.empty.string":"", "percent.d":"%ld", "percent.ld":" %ld"}
string_map = {}
symbol_table = {}
ocuppied_temp = []
class_tag = {"Bool":0, "Int":1, "String":3}

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

def attr2asm(cls_name, attributes):
    global class_map
    global imp_map
    global parent_map
    global aast

    # this function is used to print attribute constructor

    if attributes != [] :
        ret = tab_6 + "## initialize attributes\n"
    else:
        ret = ""
    for i, attr in enumerate(attributes):
        # insert into symbol_table
        symbol_table[attr.attr_name.ident] = [str(MEM(24 + 8*i, self_reg))]
        ret += tab_6 +  "## self[%d] holds field %s (%s)\n" % (i+3,
                attr.attr_name.ident, attr.attr_type.ident)
        if attr.attr_type.ident in ["String", "Int", "Bool"]:
            ret += tab_6 + "## new %s\n" % attr.attr_type.ident
            ret += str(PUSH("q",rbp)) + "\n"
            ret += str(PUSH("q",self_reg)) + "\n"
            ret += str(MOV("q", "$%s..new" % attr.attr_type.ident, temp_reg)) + "\n"
            ret += str(CALL(temp_reg)) + "\n"
            ret += str(POP("q", self_reg)) + "\n"
            ret += str(POP("q", rbp)) + "\n"
            ret += str(MOV("q", acc_reg, MEM(24+8*i, self_reg))) + "\n"
        else:
            ret += str(MOV("q", "$0", acc_reg)) + "\n"
            ret += str(MOV("q", acc_reg, MEM(24+8*i, self_reg))) + "\n"
    
    for i, attr in enumerate(attributes):
        if attr.exp != None:
            ret+= tab_6 + "## self[%d] %s initializer <- %s\n" % \
                (i+3,attr.attr_name.ident,str(attr.exp.exp_type))  
            ret += cgen(cls_name,attr.exp) 
            ret += str(MOV("q", acc_reg, MEM(24+8*i, self_reg))) + "\n"
        else:
            ret+= tab_6 + "## self[%d] %s initializer -- none " % \
                    (i+3, attr.attr_name.ident) + "\n"
    return ret

def cgen(cur_cls,exp):
    ret = ""
    global label
    global vtable_map
    global symbol_table
    
    if isinstance(exp, Internal):
        return inter_cgen(exp.extra_detail)

    elif isinstance(exp, IdentifierExp):
        ## b
        #                movq 32(%r12), %r13
        variable_name = exp.ident.ident
        if variable_name == "self" :
            ret +=  str(MOV("q", self_reg, acc_reg)) +"\n"
        else:
            ret += tab_6 + "## %s\n" % variable_name
            ret += str(MOV("q", symbol_table[variable_name][-1], acc_reg)) + "\n"
        return ret

    elif isinstance(exp, New):
        ret += tab_6 + "## new %s" % exp.exp_type + "\n"
        if exp.exp_type =="SELF_TYPE":
            ret += str(PUSH("q", rbp)) + "\n"
            ret += str(PUSH("q", self_reg)) + "\n"
            ret += tab_6 + "## obtain vtable for self object\n"
            ret += str(MOV("q", MEM(16, self_reg), temp_reg)) + "\n"
            ret += tab_6 + "## look up constructor at offset 1 in vtable\n"
            ret += str(MOV("q", MEM(8,temp_reg), temp_reg)) + "\n"
            ret += str(CALL(temp_reg)) + "\n"
            ret += str(POP("q", self_reg)) + "\n"
            ret += str(POP("q", rbp)) + "\n"
            return ret
        ret += str(PUSH("q", rbp)) + "\n"
        ret += str(PUSH("q", self_reg)) + "\n"
        ret += str(MOV("q","$%s..new" % exp.exp_type, temp_reg)) + "\n"
        ret += str(CALL(temp_reg)) + "\n"
        ret += str(POP("q", self_reg)) + "\n"
        ret += str(POP("q", rbp)) + "\n"
        return ret

    elif isinstance(exp, (TrueExp, FalseExp)):
        ret += cgen(cur_cls,New(0, "Bool", None))
        if isinstance(exp, TrueExp):
            ret += str(MOV("q", "$1", temp_reg)) + "\n"
            ret += str(MOV("q", temp_reg, MEM(int_context_offset, acc_reg))) + "\n"
        return ret
 
    elif isinstance(exp, String):
        ret += cgen(cur_cls,New(0,"String",None)) 
        # Creat space store new string
        ## string10 holds "hello world"
        #                movq $string10, %r14
        #                movq %r14, 24(%r13)
        string_key = "string%d" % (len(string_map) + 1)
        string_val = exp.str_val
        if string_val in string_map.values():
            string_key = [key for key,val in string_map.iteritems() if val ==
                            string_val][0] 
        else:
            string_map[string_key] = string_val
        ret += tab_6 + "## %s holds \"%s\"" % (string_key, string_val) + "\n"
        ret += str(MOV("q", "$"+string_key, temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(24, acc_reg))) + "\n"
        return ret

    elif isinstance(exp, Integer): 

        ret += cgen(cur_cls,New(0,"Int",None))
        ret += str(MOV("q", "$%d" % exp.int_val, temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(int_context_offset, acc_reg))) + "\n"
        return ret


    elif isinstance(exp, Plus):
        free_temp_mem = MEM(0-8*len(ocuppied_temp),rbp)
        ret += cgen(cur_cls,exp.lhs) 
        # lhs address in acc_reg
        ret += str(MOV("q", MEM(int_context_offset, acc_reg), acc_reg)) + "\n"
        ret += str(MOV("q", acc_reg, free_temp_mem)) + "\n"
        ocuppied_temp.append(free_temp_mem)
        ret += cgen(cur_cls,exp.rhs)
        # lhs address in acc_reg
        ret += str(MOV("q", MEM(int_context_offset, acc_reg), acc_reg)) + "\n"
        ret += str(MOV("q", free_temp_mem, temp_reg)) + "\n"
        if isinstance(exp, Plus):
            ret += str(ADD("q", temp_reg, acc_reg)) + "\n"
        else:
            # different to official compiler TODO
            ret += str(SUB("q", temp_reg, acc_reg)) + "\n"
        ret += str(MOV("q", acc_reg, free_temp_mem)) + "\n"

        ret += cgen(cur_cls,New(0,"Int",None))
        # lhs address in acc_reg
        ret += str(MOV("q", free_temp_mem, temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(int_context_offset, acc_reg))) + "\n"
        ocuppied_temp.pop() 
        return ret

    elif isinstance(exp, Minus):
        free_temp_mem = MEM(0-8*len(ocuppied_temp),rbp)
        ret += cgen(cur_cls,exp.lhs) 

        # lhs address in acc_reg
        ret += str(MOV("q", MEM(int_context_offset, acc_reg), acc_reg)) + "\n"
        ret += str(MOV("q", acc_reg, free_temp_mem)) + "\n"
        ocuppied_temp.append(free_temp_mem)
        ret += cgen(cur_cls,exp.rhs)
        # lhs address in acc_reg
        ret += str(MOV("q", MEM(int_context_offset, acc_reg), acc_reg)) + "\n"
        ret += str(MOV("q", free_temp_mem, temp_reg)) + "\n"

        # Code for Minus Operation
        #                movq %r14, %rax
	#		subq %r13, %rax
	#		movq %rax, %r13
        #                movq %r13, 0(%rbp)
        ret += str(MOV("q", temp_reg, rax)) + "\n"
        ret += str(SUB("q", acc_reg, rax)) + "\n"
        ret += str(MOV("q", rax, acc_reg)) + "\n"

        # store back to temporary location of MEM
        ret += str(MOV("q", acc_reg, free_temp_mem)) + "\n"

        ret += cgen(cur_cls,New(0,"Int",None))
        # lhs address in acc_reg
        ret += str(MOV("q", free_temp_mem, temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(int_context_offset, acc_reg))) + "\n"
        ocuppied_temp.pop()
        return ret


    elif isinstance(exp, Times):
        free_temp_mem = MEM(0-8*len(ocuppied_temp),rbp)
        ret += cgen(cur_cls,exp.lhs) 

        # lhs address in acc_reg
        ret += str(MOV("q", MEM(int_context_offset, acc_reg), acc_reg)) + "\n"
        ret += str(MOV("q", acc_reg, free_temp_mem)) + "\n"
        
        ocuppied_temp.append(free_temp_mem) 
        
        ret += cgen(cur_cls,exp.rhs)
        # lhs address in acc_reg
        ret += str(MOV("q", MEM(int_context_offset, acc_reg), acc_reg)) + "\n"
        ret += str(MOV("q", free_temp_mem, temp_reg)) + "\n\n"

        # Code for Times Operation
        #movq %r14, %rax
        #imull %r13d, %eax
        #shlq $32, %rax
        #shrq $32, %rax
        #movl %eax, %r13d
        ret += str(MOV("q", temp_reg, rax)) + "\n"
        ret += str(IMUL("l", acc_reg_d, eax)) + "\n"
        ret += str(SHL("q", "$32", rax)) + "\n"
        ret += str(SHR("q", "$32", rax)) + "\n"
        ret += str(MOV("l", eax, acc_reg_d)) + "\n"

        # store back to temporary location of MEM
        ret += str(MOV("q", acc_reg, free_temp_mem)) + "\n"

        ret += cgen(cur_cls,New(0,"Int",None))
        # lhs address in acc_reg
        ret += str(MOV("q", free_temp_mem, temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(int_context_offset, acc_reg))) + "\n"
        ocuppied_temp.pop()
        return ret
    
    elif isinstance(exp, Divide):
        free_temp_mem = MEM(0-8*len(ocuppied_temp),rbp)
        ret += cgen(cur_cls,exp.lhs) 

        # lhs address in acc_reg
        ret += str(MOV("q", MEM(int_context_offset, acc_reg), acc_reg)) + "\n"
        ret += str(MOV("q", acc_reg, free_temp_mem)) + "\n"
       
        ocuppied_temp.append(free_temp_mem)

        ret += cgen(cur_cls,exp.rhs)
        # lhs address in acc_reg

        # Code for Divide Operation:

        ret += str(MOV("q", MEM(int_context_offset, acc_reg), temp_reg)) + "\n"
        ret += str(CMP("q", "$0", temp_reg)) + "\n"
        label = label +1
        ret += str(JNE("l%d" % label)) + "\n"
        # successfully perform jump operand, label plus one
        
        # Creat Space for Exception String
        string_key = "string%d" % (len(string_map) + 1)
        string_val = "ERROR: %s: Exception: division by zero\\n" % exp.line_num
        if string_val in string_map.values():
            string_key = [key for key,val in string_map.iteritems() if val ==
                            string_val][0] 
        else:
            string_map[string_key] = string_val
        ret += str(MOV("q", "$"+string_key, acc_reg)) + "\n"
        ret += str(MOV("q", acc_reg, rdi)) + "\n"
        
        ret += str(CALL("cooloutstr")) + "\n"
        ret += str(MOV("l", "$0", edi)) + "\n"
        ret += str(CALL("exit")) + "\n"
        ret += ".globl l%d" % label + "\n"
        ret += "{: <24}".format("l%d:" % label) + "## division is OK\n"
        ret += str(MOV("q", MEM(int_context_offset, acc_reg), acc_reg)) + "\n"
        ret += str(MOV("q", free_temp_mem, temp_reg)) + "\n\n"
        ret += str(MOV("q", "$0", rdx)) + "\n"
        ret += str(MOV("q", temp_reg, rax)) + "\n"
        ret += "cdq\n"
        ret += str(IDIV("l", acc_reg_d)) + "\n"
        ret += str(MOV("q", rax, acc_reg)) + "\n"

        # store back to temporary location of MEM
        ret += str(MOV("q", acc_reg, free_temp_mem)) + "\n"

        ret += cgen(cur_cls,New(0,"Int",None))
        # lhs address in acc_reg
        ret += str(MOV("q", free_temp_mem, temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(int_context_offset, acc_reg))) + "\n"
        ocuppied_temp.pop()
        return ret

    elif isinstance(exp, Let):
        for idx, binding in enumerate(exp.binding_list):
            ret += tab_6 + "## fp[%d] holds local %s (%s)\n" % (0-len(ocuppied_temp),
                    binding.var_ident.ident, binding.type_ident.ident)
            free_temp_mem = MEM(0-8*len(ocuppied_temp),rbp)
            ocuppied_temp.append(free_temp_mem)
            ret += cgen(cur_cls,binding)
            # Code for storing the binding back to stack
            if binding.var_ident.ident in symbol_table.keys():
                symbol_table[binding.var_ident.ident].append(str(free_temp_mem))
            else:
                symbol_table[binding.var_ident.ident] = [str(free_temp_mem)]

            # movq %r13, 0(%rbp)
            ret += str(MOV("q", acc_reg, \
                symbol_table[binding.var_ident.ident][-1])) + "\n"
        ret += cgen(cur_cls,exp.exp)

        for binding in exp.binding_list:
            ocuppied_temp.pop()
            symbol_table[binding.var_ident.ident].pop()
            if symbol_table[binding.var_ident.ident] == []:
                symbol_table.pop(binding.var_ident.ident)
        return ret

    elif isinstance(exp, Binding):
        if exp.value_exp == None:
            if exp.type_ident.ident in ["Bool","Int", "IO"]:
                ret += cgen(cur_cls,New(0,exp.type_ident.ident,None))
            elif exp.type_ident.ident in ["String"]:
                ret += cgen(cur_cls,New(0,exp.type_ident.ident,None))
                ret += str(MOV("q", "$the.empty.string", r15)) + "\n"
                ret += str(MOV("q", r15, MEM(24+8*0, acc_reg))) + "\n" 
            else:
                ret += str(MOV("q", "$0", acc_reg)) + "\n"

        else:
            ret += cgen(cur_cls,exp.value_exp)
        return ret

    elif isinstance(exp, Case):
        free_temp_mem = MEM(0-8*len(ocuppied_temp),rbp)

        br_label_map = {}
        ret += tab_6 + "## case expression begins\n"
        ret += cgen(cur_cls,exp.exp)

        # detect void case
        ret += str(CMP("q", "$0", acc_reg))+ "\n"
        label += 1
        ret += str(JE("l%d" % label)) + "\n"
        br_label_map["void"] = label
        # store acc_reg to temp0

        ret += str(MOV("q", acc_reg, free_temp_mem)) + "\n"
        # store case.exp class tag to acc reg
        ret += str(MOV("q", MEM(0, acc_reg), acc_reg)) + "\n"

        br_cls_list = []
        fix_br_label = []
        for idx, case_ele in enumerate(exp.element_list):
            label += 1
            if case_ele.type_ident.ident == "SELF_TYPE":
                case_ele_type = cur_cls
            else:
                case_ele_type = case_ele.type_ident.ident
            br_label_map[case_ele_type] = label
            fix_br_label.append(case_ele.type_ident.ident)
            ret += tab_6 + "## case %s will jump to l%d" % \
                            (case_ele.type_ident.ident, label) + "\n"

        ret += tab_6 + "## case expression: compare type tags\n"
        
        # traverse all classes, dectect the jmp label
        label += 1
        error_case_label = label
        label += 1
        case_end_label = label
        for idx,cls_name in enumerate(sorted(class_map.keys())):
            if cls_name not in fix_br_label:
                for cls in fix_br_label:
                # update label
                    if cls == find_common_ancestor(cls, cls_name):
                        br_label_map[cls_name] = br_label_map[cls]
                        break

        for idx,cls_name in enumerate(sorted(class_map.keys())):
            if cls_name in br_label_map.keys():
                ret += str(MOV("q", "$%d" % class_tag[cls_name], temp_reg))+"\n"
                ret += str(CMP("q", temp_reg, acc_reg)) + "\n"
                ret += str(JE("l%d" % br_label_map[cls_name])) + "\n"
            else: 
                ret += str(MOV("q", "$%d" % class_tag[cls_name], temp_reg))+"\n"
                ret += str(CMP("q", temp_reg, acc_reg)) + "\n"
                ret += str(JE("l%d" % error_case_label)) + "\n"

        # cgen for every branch
        # for error case
        ret += ".globl l%d\n" % error_case_label
        ret += "{: <24}".format("l%d:" % error_case_label)
        ret += "## case expression: error case\n"

        string_key = "string%d" % (len(string_map) + 1)
        string_val = "ERROR: %s: Exception: case without matching branch\\n"\
                % exp.line_num
        if string_val in string_map.values():
            string_key = [key for key,val in string_map.iteritems() if val ==
                            string_val][0] 
        else:
            string_map[string_key] = string_val

        ret += str(MOV("q", "$%s" % string_key, acc_reg)) + "\n"
        ret += str(MOV("q", acc_reg, rdi)) + "\n"
        ret += str(CALL("cooloutstr")) + "\n"
        ret += str(MOV("l", "$0", edi)) + "\n"
        ret += str(CALL("exit")) + "\n"

        # for void case
        ret += ".globl l%d\n" % br_label_map["void"]
        ret += "{: <24}".format("l%d:" % br_label_map["void"])
        ret += "## case expression: void case\n"

        string_key = "string%d" % (len(string_map) + 1)
        string_val = "ERROR: %s: Exception: case on void\\n"\
                % exp.line_num
        if string_val in string_map.values():
            string_key = [key for key,val in string_map.iteritems() if val ==
                            string_val][0] 
        else:
            string_map[string_key] = string_val

        ret += str(MOV("q", "$%s" % string_key, acc_reg)) + "\n"
        ret += str(MOV("q", acc_reg, rdi)) + "\n"
        ret += str(CALL("cooloutstr")) + "\n"
        ret += str(MOV("l", "$0", edi)) + "\n"
        ret += str(CALL("exit")) + "\n"

        # cgen for branch in case exp!!!
        ret += tab_6 + "## case expression: branches\n"
        
        for idx, case_ele in enumerate(exp.element_list):
            if case_ele.type_ident.ident == "SELF_TYPE":
                case_ele_type = cur_cls
            else:
                case_ele_type = case_ele.type_ident.ident 
            ret += ".globl l%d\n" % br_label_map[case_ele_type]
            ret += "{: <24}".format("l%d:" % \
                    br_label_map[case_ele_type]) 
            ret += "## fp[%d] holds case %s (%s)" % (0-len(ocuppied_temp),
                    case_ele.var_ident.ident, case_ele_type) + "\n"
            
            free_temp_mem = MEM(0-8*len(ocuppied_temp),rbp)
            ocuppied_temp.append(free_temp_mem)

            # add it to symbol table
            if case_ele.var_ident.ident in symbol_table.keys():
                symbol_table[case_ele.var_ident.ident].append(str(free_temp_mem))
            else:
                symbol_table[case_ele.var_ident.ident] = [str(free_temp_mem)]

            ret += cgen(cur_cls,case_ele.body_exp)
             
            ocuppied_temp.pop()
            symbol_table[case_ele.var_ident.ident].pop()
            if symbol_table[case_ele.var_ident.ident] == []:
                symbol_table.pop(case_ele.var_ident.ident)
            ret += str(JMP("l%d" % case_end_label)) + "\n"

        ret += ".globl l%d\n" % case_end_label 
        ret += "{: <24}".format("l%d:" % case_end_label) + "## case expression ends\n"
        return ret

    elif isinstance(exp, Self_Dispatch):
        ret += tab_6 + "## %s(...)" % exp.method_ident.ident + "\n"
        ret += str(PUSH("q", self_reg)) + "\n"
        ret += str(PUSH("q", rbp)) + "\n"
        for idx, arg in enumerate(exp.args):
            ret += cgen(cur_cls,arg)
            ret += str(PUSH("q", acc_reg)) + "\n"
        ret += str(PUSH("q", self_reg)) + "\n"

        ret += tab_6 + "## obtain vtable for self object of type %s\n" % cur_cls 
        ret += str(MOV("q", MEM(16, self_reg), temp_reg)) + "\n"
        vtable_offset = [idx for idx,method_name in
                enumerate(vtable_map[cur_cls]) if method_name.split('.')[1] ==
                exp.method_ident.ident]
        #print cur_cls
        #print exp.method_ident.ident
        vtable_offset = vtable_offset[0]+2
        ret += tab_6 + "## look up %s() at offset %d in vtable\n" % (exp.method_ident.ident, vtable_offset)   
        ret += str(MOV("q", MEM(vtable_offset*8, temp_reg), temp_reg)) + "\n"
        ret += str(CALL(temp_reg)) + "\n"
        ret += str(ADD("q", "$%d" % ((len(exp.args)+1)*8), rsp)) + "\n"
        ret += str(POP("q", rbp)) + "\n"
        ret += str(POP("q", self_reg)) + "\n"
        return ret

    elif isinstance(exp, Static_Dispatch):
        ret += "## %s(...)" % exp.method_ident.ident + "\n"
        #save self and rbp register
        ret += str(PUSH("q", self_reg)) + "\n"
        ret += str(PUSH("q", rbp)) + "\n"

        # cgen for arguments
        for idx, arg in enumerate(exp.args):
            ret += cgen(cur_cls,arg)
            ret += str(PUSH("q", acc_reg)) + "\n"

        # cgen for expression before .
        ret += cgen(cur_cls, exp.exp)
        # Dectect dispatch on void
        ret += str(CMP("q", "$0", acc_reg)) + "\n"
        label += 1
        ret += str(JNE("l%d" % label)) + "\n"
        # Allocation new string to store exceptions
        string_key = "string%d" % (len(string_map) + 1)
        string_val = "ERROR: %s: Exception: dispatch on void\\n" % exp.line_num
        if string_val in string_map.values():
            string_key = [key for key,val in string_map.iteritems() if val ==
                            string_val][0] 
        else:
            string_map[string_key] = string_val
        ret += str(MOV("q", "$%s" % string_key, acc_reg)) + "\n"
        ret += str(MOV("q", acc_reg, rdi)) + "\n"
        ret += str(CALL("cooloutstr")) + "\n"
        ret += str(MOV("l", "$0", edi)) + "\n"
        ret += str(CALL("exit")) + "\n"

        # if no dispatch on void jump to
        ret += ".globl l%d\n" % label
        ret += "{: <24}".format("l%d:" % label) 
        ret += str(PUSH("q", acc_reg)) + "\n"

        ret += tab_6 + "## obtain vtable for class %s\n" % exp.type_ident.ident
        ret += str(MOV("q", "$%s..vtable" % exp.type_ident.ident, temp_reg)) + "\n"

        if exp.type_ident.ident == "SELF_TYPE":
            vtable_key = cur_cls
        else:
            vtable_key = exp.type_ident.ident
        vtable_offset = [idx for idx,method_name in
                enumerate(vtable_map[vtable_key]) if method_name.split('.')[1] ==
                exp.method_ident.ident]
        #print cur_cls
        #print exp.method_ident.ident
        vtable_offset = vtable_offset[0]+2
        ret += tab_6 + "## look up %s() at offset %d in vtable\n" % (exp.method_ident.ident, vtable_offset)   
        ret += str(MOV("q", MEM(vtable_offset*8, temp_reg), temp_reg)) + "\n"
        ret += str(CALL(temp_reg)) + "\n"
        ret += str(ADD("q", "$%d" % ((len(exp.args)+1)*8), rsp)) + "\n"
        ret += str(POP("q", rbp)) + "\n"
        ret += str(POP("q", self_reg)) + "\n"
        return ret


    elif isinstance(exp, Dynamic_Dispatch):
        ret += "## %s(...)" % exp.method_ident.ident + "\n"
        #save self and rbp register
        ret += str(PUSH("q", self_reg)) + "\n"
        ret += str(PUSH("q", rbp)) + "\n"

        # cgen for arguments
        for idx, arg in enumerate(exp.args):
            ret += cgen(cur_cls,arg)
            ret += str(PUSH("q", acc_reg)) + "\n"

        # cgen for expression before .
        ret += cgen(cur_cls, exp.exp)
        # Dectect dispatch on void
        ret += str(CMP("q", "$0", acc_reg)) + "\n"
        label += 1
        ret += str(JNE("l%d" % label)) + "\n"
        # Allocation new string to store exceptions
        string_key = "string%d" % (len(string_map) + 1)
        string_val = "ERROR: %s: Exception: dispatch on void\\n" % exp.line_num
        if string_val in string_map.values():
            string_key = [key for key,val in string_map.iteritems() if val ==
                            string_val][0] 
        else:
            string_map[string_key] = string_val
        ret += str(MOV("q", "$%s" % string_key, acc_reg)) + "\n"
        ret += str(MOV("q", acc_reg, rdi)) + "\n"
        ret += str(CALL("cooloutstr")) + "\n"
        ret += str(MOV("l", "$0", edi)) + "\n"
        ret += str(CALL("exit")) + "\n"

        # if no dispatch on void jump to
        ret += ".globl l%d\n" % label
        ret += "{: <24}".format("l%d:" % label) 
        ret += str(PUSH("q", acc_reg)) + "\n"

        ret += tab_6 + "## obtain vtable from object in r1 with static type %s\n" % exp.exp.exp_type
        ret += str(MOV("q", MEM(16, acc_reg), temp_reg)) + "\n"
        if exp.exp.exp_type == "SELF_TYPE":
            vtable_key = cur_cls
        else:
            vtable_key = exp.exp.exp_type
        vtable_offset = [idx for idx,method_name in
                enumerate(vtable_map[vtable_key]) if method_name.split('.')[1] ==
                exp.method_ident.ident]
        #print cur_cls
        #print exp.method_ident.ident
        vtable_offset = vtable_offset[0]+2
        ret += tab_6 + "## look up %s() at offset %d in vtable\n" % (exp.method_ident.ident, vtable_offset)   
        ret += str(MOV("q", MEM(vtable_offset*8, temp_reg), temp_reg)) + "\n"
        ret += str(CALL(temp_reg)) + "\n"
        ret += str(ADD("q", "$%d" % ((len(exp.args)+1)*8), rsp)) + "\n"
        ret += str(POP("q", rbp)) + "\n"
        ret += str(POP("q", self_reg)) + "\n"
        return ret

    elif isinstance(exp, Block):
        for block_exp in exp.exp_list:
            ret += cgen(cur_cls,block_exp)
        return ret
    
    elif isinstance(exp, Assign):
        ret += cgen(cur_cls, exp.exp)
        ret += str(MOV("q", acc_reg, symbol_table[exp.ident.ident][-1])) + "\n"
        return ret

    elif isinstance(exp, Lt):
        ret += str(PUSH("q", self_reg)) + "\n"
        ret += str(PUSH("q", rbp)) + "\n"

        # Cgen lhs and store into stack
        ret += cgen(cur_cls, exp.lhs)
        ret += str(PUSH("q", acc_reg)) + "\n"

        # cgen rhs and store into stack
        ret += cgen(cur_cls, exp.rhs)
        ret += str(PUSH("q", acc_reg)) + "\n"

        # Store self reg to stack call lt handler
        ret += str(PUSH("q", self_reg)) + "\n"
        ret += str(CALL("lt_handler")) + "\n"

        # Free space for arguments passed into lt handler
        ret += str(ADD("q", "$24", rsp)) + "\n"

        # Store the rbp and self_reg back
        ret += str(POP("q", rbp)) + "\n"
        ret += str(POP("q", self_reg)) + "\n"
        return ret

    elif isinstance(exp, Le):
        ret += str(PUSH("q", self_reg)) + "\n"
        ret += str(PUSH("q", rbp)) + "\n"

        # Cgen lhs and store into stack
        ret += cgen(cur_cls, exp.lhs)
        ret += str(PUSH("q", acc_reg)) + "\n"

        # cgen rhs and store into stack
        ret += cgen(cur_cls, exp.rhs)
        ret += str(PUSH("q", acc_reg)) + "\n"

        # Store self reg to stack call le handler
        ret += str(PUSH("q", self_reg)) + "\n"
        ret += str(CALL("le_handler")) + "\n"

        # Free space for arguments passed into le handler
        ret += str(ADD("q", "$24", rsp)) + "\n"

        # Store the rbp and self_reg back
        ret += str(POP("q", rbp)) + "\n"
        ret += str(POP("q", self_reg)) + "\n"
        return ret

    elif isinstance(exp, Eq):
        ret += str(PUSH("q", self_reg)) + "\n"
        ret += str(PUSH("q", rbp)) + "\n"

        # Cgen lhs and store into stack
        ret += cgen(cur_cls, exp.lhs)
        ret += str(PUSH("q", acc_reg)) + "\n"

        # cgen rhs and store into stack
        ret += cgen(cur_cls, exp.rhs)
        ret += str(PUSH("q", acc_reg)) + "\n"

        # Store self reg to stack call eq handler
        ret += str(PUSH("q", self_reg)) + "\n"
        ret += str(CALL("eq_handler")) + "\n"

        # Free space for arguments passed into eq handler
        ret += str(ADD("q", "$24", rsp)) + "\n"

        # Store the rbp and self_reg back
        ret += str(POP("q", rbp)) + "\n"
        ret += str(POP("q", self_reg)) + "\n"
        return ret

    elif isinstance(exp, Not):
        # cgen expression
        ret += cgen(cur_cls, exp.exp)
        # compare to 0
        ret += str(MOV("q", MEM(24, acc_reg), acc_reg)) + "\n"
        ret += str(CMP("q", "$0", acc_reg)) + "\n"
        # allocate 3 labels
        label += 1
        truelabel = label
        label += 1
        falselabel = label
        label += 1
        endlabel = label
        ret += str(JNE("l%d" % truelabel)) + "\n"
        # false branch
        ret += ".globl l%d\n" % falselabel
        ret += "{: <24}".format("l%d:" % falselabel)
        ret += "## false branch\n"
        ret += cgen(cur_cls,New(0,"Bool",None))
        
        # invert the expr and return 
        ret += str(MOV("q", "$1", temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(24, acc_reg))) + "\n"
        ret += str(JMP("l%d" % endlabel)) + "\n"

        # true branch
        ret += ".globl l%d\n" % truelabel
        ret += "{: <24}".format("l%d:" % truelabel)
        ret += "## true branch\n"
        ret += cgen(cur_cls,New(0,"Bool",None))

        # end branch
        ret += ".globl l%d\n" % endlabel
        ret += "{: <24}".format("l%d:" % endlabel)
        ret += "## end of if conditional\n"
        return ret

    elif isinstance(exp, Negate):
        free_temp_mem = MEM(0-8*len(ocuppied_temp),rbp)
        ret += cgen(cur_cls, Integer(0, "Int", 0))

        # lhs address in acc_reg
        ret += str(MOV("q", MEM(int_context_offset, acc_reg), acc_reg)) + "\n"
        ret += str(MOV("q", acc_reg, free_temp_mem)) + "\n"
        ocuppied_temp.append(free_temp_mem)
        ret += cgen(cur_cls,exp.exp)
        # lhs address in acc_reg
        ret += str(MOV("q", MEM(int_context_offset, acc_reg), acc_reg)) + "\n"
        ret += str(MOV("q", free_temp_mem, temp_reg)) + "\n"

        # Code for Minus Operation
        #                movq %r14, %rax
	#		subq %r13, %rax
	#		movq %rax, %r12
        #                movq %r13, 0(%rbp)
        ret += str(MOV("q", temp_reg, rax)) + "\n"
        ret += str(SUB("q", acc_reg, rax)) + "\n"
        ret += str(MOV("q", rax, acc_reg)) + "\n"

        # store back to temporary location of MEM
        ret += str(MOV("q", acc_reg, free_temp_mem)) + "\n"

        ret += cgen(cur_cls,New(0,"Int",None))
        # lhs address in acc_reg
        ret += str(MOV("q", free_temp_mem, temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(int_context_offset, acc_reg))) + "\n"
        ocuppied_temp.pop()

        return ret

    elif isinstance(exp, If):
        # cgen expression
        ret += cgen(cur_cls, exp.predicate)
        # compare to 0
        ret += str(MOV("q", MEM(24, acc_reg), acc_reg)) + "\n"
        ret += str(CMP("q", "$0", acc_reg)) + "\n"
        # allocate 3 labels
        label += 1
        truelabel = label
        label += 1
        falselabel = label
        label += 1
        endlabel = label
        ret += str(JNE("l%d" % truelabel)) + "\n"
        # false branch
        ret += ".globl l%d\n" % falselabel
        ret += "{: <24}".format("l%d:" % falselabel)
        ret += "## false branch\n"
        ret += cgen(cur_cls,exp.else_body)
        
        # jump to end
        ret += str(JMP("l%d" % endlabel)) + "\n"

        # true branch
        ret += ".globl l%d\n" % truelabel
        ret += "{: <24}".format("l%d:" % truelabel)
        ret += "## true branch\n"
        ret += cgen(cur_cls,exp.then_body)

        # end branch
        ret += ".globl l%d\n" % endlabel
        ret += "{: <24}".format("l%d:" % endlabel)
        ret += "## end of if conditional\n"
        return ret
    
    elif isinstance(exp, While):
        label += 1
        checklabel = label
        label += 1
        endlabel = label

        # check while condition
        ret += ".globl l%d\n" % checklabel
        ret += "{: <24}".format("l%d:" % checklabel)
        ret += "## while conditional check\n"
        ret += cgen(cur_cls, exp.predicate)

        ret += str(MOV("q", MEM(24, acc_reg), acc_reg)) + "\n"
        ret += str(CMP("q", "$0", acc_reg)) + "\n"
        ret += str(JE("l%d" % endlabel)) + "\n"
        
        ret += cgen(cur_cls, exp.body)

        ret += str(JMP("l%d" % checklabel)) + "\n"

        # end of while loop
        ret += ".globl l%d\n" % endlabel
        ret += "{: <24}".format("l%d:" % endlabel)
        ret += "## end of while loop\n"
        return ret
   
    elif isinstance(exp, Isvoid):
        ret += cgen(cur_cls, exp.exp)

        # compare if void
        ret += str(CMP("q", "$0", acc_reg)) + "\n"
        # allocate 3 labels
        label += 1
        truelabel = label
        label += 1
        falselabel = label
        label += 1
        endlabel = label
        ret += str(JE("l%d" % truelabel)) + "\n"
        # false branch
        ret += ".globl l%d\n" % falselabel
        ret += "{: <24}".format("l%d:" % falselabel)
        ret += "## false branch of isvoid\n"
        ret += cgen(cur_cls,New(0,"Bool",None))
        
        # jump to end 
        ret += str(JMP("l%d" % endlabel)) + "\n"

        # true branch
        ret += ".globl l%d\n" % truelabel
        ret += "{: <24}".format("l%d:" % truelabel)
        ret += "## true branch of isvoid\n"
        ret += cgen(cur_cls,New(0,"Bool",None))
        ret += str(MOV("q", "$1", temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(24, acc_reg))) + "\n"

        # end branch
        ret += ".globl l%d\n" % endlabel
        ret += "{: <24}".format("l%d:" % endlabel)
        ret += "## end of isvoid\n"
        return ret

    else:
        #ret += str(MOV("q", "$0", acc_reg)) + "\n"
        #return ret
        #print exp
        #print("unhandled expression")
        exit()


def inter_cgen(method_str):
    ret = ""
    global label
    global tab_6
    global tab_3
    global string_map
    if method_str == "IO.in_int":
        ret += tab_6 + "## new Int\n"
        ret += tab_6 + "pushq %rbp\n"
        ret += tab_6 + "pushq %r12\n"
        ret += tab_6 + "movq $Int..new, %r14\n"
        ret += tab_6 + "call *%r14\n"
        ret += tab_6 + "popq %r12\n"
        ret += tab_6 + "popq %rbp\n"
        ret += tab_6 + "movq %r13, %r14\n"
        ret += tab_6 + "movl	$1, %esi\n"
        ret += tab_6 + "movl $4096, %edi\n"
        ret += tab_3 + "call calloc\n"
        ret += tab_6 + "pushq %rax\n"
        ret += tab_6 + "movq %rax, %rdi\n"
        ret += tab_6 + "movq $4096, %rsi\n"
        ret += tab_6 + "movq stdin(%rip), %rdx\n"
        ret += tab_3 + "call fgets\n" 
        ret += tab_6 + "popq %rdi \n"
        ret += tab_6 + "movl $0, %eax\n"
        ret += tab_6 + "pushq %rax\n"
        ret += tab_6 + "movq %rsp, %rdx\n"
        ret += tab_6 + "movq $percent.ld, %rsi\n"
        ret += tab_3 + "call sscanf\n"
        ret += tab_6 + "popq %rax\n"
        ret += tab_6 + "movq $0, %rsi \n"
        ret += tab_6 + "cmpq $2147483647, %rax \n"
        ret += tab_6 + "cmovg %rsi, %rax\n"
        ret += tab_6 + "cmpq $-2147483648, %rax \n"
        ret += tab_6 + "cmovl %rsi, %rax\n"
        ret += tab_6 + "movq %rax, %r13\n"
        ret += tab_6 + "movq %r13, 24(%r14)\n"
        ret += tab_6 + "movq %r14, %r13\n"
    elif method_str == "IO.in_string":
        ret += tab_6 + "## new String\n"
        ret += tab_6 + "pushq %rbp\n"
        ret += tab_6 + "pushq %r12\n"
        ret += tab_6 + "movq $String..new, %r14\n"
        ret += tab_6 + "call *%r14\n"
        ret += tab_6 + "popq %r12\n"
        ret += tab_6 + "popq %rbp\n"
        ret += tab_6 + "movq %r13, %r14\n"
        ret += tab_3 + "call coolgetstr \n"
        ret += tab_6 + "movq %rax, %r13\n"
        ret += tab_6 + "movq %r13, 24(%r14)\n"
        ret += tab_6 + "movq %r14, %r13\n"
    elif method_str == "IO.out_int":
        ret += tab_6 + "movq 24(%rbp), %r14\n"
        ret += tab_6 + "movq 24(%r14), %r13\n"
        ret += tab_6 + "movq $percent.d, %rdi\n"
        ret += tab_6 + "movl %r13d, %eax\n"
        ret += tab_6 + "cdqe\n"
        ret += tab_6 + "movq %rax, %rsi\n"
        ret += tab_6 + "movl $0, %eax\n"
        ret += tab_3 + "call printf\n"
        ret += tab_6 + "movq %r12, %r13\n"
    elif method_str == "IO.out_string":
        ret += tab_6 + "movq 24(%rbp), %r14\n"
        ret += tab_6 + "movq 24(%r14), %r13\n"
        ret += tab_6 + "movq %r13, %rdi\n"
        ret += tab_3 + "call cooloutstr\n"
        ret += tab_6 + "movq %r12, %r13\n"
    elif method_str == "String.concat":
        ret += tab_6 + "## new String\n"
        ret += tab_6 + "pushq %rbp\n"
        ret += tab_6 + "pushq %r12\n"
        ret += tab_6 + "movq $String..new, %r14\n"
        ret += tab_6 + "call *%r14\n"
        ret += tab_6 + "popq %r12\n"
        ret += tab_6 + "popq %rbp\n"
        ret += tab_6 + "movq %r13, %r15\n"
        ret += tab_6 + "movq 24(%rbp), %r14\n"
        ret += tab_6 + "movq 24(%r14), %r14\n"
        ret += tab_6 + "movq 24(%r12), %r13\n"
        ret += tab_6 + "movq %r13, %rdi\n"
        ret += tab_6 + "movq %r14, %rsi\n"
        ret += tab_3 + "call coolstrcat\n"
        ret += tab_6 + "movq %rax, %r13\n"
        ret += tab_6 + "movq %r13, 24(%r15)\n"
        ret += tab_6 + "movq %r15, %r13        \n"
    elif method_str == "String.length":
        ret += tab_6 + "## new Int\n"
        ret += tab_6 + "pushq %rbp\n"
        ret += tab_6 + "pushq %r12\n"
        ret += tab_6 + "movq $Int..new, %r14\n"
        ret += tab_6 + "call *%r14\n"
        ret += tab_6 + "popq %r12\n"
        ret += tab_6 + "popq %rbp\n"
        ret += tab_6 + "movq %r13, %r14\n"
        ret += tab_6 + "movq 24(%r12), %r13\n"
        ret += tab_6 + "movq %r13, %rdi\n"
        ret += tab_6 + "movl $0, %eax\n"
        ret += tab_3 + "call coolstrlen\n"
        ret += tab_6 + "movq %rax, %r13\n"
        ret += tab_6 + "movq %r13, 24(%r14)\n"
        ret += tab_6 + "movq %r14, %r13\n"
    elif method_str == "String.substr":
        ret += tab_6 + "## new String\n"
        ret += tab_6 + "pushq %rbp\n"
        ret += tab_6 + "pushq %r12\n"
        ret += tab_6 + "movq $String..new, %r14\n"
        ret += tab_6 + "call *%r14\n"
        ret += tab_6 + "popq %r12\n"
        ret += tab_6 + "popq %rbp\n"
        ret += tab_6 + "movq %r13, %r15\n"
        ret += tab_6 + "movq 24(%rbp), %r14\n"
        ret += tab_6 + "movq 24(%r14), %r14\n"
        ret += tab_6 + "movq 32(%rbp), %r13\n"
        ret += tab_6 + "movq 24(%r13), %r13\n"
        ret += tab_6 + "movq 24(%r12), %r12\n"
        ret += tab_6 + "movq %r12, %rdi\n"
        ret += tab_6 + "movq %r13, %rsi\n"
        ret += tab_6 + "movq %r14, %rdx\n"
        ret += tab_3 + "call coolsubstr\n"
        ret += tab_6 + "movq %rax, %r13\n"
        ret += tab_6 + "cmpq $0, %r13\n"
        # update label
        label += 1
        ret += tab_6 + "jne l%d\n" % label

        # update string
        string_key = "string%d" % (len(string_map) + 1)
        string_val = "ERROR: 0: Exception: String.substr out of range\\n"
        if string_val in string_map.values():
            string_key = [key for key,val in string_map.iteritems() if val ==
                            string_val][0] 
        else:
            string_map[string_key] = string_val
        ret += tab_6 + "movq $%s, %%r13\n" % string_key

        ret += tab_6 + "movq %r13, %rdi\n"
        ret += tab_3 + "call cooloutstr\n"
        ret += tab_6 + "movl $0, %edi\n"
        ret += tab_3 + "call exit\n"
        ret += ".globl l%d\n" % label
        ret += "{: <24}".format("l%d:" % label)
        ret += "movq %r13, 24(%r15)\n"
        ret += tab_6 + "movq %r15, %r13\n"

    elif method_str == "Object.abort":
        string_key = "string%d" % (len(string_map) + 1)
        string_val = "abort\\n"
        if string_val in string_map.values():
            string_key = [key for key,val in string_map.iteritems() if val ==
                            string_val][0] 
        else:
            string_map[string_key] = string_val
        ret += tab_6 + "movq $%s, %%r13\n" % string_key
        ret += tab_6 + "movq %r13, %rdi\n"
        ret += tab_3 + "call cooloutstr\n"
        ret += tab_6 + "movl $0, %edi\n"
        ret += tab_3 + "call exit\n"

    elif method_str == "Object.copy":
        ret += "                        movq 8(%r12), %r14\n"
        ret += "                        movq $8, %rsi\n"
        ret += "			movq %r14, %rdi\n"
        ret += "			call calloc\n"
        ret += "			movq %rax, %r13\n"
        ret += "                        pushq %r13\n"
        label = label + 1
        label1 = label
        label = label + 1
        label2 = label
        ret += ".globl l%d\n" % label1
        ret += "l%d:                    cmpq $0, %%r14\n" % label1
        ret += "			je l%d\n" % label2
        ret += "                        movq 0(%r12), %r15\n"
        ret += "                        movq %r15, 0(%r13)\n"
        ret += "                        movq $8, %r15\n"
        ret += "                        addq %r15, %r12\n"
        ret += "                        addq %r15, %r13\n"
        ret += "                        movq $1, %r15\n"
        ret += "                        subq %r15, %r14\n"
        ret += "                        jmp l%d\n" % label1 
        ret += ".globl l%d\n" % label2
        ret += "l%d:                    ## done with Object.copy loop\n" % label2
        ret += "                        popq %r13\n"
    elif method_str == "Object.type_name":
        ret += tab_6 + "## new String\n"
        ret += tab_6 + "pushq %rbp\n"
        ret += tab_6 + "pushq %r12\n"
        ret += tab_6 + "movq $String..new, %r14\n"
        ret += tab_6 + "call *%r14\n"
        ret += tab_6 + "popq %r12\n"
        ret += tab_6 + "popq %rbp\n"
        ret += tab_6 + "## obtain vtable for self object\n"
        ret += tab_6 + "movq 16(%r12), %r14\n"
        ret += tab_6 + "## look up type name at offset 0 in vtable\n"
        ret += tab_6 + "movq 0(%r14), %r14\n"
        ret += tab_6 + "movq %r14, 24(%r13)\n"
    return ret


def main():
    global class_map
    global imp_map
    global parent_map
    global aast
    global symbol_table
    global vtable_map
    global methoddef
    #tab_6 = "                        "
    
    tab_6 = "{:<24}".format("")
    #tab_4 = "{:<12}".format("")
    tab_3 = "\t\t\t"
    split = "## ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;"
    #if len(sys.argv) < 2:
    #    print("Specify .cl-type input file.")
    #    exit()
    class_map, imp_map, parent_map, aast = rd.read_type_file(sys.argv[1])
    #filename = "my_" + str(sys.argv[1][:-7]) + "s"
    filename = str(sys.argv[1][:-7]) + "s"

    #print filename
    fout = open(filename,"w")
    vtable_map = {}
    # produce vtable
    count = 10
    for idx,(cls_name,method_list) in enumerate(sorted(imp_map.items())):
        # Produce class tags
        if cls_name not in ["String", "Int", "Bool"]:
            class_tag[cls_name] = count
            count += 1
        vtable_map[cls_name] = []
        ret = tab_6 + split + "\n"
        ret += ".globl %s..vtable\n" % cls_name
        ret += "{: <24}".format("%s..vtable:" % cls_name) + \
                "## virtual function table for %s" % cls_name + "\n"
        string_num = len(string_map) + 1
        ret += tab_6 + ".quad string%d\n" % string_num 
        # insert into string map
        string_map["string%d" % string_num] = cls_name 
        ret += tab_6 + ".quad %s..new\n" % cls_name
        for method_t in method_list:
            vtable_map[cls_name].append("%s.%s" % (method_t[0], \
                           method_t[1].method_name.ident)) 
            ret += tab_6 + \
                   ".quad %s.%s\n" % (method_t[0], \
                           method_t[1].method_name.ident)
        fout.write(ret)

    # print constructor
    for idx,(cls_name,attributes) in enumerate(sorted(class_map.items())):
        ret = tab_6 + split + "\n"
        ret += ".globl %s..new\n" % cls_name
        ret += "{: <24}".format("%s..new:" % cls_name) + \
                "## constructor for %s" % cls_name + "\n"
        ret += str(PUSH("q",rbp)) + "\n"
        ret += str(MOV("q", rsp, rbp)) + "\n"
        # calculate NumTemps
        
        numTemp = 1
        for attr_temp in attributes :
            numTemp = max(numTemp, numTemp_gen(attr_temp))
        
        ret += tab_6 + "## stack room for temporaries: %d\n" % numTemp
        ret += str(MOV("q", "$%d" % (8 * numTemp), temp_reg)) + "\n"
        ret += str(SUB("q", temp_reg, rsp)) + "\n"
        ret += tab_6 + "## return address handling" + "\n"
        # get number of attribues
        if cls_name in ["Bool", "String", "Int"]:
            num_attr = 1
        else:
            num_attr = len(attributes)
        ret += str(MOV("q", "$%d" % (num_attr + 3), self_reg)) + "\n"
        ret += str(MOV("q", "$8", rsi)) + "\n"
       
        # call calloc stuff
        #ret += str(MOV("q", self_reg, rdi)) + "\n"
        #ret += tab_4 + str("call calloc") + "\n"
        #ret += str(MOV("q", rax, self_reg)) + "\n"
        ret += tab_3 + "movq %r12, %rdi\n"
        ret += tab_3 + "call calloc\n"
        ret += tab_3 + "movq %rax, %r12\n"

        # store class tag, object size and vtable pointer
        ret += tab_6 + "## store class tag, object size and vtable pointer\n"
        ret += str(MOV("q", "$%d" % (class_tag[cls_name]),temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(0,self_reg))) + "\n"
        ret += str(MOV("q", "$%d" % (num_attr + 3), temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(8,self_reg))) + "\n"
        ret += str(MOV("q", "$%s..vtable" % cls_name, temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(16,self_reg))) + "\n"
        
        # call function to print attribute
        if cls_name not in  ["String", "Int", "Bool"]:
            symbol_table = {}
            ret += attr2asm(cls_name,attributes)
        else:
            ### self[3] holds field (raw content) (Int)
            #            movq $0, %r13
            #            movq %r13, 24(%r12)
            #            ## self[3] (raw content) initializer -- none
            ## Generating Attributes for internal class
            ret += tab_6 + "## initialize attributes\n"
            if cls_name in ["Int", "Bool"]:
                ret += tab_6 + "## self[%d] holds field %s (%s)\n" % (0+3,
                "(raw content)", "Int")
                ret += str(MOV("q", "$0", acc_reg)) + "\n"
            else:
                ret += tab_6 + "## self[%d] holds field %s (%s)\n" % (0+3,
                "(raw content)", "String")
                ret += str(MOV("q", "$the.empty.string", acc_reg)) + "\n"
            
            ret += str(MOV("q", acc_reg, MEM(24+8*0, self_reg))) + "\n"
            ret+= tab_6 + "## self[%d] %s initializer -- none " % \
                    (0+3, "(raw content)") + "\n"



        #movq %r12, %r13
        #                ## return address handling
        #                movq %rbp, %rsp
        #                popq %rbp
        #                ret
        ret += str(MOV("q", self_reg, acc_reg)) + "\n"
        ret += tab_6 + "## return address handling\n"
        ret += str(MOV("q", rbp, rsp)) + "\n"
        ret += str(POP("q", rbp)) + "\n"
        ret += tab_6 + "ret\n"

        fout.write(ret)
  
    # produce method definition

    # check duplicate in method definition
    printed_list = []
    for i,(cls_name,method_list) in enumerate(sorted(imp_map.items())):
        # initialize symbol table
        symbol_table = {}
        for j, attr in enumerate(class_map[cls_name]):
            symbol_table[attr.attr_name.ident] = [str(MEM(24 + 8*j,
                    self_reg))]

        for method_t in method_list:
            method_cls = method_t[0]
            method_name = method_t[1].method_name.ident
            method_str = "%s.%s" % (method_cls, method_name)
            if method_str in printed_list:
                continue
            ret = tab_6 + split + "\n" 
            ret += ".globl %s.%s\n" % (method_cls, method_name)
            ret += "{: <24}".format("%s.%s:" % (method_cls, method_name))
            ret += "## method definition\n"
            ret += str(PUSH("q", rbp)) + "\n"
            ret += str(MOV("q", rsp, rbp)) + "\n"
            ret += str(MOV("q", MEM(16, rbp), self_reg)) + "\n"
            numTemp = max(numTemp_gen(method_t[1].body_exp), 1)
            # number of temporaries need to be determined
            ret += tab_6 + "## stack room for temporaries: %d\n" % numTemp
            ret += str(MOV("q", "$%d" % (8 * numTemp), temp_reg)) + "\n"
            ret += str(SUB("q", temp_reg, rsp)) + "\n"
            
            ret += tab_6 + "## return address handling\n"
            # traverse class map and print all attrbutes
            for j, attr in enumerate(class_map[cls_name]):
                ret += tab_6 + "## self[%d] holds field %s (%s)\n" % (j+3, attr.attr_name.ident, attr.attr_type.ident)
            
            num_formal = len(method_t[1].formals)
            for j, formal in enumerate(method_t[1].formals):
                ## fp[3] holds argument m (Int)
                ret += tab_6 + "## fp[%d] holds argument %s (%s)\n" % (2+num_formal-j, formal.formal_name.ident, formal.formal_type.ident)
                if formal.formal_name.ident in symbol_table.keys():
                    symbol_table[formal.formal_name.ident].append(str(MEM(16 +
                    8*(num_formal-j), rbp)))
                else:
                    symbol_table[formal.formal_name.ident] = [str(MEM(16 +
                    8*(num_formal-j), rbp))]

            ret += tab_6 + "## method body begins\n"
            ret += cgen(cls_name,method_t[1].body_exp) 
            ret += ".globl %s.end\n" % method_str 

            ret += "{: <24}".format("%s.end:" % method_str) 
            ret += "## method body ends\n"
            ret += tab_6 + "## return address handling\n"

            ret += str(MOV("q", rbp, rsp)) + "\n"
            ret += str(POP("q", rbp)) + "\n"
            ret += tab_6 + "ret\n"

            printed_list.append(method_str)

            # pop out symbol table
            for j, formal in enumerate(method_t[1].formals):
                symbol_table[formal.formal_name.ident].pop()
                if symbol_table[formal.formal_name.ident] == []:
                    symbol_table.pop(formal.formal_name.ident)
            
            fout.write(ret) 


    #print string_map
    ret = tab_6 + split + "\n"
    ret += tab_6 + "## global string constants\n"
    # print empty string, d and ld
    ret += ".globl the.empty.string\n"
    ret +=  "{: <24}".format("the.empty.string:")
    ret += "# \"\"\n"
    ret += ".byte 0\n\n"
    
    ret += ".globl percent.d\n"
    ret += "{: <24}".format("percent.d:")
    ret += "# \"%ld\"\n"
    ret += ".byte  37 # \'%\'\n"
    ret += ".byte 108 # \'l\'\n"
    ret += ".byte 100 # \'d\'\n"
    ret += ".byte 0\n\n"

    ret += ".globl percent.ld\n"
    ret += "{: <24}".format("percent.ld:")
    ret += "# \" %ld\"\n"
    ret += ".byte  32 # \' \'\n"
    ret += ".byte  37 # \'%\'\n"
    ret += ".byte 108 # \'l\'\n"
    ret += ".byte 100 # \'d\'\n"
    ret += ".byte 0\n\n"

    # print all strings in string_map
    string_t_list = [(k,v) for k,v in string_map.iteritems()]
    string_t_list = sorted(string_t_list, key=lambda x : int(x[0][6:]))
    for (str_key, str_val) in string_t_list:
        ret += ".globl %s\n" % str_key
        ret +=  "{: <24}".format("%s:" % str_key)
        ret += "# \"%s\"\n" % str_val
        # collect all ascii code in the string
        asc_code = [ord(c) for c in str_val]
        for code in asc_code:
            ret += ".byte"
            if code == 92:
                ret += "{:>4}".format("%s" % str(code))
                ret += " # \'\\\\\'" + "\n"
            else:
                ret += "{:>4}".format("%s" % str(code))
                ret += " # \'%s\'" % chr(code) + "\n"
        ret += ".byte 0\n\n"

    fout.write(ret)

    # print helper function ahead of main
    with open("methoddef.txt", "r") as f:
        line = f.readline()
        while line:
            fout.write(line)
            line = f.readline()

#    # print main function
#    ret = tab_6 + split + "\n"
#    ret += ".globl start\n"
#    ret +=  "{:<24}".format("start:")
#    ret += "## program begins here\n"
#    ret += tab_6 + "globl main\n"
#    ret += tab_3 + ".type main, @function\n"
#    ret += "main:\n"
#    
#
#    # print helper function after main
#    with open("methoddef2.txt", "r") as f:
#        line = f.readline()
#        while line:
#            fout.write(line)
#            line = f.readline()
#
    exit()
        

if __name__ == "__main__":
    main()
