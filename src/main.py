import json

def main():
    with open('processed/processed_data.json', 'r') as file:
        processed_data = json.load(file)

    
if __name__ == '__main__':
    main()