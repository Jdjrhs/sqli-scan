import requests
from bs4 import BeautifulSoup

def display_banner():
    banner = """
             .__                                         
  ___________|  |             ______ ____ _____    ____  
 /  ___/ ____/  |    ______  /  ___// ___\\__  \  /    \ 
 \___ < <_|  |  |__ /_____/  \___ \\  \___ / __ \|   |  \
/____  >__   |____/         /____  >\___  >____  /___|  /
     \/   |__|                   \/     \/     \/     \/  
    """
    print(banner)
    print("ZxPLOIT - SQL Injection Checker\n")

def check_url_vulnerability(url, output_file=None):
    # Menambahkan tanda ' pada akhir URL
    vulnerable_url = url + "'"
    
    try:
        # Mengirimkan permintaan GET ke URL asli dan yang sudah ditambahkan tanda '
        response_normal = requests.get(url)
        response_vulnerable = requests.get(vulnerable_url)
        
        # Memeriksa status code 500
        if response_vulnerable.status_code == 500:
            result = f"[!] Vulnerable URL (500 Error): {url}"
            print(result)
            if output_file:
                with open(output_file, 'a') as f:
                    f.write(url + '\n')
            return
        
        # Memeriksa perubahan dalam HTML
        if response_normal.text != response_vulnerable.text:
            soup = BeautifulSoup(response_vulnerable.text, 'html.parser')
            if 'mysql' in soup.get_text().lower():
                result = f"[!] Vulnerable URL (MySQL Error): {url}"
                print(result)
                if output_file:
                    with open(output_file, 'a') as f:
                        f.write(url + '\n')
            else:
                result = f"[!] Potential Vulnerable URL (HTML Changed): {url}"
                print(result)
                if output_file:
                    with open(output_file, 'a') as f:
                        f.write(url + '\n')
        else:
            print(f"[-] Not Vulnerable: {url}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error checking URL {url}: {e}")

def main():
    display_banner()
    print("Enter 'url' to check a single URL or 'list' to check a list of URLs.")
    mode = input("Mode (url/list): ").strip().lower()
    
    if mode == "url":
        url = input("Enter URL (https://website.com/info.php?id=1): ").strip()
        save_result = input("Save result? (y/n): ").strip().lower()
        if save_result == 'y':
            output_file = input("Enter output file name (with .txt extension): ").strip()
            check_url_vulnerability(url, output_file)
        else:
            check_url_vulnerability(url)
    
    elif mode == "list":
        list_name = input("Enter list name: ").strip()
        save_result = input("Save results? (y/n): ").strip().lower()
        output_file = None
        if save_result == 'y':
            output_file = input("Enter output file name (with .txt extension): ").strip()
        
        try:
            with open(list_name, 'r') as file:
                urls = file.readlines()
            
            for url in urls:
                url = url.strip()
                if url:
                    check_url_vulnerability(url, output_file)
        
        except FileNotFoundError:
            print(f"File {list_name} not found.")
    
    else:
        print("Invalid mode. Please enter 'url' or 'list'.")

if __name__ == "__main__":
    main()
