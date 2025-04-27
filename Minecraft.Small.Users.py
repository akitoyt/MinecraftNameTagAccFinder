import requests
import random
import string
import itertools

def get_username_length_range():
    while True:
        length_range = input("Enter the desired username length range or a single number (e.g., '3 to 16' or '10'): ")
        try:
            if 'to' in length_range:
                start, end = map(int, length_range.split('to'))
                if 3 <= start <= 16 and 3 <= end <= 16 and start <= end:
                    return range(start, end + 1)
                else:
                    print("Please enter a valid range between 3 and 16.")
            else:
 number
                length = int(length_range)
                if 3 <= length <= 16:
                    return [length]
                else:
                    print("Please enter a valid number between 3 and 16.")
        except ValueError:
            print("Invalid input. Please enter a valid range or number (e.g., '3 to 16' or '10').")

def generate_username(length):
    # Generate a random username with the specified length and mixed case
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_case_variations(username):
    return [''.join(variation) for variation in itertools.product(*[(ch.lower(), ch.upper()) if ch.isalpha() else (ch,) for ch in username])]

def check_namemc_status(username):
    url = f"https://namemc.com/search?q={username}"
    response = requests.get(url)
    
    if any(keyword in response.text for keyword in ["Unavailable"]):
        return False  # Used

    url = f"https://namemc.com/search?q={username}"
    response = requests.get(url)
    
    if any(keyword in response.text for keyword in ["Available"]):
        return True  # used

    return None

def check_username_availability(username, checked_usernames):
    username_lower = username.lower()

    if username_lower in checked_usernames:
        return


    checked_usernames.add(username_lower)

    variations = generate_case_variations(username)
    found_taken = False

    for variant in variations:
        url = f"https://api.mojang.com/users/profiles/minecraft/{variant}"
        response = requests.get(url)

        if "The request is blocked." in response.text:
            return

        if "id" in response.json() and not ("errorMessage" in response.text or "name" in response.json()):
            return  # Ignore this username

        if response.status_code == 400 and "errorMessage" in response.text:
            namemc_status = check_namemc_status(variant)
            if namemc_status:
                print(f"\033[92m{variant} - Available\033[0m")
            else:
                found_taken = True

        if response.status_code == 200 and "name" in response.json():
            found_taken = True
            break
 other variations, username is used
 
    if found_taken:
        print(f"\033[91m{username} - Used\033[0m")  # Red text
    else:
        print(f"\033[92m{username} - Available\033[0m")  # Green text

def main():

    lengths = get_username_length_range()
    
    num_checks = int(input(f"Enter the number of usernames of length(s) {lengths} to generate and check: "))
 usernames (case-insensitive)
    checked_usernames = set()

    for length in lengths:
        print(f"\nChecking usernames of length {length}:")
        for i in range(num_checks):

            if i % 100 == 0:
                print(f"Checking {i + 1} of {num_checks} usernames of length {length}...")

            username = generate_username(length)
            check_username_availability(username, checked_usernames)

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
