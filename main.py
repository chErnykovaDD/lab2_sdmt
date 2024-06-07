import sys
import argparse
import re

def parse_markdown(input_text):
    html_output = []
    in_preformatted = False

    for line in input_text.split('\n'):
        if line.strip() == "":
            if not in_preformatted:
                html_output.append("</p><p>")
            else:
                html_output.append("\n")
            continue

        if line.startswith("```"):
            if in_preformatted:
                html_output.append("</pre>")
            else:
                html_output.append("<pre>")
            in_preformatted = not in_preformatted
            continue

        if in_preformatted:
            html_output.append(line + "\n")  # Ensure new lines are preserved
            continue

        line = handle_markdown_elements(line)

        html_output.append(line)

    if in_preformatted:
        raise ValueError("Invalid markdown: unclosed preformatted block")

    return '<p>' + ''.join(html_output) + '</p>'

def handle_markdown_elements(line):
    markdown_elements = [
        (r'\*\*(\S.*?\S)\*\*', r'<b>\1</b>'),
        (r'__(.*?)__', r'<b>\1</b>'),
        (r'`(\S.*?\S)`', r'<tt>\1</tt>'),
        (r'(^|\s)_(\S.*?\S)_(?=\s|$)', r'\1<i>\2</i>'),
        (r'^# (.*)', r'<h1>\1</h1>'),
        (r'^## (.*)', r'<h2>\1</h2>')
    ]

    for pattern, replacement in markdown_elements:
        line = re.sub(pattern, replacement, line)

    check_unclosed_markdown(line)
    check_invalid_combinations(line)

    return line
def check_unclosed_markdown(line):
    unclosed_markdown = [
        (r'(?<!\w)_\S', "italic"),
        (r'\S_(?!\w)', "italic"),
        (r'(?<!\w)\*\*\S', "bold"),
        (r'\S\*\*(?!\w)', "bold"),
        (r'(?<!\w)`\S', "monospaced"),
        (r'\S`(?!\w)', "monospaced")
    ]

    for pattern, element in unclosed_markdown:
        if re.search(pattern, line):
            raise ValueError(f"Invalid markdown: unclosed {element}")

def check_invalid_combinations(line):
    invalid_combinations = [
        (r'\*\*\s.*\s\*\*', "spaces are not allowed between bold markers and text"),
        (r'(^|\s)_\s.*\s_(?=\s|$)', "spaces are not allowed between italic markers and text"),
        (r'`\s.*\s`', "spaces are not allowed between monospaced markers and text")
    ]

    for pattern, message in invalid_combinations:
        if re.search(pattern, line):
            raise ValueError(f"Invalid markdown: {message}")
def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def generate_html(markdown_text):
    try:
        html_output = parse_markdown(markdown_text)
        return html_output
    except ValueError as e:
        sys.stderr.write(str(e) + '\n')
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Markdown to HTML converter")
    parser.add_argument('input', help="Path to the input markdown file")
    parser.add_argument('--out', help="Path to the output HTML file")
    args = parser.parse_args()

    markdown_text = read_file(args.input)
    html_output = generate_html(markdown_text)

    if args.out:
        with open(args.out, 'w', encoding='utf-8') as file:
            file.write(html_output)
    else:
        print(html_output)

if __name__ == "__main__":
    main()