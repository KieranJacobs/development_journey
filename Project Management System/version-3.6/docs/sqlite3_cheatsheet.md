# SQLite3 & Python Cheatsheet

## The Core Flow

Every single time Python talks to the database, it follows these four steps:

1. **Connect**: `conn = sqlite3.connect("database.db")`
2. **Cursor**: `cursor = conn.cursor()`
3. **Execute**: `cursor.execute("SQL COMMAND HERE")`
4. **Commit/Close**: `conn.commit()` (if saving changes) then `conn.close()`

## Parameterized Queries (The `?`)

Never use f-strings for variables in SQL. It causes crashes with apostrophes and opens you to SQL Injection attacks. Use the `?` placeholder and pass a tuple.

| Setup | Syntax
| **One Variable** | `cursor.execute("... WHERE id = ?", (my_id,))` _(Note the trailing comma)_ |
| **Multiple Variables** | `cursor.execute("... VALUES (?, ?)", (val1, val2))` |

## CRUD Operations Dictionary

### 1. CREATE (Insert Data)

Adds a brand new row to a table.

```python
cursor.execute(
    "INSERT INTO projects (title, status) VALUES (?, ?)",
    ("New Project Name", "In Progress")
)
```

### 2. READ (Select Data)

Retrieves information from the database.

Fetch All Rows:

cursor.execute("SELECT \* FROM projects")
all_rows = cursor.fetchall() # Returns a list of all matching rows

Fetch One Specific Row:

cursor.execute("SELECT \* FROM projects WHERE id =?", (target_id))
single_row = cursor.fetchone() # Returns exactly one row (or None)

### 3. UPDATE (Modify Data)

Changes existing data in a row. Always use a WHERE clause, or you will accidentally update every single row in the entire table.

cursor.execute(
"UPDATE projects SET status = ? WHERE id = ?",
("Completed", project_id)
)

### 4. DELETE (Remove Data)

Removes a row entirely. Always use a WHERE clause, or you will delete the whole table.

cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))

### Useful SQLite Quirks

- Booleans: SQLite does not have strict True or False. It uses 1 for True and 0 for False.
- Row Factory: By default, SQLite returns tuples (e.g. (1, "Title", "Status")). By setting conn.row_factory = sqlite3.Row right after connecting, it returns dictionary-like objects so you can call row['title'] instead of guessing the index number.
