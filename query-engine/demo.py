from time import sleep
from app import (
    write_to_db,
    read_from_db,
    update_in_db,
    delete_from_db,
)
from cache.redis import write_to_cache, read_from_cache


def main():
    # Create a new user
    user_id, timestamp = write_to_db("John Doe", "john@example.com")
    print(f"User created with ID: {user_id}")

    # Read the user from cache
    user_data = read_from_cache(user_id)
    if user_data:
        print(f"User found in cache: {user_data}")
    else:
        print("User not found in cache")
        # Read the user from database
        user_data = read_from_db(user_id)
        if user_data:
            print(f"User found in DB: {user_data}")
            # Write the user to cache
            write_to_cache(user_id, user_data, timestamp)
            print("User written to cache")
        else:
            print("User not found in DB")

    # Update the user in the database
    new_email = "johndoe@example.com"
    update_timestamp = update_in_db(user_id, new_email)
    print(f"User updated in DB with new email: {new_email}")

    print(f"Sleep 3s for binlog consumer to read binlog")
    sleep(3)
    # Read the updated user from cache
    updated_user_data = read_from_cache(user_id)
    if updated_user_data:
        print(f"Updated user found in cache: {updated_user_data}")
    else:
        print("Updated user not found in cache")
        # Read the updated user from database
        updated_user_data = read_from_db(user_id)
        if updated_user_data:
            print(f"Updated user found in DB: {updated_user_data}")
            # Write the updated user to cache
            write_to_cache(user_id, updated_user_data, update_timestamp)
            print("Updated user written to cache")
        else:
            print("Updated user not found in DB")

    # Delete the user from the database
    delete_from_db(user_id)
    print(f"User deleted from DB with ID: {user_id}")

    print(f"Sleep 3s for binlog consumer to read binlog")
    sleep(3)
    # Try to read the deleted user from cache
    deleted_user_data = read_from_cache(user_id)
    if deleted_user_data:
        print(f"Deleted user found in cache: {deleted_user_data}")
    else:
        print("Deleted user not found in cache")

    # Try to read the deleted user from database
    deleted_user_data = read_from_db(user_id)
    if deleted_user_data:
        print(f"Deleted user found in DB: {deleted_user_data}")
    else:
        print("Deleted user not found in DB")


if __name__ == "__main__":
    main()
