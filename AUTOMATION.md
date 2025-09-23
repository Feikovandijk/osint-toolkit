# 🤖 OSINT Toolkit Automation

This document explains how the automated master database generation works.

## Overview

The master database (`docs/master-database.md`) is automatically generated from all individual category files. This ensures the database is always up-to-date when you add new tools.

## Files

- `generate_database.py` - Main Python script that scans all markdown files and generates the database
- `update_database.sh` - Shell script wrapper for easy execution
- `.github/workflows/update-database.yml` - GitHub Actions workflow for automatic updates

## Usage

### Manual Update

```bash
# Option 1: Run the Python script directly
python3 generate_database.py

# Option 2: Use the shell script
./update_database.sh
```

### Automatic Update

The database automatically updates when:
- You push changes to any `.md` file in the `docs/` directory
- You manually trigger the GitHub Action

## How It Works

1. **Scans** all markdown files in the `docs/` directory
2. **Extracts** tool information from tables and bullet points
3. **Categorizes** tools by their source file
4. **Generates** a comprehensive master database with:
   - Category overview with tool counts
   - Detailed tool listings by category
   - Search by tool type (search engines, analysis tools)
   - Popular tools section
   - Statistics and quick actions

## Adding New Tools

1. Add tools to the appropriate category file (e.g., `docs/social-media.md`)
2. Follow the existing table format
3. Run `python3 generate_database.py` to update the master database
4. Commit both the category file and the updated master database

## Supported Formats

The script recognizes these markdown formats:

### Tables
```markdown
| Tool Name | URL | Description |
|-----------|-----|-------------|
| Example Tool | [example.com](https://example.com) | Tool description |
```

### Bullet Points
```markdown
* [Tool Name](https://example.com) - Tool description
```

## Customization

You can modify `generate_database.py` to:
- Add new categories to `CATEGORY_INFO`
- Change the output format
- Add new search categories
- Modify the statistics generation

## Troubleshooting

- **No tools found**: Check that your markdown files use the supported table or bullet point formats
- **Python errors**: Ensure Python 3.6+ is installed
- **Permission errors**: Make sure the script has write access to the `docs/` directory
