import streamlit as st
import snowflake.connector

# Snowflake connection details (replace with your actual credentials)
SNOWFLAKE_ACCOUNT = "your_account"         # e.g., abcde-xy12345
SNOWFLAKE_USER = "your_username"
SNOWFLAKE_PASSWORD = "your_password"
SNOWFLAKE_WAREHOUSE = "your_warehouse"
SNOWFLAKE_DATABASE = "ADMIN"
SNOWFLAKE_SCHEMA = "PUBLIC"

# Create Snowflake connection
def get_connection():
    conn = snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
    return conn

# Create table if it doesn't exist
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PERSONS (
            ID INTEGER AUTOINCREMENT,
            NAME STRING NOT NULL
        )
    """)
    cursor.close()
    conn.close()

# Insert name into table
def insert_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO PERSONS (NAME) VALUES ('" + name + "')")
    cursor.close()
    conn.commit()
    conn.close()

# Streamlit App
def main():
    st.title("Insert Name into Snowflake Table")

    create_table()

    with st.form("name_form"):
        name = st.text_input("Enter name:")
        submitted = st.form_submit_button("Submit")

        if submitted:
            if name.strip():
                insert_name(name.strip())
                st.success(f"Inserted '{name}' into ADMIN.PUBLIC.PERSONS.")
            else:
                st.error("Name cannot be empty.")

if __name__ == "__main__":
    main()
