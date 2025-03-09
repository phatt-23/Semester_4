import dataclasses
import enum
from typing import Callable, Generic, List, Optional, TypeVar


def cached(f):

    cache = {} 

    def wrapper(*args, **kwargs):
        nonlocal cache 
        if args in cache:
            return cache[args]
        if len(cache) == 3:
            cache.pop(next(iter(cache)))  # pop the first (oldest)
        result = f(*args)
        cache[args] = result
        return result
    return wrapper

@cached
def fn(a, b):
    return a + b # imagine an expensive computation


T = TypeVar("T")


@dataclasses.dataclass
class ParseResult(Generic[T]):
    value: Optional[T]
    rest: str

    @staticmethod
    def invalid(rest: str) -> "ParseResult":
        return ParseResult(value=None, rest=rest)

    def is_valid(self) -> bool:
        return self.value is not None


Parser = Callable[[str], ParseResult[T]]


def parser_char(char: str) -> Parser[str]:
    if len(char) != 1:
        raise ValueError

    def closure(input: str) -> ParseResult[str]:
        return ParseResult.invalid(input) if len(input) == 0 or input[0] != char else ParseResult(char, input[1:])

    return closure 

# print(parser_char("x")(" x"))
# print(parser_char("x")("x"))
# print(parser_char("x")("xa"))
# print(parser_char("y")("xa"))

def parser_repeat(parser: Parser[T]) -> Parser[List[T]]:

    def closure(input: str) -> ParseResult[List[T]]: 
        found = []

        while len(input) > 0:
            result = parser(input)
            if not result.is_valid():
                break

            found.append(result.value)
            input = result.rest

        return ParseResult(found, input)
    return closure 

# parser_a = parser_char("a")
# parser = parser_repeat(parser_a)
# print(parser("aaax"))
# print(parser("xa"))

def parser_seq(parsers: List[Parser]) -> Parser:

    def closure(input: str):
        found = []
        rest = input 

        for parser in parsers:
            result = parser(rest)

            if not result.is_valid():
                return ParseResult.invalid(input) 

            found.append(result.value)
            rest = result.rest

        return ParseResult(found, rest)

    return closure

# parser_a = parser_char("a")
# parser_b = parser_char("b")
# parser = parser_seq([parser_a, parser_b, parser_a])
# print(parser("abax"))
# print(parser("ab"))


def parser_choice(parsers: List[Parser]) -> Parser:

    def closure(input: str):
        found = []
        rest = input 

        for parser in parsers:
            result = parser(rest)

            if result.is_valid():
                return ParseResult(result.value, result.rest) 

            found.append(result.value)
            rest = result.rest

        return ParseResult.invalid(input)

    return closure

# parser_a = parser_char("a")
# parser_b = parser_char("b")
# parser = parser_choice([parser_a, parser_b])
# print(parser("ax"))
# print(parser("bx"))
# print(parser("cx"))


R = TypeVar("R")

def parser_map(parser: Parser[R], map_fn: Callable[[R], Optional[T]]) -> Parser[T]:

    def closure(input: str) -> ParseResult[T]:
        result = parser(input)

        if result.value != None:
            value = map_fn(result.value)
            if value != None:
                return ParseResult(value, result.rest)

        return ParseResult.invalid(input)

    return closure

# parser = parser_char("x")
# parser = parser_map(parser, lambda x: None)
# print(parser("xxx"))

# parser_a = parser_char("a")
# parser = parser_map(parser_a, lambda x: x.upper())
# print(parser("ax"))
# print(parser("bx"))
# parser = parser_map(parser_a, lambda x: None)
# print(parser("ax"))


def parser_matches(filter_fn: Callable[[str], bool]) -> Parser[str]:

    def parser(input: str):
        if len(input) == 0:
            return ParseResult.invalid(input)

        if filter_fn(input[0]):
            return ParseResult(input[0], input[1:])

        return ParseResult.invalid(input)

    return parser 

# parser = parser_matches(lambda x: x in ("ab"))
# print(parser("ax"))
# print(parser("bx"))
# print(parser("cx"))
# print(parser(""))

# Use the functions above to implement the functions below.


def parser_string(string: str) -> Parser[str]:

    def parser(input: str):
        if string == "":
            return ParseResult(string, input)

        result = parser_seq([parser_char(c) for c in string])(input)

        if result.value != None:
            return ParseResult("".join(result.value), result.rest)

        return ParseResult.invalid(input)


    return parser

# parser = parser_string("abc")
# print(parser("a"))  #, "a")
# print(parser("ab"))  #  , "ab")
# print(parser("abc"))  #, "abc", "")
# print(parser("abca"))  #, "abc", "a")

# parser = parser_string("foo")
# print(parser("foox"))
# print(parser("fo"))

def parser_int(): # -> Parser[int]:

    def parser(input: str):
        number = parser_choice([parser_char(str(i)) for i in range(10)])
        result = parser_repeat(number)(input)

        if result.value != None and len(result.value) > 0:
            return ParseResult(int("".join(result.value)), result.rest)

        return ParseResult.invalid(input)

    return parser

# parser = parser_int()
# print(parser("a"))
# print(parser(" 1"))
# print(parser("x42"))
# print(parser("123x"))
# print(parser("foo"))

