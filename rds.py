import pymysql

# Database connection details
endpoint = 'database-1.cojyimmwa5y5.us-east-1.rds.amazonaws.com'
port = 3306
db_name = 'db1'
username = 'admin'
password = 'ugdqwq237e8yuhs'

def connect_to_database(endpoint, port, db_name, username, password):
    return pymysql.connect(
        host=endpoint,
        port=port,
        user=username,
        password=password,
        db=db_name
    )

def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            gender ENUM('male','female') NOT NULL
        )
    ''')

def insert_data(cursor, conn, name, age, gender):
    cursor.execute('''
        INSERT INTO users (name, age, gender) VALUES (%s, %s, %s)
    ''', (name, age, gender))
    conn.commit()

def read_data(cursor):
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()

def update_data(cursor, conn, name, age, gender):
    cursor.execute('''
        UPDATE users SET age=%s, gender=%s WHERE name=%s
    ''', (age, gender, name))
    conn.commit()

def delete_data(cursor, conn, name):
    cursor.execute('''
        DELETE FROM users WHERE name=%s
    ''', (name,))
    conn.commit()

def main():
    try:
        conn = connect_to_database(endpoint, port, db_name, username, password)
        cursor = conn.cursor()

        create_table(cursor)

        while True:
            print("\nSelect an operation:")
            print("1. Insert data (Create)")
            print("2. Query data (Read)")
            print("3. Update data")
            print("4. Delete data")
            print("5. Exit")

            choice = input("Enter choice (1-5): ")

            if choice == '1':
                name = input("Enter name: ")
                age = int(input("Enter age: "))
                gender = input("Enter gender (male/female): ").lower()
                if gender not in ['male', 'female']:
                    print("Invalid gender. Must be 'male' or 'female'.")
                    continue
                insert_data(cursor, conn, name, age, gender)
                print(f"Inserted {name}, {age}, {gender}")

            elif choice == '2':
                rows = read_data(cursor)
                print("Users:")
                for row in rows:
                    print(row)

            elif choice == '3':
                name = input("Enter name to update: ")
                age = int(input("Enter new age: "))
                gender = input("Enter new gender (male/female): ").lower()
                if gender not in ['male', 'female']:
                    print("Invalid gender. Must be 'male' or 'female'.")
                    continue
                update_data(cursor, conn, name, age, gender)
                print(f"Updated {name} to age {age}, gender {gender}")

            elif choice == '4':
                name = input("Enter name to delete: ")
                delete_data(cursor, conn, name)
                print(f"Deleted {name}")

            elif choice == '5':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

    except pymysql.MySQLError as e:
        print(f"Error: {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    main()
