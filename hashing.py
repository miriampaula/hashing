import pandas as pd
import hashlib
import matplotlib.pyplot as plt

df = pd.read_csv("nume_cu_cnp.csv", dtype={"CNP": str})
df = df.dropna(subset=["CNP"])  
cnp_list = [(row['CNP'].strip(), index) for index, row in df.iterrows()] 

table_size = 997  

hash_table = [[] for _ in range(table_size)]


def hash_function_sha256(cnp, original_index, table_size):
    combined_value = f"{cnp}{original_index}".encode()   
    hash_object = hashlib.sha256(combined_value)  
    hash_value = int(hash_object.hexdigest(), 16)  
    return hash_value % table_size  


def combined_hash(cnp, table_size):
    hash1 = int(cnp) % table_size
    hash2 = sum(ord(digit) for digit in cnp) % table_size  
    return (hash1 + hash2) % table_size


def hash_function_full_cnp(cnp, table_size):
    return int(cnp) % table_size  


def hash_function_full_cnp_and_index(cnp, original_index, table_size):
    combined_value = f"{cnp}{original_index}" 
    return int(combined_value) % table_size  

def hash_function_concatenated_ascii(cnp, table_size):
    ascii_values = ''.join(str(ord(digit)) for digit in cnp) 
    return int(ascii_values) % table_size  

def hash_function_concatenated_ascii_and_index(cnp, original_index, table_size):
    cnp = str(cnp) 
    ascii_values = ''.join(str(ord(digit)) for digit in cnp) 
    combined_value = f"{ascii_values}{original_index}"  
    return int(combined_value) % table_size  


for cnp, original_index in cnp_list:
    index = hash_function_concatenated_ascii(cnp, table_size)  
    hash_table[index].append(cnp)

# Load the sample file for lookups
df_sample = pd.read_csv("cnp_sample.csv", header=None, names=["CNP", "Original_Index"])
df_sample["CNP"] = df_sample["CNP"].astype(str).str.strip()  # Ensure CNPs are strings and stripped
df_sample["Original_Index"] = df_sample["Original_Index"].astype(str).str.strip()  # Ensure CNPs are strings and stripped


# Stats for sample lookups
iteration_count = 0
found_count = 0
total_iterations = 0
iterations_per_search = []

for _, row in df_sample.iterrows():
    cnp = row["CNP"]
    original_index = row["Original_Index"]

    index = hash_function_concatenated_ascii(cnp, table_size)

    current_iterations = 0
    found = False

    for stored_cnp in hash_table[index]:
        current_iterations += 1
        if stored_cnp == cnp:
            found = True
            break

    if found:
        found_count += 1
        total_iterations += current_iterations
        iterations_per_search.append(current_iterations)

average_iterations = total_iterations / found_count if found_count > 0 else 0

# Slot Utilization and Distribution
non_empty_bins = sum(1 for slot in hash_table if slot)
empty_bins = table_size - non_empty_bins
load_factor = non_empty_bins / table_size

# Entry distribution
entry_counts = {}
for slot in hash_table:
    count = len(slot)
    if count > 0:
        entry_counts[count] = entry_counts.get(count, 0) + 1

entry_counts_df = pd.DataFrame(list(entry_counts.items()), columns=["Entries_Per_Slot", "Number_Of_Slots"])
entry_counts_df["Percentage"] = (entry_counts_df["Number_Of_Slots"] / table_size) * 100

# Distribution statistics output
distribution_statistics = {
    "Total Iterations": total_iterations,
    "Average Iterations Per Found CNP": average_iterations,
    "Empty Slots": empty_bins,
    "Non-Empty Slots": non_empty_bins,
    "Load Factor": load_factor,
}

# Save data to a file
summary_statistics_df = pd.DataFrame({
    "Metric": ["Total Iterations", "Average Iterations Per Found CNP", "Empty Slots", 
               "Non-Empty Slots", "Load Factor"],
    "Value": [total_iterations, average_iterations, empty_bins, non_empty_bins, load_factor]
})
entry_counts_df.to_csv("hash_table_statistics.csv", index=False)
summary_statistics_df.to_csv("hash_table_summary_statistics.csv", index=False)

# Plotting results
# Histogram of entry count per slot
plt.figure(figsize=(10, 6))
plt.bar(entry_counts_df["Entries_Per_Slot"], entry_counts_df["Percentage"])
plt.xlabel("Entries Per Slot")
plt.ylabel("Percentage of Slots (%)")
plt.title("Distribution of Entries Per Slot")
plt.show()

# Histogram of iterations per search
plt.figure(figsize=(10, 6))
plt.hist(iterations_per_search, bins=range(1, max(iterations_per_search) + 1), edgecolor='black', alpha=0.7)
plt.xlabel("Iterations to Find CNP")
plt.ylabel("Frequency")
plt.title("Distribution of Iterations to Find a CNP in Sample Data")
plt.show()

# Print overall statistics to console
print("Overall Distribution Statistics:", distribution_statistics)
print("Entry distribution saved to 'hash_table_statistics.csv'")
print("Summary statistics saved to 'hash_table_summary_statistics.csv'")