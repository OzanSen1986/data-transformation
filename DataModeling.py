from typing import Callable, TypeAlias, Union


Predicate: TypeAlias = Callable[[int], bool]
StringProcessor: TypeAlias = Callable[[str], str]
Comparator: TypeAlias = Callable[[any, any], bool]

def filter_numbers(numbers: list[int], predicate: Predicate) -> list[int]:
    return [n for n in numbers if predicate(n)]


#usage

is_even: Predicate = lambda x: x % 2 == 0
result = filter_numbers([1, 2, 3, 4, 5], is_even)
print(result)


# Instead of this messy signature:
def process_data(data: dict[str, Union[list[tuple[int, str]], dict[str, float]]]) -> None:
    pass

# Use this:
ComplexData: TypeAlias = dict[str, Union[list[tuple[int, str]], dict[str, float]]]

def process_data(data: ComplexData) -> None:
    pass


