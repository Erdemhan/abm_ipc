
def onekb():
    with open('1kb.txt', 'r') as file:
        data = file.read()
    return data

def tenkb():
    with open('10kb.txt', 'r') as file:
        data = file.read()
    return data

def hundredkb():
    with open('100kb.txt', 'r') as file:
        data = file.read()
    return data
