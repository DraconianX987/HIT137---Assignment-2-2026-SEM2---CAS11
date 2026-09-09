# Question 1 (Ian Lu)

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

print(f"\nshift1 = {shift1}\nshift2 = {shift2}")

with open("raw_text.txt", 'r') as f: # raw_text.txt must be in same folder as cipher.py
    content = f.read()

encryption = []

for n in range(0, len(content)):
    encryption.append(content[n])

shift_performed = [] # Used to determine what step to perfrom during decryption to reverse encryption

for e in range (0, len(encryption)): # Will not work for shift inputs of very large values, e.g. 1000
    ascii_value = ord(encryption[e])
    if 97 <= ascii_value <= 110:
        ascii_shift = ascii_value + (shift1 * shift2)
        encryption[e] = chr(ascii_shift)
        shift_performed.append(1)
    elif 111 <= ascii_value <= 122:
        ascii_shift = ascii_value - (shift1 + shift2)
        encryption[e] = chr(ascii_shift)
        shift_performed.append(2)
    elif 65 <= ascii_value <= 77:
        ascii_shift = ascii_value - shift1
        encryption[e] = chr(ascii_shift)
        shift_performed.append(3)
    elif 78 <= ascii_value <= 90:
        ascii_shift = ascii_value + shift2^2
        encryption[e] = chr(ascii_shift)
        shift_performed.append(4)
    elif 48 <= ascii_value <= 57:
        ascii_shift = ascii_value + (shift1 - shift2)
        encryption[e] = chr(ascii_shift)
        shift_performed.append(5)
    else:
        shift_performed.append("Nil") # Values appended to shift_performed correspond to the shifts laid out in assingment 2 instructions. "Nil" is used for "other" characters, which aren't shifted at all

encrypted_text = "".join(encryption)
#print("\n", encrypted_text)

with open("encrypted_text.txt", 'w') as f:
    f.write(encrypted_text)

with open("encrypted_text.txt", 'r') as f:
    content = f.read()

encrypted_text_file = []

for n in range(0, len(content)):
    encrypted_text_file.append(content[n])

decryption = []

for d in range(0, len(encrypted_text_file)):
    ascii_value = ord(encrypted_text_file[d])
    if shift_performed[d] == 1:
        ascii_shift = ascii_value - (shift1 * shift2)
        decryption.append(chr(ascii_shift))
    elif shift_performed[d] == 2:
        ascii_shift = ascii_value + (shift1 + shift2)
        decryption.append(chr(ascii_shift))
    elif shift_performed[d] == 3:
        ascii_shift = ascii_value + shift1
        decryption.append(chr(ascii_shift))
    elif shift_performed[d] == 4:
        ascii_shift = ascii_value - shift2^2
        decryption.append(chr(ascii_shift))
    elif shift_performed[d] == 5:
        ascii_shift = ascii_value - (shift1 - shift2)
        decryption.append(chr(ascii_shift))
    else:
        decryption.append(encrypted_text_file[d]) # No transformation required. This line just appends the "other" characters to the decryption list

decrypted_text = "".join(decryption)
#print("\n", decrypted_text)

with open("decrypted_text.txt", 'w') as f:
    f.write(decrypted_text)