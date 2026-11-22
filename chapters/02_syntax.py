# Chapter 2: syntax.

def greet(name, greeting="Hello", shout=False):
    message = f"{greeting}, {name}!"
    if shout and name is not None:
        message = message.upper()
    return message


items = []
if not items:
    print("an empty list counts as false")

print(greet("Ada"))
print(greet("Ada", shout=True))
print(greet("Ada", greeting="Hi"))

for i, word in enumerate(["red", "green", "blue"]):
    print(i, word)
