def area(r):
    a=3.14*r*r
    return a
 
l1=[1,2,3]
for i in l1:
    s=area(i)
    print("the area is "'{0:5f}'.format(s))