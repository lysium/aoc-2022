
def main(file):
    f = open(file, "r")
    max_calories = [0, 0, 0]
    elf_calories = 0

    for line in f.readlines():
        line = line.replace("\n", "")
        if line == "":
            for i in range(3):
                if elf_calories >= max_calories[i]:
                    old_max = max_calories[i]
                    max_calories[i] = elf_calories
                    elf_calories = old_max
            elf_calories = 0
            pass
        else:
            calories = int(line)
            elf_calories += calories
    print(max_calories, sum(max_calories))


if __name__ == "__main__":
    main("input01.txt")
