# Grailed Auto-Uploader

Automation tool for bulk uploading listings to Grailed.com. Handles product photos, descriptions, measurements and automated form filling.

## Features
- Drag-and-drop interface
- Batch photo processing
- Automated listing creation
- Measurement tracking
- GPT-assisted descriptions and tag generation

## Requirements

### Required Software
- Python 3.7+
- Chrome browser
- Adobe Lightroom (for photo editing)

### Optional Software
- GPT for Work (for automated description writing and care tag data extraction)

### Python Packages
```bash
pip install selenium
pip install pandas
pip install tkinter
pip install pyinstaller  # if creating executable
```

## File Structure
```
project/
├── scripts/
│   ├── grailed_gui.py
│   ├── grailed_uploader.py
│   └── config.json
├── data/
│   ├── listings.xlsx
│   ├── measurements.txt
│   └── images/
```

## Setup
1. Install dependencies
2. Configure config.json with Grailed credentials
3. Prepare product data:
   - Excel spreadsheet with listing details
   - Measurements text file
   - Product photos (named consistently)
4. Run GUI:
   ```bash
   python grailed_gui.py
   ```

## Workflow Overview
1. Photo capture and editing
2. Data entry in Excel template
3. Measurement documentation
4. GPT description generation (optional)
5. Automated upload via GUI

## Note on GPT Usage
This workflow uses GPT (Vision or GPT-4) in two ways:
1. Extract care instructions and composition from product tag photos
2. Generate standardized product descriptions and tags

These steps can be done manually in Excel if GPT access isn't available. The automation will work with either method.

## Contributing
This is an open source tool for the Grailed community. Contributions welcome.