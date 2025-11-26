import pandas as pd

# Load the CSV file
data = pd.read_csv("benchmark_results_threads.csv")

# Map column indexes to their names
column_indexes = [1, 3, 5, 7, 9]  # 0-based index for columns C, E, G, I, K
cAnswers = [0, 2, 4, 6, 8]  # 0-based index for columns C, E, G, I, K
columns = [data.columns[idx] for idx in column_indexes]
columnsAnswers = [data.columns[idx] for idx in cAnswers]

# Create the array of tuples
result = []
winner_counts = {col: 0 for col in columns}  # Dictionary to count winners

for index, row in data.iterrows():
    if len(result) >= 100:
        break  # Limit to 100 tuples
    values = [row[col] for col in columns]
    answers = [row[col] for col in columnsAnswers]
    if all(answer == "unknown" for answer in answers):
        continue

    min_value = min(values)
    min_answer = answers[values.index(min_value)]

    while min_answer == "unknown":
        index = values.index(min_value)
        values.pop(values.index(min_value))
        answers.pop(index)
        min_value = min(values)
        min_answer = answers[values.index(min_value)]

    min_column = columns[values.index(min_value)]
    result.append((min_value, min_column))
    winner_counts[min_column] += 1  # Increment the count for the winning column

# Output the result
print("Array of tuples (MIN, column title):")
print(result)

# Output the winner counts
print("\nWinner counts by column:")
for col, count in winner_counts.items():
    print(f"{col}: {count}")
