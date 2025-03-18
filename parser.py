import ply.yacc as yacc
from tokens import *

start = "program"

def p_func_ref(p):
    '''func_ref : STRING CALLED FUNC'''
    p[0] = ("FUNC", p[1])

def p_var_ref(p):
    '''var_ref : STRING CALLED VAR'''
    p[0] = ("VAR", p[1])

def p_var_read(p):
    '''var_read : var_ref POSSESSIVE VALUE'''
    p[0] = ("VAR_READ", p[1][1])

def p_LITERAL(p):
    '''
    LITERAL : NUMBER
            | STRING
            | var_read
            | LITERAL PLUS LITERAL
            | LITERAL MINUS LITERAL
            | LITERAL MULTIPLY LITERAL
            | LITERAL DIVIDE LITERAL
            | LITERAL MODULO LITERAL
            | LITERAL EXPONENT LITERAL
            | conditional
    '''
    if len(p) > 2:
        p[0] = ({"+": "PLUS", "-": "MINUS", "*": "MULTIPLY", "/": "DIVIDE", "%": "MODULO", "^": "EXPONENT"}[p[2]], p[1], p[3])
    else: 
        if isinstance(p[1], tuple):
            p[0] = p[1]
        else:
            p[0] = ("NUMBER" if isinstance(p[1], int) else "STRING", p[1])

def p_action(p):
    '''
    action : var_ref TO LITERAL OBJECT ASSIGN
           | var_ref OBJECT INCREMENT
           | var_ref OBJECT DECREMENT
           | var_ref TO INPUT
           | var_ref OBJECT CONV_INT
           | var_ref OBJECT CONV_STRING
           | var_ref OBJECT CONV_FLOAT
           | LITERAL QUOTE PRINT
           | func_ref OBJECT CALL
           | LITERAL OBJECT RETURN
           | END
           | RETURN
    '''

    action_name = verbs[p[len(p) - 1]]
    if action_name == "ASSIGN":
        p[0] = ("ASSIGN", p[1], p[3])
    elif action_name == "PRINT":
        p[0] = ("PRINT", p[1])
    elif action_name == "CALL":
        p[0] = ("CALL", p[1])
    elif action_name == "RETURN":
        if len(p) == 2:
            p[0] = ("RETURN", None)
        else:
            p[0] = ("RETURN", p[1])
    elif action_name == "END":
        p[0] = ("END", )
    elif action_name == "INCREMENT":
        p[0] = ("INCREMENT", p[1])
    elif action_name == "DECREMENT":
        p[0] = ("DECREMENT", p[1])
    elif action_name == "INPUT":
        p[0] = ("INPUT", p[1])
    elif action_name == "CONV_INT":
        p[0] = ("CONV_INT", p[1])
    elif action_name == "CONV_STRING":
        p[0] = ("CONV_STRING", p[1])
    elif action_name == "CONV_FLOAT":
        p[0] = ("CONV_FLOAT", p[1])

    p[0] = [p[len(p) - 1], p[0]]

def p_forloop_line(p):
    '''
    forloop_line : BELOW OBJECT LITERAL TIMES_LOOP
    '''

    p[0] = ("FOR", p[3])

def p_conditional(p):
    '''
    conditional : LITERAL TOPIC LITERAL COMPARE GREATER GREATER_B
                | LITERAL TOPIC LITERAL COMPARE LESSER LESSER_B
                | LITERAL TOPIC LITERAL TO EQUAL EQUAL_B
                | LITERAL TOPIC LITERAL COMPARE GREATER NOT_GREATER_B
                | LITERAL TOPIC LITERAL COMPARE LESSER NOT_LESSER_B
                | LITERAL TOPIC LITERAL TO EQUAL NOT_EQUAL_B
    '''

    if len(p) in [2, 3]:
        p[0] = (reserved[p[1]], )
    else:
        compare_type = reserved[p[5]]
        if compare_type == "GREATER":
            p[0] = (reserved[p[6]][:-2], p[1], p[3])
        elif compare_type == "LESSER":
            p[0] = (reserved[p[6]][:-2], p[1], p[3])
        elif compare_type == "EQUAL":
            p[0] = (reserved[p[6]][:-2], p[1], p[3])

def p_ifstatement_line(p):
    '''
    ifstatement_line : conditional THEN
    '''

    p[0] = ("IF", p[1])

def p_whilestatement(p):
    '''
    whilestatement_line : conditional WHILE
    '''

    p[0] = ("WHILE", p[1])

def p_line(p):
    '''
    line : action TE_VERB_B line
         | action NEGATIVE_TE_VERB_B line
         | action VERB_B
         | action NEGATIVE_VERB_B
         | forloop_line line CONTINUE line
         | forloop_line line
         | ifstatement_line line CONTINUE line
         | ifstatement_line line
         | ifstatement_line line ELSE line
         | ifstatement_line line ELSE line CONTINUE line
         | whilestatement_line line CONTINUE line
         | whilestatement_line line
    '''

    if len(p) == 3:
        if p[2] in base_forms.values():
            verb = p[1][0]
            statement = p[1][1]
            if p[2] != base_forms[verb]:
                raise ValueError("Invalid verb: '{}{}'; did you mean '{}{}'?".format(verb, p[2], verb, base_forms[verb]))
            p[0] = [statement]
        elif p[2] in negative_forms.values():
            verb = p[1][0]
            if p[2] != negative_forms[verb]:
                raise ValueError("Invalid verb: '{}{}'; did you mean '{}{}'?".format(verb, p[2], verb, negative_forms[verb]))
            p[0] = [("SKIP")]
        elif p[1][0] == "FOR":
            p[0] = [("FOR", p[1][1], p[2])]
        elif p[1][0] == "IF":
            p[0] = [("IF", p[1][1], p[2])]
        elif p[1][0] == "WHILE":
            p[0] = [("WHILE", p[1][1], p[2])]
    else:
        if p[2] in te_forms.values():
            verb = p[1][0]
            statement = p[1][1]
            if p[2] != te_forms[verb]:
                raise ValueError("Invalid verb: '{}{}'; did you mean '{}{}'?".format(verb, p[2], verb, te_forms[verb]))
            p[0] = [statement] + p[3]
        elif p[2] in negative_te_forms.values():
            verb = p[1][0]
            if p[2] != negative_te_forms[verb]:
                raise ValueError("Invalid verb: '{}{}'; did you mean '{}{}'?".format(verb, p[2], verb, negative_te_forms[verb]))
            p[0] = [("SKIP")] + p[3]
        elif p[1][0] == "FOR":
            p[0] = [("FOR", p[1][1], p[2])] + p[4]
        elif p[1][0] == "IF":
            if len(p) == 5:
                if p[3] == "そして":
                    p[0] = [("IF", p[1][1], p[2])] + p[4]
                else:
                    p[0] = [("IF", p[1][1], p[2], p[4])]
            elif len(p) == 7:
                p[0] = [("IF", p[1][1], p[2], p[4])] + p[6]
        elif p[1][0] == "WHILE":
            p[0] = [("WHILE", p[1][1], p[2])] + p[4]

def p_program(p):
    '''
    program : program line
            | line
            |
    '''

    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_error(p):
    print(f"Syntax error at {p.value}")

parser = yacc.yacc()