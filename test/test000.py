from docx import Document

def extract_hyperlinks(docx_file):
    doc = Document(docx_file)
    links = []
    for para in doc.paragraphs:
        for run in para.runs:
            if run.underline and run.font.color.rgb is not None:
                links.append((run.text, run.hyperlink))
    return links

# 使用示例
links = extract_hyperlinks("test.docx")
for text, hyperlink in links:
    print(f"文本: {text}, 链接: {hyperlink}")
