"""
Word Count Program
Counts the frequency of distinct words in a text file.

"""

import sys
import time


def read_file(filename):
    """
    Read content from a file.

    """
    try:
        with open(filename, 'r', encoding='utf-8') as file_handle:
            content = file_handle.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read '{filename}'.")
        return None
    except IOError as error:
        print(f"Error reading file: {error}")
        return None


def is_valid_word_character(char):
    """
    Check if a character is valid for a word (alphanumeric or apostrophe).

    """
    # Check if alphabetic (a-z, A-Z)
    if (ord('a') <= ord(char) <= ord('z') or
            ord('A') <= ord(char) <= ord('Z')):
        return True
    # Check if numeric (0-9)
    if ord('0') <= ord(char) <= ord('9'):
        return True
    # Allow apostrophes in words
    if char == "'":
        return True
    return False


def to_lowercase(text):
    """
    Convert text to lowercase using basic algorithm.

    """
    result = ""
    for char in text:
        if ord('A') <= ord(char) <= ord('Z'):
            # Convert uppercase to lowercase
            result += chr(ord(char) + 32)
        else:
            result += char
    return result


def extract_words(text):
    """
    Extract words from text using basic string processing.

    """
    words = []
    current_word = ""

    for char in text:
        if is_valid_word_character(char):
            current_word += char
        else:
            # End of word
            if current_word:
                # Convert to lowercase and add to list
                lowercase_word = to_lowercase(current_word)
                words.append(lowercase_word)
                current_word = ""

    # Don't forget the last word if text doesn't end with separator
    if current_word:
        lowercase_word = to_lowercase(current_word)
        words.append(lowercase_word)

    return words


def count_word_frequencies(words):
    """
    Count frequency of each word using basic algorithm.
    """
    # Manual frequency counting without using dict
    unique_words = []
    frequencies = []

    for word in words:
        # Skip empty words
        if not word:
            continue

        # Try to validate word contains some alphabetic characters
        has_letter = False
        for char in word:
            if (ord('a') <= ord(char) <= ord('z') or
                    ord('A') <= ord(char) <= ord('Z')):
                has_letter = True
                break

        if not has_letter:
            print(f"Warning: Skipping invalid word '{word}'")
            continue

        # Check if word already exists in our list
        found = False
        for i, unique_word in enumerate(unique_words):
            if unique_word == word:
                frequencies[i] += 1
                found = True
                break

        # If not found, add new word
        if not found:
            unique_words.append(word)
            frequencies.append(1)

    # Combine into list of tuples
    word_freq_pairs = []
    for i, unique_word in enumerate(unique_words):
        word_freq_pairs.append((unique_word, frequencies[i]))

    return word_freq_pairs


def sort_word_frequencies(word_freq_pairs):
    """
    Sort word frequency pairs by frequency (descending), then alphabetically.

    """
    # Create a copy to avoid modifying original
    sorted_pairs = []
    for pair in word_freq_pairs:
        sorted_pairs.append(pair)

    # Bubble sort - sort by frequency descending, then alphabetically
    n = len(sorted_pairs)
    for i in range(n):
        for j in range(0, n - i - 1):
            # Sort by frequency (descending), then alphabetically
            if (sorted_pairs[j][1] < sorted_pairs[j + 1][1] or
                (sorted_pairs[j][1] == sorted_pairs[j + 1][1] and
                 sorted_pairs[j][0] > sorted_pairs[j + 1][0])):
                # Swap
                temp = sorted_pairs[j]
                sorted_pairs[j] = sorted_pairs[j + 1]
                sorted_pairs[j + 1] = temp

    return sorted_pairs


def format_results(word_freq_pairs, elapsed_time):
    """
    Format results for output.

    """
    output = "=" * 60 + "\n"
    output += "WORD FREQUENCY ANALYSIS RESULTS\n"
    output += "=" * 60 + "\n\n"

    total_words = 0
    for pair in word_freq_pairs:
        total_words += pair[1]

    output += f"Total words processed: {total_words}\n"
    output += f"Distinct words found: {len(word_freq_pairs)}\n"
    output += f"Execution time: {elapsed_time:.4f} seconds\n"
    output += "\n" + "-" * 60 + "\n"
    output += f"{'WORD':<30} {'FREQUENCY':>10}\n"
    output += "-" * 60 + "\n"

    for word, frequency in word_freq_pairs:
        output += f"{word:<30} {frequency:>10}\n"

    output += "=" * 60 + "\n"

    return output


def write_results_to_file(content, filename):
    """
    Write results to output file.

    """
    try:
        with open(filename, 'w', encoding='utf-8') as file_handle:
            file_handle.write(content)
        print(f"\nResults written to '{filename}'")
    except PermissionError:
        print(f"Error: Permission denied to write to '{filename}'.")
    except IOError as error:
        print(f"Error writing to file: {error}")


def main():
    """Main program execution."""
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python wordCount.py fileWithData.txt")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = "WordCountResults.txt"

    print(f"Processing file: {input_filename}")
    print("=" * 60)

    # Start timing
    start_time = time.time()

    # Read file
    file_content = read_file(input_filename)
    if file_content is None:
        print("Failed to read input file. Exiting.")
        sys.exit(1)

    # Extract words
    print("Extracting words...")
    words = extract_words(file_content)

    if not words:
        print("Warning: No valid words found in file.")
        elapsed_time = time.time() - start_time
        output = format_results([], elapsed_time)
        print(output)
        write_results_to_file(output, output_filename)
        return

    # Count frequencies
    print("Counting word frequencies...")
    word_freq_pairs = count_word_frequencies(words)

    # Sort results
    print("Sorting results...")
    sorted_pairs = sort_word_frequencies(word_freq_pairs)

    # Calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Format and display results
    output = format_results(sorted_pairs, elapsed_time)
    print("\n" + output)

    # Write to file
    write_results_to_file(output, output_filename)

    print("\nProcessing complete!")


if __name__ == "__main__":
    main()
