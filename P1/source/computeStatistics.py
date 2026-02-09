"""
Number Stadistics
This code converts calculates descriptive statistics (mean, median, mode, standard deviation, variance).
"""
import sys
import time


def read_data_from_file(filename):
    """
    Read numerical data from a file, handling invalid entries.
    """
    data = []
    invalid_count = 0

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        number = float(line)
                        data.append(number)
                    except ValueError:
                        invalid_count += 1
                        print(f"Warning: Invalid data at line {line_num}: "
                              f"'{line}' - Skipping")

        if invalid_count > 0:
            print(f"\nTotal invalid entries skipped: {invalid_count}\n")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied to read '{filename}'.")
        sys.exit(1)
    except (IOError, OSError) as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    return data


def calculate_mean(data):
    """
    Calculate the arithmetic mean of a dataset.

    """
    if not data:
        return 0

    total = 0
    for value in data:
        total += value

    return total / len(data)


def calculate_median(data):
    """
    Calculate the median of a dataset.

    """
    if not data:
        return 0

    # Sort the data using bubble sort
    sorted_data = data.copy()
    n = len(sorted_data)

    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_data[j] > sorted_data[j + 1]:
                sorted_data[j], sorted_data[j + 1] = \
                    sorted_data[j + 1], sorted_data[j]

    # Find median
    if n % 2 == 0:
        median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    else:
        median = sorted_data[n // 2]

    return median


def calculate_mode(data):
    """
    Calculate the mode of a dataset 

    """
    if not data:
        return []

    # Count frequencies and track first occurrence
    frequency = {}
    first_occurrence = {}

    for index, value in enumerate(data):
        if value not in frequency:
            frequency[value] = 0
            first_occurrence[value] = index
        frequency[value] += 1

    # Find maximum frequency
    max_freq = 0
    for freq in frequency.values():
        max_freq = max(max_freq, freq)

    # If all values appear only once, there's no mode
    if max_freq == 1:
        return []

    # Find the first occurring value with maximum frequency
    first_mode = None
    earliest_position = len(data)

    for value, freq in frequency.items():
        if freq == max_freq:
            if first_occurrence[value] < earliest_position:
                earliest_position = first_occurrence[value]
                first_mode = value

    return [first_mode] if first_mode is not None else []


def calculate_variance(data, mean):
    """
    Calculate the variance of a dataset.

    """
    if len(data) <= 1:
        return 0

    sum_squared_diff = 0
    for value in data:
        diff = value - mean
        sum_squared_diff += diff * diff

    variance = sum_squared_diff / (len(data) - 1)
    return variance


def calculate_std_deviation(variance):
    """
    Calculate the standard deviation from variance.

    """
    # Calculate square root using Newton's method
    if variance == 0:
        return 0

    # Initial guess
    x = variance
    epsilon = 1e-10

    while True:
        root = 0.5 * (x + variance / x)
        if abs(root - x) < epsilon:
            break
        x = root

    return root


def format_results(stats_dict):
    """
    Format the statistics results as a string.

    """
    data = stats_dict['data']
    mean = stats_dict['mean']
    median = stats_dict['median']
    mode = stats_dict['mode']
    std_dev = stats_dict['std_dev']
    variance = stats_dict['variance']
    elapsed_time = stats_dict['elapsed_time']

    results = []
    results.append("=" * 60)
    results.append("DESCRIPTIVE STATISTICS RESULTS")
    results.append("=" * 60)
    results.append(f"Count of numbers: {len(data)}")
    results.append(f"Mean: {mean:.4f}")
    results.append(f"Median: {median:.4f}")

    if mode:
        mode_str = ", ".join([f"{m:.4f}" for m in sorted(mode)])
        results.append(f"Mode: {mode_str}")
    else:
        results.append("Mode: No mode (all values appear once)")

    results.append(f"Standard Deviation: {std_dev:.4f}")
    results.append(f"Variance: {variance:.4f}")
    results.append("=" * 60)
    results.append(f"Elapsed Time: {elapsed_time:.6f} seconds")
    results.append("=" * 60)

    return "\n".join(results)


def write_results_to_file(content, filename="StatisticsResults.txt"):
    """
    Write results to a file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"\nResults saved to '{filename}'")
    except (IOError, OSError) as e:
        print(f"Error writing to file '{filename}': {e}")


def main():
    """Main program execution."""
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python computeStatistics.py fileWithData.txt")
        sys.exit(1)

    filename = sys.argv[1]

    print(f"Reading data from '{filename}'...\n")

    # Start timing
    start_time = time.time()

    # Read data from file
    data = read_data_from_file(filename)

    if not data:
        print("Error: No valid data found in the file.")
        sys.exit(1)

    print(f"Successfully loaded {len(data)} numbers.")
    print("Calculating statistics...\n")

    # Calculate statistics
    mean = calculate_mean(data)
    median = calculate_median(data)
    mode = calculate_mode(data)
    variance = calculate_variance(data, mean)
    std_dev = calculate_std_deviation(variance)

    # End timing
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Format results
    stats_dict = {
        'data': data,
        'mean': mean,
        'median': median,
        'mode': mode,
        'std_dev': std_dev,
        'variance': variance,
        'elapsed_time': elapsed_time
    }
    results = format_results(stats_dict)

    # Display results on screen
    print(results)

    # Write results to file
    write_results_to_file(results)


if __name__ == "__main__":
    main()
