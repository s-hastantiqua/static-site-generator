def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
                This is the same paragraph on a new line                

* This is a list
* with items

"""
print(markdown_to_blocks(markdown))
