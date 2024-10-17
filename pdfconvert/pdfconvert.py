import argparse
import os
from pdf2image import convert_from_path
from PIL import Image
import PyPDF2
import io
from pdf2docx import Converter

class PDFConverter:
    def __init__(self):
        self.operations = {
            'pdf2img': self.pdf_to_image,
            'img2pdf': self.image_to_pdf,
            'extract_text': self.extract_text,
            'merge': self.merge_pdfs,
            'split': self.split_pdf,
            'pdf2docx': self.pdf_to_docx,
            'delete_pages': self.delete_pages
        }

    def pdf_to_image(self, input_path, output_path):
        pages = convert_from_path(input_path)
        for i, page in enumerate(pages):
            page.save(f"{output_path}_page_{i+1}.jpg", "JPEG")
        print(f"Converted {input_path} to images in {output_path}")

    def image_to_pdf(self, input_path, output_path):
        image = Image.open(input_path)
        pdf_bytes = io.BytesIO()
        image.save(pdf_bytes, format='PDF')
        with open(output_path, 'wb') as f:
            f.write(pdf_bytes.getvalue())
        print(f"Converted {input_path} to PDF: {output_path}")

    def extract_text(self, input_path, output_path):
        with open(input_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Extracted text from {input_path} to {output_path}")

    def merge_pdfs(self, input_paths, output_path):
        merger = PyPDF2.PdfMerger()
        for path in input_paths:
            merger.append(path)
        merger.write(output_path)
        merger.close()
        print(f"Merged PDFs into {output_path}")

    def split_pdf(self, input_path, output_path):
        with open(input_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for i, page in enumerate(reader.pages):
                writer = PyPDF2.PdfWriter()
                writer.add_page(page)
                with open(f"{output_path}_page_{i+1}.pdf", 'wb') as out_file:
                    writer.write(out_file)
        print(f"Split {input_path} into separate pages in {output_path}")

    def pdf_to_docx(self, input_path, output_path):
        cv = Converter(input_path)
        cv.convert(output_path)
        cv.close()
        print(f"Converted {input_path} to DOCX: {output_path}")

    def delete_pages(self, input_path, output_path, pages_to_delete):
        with open(input_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()

            pages_to_delete = set(map(int, pages_to_delete.split(',')))
            for i, page in enumerate(reader.pages):
                if i + 1 not in pages_to_delete:
                    writer.add_page(page)

            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

        print(f"Deleted pages {pages_to_delete} from {input_path} and saved to {output_path}")

    def convert(self, operation, input_path, output_path, extra_args=None):
        if operation in self.operations:
            if operation == 'merge':
                self.operations[operation](input_path.split(), output_path)
            elif operation == 'delete_pages':
                if extra_args is None:
                    print("Error: Pages to delete must be specified.")
                    return
                self.operations[operation](input_path, output_path, extra_args)
            else:
                self.operations[operation](input_path, output_path)
        else:
            print(f"Unsupported operation: {operation}")

def main():
    parser = argparse.ArgumentParser(description="PDF Converter")
    parser.add_argument('operation', choices=['pdf2img', 'img2pdf', 'extract_text', 'merge', 'split', 'pdf2docx', 'delete_pages'],
                        help='Conversion operation to perform')
    parser.add_argument('input', help='Input file or directory')
    parser.add_argument('output', help='Output file or directory')
    parser.add_argument('--pages', help='Pages to delete (comma-separated list of page numbers, for delete_pages operation)')
    args = parser.parse_args()

    converter = PDFConverter()
    converter.convert(args.operation, args.input, args.output, args.pages)

if __name__ == "__main__":
    main()