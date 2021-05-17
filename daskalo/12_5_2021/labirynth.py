from queue import Queue

import math

n, m = map(int, input().split());

arr = [0] * n;
dist = [0] * n;

for i in range(n):
    arr[i] = list(map(int, input().split()));
    dist[i] = [-1] * m;

k = int(input())
enemies = [0]*k;
for i in range(k):
    enemies[i] = list(map(int, input().split()));

x, y = map(int, input().split());

q = Queue();

q.put(tuple(x,y));
dist[x][y] = 0;

def check(x, y, i, j):    
    if i >= 0 and i < n and j >= 0 and j < m and arr[i][j] == 0 and dist[i][j] == -1:
        dist[i][j] = dist[x][y] + 1;
        q.put(tuple(i,j));

while not q.empty():
    i, j = q.get();
    check(i, j, i-1, j);
    check(i, j, i+1, j);
    check(i, j, i, j-1);
    check(i, j, i, j+1);

print((min([dist[enemies[i][0]][enemies[i][1]] for i in range(k)])+1) // 2);
