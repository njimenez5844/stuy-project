import pandas as pd
import PyPDF2

with open('Biology Textbook.pdf', 'rb') as file:
    
    pdf_reader = PyPDF2.PdfReader(file)

    chapter_ranges = {
        'Chapter 1': [25, 26],
        'Chapter 2': [54, 54],
        'Chapter 3': [88, 89],
        'Chapter 4': [115,116],
        'Chapter 5': [133,134],
        'Chapter 6': [151,152],
        'Chapter 7': [171,172],
        'Chapter 8': [196,197],
        'Chapter 9': [222,223],
        'Chapter 10': [247,247],
        'Chapter 11': [272,273],
        'Chapter 12': [289,290],
        'Chapter 13': [322,323],
        'Chapter 14': [353,354],
        'Chapter 15': [400,401],
        'Chapter 16': [446,448],
        'Chapter 17': [474,475],
        'Chapter 18': [497,498],
        'Chapter 19': [527,528],
        'Chapter 20': [565,566],
        'Chapter 21': [591,592],
    }

    questions = []
    page_advancement = 8

    for chapter_title, page_range in chapter_ranges.items():
        
        chapter_text = ''
        for page_num in range(page_range[0] + page_advancement - 1, page_range[1] + page_advancement):
            page = pdf_reader.pages[page_num]
            chapter_text += page.extract_text()
        
        question_texts = chapter_text.split('\n')
        
        i = 0
        for question_text in question_texts:
            
            if question_text.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.','10','11.','12.', '13.', '14.', '15.', '16.', '17.', '18.', '19.','20.','21.','22.')):
            
                question_parts = question_text.split(maxsplit=1)
                question_number = int(question_text.strip()[0])
                question_text = question_parts[0] + " " + question_parts[1].strip()
                i += 1
                question = {
                    'Chapter Number': chapter_title.split()[1],
                    'Question Number': question_number,
                    'Question Text': question_text
                }
                #print(question)
                questions.append(f"-{question}-")

    df = pd.DataFrame(questions)

    df.to_csv('bio.csv', index=False)

