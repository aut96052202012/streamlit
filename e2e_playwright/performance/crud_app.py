# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import streamlit as st

# Initialize the database in session state if it doesn't exist
if "database" not in st.session_state:
    st.session_state.database = {}


# Function to display the database
def display_database():
    st.subheader("Database")
    for key, value in st.session_state.database.items():
        st.write(
            f"ID: {key}, Name: {value['name']}, Age: {value['age']}, Email: {value['email']}, Address: {value['address']}"
        )


st.title("CRUD App")

# Create tabs for different operations
tab1, tab2, tab3 = st.tabs(["Create", "Update", "Delete"])

# Create a form for the user to input information
with tab1:
    st.header("Create a new record")
    with st.form("create_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        email = st.text_input("Email")
        address = st.text_input("Address")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if name and email and address:
                id = len(st.session_state.database) + 1
                st.session_state.database[id] = {
                    "name": name,
                    "age": age,
                    "email": email,
                    "address": address,
                }
                st.success("Record added successfully!")
            else:
                st.error("Please fill in all fields.")

# Create a form to update information
with tab2:
    st.header("Update an existing record")
    update_id = st.number_input("Enter ID to update", min_value=1, step=1)

    if update_id in st.session_state.database:
        existing_record = st.session_state.database[update_id]
        new_name = st.text_input("New Name", value=existing_record["name"])
        new_age = st.number_input(
            "New Age", min_value=0, max_value=120, value=existing_record["age"]
        )
        new_email = st.text_input("New Email", value=existing_record["email"])
        new_address = st.text_input("New Address", value=existing_record["address"])
    else:
        new_name = st.text_input("New Name")
        new_age = st.number_input("New Age", min_value=0, max_value=120)
        new_email = st.text_input("New Email")
        new_address = st.text_input("New Address")

    update_button = st.button("Update")

    if update_button:
        if update_id in st.session_state.database:
            st.session_state.database[update_id] = {
                "name": new_name,
                "age": new_age,
                "email": new_email,
                "address": new_address,
            }
            st.success("Record updated successfully!")
        else:
            st.error("ID not found.")

# Create a form to delete information
with tab3:
    st.header("Delete a record")
    with st.form("delete_form"):
        delete_id = st.number_input("Enter ID to delete", min_value=1, step=1)
        delete_button = st.form_submit_button("Delete")

        if delete_button:
            if delete_id in st.session_state.database:
                del st.session_state.database[delete_id]
                st.success("Record deleted successfully!")
            else:
                st.error("ID not found.")

display_database()
