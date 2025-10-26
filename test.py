operator = input("Wat wil je doen(+, -, *, /): ")
x = int(input("Eerste getal: "))
y = int(input("Tweede getal: "))

if operator == "+":
    print(x+y)

elif operator == "-":
    print(x-y)

elif operator == "*":
    print(x*y)

elif operator == "/":
    print(x/y)

else:
    print("error: geen juiste operator")