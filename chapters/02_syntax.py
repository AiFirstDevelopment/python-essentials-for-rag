# Chapter 2: syntax. Blocks are indented. The empty value is None; the booleans are True and False.


def greet(name, greeting="Hello", shout=False):
    message = f"{greeting}, {name}!"          # an f-string puts values into text
    if shout and name is not None:
        message = message.upper()
    return message


print(greet("Ada"))                            # Hello, Ada!
print(greet("Ada", shout=True))                # keyword argument: HELLO, ADA!
print(greet("Ada", greeting="Hi"))             # Hi, Ada!

for i, word in enumerate(["read", "chunk", "embed"]):
    print(i, word)
