from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from project.generators.primes import get_kth_prime

# Тест для простых чисел
@pytest.mark.parametrize("k, expected", [
    (1, 2),
    (2, 3),
    (3, 5),
    (4, 7),
    (5, 11),
])
def test_get_kth_prime(k, expected):
    assert get_kth_prime(k) == expected


# Тест на исключение при k < 1
@pytest.mark.parametrize("k", [-1, 0])
def test_get_kth_prime_invalid_k(k):
    with pytest.raises(ValueError, match="k должно быть больше или равно 1"):
        get_kth_prime(k)


def test_prime_generator_first_primes(prime_gen):
    """Test if the first few prime numbers are generated correctly."""
    assert next(prime_gen) == 2
    assert next(prime_gen) == 3
    assert next(prime_gen) == 5
    assert next(prime_gen) == 7
    assert next(prime_gen) == 11
    assert next(prime_gen) == 13
