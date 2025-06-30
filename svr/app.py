import sys
import os
import importlib.util

parse_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parse.py')
spec = importlib.util.spec_from_file_location('parse', parse_path)
if spec is None or spec.loader is None:
    print('Error: Could not load parse.py module.')
    sys.exit(1)
parse_module = importlib.util.module_from_spec(spec)
sys.modules['parse'] = parse_module
spec.loader.exec_module(parse_module)
extract_from_html = parse_module.extract_from_html

def main():
    if len(sys.argv) != 2:
        print("Usage: python app.py <path_to_html_file>")
        sys.exit(1)
    html_file = sys.argv[1]
    if not os.path.isfile(html_file):
        print(f"Error: File '{html_file}' does not exist.")
        sys.exit(1)
    try:
        output_path = extract_from_html(html_file)
        print(f"Parsing complete. Output written to: {output_path}")
    except Exception as e:
        print(f"Error during parsing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
