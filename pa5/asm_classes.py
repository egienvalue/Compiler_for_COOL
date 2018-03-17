## %rax Return value 
## %rbx Callee saved 
## %rcx 4th argument 
## %rdx 3rd argument 
## %rsi 2nd argument 
## %rdi 1st argument 
## %rbp Callee saved 
## %rsp Stack pointer 
## %r8 5th argument
## %r9 6th argument 
## %r10 Scratch register 
## %r11 Scratch register 
## %r12 Callee saved
## %r13 Callee saved 
## %r14 Callee saved 
## %r15 Callee saved

## new Int


class Register(object):
    offset = None
        
class RAX(Register):
    def __init__(self, _offset=None):
        self.offset = _offset

    def __str__(self):
        if self.offset == None:
            return "%rax"
        else:
            return "%d(%rax)" % self.offset
class EAX(Register):
    def __init__(self, _offset=None):
        self.offset = _offset

    def __str__(self):
        if self.offset == None:
            return "%eax"
        else:
            return "%d(%eax)" % self.offset

class RBX(Register):
    def __init__(self, _offset=None):
        self.offset = _offset

    def __str__(self):
        if self.offset == None:
            return "%rbx"
        else:
            return "%d(%rbx)" % self.offset


class RCX(Register):
    def __init__(self, _offset=None):
        self.offset = _offset

    def __str__(self):
        if self.offset == None:
            return "%rcx"
        else:
            return "%d(%rcx)" % self.offset


class RDX(Register):
    def __init__(self, _offset=None):
        self.offset = _offset

    def __str__(self):
        if self.offset == None:
            return "%rdx"
        else:
            return "%d(%rdx)" % self.offset


class RSI(Register):
    def __init__(self, _offset=None):
        self.offset = _offset

    def __str__(self):
        if self.offset == None:
            return "%rsi"
        else:
            return "%d(%rsi)" % self.offset

class RDI(Register):
    def __init__(self, _offset=None):
        self.offset = _offset

    def __str__(self):
        if self.offset == None:
            return "%rdi"
        else:
            return "%d(%rdi)" % self.offset

class EDI(Register):
    def __init__(self, _offset=None):
        self.offset = _offset

    def __str__(self):
        if self.offset == None:
            return "%edi"
        else:
            return "%d(%edi)" % self.offset

class RBP(Register):
    def __init__(self, _offset=None):
        self.offset = _offset

    def __str__(self):
        if self.offset == None:
            return "%rbp"
        else:
            return "%d(%rbp)" % self.offset

class RSP(Register):
    def __init__(self, _offset=None):
        self.offset = _offset

    def __str__(self):
        if self.offset == None:
            return "%rsp"
        else:
            return "%d(%rsp)" % self.offset

class MEM(object):
    def __init__(self, _offset, _register):
        self.offset = _offset
        self.register = _register
    def __str__(self):
        ret = "%d(%s)" % (self.offset, str(self.register))
        return ret
        

class R(Register):
    def __init__(self, _reg_num, _len=""):
        self.reg_num = _reg_num
        self.len = _len

    def __str__(self):
        return "%r" + "%d%s" % (self.reg_num, self.len)

class PUSH(object):
    def __init__(self, _len, _oprand):
        self.len = _len
        self.oprand = _oprand 
    def __str__(self):
        ret = "push%s %s" % (str(self.len),str(self.oprand))
        return "{: <24}".format("") + ret

class MOV(object):
    def __init__(self, _len, _oprand1, _oprand2):
        self.len = _len
        self.oprand1 = _oprand1
        self.oprand2 = _oprand2
    def __str__(self):
        ret = "mov%s %s, %s" % (str(self.len), str(self.oprand1), str(self.oprand2))
        return "{: <24}".format("") + ret

class SHL(object):
    def __init__(self, _len, _oprand1, _oprand2):
        self.len = _len
        self.oprand1 = _oprand1
        self.oprand2 = _oprand2
    def __str__(self):
        ret = "shl%s %s, %s" % (str(self.len), str(self.oprand1), str(self.oprand2))
        return "{: <24}".format("") + ret

class SHR(object):
    def __init__(self, _len, _oprand1, _oprand2):
        self.len = _len
        self.oprand1 = _oprand1
        self.oprand2 = _oprand2
    def __str__(self):
        ret = "shr%s %s, %s" % (str(self.len), str(self.oprand1), str(self.oprand2))
        return "{: <24}".format("") + ret

class SUB(object):
    def __init__(self, _len, _oprand1, _oprand2):
        self.len = _len
        self.oprand1 = _oprand1
        self.oprand2 = _oprand2
    def __str__(self):
        ret = "sub%s %s, %s" % (str(self.len),str(self.oprand1), str(self.oprand2))
        return "{: <24}".format("") + ret

class ADD(object):
    def __init__(self, _len, _oprand1, _oprand2):
        self.len = _len
        self.oprand1 = _oprand1
        self.oprand2 = _oprand2
    def __str__(self):
        ret = "add%s %s, %s" % (str(self.len),str(self.oprand1), str(self.oprand2))
        return "{: <24}".format("") + ret


class CALL(object):
    def __init__(self, _oprand):
        self.oprand = _oprand

    def __str__(self):
        if isinstance(self.oprand, Register): 
            ret = "call *%s" % str(self.oprand)
        else:
            ret = "call %s" % str(self.oprand)
        return "{: <24}".format("") + ret

class POP(object):
    def __init__(self, _len, _oprand):
        self.len = _len
        self.oprand = _oprand 
    def __str__(self):
        ret = "pop%s %s" % (str(self.len),str(self.oprand))
        return "{: <24}".format("") + ret

class IMUL(object):
    def __init__(self, _len, _oprand1, _oprand2):
        self.len = _len
        self.oprand1 = _oprand1
        self.oprand2 = _oprand2
    def __str__(self):
        ret = "imul%s %s, %s" % (str(self.len),str(self.oprand1), str(self.oprand2))
        return "{: <24}".format("") + ret

class IDIV(object):
    def __init__(self, _len, _oprand1):
        self.len = _len
        self.oprand1 = _oprand1
    def __str__(self):
        ret = "idiv%s %s" % (str(self.len),str(self.oprand1))
        return "{: <24}".format("") + ret


class CMP(object):
    def __init__(self, _len, _oprand1, _oprand2):
        self.len = _len
        self.oprand1 = _oprand1
        self.oprand2 = _oprand2
    def __str__(self):
        ret = "cmp%s %s, %s" % (str(self.len),str(self.oprand1), str(self.oprand2))
        return "{: <24}".format("") + ret

# Jump Not Equal
class JNE(object):
    def __init__(self, _oprand):
        self.oprand = _oprand

    def __str__(self):
        if isinstance(self.oprand, Register): 
            ret = "jne *%s" % str(self.oprand)
        else:
            ret = "jne %s" % str(self.oprand)
        return "{: <24}".format("") + ret
