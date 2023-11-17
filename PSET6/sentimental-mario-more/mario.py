from cs50 import get_int


def main():
    while True:
        height = get_int("Height: ")
        if 1 <= height < 9:
            break

    for i in range(height):
        print(" " * ((height - 1) - i) + "#" * (i + 1) + "  " + "#" * (i + 1))


if __name__ == '__main__':
    main()
