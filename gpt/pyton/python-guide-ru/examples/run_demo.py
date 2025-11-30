from package import greet


def main() -> None:
    for person in ("Алиса", "Боб", "Чарли"):
        print(greet(person))


if __name__ == "__main__":
    main()
