"""
Number Base Converter 

This code converts decimal numbers to binary and hexadecimal representations.
It processes input files containing decimal numbers and generates a formatted
output file with conversion results.
"""

import sys
import time


def decimal_to_binary(num):
    """
    Convert a decimal number to binary using basic algorithm.
    Uses two's complement for negative numbers (32-bit).
    """
    if num == 0:
        return "0"
    # Handle negative numbers using two's complement (32-bit)
    if num < 0:
        # Two's complement: convert to 32-bit unsigned equivalent
        num = (1 << 32) + num
        # 2^32 + num (since num is negative)

    # Convert to binary
    binary = ""
    temp = num
    while temp > 0:
        remainder = temp % 2
        binary = str(remainder) + binary
        temp = temp // 2

    return binary


def decimal_to_hexadecimal(num):
    """
    Convert a decimal number to hexadecimal using basic algorithm.
    Uses two's complement for negative numbers (32-bit).
    """
    if num == 0:
        return "0"
    # Handle negative numbers using two's complement (32-bit)
    if num < 0:
        # Two's complement: convert to 32-bit unsigned equivalent
        num = (1 << 32) + num  # 2^32 + num (since num is negative)

    # Hex digits mapping
    hex_digits = "0123456789ABCDEF"

    hexadecimal = ""
    temp = num
    while temp > 0:
        remainder = temp % 16
        hexadecimal = hex_digits[remainder] + hexadecimal
        temp = temp // 16

    return hexadecimal


def validate_and_convert(value):
    """
    Validate input and convert to integer.

    Args:
        value: String value to validate and convert

    Returns:
        tuple: (success: bool, number: int or None, error_message: str or None)
    """
    try:
        # Strip whitespace
        value = value.strip()
        # Check if empty
        if not value:
            return False, None, "Empty value"
        # Convert to integer
        num = int(value)
        return True, num, None

    except ValueError:
        return False, None, f"Invalid number format: '{value}'"


def write_output_file(output_filename, results, errors, stats):
    """
    Write conversion results to output file.

    Args:
        output_filename: Path to output file
        results: List of conversion result strings
        errors: List of error messages
        stats: Dictionary containing total_processed, total_errors, elapsed_time
    """
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.write("=" * 70 + "\n")
        outfile.write("NUMBER BASE CONVERSION RESULTS\n")
        outfile.write("=" * 70 + "\n\n")

        if results:
            for result in results:
                outfile.write(result + "\n")
        else:
            outfile.write("No valid numbers were processed.\n")

        outfile.write("\n" + "=" * 70 + "\n")
        outfile.write("STATISTICS\n")
        outfile.write("=" * 70 + "\n")
        outfile.write(f"Total items processed: {stats['total_processed']}\n")
        outfile.write(f"Total errors: {stats['total_errors']}\n")
        outfile.write(f"Execution time: {stats['elapsed_time']:.6f} seconds\n")
        outfile.write("=" * 70 + "\n")

        if errors:
            outfile.write("\nERRORS ENCOUNTERED:\n")
            outfile.write("-" * 70 + "\n")
            for error in errors:
                outfile.write(error + "\n")


def display_results(results, stats, output_filename):
    """
    Display conversion results on screen.

    Args:
        results: List of conversion result strings
        stats: Dictionary containing total_processed, total_errors, elapsed_time
        output_filename: Path to output file
    """
    print("-" * 70)
    print("\nCONVERSION RESULTS:")
    print("=" * 70)

    if results:
        # Display first 10 and last 10 results if more than 20
        if len(results) <= 20:
            for result in results:
                print(result)
        else:
            for result in results[:10]:
                print(result)
            print(f"\n... ({len(results) - 20} more results) ...\n")
            for result in results[-10:]:
                print(result)
    else:
        print("No valid numbers were processed.")

    print("\n" + "=" * 70)
    print("STATISTICS")
    print("=" * 70)
    print(f"Total items processed: {stats['total_processed']}")
    print(f"Total errors: {stats['total_errors']}")
    print(f"Execution time: {stats['elapsed_time']:.6f} seconds")
    print("=" * 70)

    print(f"\nResults saved to '{output_filename}'")


def process_line(line, line_number, results, errors, stats):
    """
    Process a single line from the input file.

    Args:
        line: Line to process
        line_number: Current line number
        results: List to append results to
        errors: List to append errors to
        stats: Statistics dictionary to update
    """
    # Skip empty lines
    if not line.strip():
        return

    success, num, error_msg = validate_and_convert(line)

    if success:
        # Perform conversions and store result
        results.append(
            f"Decimal: {num:>15} | "
            f"Binary: {decimal_to_binary(num):>20} | "
            f"Hexadecimal: {decimal_to_hexadecimal(num):>15}"
        )
        stats['total_processed'] += 1
    else:
        # Handle error
        error_line = f"Line {line_number}: {error_msg}"
        errors.append(error_line)
        print(f"ERROR - {error_line}")
        stats['total_errors'] += 1


def process_file(input_filename, output_filename):
    """
    Process input file and generate conversion results.

    Args:
        input_filename: Path to input file containing decimal numbers
        output_filename: Path to output file for results

    Returns:
        tuple: (total_processed, total_errors, elapsed_time)
    """
    start_time = time.time()
    results = []
    errors = []
    stats = {'total_processed': 0, 'total_errors': 0, 'elapsed_time': 0}

    try:
        # Read and process input file
        with open(input_filename, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        print(f"Processing {len(lines)} items from '{input_filename}'...")
        print("-" * 70)

        # Process each line
        for line_number, line in enumerate(lines, start=1):
            process_line(line, line_number, results, errors, stats)

        # Calculate elapsed time
        stats['elapsed_time'] = time.time() - start_time

        # Write and display results
        write_output_file(output_filename, results, errors, stats)
        display_results(results, stats, output_filename)

        return stats['total_processed'], stats['total_errors'], stats['elapsed_time']

    except FileNotFoundError:
        print(f"ERROR: File '{input_filename}' not found.")
        sys.exit(1)
    except PermissionError:
        print(f"ERROR: Permission denied accessing '{input_filename}'.")
        sys.exit(1)
    except IOError as e:
        print(f"ERROR: I/O error occurred: {str(e)}")
        sys.exit(1)


def main():
    """
    Main function to handle command line arguments and initiate processing.
    """
    # Check command line arguments
    if len(sys.argv) < 2:
        print("ERROR: Missing required argument.")
        print("\nUsage: python convert_numbers.py fileWithData.txt")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = "ConvertionResults.txt"

    print("=" * 70)
    print("NUMBER BASE CONVERTER")
    print("=" * 70)
    print(f"Input file: {input_filename}")
    print(f"Output file: {output_filename}")
    print("=" * 70 + "\n")

    # Process the file
    process_file(input_filename, output_filename)


if __name__ == "__main__":
    main()
