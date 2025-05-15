import os
import requests
from tabulate import tabulate

def process_file(file_path):
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f, 'application/octet-stream')}
        response = requests.post('http://localhost:8000/classify_file', files=files)
        if response.status_code == 200:
            data = response.json()
            return data['file_class'], data.get('confidence', 0.0)
        else:
            return f"Error: {response.json().get('error', 'Unknown error')}", 0.0

def main():
    results = []
    files_dir = 'files'
    
    # Process all files in the directory
    for filename in os.listdir(files_dir):
        if filename.endswith(('.pdf', '.docx', '.doc', '.jpg', '.png')):
            file_path = os.path.join(files_dir, filename)
            classification, confidence = process_file(file_path)
            results.append([filename, classification, confidence])
    
    # Sort results by filename
    results.sort(key=lambda x: x[0])
    
    # Display results in a table
    headers = ['Filename', 'Classification', 'Confidence']
    print("\nDocument Classification Results:")
    print(tabulate(results, headers=headers, tablefmt='grid', floatfmt=".2%"))
    
    # Print summary statistics
    print("\nSummary:")
    classifications = {}
    for _, cls, conf in results:
        if not str(cls).startswith('Error'):
            classifications[cls] = classifications.get(cls, 0) + 1
    
    for cls, count in sorted(classifications.items()):
        print(f"{cls}: {count} documents")

if __name__ == '__main__':
    main() 