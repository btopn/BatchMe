#!/usr/bin/env python3
"""
BatchMe - UPC Barcode Generator
Generates UPC barcode images from a list of UPC numbers
"""

import os
import sys
from pathlib import Path
from typing import List
import barcode
from barcode.writer import ImageWriter
from PIL import Image


class UPCBarcodeGenerator:
    """Generate UPC barcode images from UPC numbers"""

    def __init__(self, output_dir: str = "barcodes"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def clean_upc(self, upc: str) -> str:
        """Clean and validate UPC string"""
        # Remove whitespace and dashes
        cleaned = ''.join(c for c in upc if c.isdigit())
        return cleaned

    def generate_barcode(self, upc: str, index: int) -> str:
        """
        Generate a single UPC barcode image

        Args:
            upc: UPC number string
            index: Index number for ordering

        Returns:
            Path to generated image file
        """
        cleaned_upc = self.clean_upc(upc)

        # Validate UPC length (UPC-A is 12 digits, UPC-E is 8 digits)
        if len(cleaned_upc) not in [8, 12]:
            raise ValueError(f"Invalid UPC length: {len(cleaned_upc)} digits. Must be 8 or 12 digits.")

        # Determine barcode type
        if len(cleaned_upc) == 12:
            barcode_class = barcode.get_barcode_class('upca')
        else:
            barcode_class = barcode.get_barcode_class('upce')

        # Generate filename with zero-padded index for proper sorting
        filename = f"{index:04d}_{cleaned_upc}"
        output_path = self.output_dir / filename

        # Create barcode with ImageWriter for PNG output
        upc_barcode = barcode_class(cleaned_upc, writer=ImageWriter())

        # Save the barcode
        full_path = upc_barcode.save(str(output_path))

        return full_path

    def generate_batch(self, upc_list: List[str]) -> List[str]:
        """
        Generate barcode images for a list of UPCs

        Args:
            upc_list: List of UPC number strings

        Returns:
            List of paths to generated image files
        """
        generated_files = []
        errors = []

        for index, upc in enumerate(upc_list, start=1):
            # Skip empty lines
            if not upc.strip():
                continue

            try:
                file_path = self.generate_barcode(upc.strip(), index)
                generated_files.append(file_path)
                print(f"✓ Generated {index}/{len(upc_list)}: {upc.strip()}")
            except Exception as e:
                error_msg = f"✗ Error generating barcode for '{upc.strip()}': {str(e)}"
                errors.append(error_msg)
                print(error_msg, file=sys.stderr)

        if errors:
            print(f"\n⚠ Completed with {len(errors)} error(s)")
        else:
            print(f"\n✓ Successfully generated {len(generated_files)} barcodes!")

        print(f"\nBarcodes saved to: {self.output_dir.absolute()}")

        return generated_files


def cli_mode():
    """Command-line interface mode"""
    print("=" * 60)
    print("BatchMe - UPC Barcode Generator (CLI Mode)")
    print("=" * 60)
    print("\nPaste your UPC numbers below (one per line).")
    print("Press Ctrl+D (Mac/Linux) or Ctrl+Z then Enter (Windows) when done.\n")

    # Read UPC numbers from stdin
    upc_list = []
    try:
        for line in sys.stdin:
            upc_list.append(line.strip())
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
        sys.exit(0)

    if not upc_list:
        print("No UPC numbers provided.")
        sys.exit(1)

    # Generate barcodes
    generator = UPCBarcodeGenerator()
    generator.generate_batch(upc_list)


def gui_mode():
    """GUI mode using tkinter"""
    try:
        import tkinter as tk
        from tkinter import scrolledtext, messagebox, filedialog
    except ImportError:
        print("Error: tkinter is not available. Please use CLI mode instead.")
        sys.exit(1)

    class BarcodeGeneratorGUI:
        def __init__(self, root):
            self.root = root
            self.root.title("BatchMe - UPC Barcode Generator")
            self.root.geometry("700x600")

            # Header
            header = tk.Label(
                root,
                text="BatchMe - UPC Barcode Generator",
                font=("Arial", 16, "bold"),
                pady=10
            )
            header.pack()

            # Instructions
            instructions = tk.Label(
                root,
                text="Paste your UPC numbers below (one per line), then click Generate",
                font=("Arial", 10)
            )
            instructions.pack()

            # Text input area
            input_frame = tk.Frame(root)
            input_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            tk.Label(input_frame, text="UPC Numbers:", font=("Arial", 10, "bold")).pack(anchor=tk.W)

            self.text_input = scrolledtext.ScrolledText(
                input_frame,
                height=15,
                width=60,
                font=("Courier", 11)
            )
            self.text_input.pack(fill=tk.BOTH, expand=True)

            # Buttons frame
            button_frame = tk.Frame(root)
            button_frame.pack(pady=10)

            # Generate button
            self.generate_btn = tk.Button(
                button_frame,
                text="Generate Barcodes",
                command=self.generate_barcodes,
                bg="#4CAF50",
                fg="white",
                font=("Arial", 12, "bold"),
                padx=20,
                pady=10
            )
            self.generate_btn.pack(side=tk.LEFT, padx=5)

            # Clear button
            clear_btn = tk.Button(
                button_frame,
                text="Clear",
                command=self.clear_input,
                font=("Arial", 12),
                padx=20,
                pady=10
            )
            clear_btn.pack(side=tk.LEFT, padx=5)

            # Output directory button
            output_btn = tk.Button(
                button_frame,
                text="Choose Output Folder",
                command=self.choose_output_dir,
                font=("Arial", 12),
                padx=20,
                pady=10
            )
            output_btn.pack(side=tk.LEFT, padx=5)

            # Status label
            self.status_label = tk.Label(
                root,
                text="Ready",
                font=("Arial", 10),
                fg="gray"
            )
            self.status_label.pack(pady=5)

            # Output directory
            self.output_dir = "barcodes"
            self.output_label = tk.Label(
                root,
                text=f"Output: {Path(self.output_dir).absolute()}",
                font=("Arial", 9),
                fg="blue"
            )
            self.output_label.pack()

        def choose_output_dir(self):
            """Let user choose output directory"""
            directory = filedialog.askdirectory(initialdir=self.output_dir)
            if directory:
                self.output_dir = directory
                self.output_label.config(text=f"Output: {Path(self.output_dir).absolute()}")

        def clear_input(self):
            """Clear the text input"""
            self.text_input.delete(1.0, tk.END)
            self.status_label.config(text="Ready", fg="gray")

        def generate_barcodes(self):
            """Generate barcodes from input"""
            # Get text input
            text = self.text_input.get(1.0, tk.END)
            upc_list = [line.strip() for line in text.split('\n') if line.strip()]

            if not upc_list:
                messagebox.showwarning("No Input", "Please paste UPC numbers first.")
                return

            # Disable button during generation
            self.generate_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Generating barcodes...", fg="orange")
            self.root.update()

            try:
                # Generate barcodes
                generator = UPCBarcodeGenerator(self.output_dir)
                generated_files = generator.generate_batch(upc_list)

                # Show success message
                self.status_label.config(
                    text=f"✓ Successfully generated {len(generated_files)} barcodes!",
                    fg="green"
                )

                messagebox.showinfo(
                    "Success",
                    f"Generated {len(generated_files)} barcodes!\n\n"
                    f"Location: {Path(self.output_dir).absolute()}\n\n"
                    f"You can now drag and drop these images into your Numbers spreadsheet."
                )

                # Ask if user wants to open the folder
                if messagebox.askyesno("Open Folder", "Would you like to open the output folder?"):
                    import subprocess
                    subprocess.call(['open', str(Path(self.output_dir).absolute())])

            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}", fg="red")
                messagebox.showerror("Error", f"An error occurred:\n\n{str(e)}")
            finally:
                self.generate_btn.config(state=tk.NORMAL)

    # Create and run GUI
    root = tk.Tk()
    app = BarcodeGeneratorGUI(root)
    root.mainloop()


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        cli_mode()
    else:
        # Default to GUI mode
        gui_mode()


if __name__ == "__main__":
    main()
