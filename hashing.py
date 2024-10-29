import pandas as pd
import hashlib

# Load the data and ensure CNP is treated as a string
df = pd.read_csv("nume_cu_cnp.csv", dtype={"CNP": str})
df = df.dropna(subset=["CNP"])  # Remove rows where CNP is NaN
cnp_list = [(row['CNP'].strip(), index) for index, row in df.iterrows()]  # Strip whitespace

table_size = 900907  # A prime number for better distribution

# Initialize the hash table as a list of lists
hash_table = [[] for _ in range(table_size)]


# Function to hash using SHA-256
def hash_function_sha256(cnp, original_index, table_size):
    combined_value = f"{cnp}{original_index}".encode()  # Combine CNP and index, encode to bytes
    hash_object = hashlib.sha256(combined_value)  # Create SHA-256 hash
    hash_value = int(hash_object.hexdigest(), 16)  # Convert hex digest to int
    return hash_value % table_size  # Return modulus with table size


def combined_hash(cnp, table_size):
    hash1 = int(cnp) % table_size
    hash2 = sum(ord(digit) for digit in cnp) % table_size
    return (hash1 + hash2) % table_size

# Function to hash using full CNP
def hash_function_full_cnp(cnp, table_size):
    return int(cnp) % table_size  # Convert to int and take modulus



def hash_function_full_cnp_and_index(cnp, original_index, table_size):
    combined_value = f"{cnp}{original_index}"  # Concatenate CNP and original index
    return int(combined_value) % table_size  # Convert to int and take modulus

# Function to hash using concatenated ASCII values
def hash_function_concatenated_ascii(cnp, table_size):
    ascii_values = ''.join(str(ord(digit)) for digit in cnp)  # Concatenate ASCII values as a string
    return int(ascii_values) % table_size  # Convert to int and take modulus

# Function to hash using concatenated ASCII values and original index
def hash_function_concatenated_ascii_and_index(cnp, original_index, table_size):
    cnp = str(cnp)  # Ensure cnp is treated as a string
    ascii_values = ''.join(str(ord(digit)) for digit in cnp)  # Concatenate ASCII values as a string
    combined_value = f"{ascii_values}{original_index}"  # Concatenate ASCII values and original index
    return int(combined_value) % table_size  # Convert to int and take modulus



# Insert CNPs into the hash table and keep track of their indices
for cnp, original_index in cnp_list:
    index = hash_function_concatenated_ascii_and_index(cnp, original_index, table_size)  # Use full CNP hash function for insertion
    print(f"Inserting CNP: {cnp} at index: {index}")  # Debugging print
    hash_table[index].append(cnp)

# Read the sample
df_sample = pd.read_csv("cnp_sample.csv", header=None, names=["CNP", "Original_Index"])

# Search the hash table for each CNP in the sample and count iterations
iteration_count = 0
found_count = 0
total_iterations = 0  # Initialize total iterations to count for all found CNPs

for _, row in df_sample.iterrows():
    # Verifică și convertește CNP-ul la string
    cnp = str(row['CNP'])  # Asigură-te că este un string
    original_index = row['Original_Index']
    
    # Elimină eventualele spații albe
    cnp = cnp.strip()  # Acum poți aplica strip() fără erori

    index = hash_function_concatenated_ascii_and_index(cnp, original_index, table_size)  # Folosește funcția de hash
    # Caută în lista la indexul calculat
    current_iterations = 0  # Contorizează iterațiile pentru CNP-ul curent
    found = False

    for stored_cnp in hash_table[index]:
        current_iterations += 1  # Incrementare contor iterații
        if stored_cnp == cnp:  # Verifică dacă am găsit CNP-ul
            found = True
            break  # Ieși din buclă odată ce ai găsit CNP-ul

    if found:
        found_count += 1
        total_iterations += current_iterations  # Adaugă iterațiile curente la total

    iteration_count += 1  # Contorizează numărul total de CNP-uri verificate
# Calculate the average iterations per found CNP
average_iterations = total_iterations / found_count if found_count > 0 else 0


print(df_sample.head())  # Vezi primele câteva rânduri din df_sample

# Display statistical results
print(f"Total CNP-uri găsite: {found_count}")
print(f"Total iterații: {total_iterations}")
print(f"Media iterațiilor per CNP găsit: {average_iterations:.2f}")

# Check the uniformity of the distribution
non_empty_bins = sum(1 for slot in hash_table if slot)  # Count non-empty slots
print(f"Total sloturi goale: {len(hash_table) - non_empty_bins} din {table_size}")
print(f"Procent sloturi utilizate: {non_empty_bins / table_size:.2%}")

# Distribution analysis of entries in the hash table
entry_counts = {}
for slot in hash_table:
    count = len(slot)
    if count > 0:
        if count in entry_counts:
            entry_counts[count] += 1
        else:
            entry_counts[count] = 1

# Calculate and print percentages
total_slots = len(hash_table)
for count, num_slots in entry_counts.items():
    percentage = (num_slots / total_slots) * 100
    print(f"Procent sloturi cu {count} intrări: {percentage:.2f}%")