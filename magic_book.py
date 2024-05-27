import regex
import os
import json
import pickle
import datetime

# Define the emoji whitelist
file_type_cipher = {
    "📝\u200d🔒\u200d💾": ".txt",
    "📝\u200d🔒\u200d📘": ".md",
    "📝\u200d🔒\u200d🔑": ".yaml",
    "📝\u200d🔒\u200d🥒": ".pkl",
    "📝\u200d🔒\u200d🐍": ".py",
    "📝\u200d🔒\u200d🔍": ".json",
    "📝\u200d🔒\u200d🌐": ".html",
    "📝\u200d🔒\u200d🎨": ".css",
    "📝\u200d🔒\u200d📜": ".js",
    "📝\u200d🔒\u200d📦": ".xml",
    "📝\u200d🔒\u200d📄": ".pdf",
    "📝\u200d🔒\u200d🔒": ".docx",
    "📝\u200d🔒\u200d📊": ".xlsx",
    "📝\u200d🔒\u200d📑": ".csv",
    "🔮\u200d🔮\u200d🔮": "magic_book",  # Magic book request
    "📝\u200d🔒\u200d🔍\u200d🔍": "metadata_request",  # Metadata request
    "📝\u200d🔒\u200d🔍\u200d💾": "metadata_write"  # Metadata write
}

def detect_file_type(content):
    emoji_sequence_pattern = regex.compile(r'(\p{Emoji_Presentation}\u200d[\p{Emoji_Presentation}\u200d]*){3}')
    emoji_sequence_match = emoji_sequence_pattern.search(content)

    if emoji_sequence_match:
        emoji_sequence = emoji_sequence_match.group()
        if emoji_sequence in file_type_cipher:
            return file_type_cipher[emoji_sequence]

    return None

def handle_content(content, file_type_cipher):
    emoji_sequence = detect_file_type(content)
    if not emoji_sequence or emoji_sequence not in file_type_cipher:
        print("Invalid or missing emoji sequence.")
        return

    file_type = file_type_cipher[emoji_sequence]

    if file_type == "magic_book":
        # Handle magic book request
        message = show_magic_book(file_type_cipher)
        print(message)
        return message
    elif file_type == "metadata_request":
        message = retrieve_metadata(content)
        print(message)
        return message
    elif file_type == "metadata_write":
        message = write_metadata(content)
        print(message)
        return message
    else:
        # Handle normal file write
        message = write_file(content, file_type)
        print(message)
        return message

def write_file(content, file_type):
    # Extract metadata and file content
    parts = content.split(file_type_cipher["📝\u200d🔒\u200d🔍\u200d💾"])
    if len(parts) != 3:
        return "Invalid format for writing file."

    metadata, file_content = parts[1], parts[2]
    metadata = json.loads(metadata.strip())
    file_content = file_content.strip()

    # Extract metadata information
    file_name = metadata.get("name", f"output{file_type}")
    storage_path = metadata.get("path", "output_files")
    classifications = metadata.get("classifications", [])
    file_id = metadata.get("id", "A1")

    # Ensure storage path exists
    os.makedirs(storage_path, exist_ok=True)

    # Write metadata to a file
    metadata_path = os.path.join(storage_path, f"{file_name}_{file_id}_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f)

    # Write content to a file
    file_path = os.path.join(storage_path, file_name + file_type)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(file_content)

    return f"Content and metadata saved as {file_path}"

def write_metadata(content):
    # Extract metadata
    parts = content.split(file_type_cipher["📝\u200d🔒\u200d🔍\u200d💾"])
    if len(parts) != 3:
        return "Invalid format for writing metadata."

    metadata = parts[1].strip()
    metadata_dict = json.loads(metadata)

    # Process and store metadata
    metadata_name = metadata_dict.get("name", "default_metadata")
    metadata_path = metadata_dict.get("path", "metadata_files")
    file_id = metadata_dict.get("id", "A1")
    os.makedirs(metadata_path, exist_ok=True)

    # Save metadata to a file
    metadata_file_path = os.path.join(metadata_path, f"{metadata_name}_{file_id}_metadata.json")
    with open(metadata_file_path, "w", encoding="utf-8") as f:
        json.dump(metadata_dict, f)

    return f"Metadata saved as {metadata_file_path}"

def retrieve_metadata(content):
    parts = content.split()
    if len(parts) < 2:
        return "Invalid format for requesting metadata."

    file_id = parts[1]
    metadata_path = f"output_metadata_{file_id}.json"

    if not os.path.exists(metadata_path):
        return "Metadata not found."

    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return f"Metadata for file {file_id}: {metadata}"

def show_magic_book(file_type_cipher):
    # Dictionary to hold files by type
    files_by_type = {ext: [] for ext in file_type_cipher.values() if ext != "magic_book"}

    # List all files in the current directory and subdirectories
    for root, dirs, files in os.walk('.'):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1]
            if file_ext in files_by_type:
                files_by_type[file_ext].append(file_path)

    # Prepare the message
    magic_book_message = "Magic Words Detected! Magic Book:\n"
    for file_type, file_list in files_by_type.items():
        if file_list:
            magic_book_message += f"{file_type} files:\n"
            for file_path in file_list:
                magic_book_message += f"  - {file_path}\n"

    return magic_book_message

# Example content with emoji sequence for writing file
example_content = "📝\u200d🔒\u200d💾📝\u200d🔒\u200d🔍\u200d💾{\"name\": \"example_file\", \"path\": \"example_path\", \"id\": \"A1\", \"classifications\": [{\"category\": \"example_category\", \"class\": \"example_class\"}]}📝\u200d🔒\u200d🔍\u200d💾This is a sample text file content.📝\u200d🔒\u200d💾"
response = handle_content(example_content, file_type_cipher)
print(response)

# Example request for the magic book overview
magic_book_content = "🔮\u200d🔮\u200d🔮"
response = handle_content(magic_book_content, file_type_cipher)
print(response)

# Example request for the magic book with specific file type
magic_book_content = "🔮\u200d🔮\u200d🔮 .txt"
response = handle_content(magic_book_content, file_type_cipher)
print(response)

# Example request for metadata retrieval
metadata_request_content = "📝\u200d🔒\u200d🔍\u200d🔍 1 metadata"
response = handle_content(metadata_request_content, file_type_cipher)
print(response)
