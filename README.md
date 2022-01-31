# fastapitest

from this freeCodeCamp.org course: https://youtu.be/0sOvCWFmrtA

## Restricting ORM filter to only show one user's posts
See: https://www.youtube.com/watch?v=0sOvCWFmrtA&t=30468s

## Using psycopg2 instead of SQLAlchemy
This code could be added to app/database.py:
```
# This code is optional, since we're using SQL Alchemy ORM, and not the
# psycopg2 library
# Setup database connection
while True:
    try:
        conn = psycopg2.connect(
            host=settings.database_hostname,
            database=settings.database_name,
            user=settings.database_username,
            password=settings.database_password,
            # Sets up python dict with column name and value
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successful")

        # break out of while loop if true
        break
    except Exception as error:
        print("Database connection failed")
        print("Error: ", error)

        # wait before reconnecting
        time.sleep(2)
```