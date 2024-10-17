from .pdfconvert import PDFConverter

def main():
    import argparse

    parser = argparse.ArgumentParser(description='PDF Converter')
    parser.add_argument('operation', choices=['pdf2img', 'img2pdf', 'extract_text', 'merge', 'split', 'pdf2docx', 'delete_pages'])
    parser.add_argument('--input', required=True, help='Input file or directory')
    parser.add_argument('--output', required=True, help='Output file or directory')
    parser.add_argument('--pages', help='Pages to delete (comma-separated list of page numbers, for delete_pages operation)')

    args = parser.parse_args()

    converter = PDFConverter()
    if args.operation == 'delete_pages' and args.pages:
        converter.operations[args.operation](args.input, args.output, args.pages)
    else:
        converter.operations[args.operation](args.input, args.output)