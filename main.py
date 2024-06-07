import sys
import argparse
import re

def parse_markdown(input_text, to_ansi=False):
    output = []
    in_preformatted = False

    for line in input_text.split('\n'):
        if line.strip() == "":
            if not in_preformatted:
                output.append("</p><p>" if not to_ansi else "\n\n")
            else:
                output.append("\n")
            continue

        if line.startswith("```"):
            if in_preformatted:
                output.append("</pre>" if not to_ansi else "\033[0m")  # Disable inverse mode
            else:
                output.append("<pre>" if not to_ansi else "\033[7m")  # Enable inverse mode
            in_preformatted = not in_preformatted
            continue

        if in_preformatted:
            output.append(line + "\n")  # Ensure new lines are preserved
            continue

        line = handle_markdown_elements(line, to_ansi)

        output.append(line)

    if in_preformatted:
        raise ValueError("Invalid markdown: unclosed preformatted block")

    # Add <p> tags at the beginning and end of the parsed markdown string
    return '<p>' + ''.join(output) + '</p>' if not to_ansi else ''.join(output).strip('\n\n')

def handle_markdown_elements(line, to_ansi):
    check_nested_formatting(line)

    if to_ansi:
        markdown_elements = [
            (r'\*\*(\S.*?\S)\*\*', r'\033[1m\1\033[0m'),  # Bold
            (r'__(.*?)__', r'\033[1m\1\033[0m'),          # Bold
            (r'`(\S.*?\S)`', r'\033[7m\1\033[0m'),        # Monospaced
            (r'(^|\s)_(\S.*?\S)_(?=\s|$)', r'\1\033[3m\2\033[0m'),  # Italic
            (r'^# (.*)', r'\033[1;4m\1\033[0m'),          # H1
            (r'^## (.*)', r'\033[1m\1\033[0m')            # H2
        ]
    else:
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

def check_nested_formatting(line):
    nested_patterns = [
        (r'\*\*(.*?)_(.*?)_\*\*', "nested bold and italic"),
        (r'_(.*?)\*\*(.*?)\*\*_', "nested italic and bold"),
        (r'\*\*(.*?)`(.*?)`\*\*', "nested bold and monospaced"),
        (r'`(.*?)\*\*(.*?)\*\*`', "nested monospaced and bold"),
        (r'_(.*?)`(.*?)`_', "nested italic and monospaced"),
        (r'`(.*?)_(.*?)_`', "nested monospaced and italic")
    ]

    for pattern, message in nested_patterns:
        if re.search(pattern, line):
            raise ValueError(f"Invalid markdown: {message}")

def check_unclosed_markdown(line):
    unclosed_markdown = [
        (r'(?<!\w)_\S', "italic"),
        (r'\S_(?!\w)', "italic"),
        (r'(?<!\w)\*\*\S', "bold"),
        (r'\S\*\*(?!\w)', "bold"),
        # Перевірка, чи ловить СI помилку (r'(?<!\w)`\S', "monospaced"),
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

def generate_output(markdown_text, to_ansi=False):
    try:
        output = parse_markdown(markdown_text, to_ansi)
        return output
    except ValueError as e:
        sys.stderr.write(str(e) + '\n')
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Markdown to HTML/ANSI converter")
    parser.add_argument('input', help="Path to the input markdown file")
    parser.add_argument('--out', help="Path to the output file")
    parser.add_argument('--format', choices=['html', 'ansi'], help="Output format: html or ansi")
    args = parser.parse_args()

    markdown_text = read_file(args.input)

    if args.format == 'ansi' or (not args.format and not args.out):
        output = generate_output(markdown_text, to_ansi=True)
    else:
        output = generate_output(markdown_text)

    if args.out:
        with open(args.out, 'w', encoding='utf-8') as file:
            file.write(output)
    else:
        print(output)

if __name__ == "__main__":
    main()