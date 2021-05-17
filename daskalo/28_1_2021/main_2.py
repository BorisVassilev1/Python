n = int(input())
znaci = input()
visochini = [0]
for znak in znaci:
    if znak == '>':
        visochini.append(visochini[-1]-1)
    else:
        visochini.append(visochini[-1]+1)
nai_nisko = min(visochini)
add = 0-nai_nisko
for i in range(len(visochini)):
    visochini[i] += add
print("".join(str(vis)+" " for vis in visochini))