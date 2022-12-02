
def main(file):
    f = open(file, "r")
    max_calories = 0
    elf_calories = 0

    for line in f.readlines():
        line = line.replace("\n", "")
        if line == "":
            max_calories = max(max_calories, elf_calories)
            elf_calories = 0
            pass
        else:
            calories = int(line)
            elf_calories += calories
    print(max_calories)


if __name__ == "__main__":
    main("input.txt")
