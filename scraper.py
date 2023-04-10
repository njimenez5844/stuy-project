import pandas as pd
import PyPDF2

with open('Chemistry Textbook.pdf', 'rb') as file:
    
    pdf_reader = PyPDF2.PdfReader(file)

    chapter_ranges = {
        'Chapter 1': [35, 40],
        'Chapter 2': [75, 81],
        'Chapter 3': [111, 119],
        'Chapter 4': [154,161],
        'Chapter 5': [202,211],
        'Chapter 6': [248,253],
        'Chapter 7': [290,298],
        'Chapter 8': [329,356],
        'Chapter 9': [384,393],
        'Chapter 10': [424,433],
        'Chapter 11': [463,471],
        'Chapter 12': [514,523],
        'Chapter 13': [558,566],
        'Chapter 14': [609,621],
        'Chapter 15': [661,663],
        'Chapter 16': [708,715],
        'Chapter 17': [758,763],
        'Chapter 18': [803,805],
        'Chapter 19': [838,847],
        'Chapter 20': [898,899],
        'Chapter 21': [935,941],
        'Chapter 22': [979,984],
        'Chapter 23': [1022,1028],
        'Chapter 24': [1072,1078]
    }

    questions = []
    page_advancement = 40

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
                question_text =  question_parts[1].strip()
                i += 1
                question = {
                    'Chapter Number': chapter_title.split()[1],
                    'Question Number': question_number,
                    'Question Text': question_text
                }
                #print(question)
                questions.append(f"-{question}-")

    df = pd.DataFrame(questions)

    df.to_csv('chem.csv', index=False)

