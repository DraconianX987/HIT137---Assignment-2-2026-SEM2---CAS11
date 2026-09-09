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

with open("raw_text.txt", 'r') as f:
    content = f.read()

encryption = []

for n in range(0, len(content)):
    encryption.append(content[n])

#print(encryption)
print("\n")

for e in range (0, len(encryption)):
    ascii_value = ord(encryption[e])
    if 97 <= ascii_value <= 110:
        ascii_shift = ascii_value + (shift1 * shift2)
        encryption[e] = chr(ascii_shift)
    if 111 <= ascii_value <= 122:
        ascii_shift = ascii_value - (shift1 + shift2)
        encryption[e] = chr(ascii_shift)
    if 65 <= ascii_value <= 77:
        ascii_shift = ascii_value - shift1
        encryption[e] = chr(ascii_shift)
    if 78 <= ascii_value <= 90:
        ascii_shift = ascii_value + shift2^2
        encryption[e] = chr(ascii_shift)
    if 48 <= ascii_value <= 57:
        ascii_shift = ascii_value + (shift1 - shift2)
        encryption[e] = chr(ascii_shift)

#print(encryption)