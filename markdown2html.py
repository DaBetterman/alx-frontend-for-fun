#!/usr/bin/python3
"""
A script to convert Markdown to HTML.

"""

import sys
import os
import hashlib

def convert_markdown_to_html(markdown_file, output_file):
    with open(markdown_file, 'r') as md_file, open(output_file, 'w') as html_file:
        in_list = False
        in_ordered_list = False

        for line in md_file:
            stripped_line = line.strip()

            # Converting the headings
            if stripped_line.startswith('#'):
                heading_level = len(stripped_line) - len(stripped_line.lstrip('#'))
                if 1 <= heading_level <= 6:
                    heading_text = stripped_line.strip('#').strip()
                    html_file.write(f'<h{heading_level}>{heading_text}</h{heading_level}>\n')
                continue
            
            # Converting the unordered lists
            if stripped_line.startswith('- '):
                if not in_list:
                    in_list = True
                    html_file.write('<ul>\n')
                html_file.write(f'    <li>{stripped_line[2:]}</li>\n')
                continue
            else:
                if in_list:
                    html_file.write('</ul>\n')
                    in_list = False

            # Converting the ordered lists
            if stripped_line.startswith('* '):
                if not in_ordered_list:
                    in_ordered_list = True
                    html_file.write('<ol>\n')
                html_file.write(f'    <li>{stripped_line[2:]}</li>\n')
                continue
            else:
                if in_ordered_list:
                    html_file.write('</ol>\n')
                    in_ordered_list = False

            # Converting the paragraphs
            if stripped_line and not stripped_line.startswith('#') and not stripped_line.startswith('- ') and not stripped_line.startswith('* '):
                if '<ul>' not in line and '<ol>' not in line:
                    html_file.write('<p>\n')
                    html_file.write(f'    {stripped_line}\n')
                    html_file.write('</p>\n')
                    continue

            # Converting the bold and emphasis text
            line = line.replace('**', '<b>').replace('__', '<em>')
            line = line.replace('**', '</b>').replace('__', '</em>')

            # Converting the custom markdown to MD5 or remove 'c'
            if '[[' in line and ']]' in line:
                content = line[line.find('[[') + 2:line.find(']]')]
                md5_hashed = hashlib.md5(content.encode()).hexdigest()
                line = line.replace(f'[[{content}]]', md5_hashed)
            if '((' in line and '))' in line:
                content = line[line.find('((') + 2:line.find('))')]
                content_no_c = content.replace('c', '').replace('C', '')
                line = line.replace(f'(({content}))', content_no_c)

            html_file.write(line)

        if in_list:
            html_file.write('</ul>\n')
        if in_ordered_list:
            html_file.write('</ol>\n')

def main():

    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)
    
    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    # Checking if the Markdown file exists
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        exit(1)

    # Converting the Markdown file to an HTML file
    convert_markdown_to_html(markdown_file, output_file)

    # If everything is fine, exit with status 0
    exit(0)

if __name__ == "__main__":
    main()
