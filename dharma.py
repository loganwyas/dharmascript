from sys import argv
from lark import Lark, Token, Tree

false = "Gale"
true = "Linus"

parser = Lark(r"""
    start: ">: 4 8 15 16 23 42" | ">: 4 8 15 16 23 42" "\n" (function | statement)*
    
    statement: for | single_line | if_statement | while
    
    assignment: WORD "=" value
    single_line: (function_call | assignment) "?"
    
    for: "for" "(" (variable "?" num "?" num "?" (num "?"?)?) ")" "{{" (statement)* "}}"
    
    while: "while" "(" value ")" "{{" (statement)* "}}"
    
    function: "make" WORD "(" (WORD? | (WORD) ("," WORD)*) ")" "{{" (statement)* "}}"
    function_call: WORD  "(" (value? | (value) ("," value)*) ")"
    
    if: "if" "(" value ")" "{{" (statement)* "}}"
    if_statement: if ("else " if)* ("else" "{{" (statement)* "}}")?
    
    value: num | string | bool | function_call | variable | calculation | "(" value ")"
    variable: WORD
    
    string: ESCAPED_STRING
    
    calculation: value math_symbol value
    math_symbol: SYMBOL
    SYMBOL: "+" | "-" | "*" | "/"
    num: SIGNED_NUMBER
    
    bool: BOOL | "(" bool ")" | bool " " bool_sep " " bool | bool_opp bool | value bool_comp value
    bool_sep: BOOL_SEPARATOR
    bool_opp: "lie"
    bool_comp: BOOL_COMPARER
    BOOL: "{true}" | "{false}"
    BOOL_SEPARATOR: "and" | "or"
    BOOL_COMPARER: "==" | ">=" | "<=" | ">" | "<"

    %import common.WORD
    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS

    """.format(true=true, false=false))


def raiseException(message):
    raise Exception("SYSTEM FAILURE: " + message)


def execute(*args):
    print(*args)


variables = {}
functions = {
    "execute": execute
}

illegalNames = [true, false, "if", "for", "while", "else", "make"]

func_instructions = {}
functionArgs = {}


def run_function(name, *args):
    if name in functions.keys():
        if name in functionArgs.keys():
            if len(args) != len(functionArgs[name]):
                raiseException("Function " + name + " was given " + str(len(args)) +
                               " arguments, but expected " + str(len(functionArgs[name])) + ".")
            else:
                for i, arg in enumerate(args):
                    variables[functionArgs[name][i]] = arg
                functions[name]()
                for arg in functionArgs[name]:
                    variables.pop(arg)
        else:
            functions[name](*args)
    else:
        raiseException("Function " + name + " does not exist.")


def run_created_function(name):
    for inst in func_instructions[name]:
        run_instruction(inst)


def create_function(t):
    vals = t.children
    name = vals[0].value
    if name in illegalNames:
        raiseException("Cannot use \"" + name + "\" as a function name.")
    i = 1
    args = []
    while not type(vals[i]) == Tree:
        args.append(vals[i].value)
        i += 1
    func = "lambda: run_created_function('" + name + "')"
    func_instructions[name] = vals[i:]
    functions[name] = eval(func)
    functionArgs[name] = args


def bool_to_lang(val):
    if (val):
        return true
    return false


def evaluate_bool(t):
    val = ""
    for line in t.children:
        if type(line) == Token:
            exp = line.value
            if exp == true:
                val += " True "
            else:
                val += " False "
        elif type(line) == str:
            val += line
        elif line.data == "bool":
            val += str(evaluate_bool(line))
        elif line.data == "bool_sep" or line.data == "bool_comp":
            val += " " + line.children[0].value + " "
        elif line.data == "bool_opp":
            val += " not "
        elif line.data == "value":
            val += str(get_backend_value(line))
    return eval(val)


def get_lang_value(value):
    if type(value) == Tree:
        return get_value(value)
    elif type(value) == bool:
        return bool_to_lang(value)
    elif type(value) == str:
        return value.strip("\"")
    else:
        return value


def get_value(t):
    if t.data == "value":
        val = t.children[0]
        if val.data == "bool":
            return bool_to_lang(evaluate_bool(val))
        elif val.data == "string":
            return val.children[0].value.strip("\"")
        elif val.data == "variable":
            return get_lang_value(get_var(val))
        elif val.data == "calculation":
            calc = ""
            for c in val.children:
                if c.data == "math_symbol":
                    calc += " " + c.value + " "
                else:
                    calc += str(get_value(c))
            return eval(calc)

        return val.children[0].value
    else:
        raiseException("Non-value was passed")


def get_backend_value(t):
    if t.data == "value":
        val = t.children[0]
        if val.data == "bool":
            return evaluate_bool(val)
        elif val.data == "string":
            return val.children[0].value
        elif val.data == "variable":
            return get_var(val)
        elif val.data == "num":
            return int(val.children[0].value)
        elif val.data == "calculation":
            calc = ""
            for c in val.children:
                if c.data == "math_symbol":
                    calc += " " + c.children[0].value + " "
                else:
                    calc += str(get_value(c))
            return eval(calc)
        return val.children[0].value
    else:
        raiseException("Non-value was passed")


def assign_value(t):
    var = ""
    for i, line in enumerate(t.children):
        if i == 0:
            var = line.value
            if var in illegalNames:
                raiseException(
                    "\"" + var + "\" cannot be used as a variable."
                )
        elif line.data == "value":
            variables[var] = get_backend_value(t.children[i])


def get_var(t):
    if t.data == "variable":
        var = t.children[0].value
        if var in variables.keys():
            return variables[var]
        else:
            raiseException(
                "The variable \"" + var + "\" has not been defined."
            )


def run_instruction(t):
    if t.data == "statement" or t.data == "single_line":
        run_instruction(t.children[0])
    elif t.data == "if":
        boolean = True
        for line in t.children:
            if line.data == "value":
                boolean = get_backend_value(line)
            elif line.data == "statement" and boolean:
                run_instruction(line.children[0])
        return boolean
    elif t.data == "if_statement":
        for c in t.children:
            if c.data == "if":
                success = run_instruction(c)
                if success:
                    return
            elif c.data == "statement":
                run_instruction(c.children[0])
    elif t.data == "assignment":
        assign_value(t)
    elif t.data == "function_call":
        func = ""
        args = []
        for i, val in enumerate(t.children):
            if i == 0:
                func = val.value
            else:
                args.append(get_lang_value(t.children[i]))
        run_function(func, *tuple(args))
    elif t.data == "for":
        c = t.children
        variables[c[0].children[0].value] = int(c[1].children[0].value)
        if type(c[3].children[0]) == Tree:
            for_loop_step(
                c[4:],
                c[0].children[0].value,
                int(c[2].children[0].value)
            )
        else:
            for_loop_step(
                c[4:],
                c[0].children[0].value,
                int(c[2].children[0].value),
                int(c[3].children[0].value)
            )
    elif t.data == "while":
        while True:
            boolean = True
            for line in t.children:
                if line.data == "value":
                    boolean = get_backend_value(line)
                    if not boolean:
                        return
                elif line.data == "statement" and boolean:
                    run_instruction(line.children[0])
    elif t.data == "function":
        create_function(t)


def for_loop_step(instructions, var, maximum, step=None):
    if (variables[var] <= maximum):
        for i in instructions:
            run_instruction(i)
        if step != None:
            variables[var] += step
        for_loop_step(instructions, var, maximum, step)


def run_file(program):
    parse_tree = parser.parse(program)
    # print(parse_tree.pretty())
    for inst in parse_tree.children:
        run_instruction(inst)


def main():
    try:
        if len(argv) < 2:
            raiseException("A filename must be given as an argument.")
        with open(argv[1], "r") as f:
            text = f.read()
            run_file(text)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
