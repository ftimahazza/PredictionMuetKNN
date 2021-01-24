import streamlit as st
import pandas as pd
from math import sqrt
from csv import reader


st.write("""
# Prediction of MUET Result using KNN algorithm 
""")

# Converting the grade into numerical data
def user_input(course):
    if course == 'A+':
        return 8
    elif course == 'A':
        return 7
    elif course == 'A-':
        return 6
    elif course == 'B+':
        return 5
    elif course == 'B':
        return 4
    elif course == 'B-':
        return 3
    elif course == 'C+':
        return 2
    elif course == 'C':
        return 1


# Load a CSV file
def load_csv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset


# Convert string column to float
def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())


# Calculate the Euclidean distance between two vectors
def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1) - 1):
        distance += (row1[i] - row2[i]) ** 2
    return sqrt(distance)


# Locate the most similar neighbours
def get_neighbours(train, test_row, num_neighbours):
    distances = list()
    for train_row in train:
        dist = euclidean_distance(test_row, train_row)
        distances.append((train_row, dist))
    distances.sort(key=lambda tup: tup[1])
    neighbours = list()
    for i in range(num_neighbours):
        neighbours.append(distances[i][0])
    return neighbours


# Make a prediction with neighbours
def predict_classification(train, test_row, num_neighbours):
    neighbours = get_neighbours(train, test_row, num_neighbours)
    output_values = [row[-1] for row in neighbours]
    prediction = max(set(output_values), key=output_values.count)
    return prediction


# kNN Algorithm
def k_nearest_neighbours(train, test, num_neighbours):
    predictions = list()
    for row in test:
        output = predict_classification(train, row, num_neighbours)
        predictions.append(output)
    return (predictions)


# For user input parameters
st.write('Please enter the grade for each course in capital letter. (For example: A+)')
st.write('The range allows only from C to A+.')

try:
    elc120 = st.text_input('ELC121', 'A')
    elc150 = st.text_input('ELC151', 'A-')
    elc230 = st.text_input('ELC231', 'A')
    elc120 = user_input(elc120)
    elc150 = user_input(elc150)
    elc230 = user_input(elc230)
    input = (elc120, elc150, elc230)
    # Loading csv file
    dataset = load_csv('dataset.csv')

    # Convert class column to float
    for i in range(len(dataset[0]) - 1):
        str_column_to_float(dataset, i)

    # Define K value
    num_neighbours = 9

    # Predict the input of the result
    result = predict_classification(dataset, input, num_neighbours)

    # Displaying the output
    st.subheader('Prediction of MUET Result: ')
    st.write('Band', result)
except:
    st.error('An error occured. Please make sure your input is correct')
    pass


