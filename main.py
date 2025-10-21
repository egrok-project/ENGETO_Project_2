# Projekt 2 - Bulls & Cows
# Autor: Emil Grokhotov
# Popis: Hra Bulls & Cows v konzoli s omezeným počtem pokusů, statistikami a časem.

from random import choice, sample
from typing import Tuple
import time

LENGTH = 4
SEPARATOR = "-" * 47


def generate_secret() -> str:
    """Generate random 4-digit number as string. Have unique digits and not start with zero."""
    first = choice("123456789")
    others = sample([d for d in "0123456789" if d != first], LENGTH - 1)
    return first + "".join(others)


def validate_guess(guess: str) -> Tuple[bool, str]:
    """Check player's guess. Return (valid, error_message)."""
    if len(guess) != LENGTH:
        return False, f"Guess must be {LENGTH} digits long."
    if not guess.isdigit():
        return False, "Guess must contain only digits."
    if guess[0] == "0":
        return False, "Guess must not start with zero."
    if len(set(guess)) != len(guess):
        return False, "Guess must not contain duplicate digits."
    return True, ""


def count_bulls_cows(secret: str, guess: str) -> Tuple[int, int]:
    """Return number of bulls (correct digit & place) and cows (correct digit, wrong place)."""
    bulls = sum(s == g for s, g in zip(secret, guess))
    common = sum(min(secret.count(d), guess.count(d)) for d in set(guess))
    cows = common - bulls
    return bulls, cows


def fmt_unit(word: str, n: int) -> str:
    """Return string with correct singular/plural form."""
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def play_game() -> Tuple[int, float, bool]:
    """Play one game. Return (guesses, duration, success)."""
    print("Hi there!")
    print(SEPARATOR)
    print("I've generated a random 4 digit number for you.")
    print("Let's play a bulls and cows game.")
    print(SEPARATOR)

    # choose attempts
    attempts_limit: int | None = None
    choice_limit = input("Set maximum attempts (Enter for unlimited): ").strip()
    if choice_limit.isdigit():
        attempts_limit = int(choice_limit)
        print(f"You have {attempts_limit} attempts.")
    else:
        print("No limit. Guess until correct!")

    print(SEPARATOR)
    print("Enter a number:")
    print(SEPARATOR)

    secret = generate_secret()
    guesses = 0
    start_time = time.time()

    while True:
        guess = input(">>> ").strip()
        valid, msg = validate_guess(guess)
        if not valid:
            print(f"Invalid guess: {msg}")
            continue

        guesses += 1
        bulls, cows = count_bulls_cows(secret, guess)

        if bulls == LENGTH:
            duration = time.time() - start_time
            print("Correct, you've guessed the right number")
            print(f"in {guesses} guesses!")
            print(f"Time taken: {duration:.1f} seconds")
            print(SEPARATOR)
            print("That's amazing!")
            return guesses, duration, True

        if attempts_limit is not None and guesses >= attempts_limit:
            duration = time.time() - start_time
            print("Out of attempts! The secret number was:", secret)
            return guesses, duration, False

        bulls_str = fmt_unit("bull", bulls)
        cows_str = fmt_unit("cow", cows)
        print(f"{bulls_str}, {cows_str}")


def show_stats(stats: list[Tuple[int, float, bool]]) -> None:
    """Display statistics of all games played."""
    if not stats:
        return
    games = len(stats)
    wins = sum(1 for _, _, success in stats if success)
    avg_guesses = sum(g for g, _, _ in stats) / games
    avg_time = sum(t for _, t, _ in stats) / games
    print(SEPARATOR)
    print(f"Games played: {games}")
    print(f"Wins: {wins}, Losses: {games - wins}")
    print(f"Average guesses: {avg_guesses:.2f}")
    print(f"Average time: {avg_time:.1f} seconds")


def main() -> None:
    """Main loop with replay and statistics."""
    stats: list[Tuple[int, float, bool]] = []

    while True:
        guesses, duration, success = play_game()
        stats.append((guesses, duration, success))

        again = input("Do you want to play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing! Bye!")
            show_stats(stats)
            break


if __name__ == "__main__":
    main()
