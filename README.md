# 🔮‍🔮‍🔮 Welcome to: `magic_book` 🔮‍🔮‍🔮
## Code for a Magic Book Enabling Language Agents to Build Their Own Brains


## System Overview

The system is designed to handle content and metadata dynamically using emoji sequences and hierarchical organization. It allows for:

Dynamic File Naming and Organization: Files are named, stored, and categorized based on metadata.
Metadata Management: Metadata includes hierarchical categories and unique IDs using A1 notation.
Integration with Chat AI: The AI can process messages containing specific emoji sequences to trigger 
    different actions such as writing files, retrieving metadata, or invoking the "magic book."

#### Components

#### magic_book.py: 
This module contains functions for detecting file types, handling content, writing files, 
    managing metadata, and providing hierarchical views of available files.
main.py: This module integrates the chat AI with the functionalities provided by magic_book.py.

## How It Works

#### magic_book.py

Emoji Whitelist: Defines the mapping between emoji sequences and file types or actions.

detect_file_type(content):
Uses regex to find emoji sequences in the content.
Returns the corresponding file type or action.

handle_content(content, file_type_cipher):
Detects the emoji sequence in the content.
Determines the action based on the file type.
Calls the appropriate function (write_file, retrieve_metadata, write_metadata, or show_magic_book).

write_file(content, file_type):
Extracts metadata and file content.
Uses metadata to determine the file name, storage path, and classifications.
Ensures the storage path exists.
Writes the metadata and content to files.

write_metadata(content):
Extracts and processes metadata.
Stores metadata in the specified path.
Uses A1 notation for unique IDs.

retrieve_metadata(content):
Extracts the file ID from the content.
Retrieves and returns the metadata for the specified file.

show_magic_book(file_type_cipher):
Lists all files in the current directory and subdirectories.
Groups files by type and prepares a message with the hierarchical view.
main.py

send_message(client, messages, default_system_message, file_type_cipher, ...):
Sends a message to the AI and processes the response.
Calls detect_choices to handle content based on emoji sequences.

detect_choices(content, file_type_cipher):
Uses detect_file_type to find the emoji sequence.
Calls handle_content to process the content and trigger appropriate actions.

## Workflow

Sending a Message:

The send_message function is called with the content and metadata.
The content is checked for emoji sequences to determine the action.
The appropriate function is called based on the detected emoji sequence.

Writing a File:

The content includes an emoji sequence for writing a file.
handle_content calls write_file.
write_file uses metadata to name, store, and categorize the file.

Retrieving Metadata:

The content includes an emoji sequence for retrieving metadata.
handle_content calls retrieve_metadata.
retrieve_metadata returns the metadata for the specified file.

Magic Book Request:

The content includes an emoji sequence for the magic book.
handle_content calls show_magic_book.
show_magic_book returns a hierarchical view of available files.

## Example Usage

Writing a File:

```plaintext
📝‍🔒‍💾📝‍🔒‍🔍‍💾{"name": "example_file", "path": "example_path", "id": "A1", "classifications": [{"category": "example_category", "class": "example_class"}]}📝‍🔒‍🔍‍💾This is a sample text file content.📝‍🔒‍💾```

Retrieving Metadata:

```plaintext
📝‍🔒‍🔍‍🔍 1 metadata```

Magic Book Request:

```plaintext
🔮‍🔮‍🔮```

## Integration with Language AIs
The AI processes messages containing specific emoji sequences and triggers the corresponding actions:

File Writing: Handles writing files dynamically based on metadata.
Metadata Management: Retrieves and stores metadata.
Magic Book: Provides an overview of available files in a hierarchical format.

This system leverages the AI's ability to process content dynamically and manage files and metadata efficiently,
    providing a powerful tool for organizing and retrieving information based on user-defined criteria and hierarchical categorization.
