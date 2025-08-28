from database import init_db


def main():
    print("starting application...")
    init_db()
    print("Database initialized")


if __name__ == "__main__":
    main()