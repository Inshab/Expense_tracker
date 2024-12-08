from connection import create_connection, close_connection, register_user, authenticate_user
import datetime

# Function to add an expense
def add_expense(user_id, amount, category, description):
    connection = create_connection()
    cursor = connection.cursor()
    
    query = """
    INSERT INTO expenses (amount, category, description, date, user_id) 
    VALUES (%s, %s, %s, %s, %s)
    """
    expense_data = (amount, category, description, datetime.datetime.now(), user_id)
    
    try:
        cursor.execute(query, expense_data)
        connection.commit()
        print(f"Expense of ${amount} added in category '{category}' with description: {description}")
    except Exception as e:
        print(f"Error while adding expense: {e}")
    finally:
        close_connection(connection)

# Function to show daily expenses
def show_daily_expenses(user_id):
    today = datetime.datetime.now().date()
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM expenses WHERE DATE(date) = %s AND user_id = %s"
    
    try:
        cursor.execute(query, (today, user_id))
        daily_expenses = cursor.fetchall()
        if not daily_expenses:
            print("No expenses recorded for today.")
        else:
            print("\nToday's Expenses:")
            for expense in daily_expenses:
                print(f"{expense[3]} - ${expense[1]} - Category: {expense[2]} - Description: {expense[3]} - Date and time: {expense[4]}")
                
    except Exception as e:
        print(f"Error fetching daily expenses: {e}")
    finally:
        close_connection(connection)

# Function to show weekly expenses
def show_weekly_expenses(user_id):
    today = datetime.datetime.now()
    start_of_week = today - datetime.timedelta(days=today.weekday())  # Monday of the current week
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM expenses WHERE date >= %s AND user_id = %s"
    
    try:
        cursor.execute(query, (start_of_week, user_id))
        weekly_expenses = cursor.fetchall()
        if not weekly_expenses:
            print("No expenses recorded this week.")
        else:
            print("\nThis Week's Expenses:")
            for expense in weekly_expenses:
                print(f"{expense[3]} - ${expense[1]} - Category: {expense[2]} - Description: {expense[3]}")
    except Exception as e:
        print(f"Error fetching weekly expenses: {e}")
    finally:
        close_connection(connection)

# Function to show monthly expenses
def show_monthly_expenses(user_id):
    today = datetime.datetime.now()
    start_of_month = today.replace(day=1)  # First day of the current month
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM expenses WHERE date >= %s AND user_id = %s"
    
    try:
        cursor.execute(query, (start_of_month, user_id))
        monthly_expenses = cursor.fetchall()
        if not monthly_expenses:
            print("No expenses recorded this month.")
        else:
            print("\nThis Month's Expenses:")
            for expense in monthly_expenses:
                print(f"{expense[3]} - ${expense[1]} - Category: {expense[2]} - Description: {expense[3]}")
    except Exception as e:
        print(f"Error fetching monthly expenses: {e}")
    finally:
        close_connection(connection)

# Function to show total expenses
def show_total_expenses(user_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT SUM(amount) FROM expenses WHERE user_id = %s"
    
    try:
        cursor.execute(query, (user_id,))
        total_expenses = cursor.fetchone()[0]
        print(f"\nTotal Expenses Recorded: ${total_expenses}")
    except Exception as e:
        print(f"Error fetching total expenses: {e}")
    finally:
        close_connection(connection)

# Function to show category summary
def show_category_summary(user_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT category, SUM(amount) FROM expenses WHERE user_id = %s GROUP BY category"
    
    try:
        cursor.execute(query, (user_id,))
        category_summary = cursor.fetchall()
        if not category_summary:
            print("No category summary available.")
        else:
            print("\nCategory Summary:")
            for category, total in category_summary:
                print(f"{category}: ${total}")
    except Exception as e:
        print(f"Error fetching category summary: {e}")
    finally:
        close_connection(connection)

# Main function to handle user registration, login, and interactions with the tracker
def main():
    connection = create_connection()

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Register User")
        print("2. Login")
        print("3. Exit")

        choice = input("\nPlease select an option (1-3): ")

        if choice == '1':
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            register_user(connection, email, password)

        elif choice == '2':
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            user_id = authenticate_user(connection, email, password)

            if user_id:
                print(f"Logged in as {email}.")
                while True:
                    print("\nExpense Tracker Menu:")
                    print("1. Add Expense")
                    print("2. Show Daily Expenses")
                    print("3. Show Weekly Expenses")
                    print("4. Show Monthly Expenses")
                    print("5. Show Total Expenses")
                    print("6. Show Category Summary")
                    print("7. Logout")

                    action = input("\nSelect an action (1-7): ")

                    if action == '1':
                        amount = float(input("Enter amount: "))
                        category = input("Enter category: ")
                        description = input("Enter description: ")
                        add_expense(user_id, amount, category, description)

                    elif action == '2':
                        show_daily_expenses(user_id)

                    elif action == '3':
                        show_weekly_expenses(user_id)

                    elif action == '4':
                        show_monthly_expenses(user_id)

                    elif action == '5':
                        show_total_expenses(user_id)

                    elif action == '6':
                        show_category_summary(user_id)

                    elif action == '7':
                        print("Logging out...")
                        break

            else:
                print("Login failed. Try again.")

        elif choice == '3':
            close_connection(connection)
            print("Exiting program.")
            break


main()