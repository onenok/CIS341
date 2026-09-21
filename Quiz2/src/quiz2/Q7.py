def hello() -> str:
    return "Hello from quiz2!"


def reverse(n: int) -> int:
    """Reverse the digits of a positive integer.

    Leading zeros disappear, since the result is converted back to an int.
    e.g. reverse(120) == 21
    """
    return int(str(n)[::-1])


def is_palindrome(n: int) -> bool:
    """Return True if n reads the same forwards and backwards."""
    s = str(n)
    return s == s[::-1]


def count_palindromic_sums(limit: int = 1000) -> int:
    """Count how many n in [1, limit] satisfy: n + reverse(n) is a palindrome."""
    return sum(1 for n in range(1, limit + 1) if is_palindrome(n + reverse(n)))

if __name__ == "__main__":
    result = count_palindromic_sums()
    print(f"Count up to 1000: {result}")