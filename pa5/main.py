import sys
import reader as rd
from asm_classes import *
from cool_classes import *

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
class_tag = {}

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
        if attr.attr_type.ident not in ["SELF_TYPE","Object","IO"]:
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
            ret += cgen(attr.exp) 
            ret += str(MOV("q", acc_reg, MEM(24+8*i, self_reg))) + "\n"
        else:
            ret+= tab_6 + "## self[%d] %s initializer -- none " % \
                    (i+3, attr.attr_name.ident) + "\n"
    return ret

def cgen(exp):
    ret = ""
    global label
    
    if isinstance(exp, Internal):
        return inter_cgen(exp.extra_detail)

    if isinstance(exp, IdentifierExp):
        ## b
        #                movq 32(%r12), %r13
        variable_name = exp.ident.ident
        ret += tab_6 + "## %s\n" % variable_name
        ret += str(MOV("q", symbol_table[variable_name][-1], acc_reg)) + "\n"
        return ret

    if isinstance(exp, New):
        ret += tab_6 + "## new %s" % exp.exp_type + "\n"
        if exp.exp_type =="SELF_TYPE":

            ret += str(PUSH("q", rbp)) + "\n"
            ret += str(PUSH("q", self_reg)) + "\n"
            return ret
        ret += str(PUSH("q", rbp)) + "\n"
        ret += str(PUSH("q", self_reg)) + "\n"
        ret += str(MOV("q","$%s..new" % exp.exp_type, temp_reg)) + "\n"
        ret += str(CALL(temp_reg)) + "\n"
        ret += str(POP("q", self_reg)) + "\n"
        ret += str(POP("q", rbp)) + "\n"
        return ret

    if isinstance(exp, (TrueExp, FalseExp)):
        ret += cgen(New(0, "Bool", None))
        if isinstance(exp, TrueExp):
            ret += str(MOV("q", "$1", temp_reg)) + "\n"
        else: 
            ret += str(MOV("q", "$0", temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(int_context_offset, acc_reg))) + "\n"
        return ret
 
    if isinstance(exp, String):
        ret += cgen(New(0,"String",None)) 
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

    if isinstance(exp, Integer): 

        ret += cgen(New(0,"Int",None))
        ret += str(MOV("q", "$%d" % exp.int_val, temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(int_context_offset, acc_reg))) + "\n"
        return ret


    if isinstance(exp, Plus):
        free_temp_mem = MEM(0-8*len(ocuppied_temp),rbp)
        ret += cgen(exp.lhs) 

        # lhs address in acc_reg
        ret += str(MOV("q", MEM(int_context_offset, acc_reg), acc_reg)) + "\n"
        ret += str(MOV("q", acc_reg, free_temp_mem)) + "\n"
        
        ret += cgen(exp.rhs)
        # lhs address in acc_reg
        ret += str(MOV("q", MEM(int_context_offset, acc_reg), acc_reg)) + "\n"
        ret += str(MOV("q", free_temp_mem, temp_reg)) + "\n"
        if isinstance(exp, Plus):
            ret += str(ADD("q", temp_reg, acc_reg)) + "\n"
        else:
            # different to official compiler TODO
            ret += str(SUB("q", temp_reg, acc_reg)) + "\n"
        ret += str(MOV("q", acc_reg, free_temp_mem)) + "\n"

        ret += cgen(New(0,"Int",None))
        # lhs address in acc_reg
        ret += str(MOV("q", free_temp_mem, temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(int_context_offset, acc_reg))) + "\n"
        return ret

    if isinstance(exp, Minus):
        free_temp_mem = MEM(0-8*len(ocuppied_temp),rbp)
        ret += cgen(exp.lhs) 

        # lhs address in acc_reg
        ret += str(MOV("q", MEM(int_context_offset, acc_reg), acc_reg)) + "\n"
        ret += str(MOV("q", acc_reg, free_temp_mem)) + "\n"
        
        ret += cgen(exp.rhs)
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

        ret += cgen(New(0,"Int",None))
        # lhs address in acc_reg
        ret += str(MOV("q", free_temp_mem, temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(int_context_offset, acc_reg))) + "\n"
        return ret


    if isinstance(exp, Times):
        free_temp_mem = MEM(0-8*len(ocuppied_temp),rbp)
        ret += cgen(exp.lhs) 

        # lhs address in acc_reg
        ret += str(MOV("q", MEM(int_context_offset, acc_reg), acc_reg)) + "\n"
        ret += str(MOV("q", acc_reg, free_temp_mem)) + "\n"
        
        ret += cgen(exp.rhs)
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

        ret += cgen(New(0,"Int",None))
        # lhs address in acc_reg
        ret += str(MOV("q", free_temp_mem, temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(int_context_offset, acc_reg))) + "\n"
        return ret
    
    if isinstance(exp, Divide):
        free_temp_mem = MEM(0-8*len(ocuppied_temp),rbp)
        ret += cgen(exp.lhs) 

        # lhs address in acc_reg
        ret += str(MOV("q", MEM(int_context_offset, acc_reg), acc_reg)) + "\n"
        ret += str(MOV("q", acc_reg, free_temp_mem)) + "\n"
        
        ret += cgen(exp.rhs)
        # lhs address in acc_reg

        # Code for Divide Operation:
        #movq 24(%r13), %r14
        #                        cmpq $0, %r14
        #			jne l1
        #                        movq $string8, %r13
        #                        movq %r13, %rdi
        #			call cooloutstr
        #                        movl $0, %edi
        #			call exit
        #.globl l1
        #l1:                     ## division is OK
        #                        movq 24(%r13), %r13
        #                        movq 0(%rbp), %r14
        #                        
        #movq $0, %rdx
        #movq %r14, %rax
        #cdq 
        #idivl %r13d
        #movq %rax, %r13
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

        ret += cgen(New(0,"Int",None))
        # lhs address in acc_reg
        ret += str(MOV("q", free_temp_mem, temp_reg)) + "\n"
        ret += str(MOV("q", temp_reg, MEM(int_context_offset, acc_reg))) + "\n"
        return ret

    if isinstance(exp, Let):
        for idx, binding in enumerate(exp.binding_list):
            ret += tab_6 + "## fp[%d] holds local %s (%s)\n" % (-idx,
                    binding.var_ident.ident, binding.type_ident.ident)
            ret += cgen(binding)
            # Code for storing the binding back to stack
            if binding.var_ident.ident in symbol_table.keys():
                free_temp_mem = MEM(0-8*len(ocuppied_temp),rbp)
                ocuppied_temp.append(free_temp_mem)
                symbol_table[binding.var_ident.ident].append(str(free_temp_mem))
            else:
                free_temp_mem = MEM(0-8*len(ocuppied_temp),rbp)
                ocuppied_temp.append(free_temp_mem)
                symbol_table[binding.var_ident.ident] = [str(free_temp_mem)]

            # movq %r13, 0(%rbp)
            ret += str(MOV("q", acc_reg, \
                symbol_table[binding.var_ident.ident][-1])) + "\n"
        ret += cgen(exp.exp)

        for binding in exp.binding_list:
            ocuppied_temp.pop()
            symbol_table[binding.var_ident.ident].pop()
            if symbol_table[binding.var_ident.ident] == []:
                symbol_table.pop(binding.var_ident.ident)
        return ret

    if isinstance(exp, Binding):
        ret += cgen(exp.value_exp)
        return ret

    if isinstance(exp, Case):
        free_temp_mem = MEM(0-8*len(ocuppied_temp),rbp)

        br_label_map = {}
        ret += tab_6 + "## case expression begins\n"
        ret += cgen(exp.exp)

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
            br_label_map[case_ele.type_ident.ident] = label
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
        ret += "## case expresion: error case\n"

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
        ret += "## case expresion: void case\n"

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
            ret += ".globl l%d\n" % br_label_map[case_ele.type_ident.ident]
            ret += "{: <24}".format("l%d" % \
                    br_label_map[case_ele.type_ident.ident]) 
            ret += "## fp[%d] holds case %s (%s)" % (0-len(ocuppied_temp),
                    case_ele.var_ident.ident, case_ele.type_ident.ident) + "\n"
            free_temp_mem = MEM(0-8*len(ocuppied_temp),rbp)
            ocuppied_temp.append(free_temp_mem)
            ret += cgen(case_ele.body_exp)
            ocuppied_temp.pop()
            ret += str(JMP("l%d" % case_end_label)) + "\n"

        ret += ".globl l%d\n" % case_end_label 
        ret += "{: <24}".format("l%d:" % case_end_label) + "## case expression ends\n"
        return ret

    if isinstance(exp, Self_Dispatch):
        ret += "## %s(...)" % exp.method_ident.ident + "\n"
        ret += str(PUSH("q", self_reg)) + "\n"
        ret += str(PUSH("q", rbp)) + "\n"
        for idx, arg in enumerate(exp.args):
            ret += cgen(arg)
            ret += str(PUSH("q", acc_reg)) + "\n"
            ret += str(PUSH("q", self_reg)) + "\n"
        ret += tab_6 + "## obtain vtable for self object of type %s\n" % exp.exp_type 
        ret += str(MOV("q", MEM(16, self_reg), temp_reg)) + "\n"
        return ret

    if isinstance(exp, Block):
        for block_exp in exp.exp_list:
            ret += cgen(block_exp)
        return ret

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
    #tab_6 = "                        "
    
    tab_6 = "{:<24}".format("")
    #tab_4 = "{:<12}".format("")
    tab_3 = "\t\t\t"
    split = "## ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;"
    if len(sys.argv) < 2:
        print("Specify .cl-type input file.")
        exit()
    class_map, imp_map, parent_map, aast = rd.read_type_file(sys.argv[1])
    filename = "my_" + str(sys.argv[1][:-7]) + "s"
    print filename
    fout = open(filename,"w")

    # produce vtable
    for idx,(cls_name,method_list) in enumerate(sorted(imp_map.items())):
        # Produce class tags
        class_tag[cls_name] = idx

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
        ret += tab_6 + "## stack room for temporaries: 1\n"
        ret += str(MOV("q", "$8", temp_reg)) + "\n"
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
            num_temp = 1
            # number of temporaries need to be determined FIXME
            ret += tab_6 + "## stack room for temporaries: %d\n" % num_temp
            ret += str(MOV("q", "$%d" % 8 * num_temp, temp_reg)) + "\n"
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
            ret += cgen(method_t[1].body_exp) 
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
    exit()
        

if __name__ == "__main__":
    main()
