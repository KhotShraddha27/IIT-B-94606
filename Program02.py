#  Comma-separated user input
numbers = input("Enter numbers (comma-separated): ")

# Split input and convert to integers
nums_list = numbers.split(",")
even_count = 0
odd_count = 0

# Even-Odd num_count
for n in nums_list:
    num = int(n.strip())
    if num % 2 == 0:
        even_count += 1
    else:
        odd_count += 1

# Print results
print("Even numbers:", even_count)
print("Odd numbers:", odd_count)
