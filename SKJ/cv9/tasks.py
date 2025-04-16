def brackets_depth(input: str) -> list[int]:
    stack: list[str] = []
    depths: list[int] = []
    started_opening: bool = False

    for c in input:
        if c in '(<{[':
            stack.append(c)  
            started_opening = True
            continue

        idx = len(stack) - 1
        if idx < 0:
            continue
        end = stack[idx]

        if any([end == '(' and c == ')', 
                end == '<' and c == '>',
                end == '{' and c == '}',
                end == '[' and c == ']',
                end == '"' and c == '"',
                end == "'" and c == "'"]): 
            if started_opening:
                depths.append(len(stack))
                started_opening = False
            stack.pop()
            continue
        
        raise ValueError("Input is not valid")

    return depths or [0]


def validate(input: str) -> bool:
    stack: list[str] = ['$']  # zavora

    in_double_quotes = False
    in_single_quotes = False

    for i,c in enumerate(input):
        print(c, "for", stack, in_double_quotes, in_single_quotes)

        if c in '(<{[' and not (in_double_quotes or in_single_quotes):
            stack.append(c)

        elif c in ']}>)' and not (in_double_quotes or in_single_quotes):
            if any((stack[len(stack)-1] == "(" and c == ")",
                    stack[len(stack)-1] == "[" and c == "]",
                    stack[len(stack)-1] == "<" and c == ">",
                    stack[len(stack)-1] == "{" and c == "}",
                    )):
                stack.pop()
            else:
                return False

        elif c == '"' and not in_single_quotes:
            if not in_double_quotes:
                stack.append(c)
                in_double_quotes = True

            # is in double quotes
            else: 
                if i > 0 and input[i-1] == '\\':
                    pass
                else:
                    stack.pop()
                    in_double_quotes = False

        elif c == "'" and not in_double_quotes:
            if not in_single_quotes:
                stack.append(c)
                in_single_quotes = True

            # is in double quotes
            else: 
                if i > 0 and input[i-1] == '\\':
                    pass
                else:
                    stack.pop()
                    in_single_quotes = False

        elif not(in_double_quotes or in_single_quotes):
            return False

        print("     ", stack)
                
    return stack[len(stack)-1] == '$'


if __name__ == "__main__":
    # '' = [0]
    # '()' = [1]
    # '[](()){}' = [1,2,1]
    # '[]<(()){}>' = [1,3,2]
    # print(brackets_depth('a'))
    # print(brackets_depth('()'))
    # print(brackets_depth('[](()){}'))
    # print(brackets_depth('[]<(()){}>'))
    # print(brackets_depth('"'))
    # print(brackets_depth("'"))
    # print(validate('"\\"\\"'))
    # print(validate("'a'"))
        # ()   = True
        # (<>) = True
        # (<)> = False # ) does not close <
        # ("") = True
        # "(") = False # no opening (
        # "'" = True
        # "\"" = True

    # print(validate('"\""'))
    # print(validate('"\\"\\"'))
    # print(validate('{[\')>{[\\\'asdf\']}'))
    print(validate('"as\'df"()\'<{[(\' {asdf}'))
