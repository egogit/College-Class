import numpy as np
from math import ceil

arr = list(map(int, input().split()))
arr.sort()

n = len(arr)
mn = arr[0]
mx = arr[-1]

K = 1

while(n > 2**K):
    K += 1;


interval = ceil((mx - mn) / K)
firstll = mn - 0.5

ans = [["계급값", "도수", "상대도수", "백분율"]]

for i in range(K):
    ans.append([f"{firstll:.2f}~{(firstll + interval):.2f}", 0, 0, 0])
    for num in arr:
        if firstll <= num <= (firstll + interval):
            ans[-1][1] += 1

    ans[-1][2] = ans[-1][1] / n
    ans[-1][3] = ans[-1][2] * 100
    firstll += interval

for row in ans:
    print("\t".join(map(str, row)))
    
l = len(list(filter(lambda x : x >= 49, arr)))
print(l)
