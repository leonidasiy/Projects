inp_num = input("Enter the number (base 10): ")
inp_base = input("Enter the base: ")

num, base = int(inp_num), int(inp_base)
mapping = {10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F", 16: "G", 17: "H", 18: "I", 19: "J", 20: "K", 21: "L", 22: "M", 23: "N", 
           24: "O", 25: "P", 26: "Q", 27: "R", 28: "S", 29: "T", 30: "U", 31:"V" , 32: "W", 33: "X", 34: "Y", 35: "Z"}
def convbase(num, base):
    num_ = ""
    while num > 0:
        digit = num % base
        if digit > 9:
            digit = mapping[digit]
        num_ = str(digit) + num_
        num //= base
    return num_
print(convbase(num, base), f"(base {base})")