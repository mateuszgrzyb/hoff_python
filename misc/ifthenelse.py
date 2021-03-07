from llvmlite import ir

double = ir.DoubleType()

fun_type = ir.FunctionType(double, [double, double])

module = ir.Module(name='main')

func = ir.Function(module, fun_type, name='fpadd')

