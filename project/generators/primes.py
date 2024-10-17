def prime_generator():
    primes = []
    num = 2
    while True:
        if all(num % p != 0 for p in primes):
            primes.append(num)
            yield num
        num += 1


def prime_decorator(func):
    def wrapper(k):
        if k < 1:
            raise ValueError("k должно быть больше или равно 1")
        gen = prime_generator()
        prime = None
        for _ in range(k):
            prime = next(gen)
        return func(prime)

    return wrapper


@prime_decorator
def get_kth_prime(prime):
    return prime
