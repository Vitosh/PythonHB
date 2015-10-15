k = 4
c = [1,2,3,4,5,6]
n = len(c)
arr = [None]*k


def embedded_loops(index):
    if index >= k:
        print(arr)
    else:
        for i in range(0, n):
            arr[index] = i
            embedded_loops(index+1)

embedded_loops(0)
