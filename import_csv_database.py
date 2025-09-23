#!/usr/bin/env python3
"""
CSV Database Importer for OSINT Toolkit

This script imports all entries from database.csv and adds them to the appropriate
category markdown files in the proper table format.
"""

import csv
import os
from collections import defaultdict

# Category file mappings
CATEGORY_FILES = {
    "News & Event Monitoring": "news-monitoring.md",
    "OPSEC & Privacy": "opsec-privacy.md", 
    "Social Media Intelligence": "social-media.md",
    "Verification & Resources": "verification-resources.md",
    "Image & Video Analysis": "image-video.md",
    "Geospatial & Maps": "geospatial-maps.md",
    "Domain & IP Intelligence": "domain-ip.md",
    "People Search & Usernames": "people-search.md",
    "Transportation Tracking": "transportation.md",
    "Dark Web & Anonymity": "dark-web.md",
    "Extensions & Utilities": "extensions-utilities.md"
}

def read_csv_database():
    """Read and parse the CSV database."""
    entries = defaultdict(list)
    
    with open('database.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            tool = row.get('Tool', '').strip()
            url = row.get('URL', '').strip()
            description = row.get('Description', '').strip()
            category = row.get('Category', '').strip()
            
            # Skip empty rows or header rows
            if not tool or not url or tool.lower() in ['tool', 'name', 'category']:
                continue
                
            # Skip uncategorized entries
            if not category or category == 'Uncategorized':
                continue
                
            # Clean up the description
            if description and len(description) > 200:
                description = description[:197] + "..."
                
            entries[category].append({
                'tool': tool,
                'url': url,
                'description': description
            })
    
    return entries

def format_url_for_markdown(url):
    """Format URL for markdown table display."""
    # Extract domain from URL for display
    if '://' in url:
        domain = url.split('://')[1].split('/')[0]
        # Remove www. prefix
        if domain.startswith('www.'):
            domain = domain[4:]
        return f"[{domain}]({url})"
    else:
        return f"[{url}]({url})"

def update_category_file(category, tools):
    """Update a category markdown file with new tools."""
    filename = CATEGORY_FILES.get(category)
    if not filename:
        print(f"⚠️  No file mapping found for category: {category}")
        return
        
    filepath = f"docs/{filename}"
    
    # Read existing content
    existing_content = ""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    # Check if file already has tools (look for existing tables)
    if "| Tool | URL | Description |" in existing_content:
        print(f"📝 {category}: File already has tools, appending new ones...")
        
        # Find the end of existing tables and add new tools
        lines = existing_content.split('\n')
        new_lines = []
        in_table = False
        
        for line in lines:
            new_lines.append(line)
            
            # Check if we're at the end of a table
            if line.startswith('---') and in_table:
                # Add new tools here
                new_lines.append("")
                new_lines.append("| Tool | URL | Description |")
                new_lines.append("|------|-----|-------------|")
                
                for tool in tools:
                    formatted_url = format_url_for_markdown(tool['url'])
                    desc = tool['description'].replace('|', '\\|')  # Escape pipes
                    new_lines.append(f"| {tool['tool']} | {formatted_url} | {desc} |")
                
                new_lines.append("")
                in_table = False
            elif "| Tool | URL | Description |" in line:
                in_table = True
        
        # Write updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
    else:
        print(f"📝 {category}: Creating new file with tools...")
        
        # Create new content
        category_name = category.replace(' & ', ' & ')
        content = f"""# {category_name}

A collection of tools and resources for {category.lower()}.

---

## Tools

| Tool | URL | Description |
|------|-----|-------------|"""

        for tool in tools:
            formatted_url = format_url_for_markdown(tool['url'])
            desc = tool['description'].replace('|', '\\|')  # Escape pipes
            content += f"\n| {tool['tool']} | {formatted_url} | {desc} |"
        
        content += "\n"
        
        # Write new content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

def main():
    """Main function to import CSV database."""
    print("🔄 Importing CSV database to OSINT Toolkit...")
    
    # Read CSV database
    entries = read_csv_database()
    
    print(f"📊 Found {sum(len(tools) for tools in entries.values())} tools across {len(entries)} categories")
    
    # Update each category file
    for category, tools in entries.items():
        print(f"📁 Processing {category}: {len(tools)} tools")
        update_category_file(category, tools)
    
    print("✅ CSV database import completed!")
    print("🚀 Run 'python3 generate_database.py' to update the master database")

if __name__ == "__main__":
    main()

