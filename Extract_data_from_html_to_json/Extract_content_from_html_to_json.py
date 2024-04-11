'''
Installation of tika:

Download Apache Tika and save the tika-server-x.x.jar file to the folder you want to run Tika from.

Reference:
https://doc.sitecore.com/xp/en/developers/102/platform-administration-and-architecture/walkthrough--using-apache-tika-to-extract-media-content-for-indexing.html

https://www.apache.org/dyn/closer.lua/tika/2.9.2/tika-server-standard-2.9.2.jar

n the folder where you saved the file, open a PowerShell prompt and start Apache Tika:
java -jar tika-server-x.x.jar --host=<Tikahostname> --port=<portnumber>
If you do not specify host and port, Apache Tika uses the defaults of localhost and 9998.


To confirm that Apache Tika is running, browse to the Tika server 
URL, http://<Tikahostname>:<portnumber>.

If the server is running, you can see a Welcome message.

'''
import json
import os
import re
from bs4 import BeautifulSoup
import tika
tika.initVM()
from tika import parser

def extract_text_from_html(html_file):
    parsed = parser.from_file(html_file)
    return parsed['content']

def clean_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    cleaned_text = soup.get_text(separator=' ')
    cleaned_text = cleaned_text.replace("\\","")
    cleaned_text = re.sub('\t|\r|\n+', ' ', cleaned_text)
    cleaned_text = cleaned_text.encode('ascii', 'ignore').decode('ascii')
    return cleaned_text.strip()

def convert_to_json(html_dir):
    data = []
    for filename in os.listdir(html_dir):
        if filename.endswith('.html'):
            html_file = os.path.join(html_dir, filename)
            text = extract_text_from_html(html_file)
            if text is not None:
                cleaned_text = clean_html(text)
                data.append({
                    'filename': filename,
                    'text': cleaned_text
                    })
            else:
                print(f"Failed to extract text from {filename}. Skipping...")
    return data

def write_json(data, output_file):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
        
def main():
    html_dir = r"C:\Project_Files\Langchain\documents\html_data"
    json_data = convert_to_json(html_dir)
    write_json(json_data, 'output.json')
    
if __name__ == "__main__":
    main()