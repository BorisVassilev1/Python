n = int(input())
s_arr = list(input())
diff_arr = [0] * n

for i in range(len(s_arr)):
    if s_arr[i] == '<':
        diff_arr[i + 1] = diff_arr[i] + 1

    if s_arr[i] == '>':
        diff_arr[i + 1] = diff_arr[i] - 1

min_h = min(diff_arr)
diff = 0 - min_h

h_arr = [0] * n

for i in range(len(diff_arr)):
    h_arr[i] = diff_arr[i] + diff

print(" ".join(map(str, h_arr)))