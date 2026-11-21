# Chapter 2: syntax for a JavaScript developer.
# Blocks are indented, not braced. null is None, true is True, && is and.


def greet(name, greeting="Hello", shout=False):
    message = f"{greeting}, {name}!"          # f-string, like `${greeting}, ${name}!`
    if shout and name is not None:
        message = message.upper()
    return message


print(greet("Ada"))                            # Hello, Ada!
print(greet("Ada", shout=True))                # keyword argument: HELLO, ADA!
print(greet("Ada", greeting="Hi"))             # Hi, Ada!

for i, word in enumerate(["read", "chunk", "embed"]):
    print(i, word)
