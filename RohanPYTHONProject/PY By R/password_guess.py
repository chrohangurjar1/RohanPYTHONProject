import itertools
import string


def password_guess(target_password, max_length):
    characters = string.ascii_letters + string.digits + string.punctuation  # Character set
    attempts = 0

    # Loop through each possible length of password from 1 to max_length
    for length in range(1, max_length + 1):
        # Generate all possible combinations of the given length
        for guess in itertools.product(characters, repeat=length):
            attempts += 1
            guess_password = ''.join(guess)

            # Print the current guess (optional for debugging)
            print(f"Trying: {guess_password}")

            # If the guess matches the target password, return success
            if guess_password == target_password:
                print(f"Password found: '{guess_password}' in {attempts} attempts")
                return True

    print(f"Password not found within {attempts} attempts.")
    return False


# Example usage
target_password = "Rohan15@"  # Change this to the password you're testing
max_length = 8 # Maximum length of password to guess

password_guess(target_password, max_length)
var = 23