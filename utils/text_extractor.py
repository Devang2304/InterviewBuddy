import pymupdf

class text_extractor:
    def __init__(self):
        self.text = None
    
    def extract_text(self,file_path):
        doc = pymupdf.open(file_path)
        out = open('../extracted_data/temp_resume_data.txt', 'wb')
        for page in doc:
            text = page.get_text().encode("utf-8")
            out.write(text)
        out.close()
        

if __name__ == "__main__":
    file_path = "../../../MY RESUME_DEVANG/barclays resume/Devang_Vartak_Resume.pdf"
    obj = text_extractor()
    obj.extract_text(file_path)
        
    