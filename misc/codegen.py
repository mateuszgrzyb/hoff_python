
from llvmlite import ir

Float = ir.DoubleType

def function_type(n):
    return ir.FunctionType(Float(), (Float() for _ in range(n)))


class Module:
    def __init__(self, name: str) -> None:
        self.encoding = 'utf-8'
        self.module = ir.Module(name)

    def add_func(self, name: str) -> None:
        double = ir.DoubleType()
        fnty = ir.FunctionType(double, (double, double))
        func = ir.Function(self.module, fnty, name)
        
        block = func.append_basic_block(name='entry')
        builder = ir.IRBuilder(block)
        a, b = func.args
        result = builder.fadd(a, b, name='result')
        builder.ret(result)

    def add_main(self, f: ir.Function, args) -> None:
        int32 = ir.IntType(32)
        int8 = ir.IntType(8)
        fnty = ir.FunctionType(int32, [])
        main = ir.Function(self.module, fnty, 'main')

        block = main.append_basic_block(name='entry')
        builder = ir.IRBuilder(block)
        ptr = builder.gep(args, [int8(0), int8(0)]).pointer
        print(type(ptr))

        builder.call(f, [ptr])

        builder.ret(int32(0))

    def add_printf(self) -> ir.Function:
        int32 = ir.IntType(32)
        int8 = ir.IntType(8)
        fnty = ir.FunctionType(int32, [int8.as_pointer()], var_arg=True)
        return ir.Function(self.module, fnty, 'printf')

    def add_string(self, name: str, string: str) -> ir.GlobalVariable:
        string = string + '\0'
        arraytype = ir.ArrayType(ir.IntType(8), len(string))
        var = ir.GlobalVariable(self.module, arraytype, name)
        var.global_constant = True
        var.initializer = ir.Constant(arraytype, bytearray(string.encode('utf-8')))
        return var

    
    def print_floats(self, floats) -> None:
        pass 

    def __str__(self) -> str:
        return str(self.module)


if __name__ == '__main__':
    m = Module('main')
    test = m.add_string('test', 'ala ma kota i co z tego?')
    printf = m.add_printf()
    m.add_func('a_plus_b')
    m.add_main(printf, test)

    print(m)
