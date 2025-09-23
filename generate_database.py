#!/usr/bin/env python3
"""
OSINT Toolkit Master Database Generator

This script automatically generates the master-database.md file by scanning
all markdown files in the docs/ directory and extracting tool information.
"""

import os
import re
from pathlib import Path
from datetime import datetime

# Configuration
DOCS_DIR = "docs"
MASTER_DB_FILE = "docs/master-database.md"
EXCLUDE_FILES = ["index.md", "master-database.md"]

# Category mappings
CATEGORY_INFO = {
    "geospatial-maps.md": {
        "name": "Geospatial & Maps",
        "description": "Maps, satellite imagery, location finding, and geographic data"
    },
    "social-media.md": {
        "name": "Social Media Intelligence",
        "description": "Social media search and analysis"
    },
    "image-video.md": {
        "name": "Image & Video Analysis", 
        "description": "Reverse image search, metadata, and video forensics"
    },
    "domain-ip.md": {
        "name": "Domain & IP Intelligence",
        "description": "WHOIS, DNS, website analysis"
    },
    "people-search.md": {
        "name": "People Search & Usernames",
        "description": "Individual and username research"
    },
    "transportation.md": {
        "name": "Transportation Tracking",
        "description": "Aircraft and maritime tracking"
    },
    "news-monitoring.md": {
        "name": "News & Event Monitoring",
        "description": "Live maps, news aggregators"
    },
    "dark-web.md": {
        "name": "Dark Web & Anonymity",
        "description": "Tor, I2P, dark web tools"
    },
    "opsec-privacy.md": {
        "name": "OPSEC & Privacy",
        "description": "Security and privacy tools"
    },
    "verification-resources.md": {
        "name": "Verification & Resources",
        "description": "Handbooks, tutorials, guides"
    },
    "extensions-utilities.md": {
        "name": "Extensions & Utilities",
        "description": "Browser plugins, utilities"
    }
}

def extract_tools_from_markdown(file_path):
    """Extract tool information from a markdown file."""
    tools = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for tables (markdown table format) - handle variable column counts
        # First, find all table rows
        table_rows = re.findall(r'\|([^|\n]+)\|([^|\n]+)\|([^|\n]+)(?:\|([^|\n]+))?(?:\|([^|\n]+))?\|', content, re.MULTILINE)
        
        for table_row in table_rows:
            # Clean up the row data
            row_data = [cell.strip() for cell in table_row if cell.strip()]
            
            if len(row_data) >= 3:
                name = row_data[0]
                url = row_data[1]
                description = row_data[2] if len(row_data) > 2 else ""
                
                # Skip header rows
                if name.lower() in ['name', 'tool', 'service'] or '---' in name or 'description' in name.lower():
                    continue
                    
                # Extract URL from markdown link format [text](url)
                url_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', url)
                if url_match:
                    display_url = url_match.group(1)
                    actual_url = url_match.group(2)
                else:
                    display_url = url
                    actual_url = url
                
                tools.append({
                    'name': name,
                    'url': actual_url,
                    'display_url': display_url,
                    'description': description
                })
        
        # Also look for bullet points as fallback
        if not tools:
            bullet_pattern = r'\* \[([^\]]+)\]\(([^)]+)\) - (.+)'
            bullets = re.findall(bullet_pattern, content)
            
            for bullet in bullets:
                tools.append({
                    'name': bullet[0].strip(),
                    'url': bullet[1].strip(),
                    'display_url': bullet[1].strip(),
                    'description': bullet[2].strip()
                })
                
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return tools

def generate_master_database():
    """Generate the master database markdown file."""
    
    # Collect all tools from all files
    all_tools = {}
    category_stats = {}
    
    for filename in os.listdir(DOCS_DIR):
        if filename.endswith('.md') and filename not in EXCLUDE_FILES:
            file_path = os.path.join(DOCS_DIR, filename)
            tools = extract_tools_from_markdown(file_path)
            
            if tools:
                all_tools[filename] = tools
                category_stats[filename] = len(tools)
    
    # Generate the markdown content
    content = f"""# Master OSINT Database

A comprehensive, searchable database of all OSINT tools and resources organized by category and functionality.

*Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

---

## Quick Category Access

| Category | Description | Tools Count | Direct Link |
|----------|-------------|-------------|-------------|"""

    # Add category overview
    for filename, info in CATEGORY_INFO.items():
        if filename in category_stats:
            tool_count = category_stats[filename]
            content += f"\n| {info['name']} | {info['description']} | {tool_count}+ | [View Tools →]({filename.replace('.md', '')}) |"
    
    content += "\n\n---\n\n## All Tools by Category\n\n"
    
    # Add detailed tool listings
    for filename, tools in all_tools.items():
        if filename in CATEGORY_INFO:
            info = CATEGORY_INFO[filename]
            content += f"### {info['name']}\n\n"
            content += f"*{info['description']}*\n\n"
            
            if tools:
                content += "| Tool | URL | Description |\n"
                content += "|------|-----|-------------|\n"
                
                for tool in tools:
                    # Clean up the description
                    desc = tool['description'].replace('|', '\\|')  # Escape pipes
                    if len(desc) > 100:
                        desc = desc[:97] + "..."
                    
                    content += f"| {tool['name']} | [{tool['display_url']}]({tool['url']}) | {desc} |\n"
            else:
                content += "*No tools found in this category.*\n"
            
            content += "\n---\n\n"
    
    # Add search sections
    content += """## Search by Tool Type

### Search Engines
| Tool | Category | Description |
|------|----------|-------------|"""

    # Find search engines
    search_keywords = ['search', 'engine', 'dork', 'query']
    for filename, tools in all_tools.items():
        if filename in CATEGORY_INFO:
            for tool in tools:
                if any(keyword in tool['name'].lower() or keyword in tool['description'].lower() 
                      for keyword in search_keywords):
                    category_name = CATEGORY_INFO[filename]['name']
                    content += f"\n| {tool['name']} | [{category_name}]({filename.replace('.md', '')}) | {tool['description'][:80]}... |"

    content += """

### Analysis Tools
| Tool | Category | Description |
|------|----------|-------------|"""

    # Find analysis tools
    analysis_keywords = ['analysis', 'analyze', 'investigation', 'forensic', 'scan', 'check']
    for filename, tools in all_tools.items():
        if filename in CATEGORY_INFO:
            for tool in tools:
                if any(keyword in tool['name'].lower() or keyword in tool['description'].lower() 
                      for keyword in analysis_keywords):
                    category_name = CATEGORY_INFO[filename]['name']
                    content += f"\n| {tool['name']} | [{category_name}]({filename.replace('.md', '')}) | {tool['description'][:80]}... |"

    content += """

---

## Quick Reference

### Most Popular Tools
| Tool | Category | Why It's Popular |
|------|----------|------------------|"""

    # Add some popular tools (you can customize this list)
    popular_tools = [
        ("Google Dorks", "domain-ip.md", "Free, powerful search operators"),
        ("Have I Been Pwned", "dark-web.md", "Essential breach checking"),
        ("Shodan", "domain-ip.md", "Internet device discovery"),
        ("TinEye", "image-video.md", "Reverse image search"),
        ("FlightRadar24", "transportation.md", "Real-time flight tracking")
    ]
    
    for tool_name, category_file, reason in popular_tools:
        if category_file in CATEGORY_INFO:
            category_name = CATEGORY_INFO[category_file]['name']
            content += f"\n| {tool_name} | [{category_name}]({category_file.replace('.md', '')}) | {reason} |"

    content += f"""

### Quick Actions
- **Need to find someone?** → Start with [People Search](people-search)
- **Investigating a website?** → Check [Domain & IP Intelligence](domain-ip)
- **Looking for images?** → Use [Image & Video Analysis](image-video)
- **Dark web research?** → Browse [Dark Web & Anonymity](dark-web)
- **Privacy concerns?** → Review [OPSEC & Privacy](opsec-privacy)

---

## Tool Statistics

| Category | Tools Count | Last Updated |
|----------|-------------|--------------|"""

    # Add statistics
    for filename, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
        if filename in CATEGORY_INFO:
            category_name = CATEGORY_INFO[filename]['name']
            content += f"\n| {category_name} | {count}+ | Active |"

    content += f"""

---

"""

    # Write the file
    with open(MASTER_DB_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Master database generated successfully!")
    print(f"📊 Found {sum(category_stats.values())} tools across {len(category_stats)} categories")
    print(f"📝 Updated: {MASTER_DB_FILE}")

if __name__ == "__main__":
    generate_master_database()
