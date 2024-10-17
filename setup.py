from setuptools import setup, find_packages

setup(
    name='pdfconvert',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'argparse',
        'pdf2image',
        'Pillow',
        'PyPDF2',
        'pdf2docx'
    ],
    entry_points={
        'console_scripts': [
            'pdfconvert=pdfconvert:main',
        ],
    },
    author='fukayatti0',
    author_email='st24162yk@gm.ibaraki-ct.ac.jp',
    description='A tool for converting and manipulating PDF files',
    url='https://github.com/fukayatti0/pdfconvert',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)