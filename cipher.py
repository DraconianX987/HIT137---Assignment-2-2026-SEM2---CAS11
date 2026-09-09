# Question 1

shift = [0,0]
i = 0

while i < 2:
    user_input = input(f"Enter shift{i+1} (must be a non-negative integer): ")
    try:
        number = int(user_input)
        if number >= 0:
            shift[i] = number
            i += 1
        else:
            print("Negative integer entered")
    except ValueError:
        print("ERROR (non-integer entered)")

shift1 = shift[0]
shift2 = shift[1]

print(shift1, shift2)