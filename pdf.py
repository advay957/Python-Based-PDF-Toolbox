import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from PIL import Image
import os


def log(msg, color="white"):
    colors = {
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "blue": "\033[94m",
        "white": "\033[97m" 
    }
    print(colors[color] + msg + "\033[0m")

# GUI
class PDFToolkit:
    def __init__(self, root):
        self.root = root
        root.title("PDF Toolkit - GUI Version")
        root.geometry("500x420")
        root.config(bg="#03066E")

        tk.Label(root, text="PDF Toolkit", font=("Arial", 22, "bold"), fg="white", bg="#0B0B0B").pack(pady=10)

        btn_style = {"font": ("Arial", 14), "bg": "#1e88e5", "fg": "white", "width": 25}

        tk.Button(root, text="Merge PDFs", command=self.merge_pdf, **btn_style).pack(pady=8)
        tk.Button(root, text="Merge Selected Pages", command=self.merge_selected_pages, **btn_style).pack(pady=8)
        tk.Button(root, text="Split PDF", command=self.split_pdf, **btn_style).pack(pady=8)
        tk.Button(root, text="Image to PDF", command=self.image_to_pdf, **btn_style).pack(pady=8)

        self.progress = ttk.Progressbar(root, length=300, mode="determinate")
        self.progress.pack(pady=20)

    # Merge PDFs
    def merge_pdf(self):
        files = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF Files", "*.pdf")])
        if not files:
            return

        save_as = filedialog.asksaveasfilename(defaultextension=".pdf")

        merger = PdfMerger()
        try:
            for f in files:
                merger.append(f)
                log(f"Merging: {f}", "blue")
            
            merger.write(save_as)
            merger.close()
            log("Merge Successful!", "green")
            messagebox.showinfo("Success", "PDFs merged successfully!")
        except Exception as e:
            log(str(e), "red")
            messagebox.showerror("Error", "Failed to merge PDFs!")

    # Merge Selected Pages
    def merge_selected_pages(self):
        file = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF Files", "*.pdf")])
        if not file:
            return

        pages = tk.simpledialog.askstring("Pages", "Enter pages (e.g., 1-3,5,7-9):")
        if not pages:
            return

        save_as = filedialog.asksaveasfilename(defaultextension=".pdf")

        reader = PdfReader(file)
        writer = PdfWriter()

        try:
            page_ranges = pages.split(",")

            for pr in page_ranges:
                if "-" in pr:
                    start, end = map(int, pr.split("-"))
                    for p in range(start - 1, end):
                        writer.add_page(reader.pages[p])
                else:
                    writer.add_page(reader.pages[int(pr) - 1])

            with open(save_as, "wb") as f:
                writer.write(f)
            
            log("Selected pages merged!", "green")
            messagebox.showinfo("Success", "Selected pages merged successfully!")

        except Exception as e:
            log(str(e), "red")
            messagebox.showerror("Error", "Invalid page numbers!")

    # Split Pdf
    def split_pdf(self):
        file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file:
            return

        save_folder = filedialog.askdirectory()

        try:
            reader = PdfReader(file)
            total = len(reader.pages)

            for i in range(total):
                self.progress["value"] = (i+1) / total * 100
                self.root.update_idletasks()

                writer = PdfWriter()
                writer.add_page(reader.pages[i])

                with open(f"{save_folder}/page_{i+1}.pdf", "wb") as f:
                    writer.write(f)

            log("Split Successful!", "green")
            messagebox.showinfo("Success", "PDF split into pages!")
        except:
            log("Failed to split PDF", "red")
            messagebox.showerror("Error", "Could not split PDF!")

    # Image to PDF
    def image_to_pdf(self):
        files = filedialog.askopenfilenames(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if not files:
            return

        save_as = filedialog.asksaveasfilename(defaultextension=".pdf")

        try:
            img_list = []
            first = Image.open(files[0]).convert("RGB")

            for f in files[1:]:
                img_list.append(Image.open(f).convert("RGB"))

            first.save(save_as, save_all=True, append_images=img_list)
            log("Images converted to PDF!", "green")
            messagebox.showinfo("Success", "Image to PDF conversion successful!")
        except:
            log("Failed to convert images!", "red")
            messagebox.showerror("Error", "Image conversion failed!")


# ----------------------- Run App -----------------------
root = tk.Tk()
PDFToolkit(root)
root.mainloop()
