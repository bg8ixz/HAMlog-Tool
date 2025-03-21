import random
import string

def generate_string():
    return 'B' + random.choice('GHD') + str(random.randint(0, 9)) + ''.join(random.choices(string.ascii_uppercase, k=3))

unique_strings = set()
while len(unique_strings) < 100:
    candidate = generate_string()
    if candidate not in unique_strings:
        unique_strings.add(candidate)

# Now, unique_strings contains 100 unique strings with the fourth to sixth characters being uppercase letters.
# To display these strings, you can add the following lines:
for s in unique_strings:
    print(s)