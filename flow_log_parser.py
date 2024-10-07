import csv

# Function to read the lookup table and store it in a dictionary
def read_lookup_table(file_path):
    lookup_dict = {}
    print(f"Reading lookup table from {file_path}...\n")
    with open(file_path, 'r') as lookup_file:
        csv_reader = csv.DictReader(lookup_file)
        for row in csv_reader:
            port = row['dstport'].strip()
            protocol = row['protocol'].strip().lower()
            tag = row['tag'].strip()
            lookup_dict[(port, protocol)] = tag
            print(f"Lookup Table Entry: (Port: {port}, Protocol: {protocol}) -> Tag: {tag}")
    print(f"\nLookup table read successfully. Total mappings: {len(lookup_dict)}\n")
    return lookup_dict

# Function to parse the flow logs and count tag matches and port/protocol combinations
def parse_flow_logs(file_path, lookup_dict):
    tag_counts = {}
    port_protocol_counts = {}

    # Map protocol numbers to names (assuming standard protocols)
    protocol_map = {'6': 'tcp', '17': 'udp', '1': 'icmp'}

    print(f"Reading flow logs from {file_path}...\n")
    with open(file_path, 'r') as log_file:
        for idx, line in enumerate(log_file):
            fields = line.strip().split()
            if len(fields) < 8:
                print(f"Skipping malformed line {idx + 1}: {line}")
                continue  # Skip malformed lines

            # Extract destination port and protocol number
            dstport = fields[5].strip()
            protocol_number = fields[6].strip()
            protocol_name = protocol_map.get(protocol_number, protocol_number).lower()  # Convert protocol number to name

            # Print the parsed values for each log entry
            print(f"Log Entry {idx + 1}: dstport={dstport}, protocol={protocol_name}")

            # Check for matching tag in the lookup table using (dstport, protocol_name)
            tag = lookup_dict.get((dstport, protocol_name), 'Untagged')
            print(f"Attempting to match: (Port: {dstport}, Protocol: {protocol_name}) -> Tag: {tag}")

            # Count the tag
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

            # Count the port/protocol combination
            port_protocol_key = (dstport, protocol_name)
            port_protocol_counts[port_protocol_key] = port_protocol_counts.get(port_protocol_key, 0) + 1

    print(f"\nFlow logs parsed successfully.\nTag Counts: {tag_counts}\nPort/Protocol Counts: {port_protocol_counts}")
    return tag_counts, port_protocol_counts

# Function to write the output to files
def write_output(tag_counts, port_protocol_counts, output_file):
    print(f"Writing results to {output_file}...\n")

    with open(output_file, 'w') as out_file:
        # Write tag counts
        out_file.write("Tag Counts:\n")
        out_file.write("Tag,Count\n")
        for tag in sorted(tag_counts):  # Sort tags for consistent output
            count = tag_counts[tag]
            out_file.write(f"{tag},{count}\n")

        # Write port/protocol combination counts
        out_file.write("\nPort/Protocol Combination Counts:\n")
        out_file.write("Port,Protocol,Count\n")
        for (port, protocol), count in sorted(port_protocol_counts.items()):
            out_file.write(f"{port},{protocol},{count}\n")

    print("Results written successfully.")

# Main function
def main():
    # File paths
    lookup_file = 'lookup.csv'
    flow_log_file = 'flow_logs.txt'
    output_file = 'output.txt'

    # Read lookup table
    lookup_dict = read_lookup_table(lookup_file)

    # Print lookup table for debugging
    print("\n=== Lookup Table ===")
    for (port, protocol), tag in lookup_dict.items():
        print(f"(Port: {port}, Protocol: {protocol}) -> Tag: {tag}")

    # Parse flow logs
    tag_counts, port_protocol_counts = parse_flow_logs(flow_log_file, lookup_dict)

    # Print output to console before writing to file
    print("\n=== Final Tag Counts ===")
    for tag, count in tag_counts.items():
        print(f"{tag}: {count}")

    print("\n=== Final Port/Protocol Combination Counts ===")
    for (port, protocol), count in port_protocol_counts.items():
        print(f"{port}/{protocol}: {count}")

    # Write output
    write_output(tag_counts, port_protocol_counts, output_file)

    print(f"Parsing completed. Check '{output_file}' for the results.")

# Entry point for the script
if __name__ == "__main__":
    main()
