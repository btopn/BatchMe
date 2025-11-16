# BatchMe - UPC Barcode Generator

A lightweight, easy-to-use batch UPC barcode generator perfect for creating barcode images to paste into Numbers spreadsheets on macOS.

## Features

- ✨ **Simple GUI interface** - Just paste and click!
- 📋 **Batch processing** - Handle hundreds of UPCs at once
- 🔢 **Maintains order** - Barcodes are numbered in the same order as your input
- 🖼️ **High-quality images** - Clean PNG barcode images ready for spreadsheets
- 🚀 **Lightweight** - Minimal dependencies, fast performance
- 💻 **CLI option available** - For power users who prefer command line

## Installation

### Prerequisites

- Python 3.7 or higher (check with `python3 --version`)
- pip (Python package manager)

### Setup

1. Clone or download this repository
2. Open Terminal and navigate to the BatchMe folder:
   ```bash
   cd /path/to/BatchMe
   ```

3. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

That's it! You're ready to generate barcodes.

## Usage

### GUI Mode (Recommended for Mac users)

This is the easiest way to use BatchMe:

1. Run the program:
   ```bash
   python3 barcode_generator.py
   ```

2. A window will open. Simply:
   - **Paste** your UPC numbers (one per line) into the text area
   - Click **"Generate Barcodes"**
   - The program will create barcode images in the `barcodes` folder

3. After generation:
   - Click "Yes" when asked if you want to open the folder
   - The barcodes will be numbered (0001, 0002, etc.) in the same order as your input
   - Simply drag and drop the images into your Numbers spreadsheet!

#### Customizing Output Location

Click **"Choose Output Folder"** to save barcodes to a different location.

### CLI Mode (For command-line users)

If you prefer the command line:

1. Run with the `--cli` flag:
   ```bash
   python3 barcode_generator.py --cli
   ```

2. Paste your UPC numbers (one per line)

3. Press `Ctrl+D` when done

4. Barcodes will be generated in the `barcodes` folder

### Reading from a File

You can also pipe UPC numbers from a text file:

```bash
python3 barcode_generator.py --cli < upc_list.txt
```

## Workflow with Numbers

Here's the complete workflow for using BatchMe with Numbers:

1. **Prepare your UPCs** in Numbers:
   - Copy the column of UPC numbers from your Numbers spreadsheet

2. **Generate barcodes**:
   - Run BatchMe (`python3 barcode_generator.py`)
   - Paste the UPC numbers
   - Click "Generate Barcodes"

3. **Insert into Numbers**:
   - Open the `barcodes` folder
   - Sort by name (they're numbered in order: 0001, 0002, etc.)
   - Drag and drop the images into the corresponding rows in Numbers
   - Or use Insert → Image for each barcode

## UPC Format Support

BatchMe supports both standard UPC formats:

- **UPC-A**: 12-digit codes (most common)
- **UPC-E**: 8-digit codes (compressed format)

The program automatically detects which format to use based on the number of digits.

## Examples

### Input (UPC numbers)
```
012345678905
725272730706
614141000036
123456789012
```

### Output
The program generates 4 files:
- `0001_012345678905.png`
- `0002_725272730706.png`
- `0003_614141000036.png`
- `0004_123456789012.png`

Each file contains a scannable barcode image ready to paste into your spreadsheet!

## Troubleshooting

### "Invalid UPC length" error

Make sure your UPC numbers are either 8 or 12 digits long. Remove any spaces, dashes, or other characters.

### "tkinter is not available" error

If you see this error when running GUI mode:
1. Try CLI mode instead: `python3 barcode_generator.py --cli`
2. Or install tkinter:
   ```bash
   # On Mac with Homebrew
   brew install python-tk
   ```

### Images won't open in Numbers

Make sure you're using PNG files (not SVG). BatchMe generates PNG by default, so this shouldn't be an issue.

## Performance

BatchMe is lightweight and fast:
- Generates ~100 barcodes in under 5 seconds on an Intel Mac
- Minimal memory usage
- No heavy dependencies

## File Structure

```
BatchMe/
├── barcode_generator.py    # Main program
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── barcodes/               # Output folder (created automatically)
    ├── 0001_123456789012.png
    ├── 0002_234567890123.png
    └── ...
```

## Advanced Options

### Customizing Barcode Appearance

The barcode images use sensible defaults, but you can modify the code if needed. Look for the `ImageWriter` configuration in `barcode_generator.py`.

### Batch Processing Large Files

For very large batches (1000+ UPCs), consider:
1. Using CLI mode for better performance
2. Processing in chunks to avoid memory issues
3. Using an SSD for faster file I/O

## License

Free to use for personal and commercial projects.

## Support

If you encounter any issues:
1. Check the Troubleshooting section
2. Ensure all dependencies are installed correctly
3. Verify your UPC numbers are valid (8 or 12 digits)

---

**Happy barcode generating!** 📊✨
