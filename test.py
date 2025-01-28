import pickle

# Load the dictionary from the pickle file
with open('Data/download_info.pkl', 'rb') as f:
    download_info = pickle.load(f)

# Print the original dictionary
print("Original Dictionary:")
print(download_info)

# Create an inverse dictionary
# The key is the file path, and the value is the original URL
inverse_download_info = {v: k for k, v in download_info.items()}

# Print the inverse dictionary
print("\nInverse Dictionary:")
print(inverse_download_info)

# Optional: Save the inverse dictionary to a new pickle file
with open('Data/inverse_download_info.pkl', 'wb') as f:
    pickle.dump(inverse_download_info, f)
print("\nInverse dictionary saved to 'inverse_download_info.pkl'.")