from pypdf import PdfReader, PdfWriter
from datetime import datetime


def add_meta(w,tit,):
    ''' add meta data to pdf file '''
    try:
        w.add_metadata(
            {
                "/Author": "Dr Daniel Zhang",
                "/Producer": "reveal.js + Python",
                "/Title": "Lecture_1_Induction",
                "/Subject": "Artificial Intelligence and Machine Learning",
                "/Keywords": "AI, ML, Induction",
                "/CreationDate": datetime.now().strftime('%Y%m%d-%H%M%S'),
                "/ModDate": datetime.now().strftime('%Y%m%d-%H%M%S'),
                "/Creator": "Dr Daniel Zhang",
                "/Company": "Falmouth University",
            }
        )
    except:
        return None
    
def get_size(r):
    ''' get the number of pages from the given reader object '''
    try:
        return len(r.pages)
    except:
        return None
    
def get_pages(r):
    ''' get all pages from the given reader object '''
    try:
        return r.pages
    except:
        return None

def get_page(r,pg):
    ''' read one page from the reader object
        r:  reader
        pg: page number (0-based)
    '''
    try:
        return r.pages[pg]
    except:
        return None

def get_text(pg):
    ''' get the content from a given page
        pg: the page object returned by get_page()
    '''
    try:
        return pg.extract_text()
    except:
        return None
    
def add_bookmark(w,bk,pg,pr):
    ''' add bookmark to the pdf file
        w:  writer
        bk: bookmark string
        pg: page number (0-based)
        pr: parent (None or the parent bookmark returned by last add_bookmark() call)
        return the bookmark or None
    ''' 
    try:
        return w.add_bookmark(bk,pg,pr)
    except:
        return None

def write_pdf(fn,pgs,bks=None):
    ''' write pdf files with optional bookmarks
        fn: file name string
        pgs:pages
        bks:bookmarks or None 
    '''
    try:
        if bks and len(pgs) != len(bks):
            raise Exception('Pages and Bookmarks have different number of items')
        w = PdfWriter()
        for i,page in enumerate(pgs):
            w.add_page(page)
            print(f'page {i} added')
            if bks:
                w.add_outline_item(bks[i],i,None)
                print(f'\tbookmark[{i}] added: {bks[i]}')
        # write out files
        print(f'writing to file: {fn}')
        with open(fn, "wb") as f:
            w.write(f)
        return True
    except:
        return False

if __name__ == '__main__':
    fname = r"C:\Users\xenos\Documents\GitHub\UK_Teaching\Uni\Falmouth\COMP712\1_Induction.pdf"
    r = PdfReader(fname)
    p1 = get_page(r,0)
    t1 = get_text(p1)
    n = get_size(r)
    print(f'PDF pages: {n}')
    print(f'The 1st page: {t1}')
    f1 = r'test1.pdf'
    f2 = r'test2.pdf'
    k = [f'Page {i+1}' for i in range(n)]
    # write_pdf(f1,r.pages)
    write_pdf(f2,r.pages,k)
