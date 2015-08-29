def remove_blocks(lst_towers):
    
    for i in range(1, len(lst_towers)-1):        
        for k in range(0, len(lst_towers[i])):            
            b_remove = False
            
            #check height
            if k == len(lst_towers[i])-1:
                b_remove = True
            
            #check left and right
            if k > len(lst_towers[i-1])-1 or k> len(lst_towers[i+1])-1:
                b_remove = True
            
            if b_remove:
                lst_towers[i][k] = 0
    
    lst_towers[0] = [0]
    lst_towers[-1] = [0]
    lst_new = []
    
    for k in range(0,len(lst_towers)-1):
        temp = []
        temp = [x for x in lst_towers[k] if x != 0]
        if len(temp):
            lst_new.append(temp)
    
    return lst_new
    
lines = int(input())
lst_first_line = list(map(int, input().split()))

lst_towers = []

for i in range(0,lines):
    lst_temp = list()
    for z in range(0, lst_first_line[i]):
        lst_temp.append(1)
    lst_towers.append(lst_temp)    

counter = 0

while len(lst_towers):
    lst_towers = remove_blocks(lst_towers)
    counter += 1

print(counter)

