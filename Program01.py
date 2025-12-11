# User Input
sentence = input("Enter a sentence: ")

# Number of characters
num_chars = len(sentence)

# Number of words
words = sentence.split()
num_words = len(words)

# Number of vowels
vowels = "AaEeIiOoUu"
num_vowels = 0

for char in sentence:
    if char in vowels:
        num_vowels += 1

# Print results
print("Number of characters:", num_chars)
print("Number of words:", num_words)
print("Number of vowels:", num_vowels)
