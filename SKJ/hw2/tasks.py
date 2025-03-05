import dataclasses
import enum
from typing import Callable, Generic, List, Optional, TypeVar


def cached(f):
    """
    Create a decorator that caches up to 3 function results, based on the same parameter values.

    When `f` is called with the same parameter values that are already in the cache, return the
    stored result associated with these parameter values. You can assume that `f` receives only
    positional arguments (you can ignore keyword arguments).

    When `f` is called with new parameter values, forget the oldest inserted result in the cache
    if the cache is already full.

    Example:
        @cached
        def fn(a, b):
            return a + b # imagine an expensive computation

        fn(1, 2) == 3 # computed
        fn(1, 2) == 3 # returned from cache, `a + b` is not executed
        fn(3, 4) == 7 # computed
        fn(3, 5) == 8 # computed
        fn(3, 6) == 9 # computed, (1, 2) was now forgotten
        fn(1, 2) == 3 # computed again, (3, 4) was now forgotten
    """

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
    """
    Represents result of a parser invocation.
    If `value` is `None`, then the parsing was not successful.
    `rest` contains the rest of the input string if parsing was succesful.
    """
    value: Optional[T]
    rest: str

    @staticmethod
    def invalid(rest: str) -> "ParseResult":
        return ParseResult(value=None, rest=rest)

    def is_valid(self) -> bool:
        return self.value is not None


"""
Represents a parser: a function that takes a string as an input and returns a `ParseResult`.
"""
Parser = Callable[[str], ParseResult[T]]

"""
Below are functions that create new parsers.
They should serve as LEGO blocks that can be combined together to build more complicated parsers.
See tests for examples of usage.

Note that parsers are always applied to the beginning of the string:
```python
parser = parser_char("a")
parser("a")  # ParseResult(value="a", rest="")
parser("xa") # ParseResult(value=None, rest="xa")
```
"""


def parser_char(char: str) -> Parser[str]:
    """
    Return a parser that will parse a single character, `char`, from the beginning of the input
    string.

    Example:
        ```python
        parser_char("x")("x") => ParseResult(value="x", rest="")
        parser_char("x")("xa") => ParseResult(value="x", rest="a")
        parser_char("y")("xa") => ParseResult(value=None, rest="xa")
        ```
    """
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
    """
    Return a parser that will invoke `parser` repeatedly, while it still matches something in the
    input.

    Example:
        ```python
        parser_a = parser_char("a")
        parser = parser_repeat(parser_a)
        parser("aaax") => ParseResult(value=["a", "a", "a"], rest="x")
        parser("xa") => ParseResult(value=[], rest="xa")
        ```
    """
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
    """
    Create a parser that will apply the given `parsers` successively, one after the other.
    The result will be successful only if all parsers succeed.

    Example:
        ```python
        parser_a = parser_char("a")
        parser_b = parser_char("b")
        parser = parser_seq([parser_a, parser_b, parser_a])
        parser("abax") => ParseResult(value=["a", "b", "a"], rest="x")
        parser("ab") => ParseResult(value=None, rest="ab")
        ```
    """
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
    """
    Return a parser that will return the result of the first parser in `parsers` that matches something
    in the input.

    Example:
        ```python
        parser_a = parser_char("a")
        parser_b = parser_char("b")
        parser = parser_choice([parser_a, parser_b])
        parser("ax") => ParseResult(value="a", rest="x")
        parser("bx") => ParseResult(value="b", rest="x")
        parser("cx") => ParseResult(value=None, rest="cx")
        ```
    """
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
    """
    Return a parser that will use `parser` to parse the input data, and if it is successful, it will
    apply `map_fn` to the parsed value.
    If `map_fn` returns `None`, then the parsing result will be invalid.

    Example:
        ```python
        parser_a = parser_char("a")
        parser = parser_map(parser_a, lambda x: x.upper())
        parser("ax") => ParseResult(value="A", rest="x")
        parser("bx") => ParseResult(value=None, rest="bx")

        parser = parser_map(parser_a, lambda x: None)
        parser("ax") => ParseResult(value=None, rest="ax")
        ```
    """
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
    """
    Create a parser that will parse the first character from the input, if it is accepted by the
    given `filter_fn`.

    Example:
        ```python
        parser = parser_matches(lambda x: x in ("ab"))
        parser("ax") => ParseResult(value="a", rest="x")
        parser("bx") => ParseResult(value="b", rest="x")
        parser("cx") => ParseResult(value=None, rest="cx")
        parser("") => ParseResult(value=None, rest="")
        ```
    """
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
    """
    Create a parser that will parse the given `string`.

    Example:
        ```python
        parser = parser_string("foo")
        parser("foox") => ParseResult(value="foo", rest="x")
        parser("fo") => ParseResult(value=None, rest="fo")
        ```
    """
    def parser(input: str):
        if string == "":
            return ParseResult(string, input)

        i = 0
        while i < len(string) and i < len(input):
            if input[i] != string[i]:
                break
            i += 1
        
        if i == len(string):
            return ParseResult(string, input[i:]) 

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

def parser_int() -> Parser[int]:
    """
    Create a parser that will parse a non-negative integer (you don't have to deal with
    `-` at the beginning).

    Example:
        ```python
        parser = parser_int()
        parser("123x") => ParseResult(value=123, rest="x")
        parser("foo") => ParseResult(value=None, rest="foo")
        ```
    """
    def parser(input: str):
        numberChars = ['0','1','2','3','4','5','6','7','8','9']

        if not any([nc in input for nc in numberChars]):
            return ParseResult.invalid(input)

        value = 0
        i = 0
        while i < len(input) and input[i] in numberChars:
            value *= 10 
            value += ord(input[i]) - ord('0')
            i += 1

        if i != 0:
            return ParseResult(value, input[i:])

        return ParseResult.invalid(input)

    return parser

# parser = parser_int()
# print(parser("a"))
# print(parser(" 1"))
# print(parser("x42"))


# parser = parser_int()
# print(parser("123x"))
# print(parser("foo"))
