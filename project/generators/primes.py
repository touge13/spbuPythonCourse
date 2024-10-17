def prime_generator():
    """
    Generator function to yield an infinite sequence of prime numbers.
    
    The function keeps track of all primes found so far and uses them 
    to check if the next number is prime. If a number is not divisible 
    by any of the previously found primes, it is considered a prime.
    
    Yields:
        int: The next prime number in the sequence.
    """
    primes = []
    num = 2
    while True:
        if all(num % p != 0 for p in primes):
            primes.append(num)
            yield num
        num += 1


def prime_decorator(func):
    """
    Decorator to retrieve the k-th prime number from the prime generator.
    
    This decorator wraps a function to get the k-th prime number by 
    generating primes one by one until the k-th prime is reached.
    
    Args:
        func (function): The function to wrap that will receive the k-th prime number.
    
    Returns:
        function: A wrapper function that takes an integer k and returns the k-th prime number.
    """
    def wrapper(k):
        if k < 1:
            raise ValueError("k must be greater than or equal to 1")
        gen = prime_generator()
        prime = None
        for _ in range(k):
            prime = next(gen)
        return func(prime)

    return wrapper


@prime_decorator
def get_kth_prime(prime):
    """
    Function to return the k-th prime number.
    
    Args:
        prime (int): The k-th prime number passed by the decorator.
    
    Returns:
        int: The k-th prime number.
    """
    return prime
