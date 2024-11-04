import pandas as pd
import hashlib

df = pd.read_csv("nume_cu_cnp.csv", dtype={"CNP": str})
df = df.dropna(subset=["CNP"])  
cnp_list = [(row['CNP'].strip(), index) for index, row in df.iterrows()] 

table_size = 900907  

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
    index = hash_function_concatenated_ascii_and_index(cnp, original_index, table_size)  
    hash_table[index].append(cnp)

df_sample = pd.read_csv("cnp_sample.csv", header=None, names=["CNP", "Original_Index"])

iteration_count = 0
found_count = 0
total_iterations = 0  

for _, row in df_sample.iterrows():
    cnp = str(row['CNP'])  
    original_index = row['Original_Index']
    
    cnp = cnp.strip() 

    index = hash_function_concatenated_ascii_and_index(cnp, original_index, table_size) 
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

    iteration_count += 1  
average_iterations = total_iterations / found_count if found_count > 0 else 0


print(f"Total iterații: {total_iterations}")
print(f"Media iterațiilor per CNP găsit: {average_iterations:.2f}")

non_empty_bins = sum(1 for slot in hash_table if slot)  
print(f"Total sloturi goale: {len(hash_table) - non_empty_bins} din {table_size}")
print(f"Procent sloturi utilizate: {non_empty_bins / table_size:.2%}")

entry_counts = {}
for slot in hash_table:  
    count = len(slot)
    if count > 0:
        if count in entry_counts:
            entry_counts[count] += 1
        else:
            entry_counts[count] = 1

total_slots = len(hash_table)
for count, num_slots in entry_counts.items():
    percentage = (num_slots / total_slots) * 100
    print(f"Procent sloturi cu {count} intrări: {percentage:.2f}%")