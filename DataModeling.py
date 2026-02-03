from collections.abc import Callable
from typing import Union


Predicate = Callable[[int], bool]
StringProcessor = Callable[[str], bool]
Comparator = Callable[[any, any], bool]

def filter_numbers(numbers: list[int], predicate: Predicate) -> list[int]:
    return [n for n in numbers if predicate(n)]

def data_filter(strings: list[str], stringProcessor: StringProcessor) -> list[str]:
    return [word.upper() for word in strings if stringProcessor(word) > 4]

#usage
is_even: Predicate = lambda x: x % 2 == 0
result = filter_numbers([1, 2, 3, 4, 5], is_even)

# String Processor
make_case_upper: StringProcessor = lambda x: len(x)
result_upper = data_filter(['EMiLy', 'oScaR', 'aLi', 'necdet', 'ozanizmo'], make_case_upper)
print(result_upper)


# Instead of this messy signature:
def process_data(data: dict[str, Union[list[tuple[int, str]], dict[str, float]]]) -> None:
    pass

# Use this:
ComplexData = dict[str, Union[list[tuple[int, str]], dict[str, float]]]

def process_data(data: ComplexData) -> None:
    pass

