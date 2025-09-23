#!/bin/bash

# OSINT Toolkit Database Updater
# This script regenerates the master database from all category files

echo "🔄 Updating OSINT Toolkit Master Database..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Run the database generator
python3 generate_database.py

echo ""
echo "✅ Database update complete!"
echo "🚀 You can now view the updated master database at docs/master-database.md"
