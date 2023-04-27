print(bool("False"))

def varb(values):
    values[0] = 42
    return values


val = [1, 2, 3]
varb(val)
print(val)

a = (1, 2)
b = (3, 4)

a = a + b
print(a)