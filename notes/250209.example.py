def print_first_element_if_possible(x):
    try:
        print(x[0])
    except:
        pass


x = [3, 4]
print_first_element_if_possible(x)

x = 5
print_first_element_if_possible(x)
