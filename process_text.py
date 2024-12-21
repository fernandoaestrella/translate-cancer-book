import re

# Open the input.md file

# Open the file with UTF-8 encoding
with open('input.md', 'r', encoding='utf-8') as file:
    content = file.read()

    # Modify all page count lines like this one "> 23" to be like this "---23---"
    content = re.sub(r'>\s*(\d+)', lambda m: '---'+ m.group(1) +'---', content)

    # Remove "> " from the beginning of each line that starts with those characters
    content = re.sub(r'^> ', '', content, flags=re.MULTILINE)

    # Find all lines like "**The** **Mechanics** **Of** **Health**", remove the "**" characters, and make it a heading of level 2
    content = re.sub(r'^(\*\*[^*]+\*\*\s*)+$', lambda m: '## ' + m.group(0).replace('**', ''), content, flags=re.MULTILINE)

    # Convert all lines that contain only ">" to empty lines
    content = re.sub(r'^>$', '', content, flags=re.MULTILINE)

    # Detect paragraphs and remove newlines between each line of a paragraph
    content = re.sub(r'(?<=\S)(\n)(?=\S)', ' ', content)

    # For each line in the input
    lines = content.split('\n')

    # Loop through the lines
    for i, line in enumerate(lines):
        output_lines = ''
        # Check if the line is a page number line, e.g. "---10---"
        if line.startswith('---') and line.endswith('---'):
            # Check if the line 2 lines before it is a paragraph that does not end with a period
            if i > 1 and not lines[i-2].endswith('.'):
                # Check if there is a line 4 lines after the current one
                if i < lines.__len__() - 4:
                    # Replace the line that is 2 lines before the current line with the line that is 4 lines after the current one
                    lines[i-2] = lines[i-2] + " " + lines[i+4]
                
                    # Remove the line that is 4 lines after the current one
                    lines[i+4] = ''
                
    # Loop throught the lines
    for i, line in enumerate(lines):
        # Find lines that contain an img tag, e.g. "<img src="./y5gojttd.png" style="width:0.37847in;height:0.43056in" />"
        img_match = re.search(r'<img\s+src="([^"]+)"', line)
        if img_match:
            # Check if the current line contains text before the opening brackets of the img tag
            text_before_img = line[:img_match.start()].strip()
            if text_before_img:
                # Add a newline before the img tag
                lines[i] = line[:img_match.start()] + '\n' + line[img_match.start():]
            
            # Check if the current line contains text after the closing brackets of the img tag
            match = re.search(r'/>(.+)$', line)
            if match and match.group(1).strip():
                # Add a newline after the img tag
                lines[i] = lines[i].replace('/>', '/>\n')

    # Replace the original content with the modified content
    content = '\n'.join(lines)

    # When we detect a line with multiple italicized words, remove the entire line
    content = re.sub(r'^(\*[^*]+\*\s*)+$', '', content, flags=re.MULTILINE)

    # Create a new output.md file with the cleaned content
    with open('output.md', 'w', encoding='utf-8') as output_file:
        output_file.write(content)
