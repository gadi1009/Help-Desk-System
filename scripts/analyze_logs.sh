#!/bin/bash

# Define log file path
LOG_FILE="/home/mcipks/Desktop/New Folder 1/help_desk_system/logs/app.log"

# Define output report file path
REPORT_FILE="/home/mcipks/Desktop/New Folder 1/help_desk_system/logs/log_analysis_report.txt"

# Execute the Python log analyzer script
python3 /home/mcipks/Desktop/New Folder 1/help_desk_system/utils/log_analyzer.py "$LOG_FILE" > "$REPORT_FILE"

echo "Log analysis report generated: $REPORT_FILE"
