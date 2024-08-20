import sqlite3
from typing import List, Dict, Union

# Connect to SQLite database (or create it if it doesn't exist)
def connect_db():
    conn = sqlite3.connect("users.db")
    return conn

# Create the users table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,       -- Store aliases as a comma-separated string
                        MMR INTEGER NOT NULL,     -- Store MMR as an integer
                        lane_pref TEXT NOT NULL   -- Store lane preferences as a comma-separated string
                    )''')
    
    conn.commit()
    conn.close()

# Insert a new user into the database
def insert_user(names: List[str], MMR: int, lane_pref: List[float]):
    conn = connect_db()
    cursor = conn.cursor()

    # Insert user data
    cursor.execute('''INSERT INTO users (name, MMR, lane_pref) 
                      VALUES (?, ?, ?)''', (",".join(names), MMR, ",".join(map(str, lane_pref))))
    
    conn.commit()
    conn.close()

# View all users
def view_users() -> List[Dict[str, Union[int, List[str], int, List[float]]]]:
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch all users
    cursor.execute('''SELECT * FROM users''')
    rows = cursor.fetchall()

    conn.close()

    # Convert data into a list of dictionaries
    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "name": row[1].split(","),           # Convert comma-separated names back to list
            "MMR": row[2],                       # MMR as integer
            "lane_pref": list(map(float, row[3].split(",")))  # Convert comma-separated string back to list of floats
        })
    
    return users

# Search for a user by name (partial match on any of their names)
def search_user_by_name(name: str) -> List[Dict[str, Union[int, List[str], int, List[float]]]]:
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch users where any alias matches
    cursor.execute('''SELECT * FROM users WHERE name LIKE ?''', (f'%{name}%',))
    rows = cursor.fetchall()

    conn.close()

    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "name": row[1].split(","),           # Convert comma-separated names back to list
            "MMR": row[2],                       # MMR as integer
            "lane_pref": list(map(float, row[3].split(",")))  # Convert comma-separated string back to list of floats
        })
    
    return users

# Update user information
def update_user(user_id: int, names: List[str] = None, MMR: int = None, lane_pref: List[float] = None):
    conn = connect_db()
    cursor = conn.cursor()

    # Prepare update fields dynamically
    fields = []
    values = []

    if names:
        fields.append("name = ?")
        values.append(",".join(names))
    if MMR:
        fields.append("MMR = ?")
        values.append(MMR)
    if lane_pref:
        fields.append("lane_pref = ?")
        values.append(",".join(map(str, lane_pref)))

    if fields:
        # Generate dynamic query
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
        values.append(user_id)

        # Execute the update
        cursor.execute(query, tuple(values))
        conn.commit()

    conn.close()

# Delete a user by id
def delete_user(user_id: int):
    conn = connect_db()
    cursor = conn.cursor()

    # Delete user
    cursor.execute('''DELETE FROM users WHERE id = ?''', (user_id,))
    conn.commit()

    conn.close()

# Display all users in a readable format
def display_users(users: List[Dict[str, Union[int, List[str], int, List[float]]]]):
    if not users:
        print("No users found.")
        return
    
    for user in users:
        print(f"ID: {user['id']}")
        print(f"Names: {', '.join(user['name'])}")
        print(f"MMR: {user['MMR']}")
        print(f"Lane Preferences: {user['lane_pref']}")
        print("-" * 20)

# Example usage
if __name__ == "__main__":
    # Create the table (only needs to be done once)
    create_table()

    # Insert a few users
    insert_user(["PlayerOne", "AliasOne"], 3000, [0.7, 0.3, 0, 0, 0])
    insert_user(["PlayerTwo", "AliasTwo"], 2800, [0.5, 0.5, 0, 0, 0])
    insert_user(["PlayerThree"], 3200, [0, 0, 0.7, 0.3, 0])

    # View all users
    print("All Users:")
    all_users = view_users()
    display_users(all_users)

    # Search for a user by name
    print("\nSearch for 'PlayerOne':")
    search_result = search_user_by_name("PlayerOne")
    display_users(search_result)

    # Update a user
    print("\nUpdating PlayerTwo's MMR:")
    update_user(user_id=2, MMR=2900)

    # View users after update
    all_users = view_users()
    display_users(all_users)

    # Delete a user
    print("\nDeleting PlayerThree:")
    delete_user(user_id=3)

    # View users after deletion
    all_users = view_users()
    display_users(all_users)

