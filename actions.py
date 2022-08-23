import osascript 


def volume(isPositive, add=5):
    code, out, err = osascript.run("output volume of (get volume settings)")
    total = int(out) + (add if isPositive else -add)
    print(out)
    print(total)
    osascript.run("set volume output volume " + str(total))



