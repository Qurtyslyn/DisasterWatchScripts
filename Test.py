def get_dimensions(lst):
    if not isinstance(lst, list):
        print("Not List")
        return
    else:
        print("List")

        return[get_dimensions(lst[0])]


poly = [[[123,152],[145,678]]]
test = [[123,234],[325,675]]

#print(poly)
#print(len(poly))
#print(len(poly[0]))

#print(get_dimensions(poly))

#print(isinstance(poly,list[0]))
#print(isinstance(poly[0][0][0],list))

def checkPolygonDepth(lst):
    if  not isinstance(lst, list):
        return 0
    elif isinstance(lst, list) and not isinstance(lst[0], list):
        return 1
    elif isinstance(lst, list) and isinstance(lst[0], list) and not isinstance(lst[0][0], list):
        return 2
    else:
        return 3
    
print(checkPolygonDepth(poly))
print(checkPolygonDepth(test))
print(checkPolygonDepth(test[0]))