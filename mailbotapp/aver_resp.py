with open("incoming.logs", "r") as f:
    lines = f.readlines()
    diff = []
    for line in lines:
        cont = line.split(":")
        if len(cont) == 3 and cont[0] != "Re":
            diff.append(float(cont[2]) - float(cont[1]))
    print(sum(diff)/len(diff))
    print(len(diff))
