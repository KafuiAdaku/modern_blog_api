import os

# Print all environment variables and their values
for key, value in os.environ.items():
    print(f"{key}: {value}")
