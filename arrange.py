import streamlit as st
import pandas as pd
import numpy as np
import random

def shuffle_array(array):
    for i in range(len(array) - 1, 0, -1):
        j = random.randint(0, i)
        array[i], array[j] = array[j], array[i]

def generate_seat_arrangement(num_rows, num_columns, branch_data):
    seats = list(range(1, num_rows * num_columns + 1))
    shuffle_array(seats)

    seat_arrangement = np.array([[None] * num_columns for _ in range(num_rows)], dtype=object)

    branch_students = []

    for branch_name, num_students in branch_data:
        branch_students.extend([(branch_name, i) for i in range(1, num_students + 1)])

    shuffle_array(branch_students)

    student_counter = 0 

    for row in range(num_rows):
        for col in range(num_columns):
            if student_counter >= len(branch_students):
                return seat_arrangement
            if seat_arrangement[row, col] is None:
                branch_name, student_number = branch_students[student_counter]
                seat_arrangement[row, col] = f"{branch_name} - Seat {student_number}"
                student_counter += 1

    return seat_arrangement

st.title("Exam Seat Arrangement")

num_rows = st.number_input("Number of Rows:", min_value=1, value=4, key="num_rows")
num_columns = st.number_input("Number of Columns:", min_value=1, value=6, key="num_columns")
num_branches = st.number_input("Number of Branches:", min_value=1, value=3, key="num_branches")

branch_data = []

for i in range(num_branches):
    branch_name = st.text_input(f"Branch {i+1} Name:")
    num_students = st.number_input(f"Number of Students in {branch_name}:", min_value=1, value=5)
    branch_data.append((branch_name, num_students))

generate_button = st.button("Generate Seat Arrangement")

if "seat_arrangement" not in st.session_state:
    st.session_state.seat_arrangement = None

if generate_button:
    st.session_state.seat_arrangement = generate_seat_arrangement(num_rows, num_columns, branch_data)

if st.session_state.seat_arrangement is not None:
    st.subheader("Seat Arrangement:")
    df = pd.DataFrame(st.session_state.seat_arrangement)
    st.dataframe(df.style.set_properties(**{'text-align': 'center'}))

st.write("Note: This app ensures students from the same branch are distributed evenly across the seating arrangement.")
