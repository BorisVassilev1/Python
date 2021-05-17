n = int(input())

sequence = input()

raw = [0] * (n + 1)

curr = 1;
print(curr, end = " ");
for ch in sequence:
    if(ch == '<'):
        curr += 1
    elif(ch == '>'):
        curr -= 1
    print(curr, end = " ")
