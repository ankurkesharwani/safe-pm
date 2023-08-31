def print_table(data):
    if not data:
        print("No data to display.")
        return

    # Determine the number of columns based on the length of the first tuple
    num_columns = len(data[0])

    # Calculate the maximum width for each column
    max_width = [max(len(str(item)) for item in col) for col in zip(*data)]

    # Print the table header
    print("+" + "+".join("-" * (width + 2) for width in max_width) + "+")
    print("| \033[1m" + " | ".join(f"{item:{width}}" for item, width in zip(data[0], max_width)) + " \033[0m|")
    print("+" + "+".join("-" * (width + 2) for width in max_width) + "+")

    # Print the data rows
    for row in data[1:]:
        print("| " + " | ".join(f"{item:{width}}" for item, width in zip(row, max_width)) + " |")

    # Print the table footer
    print("+" + "+".join("-" * (width + 2) for width in max_width) + "+")
