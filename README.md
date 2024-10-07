# Flow Log Parser

This project is a Python script that parses a file containing flow log data and maps each row to a tag based on a lookup table. The script then generates summary statistics, such as the count of matches for each tag and the count of port/protocol combinations.

## Project Overview

The script is designed to process flow logs and map them to tags defined in a lookup table. The flow logs are in a specific format, and the lookup table specifies the mapping between destination ports, protocols, and tags.

### Input Files
1. **`flow_logs.txt`**: Contains the flow log data that needs to be parsed.
2. **`lookup.csv`**: Defines the tag mappings for each port and protocol combination. This file should have the following structure:

   ```csv
   dstport,protocol,tag
   25,tcp,sv_P1
   68,udp,sv_P2
   23,tcp,sv_P1
   31,udp,sv_P3
   443,tcp,sv_P2
   22,tcp,sv_P4
   3389,tcp,sv_P5
   0,icmp,sv_P5
   110,tcp,email
   993,tcp,email
   143,tcp,email
