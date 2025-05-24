def main():
    print("Welcome to the Magazine Database CLI")
    while True:
        print("\nOptions:")
        print("1. List all magazines")
        print("2. Find top publisher")
        print("3. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            from lib.models.magazine import Magazine
            for mag in Magazine.all():
                print(f"{mag.id}: {mag.name} ({mag.category})")
        elif choice == "2":
            from lib.models.magazine import Magazine
            top = Magazine.top_publisher()
            if top:
                print(f"Top Publisher: {top.name}")
            else:
                print("No publisher data.")
        elif choice == "3":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
