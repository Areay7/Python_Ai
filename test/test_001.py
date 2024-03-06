p = 0

for i in range(2,100):
    for j in range(2,i):
        if i % j == 0:
            break
    else:
        print(i , end='  ')
        p = i
print("\n最大素数: ", p, end=' ')
