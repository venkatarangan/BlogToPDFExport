# BlogToPDFExport

## Overview
Python script to export the posts in a wordpress blog to PDF files

I had to preserve the contents of one of my old blog sites at www.example.com/blogs before it gets retired. I wanted to convert all the blog posts into fully formatted PDFs. The goal was to ensure the PDFs contained text, formatting, and images, and not just screenshots, making them useful for future searching and copying. For the next two hours, I worked with ChatGPT and generated the code which I tested, debugged, corrected and than ran to get the results I wanted. Remember, the HTML classes referenced in the code are specific to the wordpress blog site, so if you are running this on your site, you may need to modify the tags accordingly, any good LLM will get it done for for you easily. 

![Cover image](/github-preview.png)

### Steps to get this code run ###
1. Clone this repo, create a new virtual environment in python and install the necessary packages in Python 
2. Configure the base URL of the blog you want to use. For this modify the *base_url* in the file *fetchallposts_titlesandurl.py* 
3. Run the *fetchallposts_titlesandurl.py* file 
4. Ensure the output csv file is generated at *example_Blogs_Posts.csv*
5. Run the *saveallurls_as_pdf.py* file to get the PDF files generated

### Packages and Their Usage
- **`requests`**: HTTP requests for web scraping.
- **`BeautifulSoup`**: HTML parsing.
- **`csv`**: Handling CSV file operations.
- **`pandas`**: Reading and processing CSV data.
- **`pdfkit`**: Converting HTML to PDF.
- **`os`**: File handling and directory operations.
- **`datetime`**: Managing date and time data.
- **`subprocess`**: Executing system commands.
- **`logging`**: Logging errors and information.

## Disclaimer
On my prompts and requirements the code was generated by ChatGPT4, I have tested the code and got the desired output PDF files. It is not intended to be production-ready. It was created to quickly complete a task. 

## Testing Environment
I tested this project on Windows 11 with the following:
1. python 3.12.3
1. beautifulsoup4-4.12.3
1. pandas-2.2.2
1. pdfkit-1.0.0.
1. pytz-2024.1

## License
This project is licensed under the MIT License.

## Contributions
This project was an experiment and is not maintained. Just take it as it is. Thanks.

## Author
Venkatarangan Thirumalai [venkatarangan.com](https://venkatarangan.com)
