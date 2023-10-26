''' Use this script to convert all markdown files to html using specified css

    Daniel.Zhang
    Oct 2023
'''

# importing modules
import os
import shutil
from glob import glob

SOURCE_PATH = r'Uni'
CSS_PATH = r'assets\dist\pan_am.css'
PANDOC_CMD = r'pandoc "MD_FILE" -f markdown -t html5 -s -o "HTML_FILE"'

# #################################################################
def get_all_files(d_path):
    ''' get all files with relative links to a dict: {uni: {module:html}} '''
    # get all html file paths 
    mds = [x[x.index(d_path)+len(d_path)+1:] for x in glob(d_path+r'/**/*.md',recursive=True)]
    # sort out after split: uni -> module -> htmls
    md_dict = {}
    for x in mds:
        parts = x.split(os.sep)
        p,f = os.sep.join(parts[:-1]), parts[-1]
        md_dict[f] = [d_path+os.sep+p,f.split('.')[0]]
    return md_dict

# #################################################################
def md_2_html(m_name,p_path_info,c_css=None,pan_path=None):
    ''' convert markdown to html
        m_name:         md name
        p_path_info:    working path information and name string [path,name(no ext)]
        c_css:          css file
        pan_path:       pandoc path
        output would be the same name but different extension
    '''
    if not pan_path:
        pan_path = 'pandoc'
    full_md_path = os.sep.join(p_path_info)
    cmd_str = PANDOC_CMD.replace('MD_FILE',full_md_path+'.md').replace('HTML_FILE',full_md_path+'.html')
    if c_css:
        # copy css to the md folder
        # css_name = c_css.split(os.sep)[-1]
        # shutil.copy(CSS_PATH,p_path_info[0]+os.sep+css_name)
        cmd_str += ' --self-contained -c "'+c_css+'"'
    os.system(cmd_str)

# #################################################################
if __name__ == '__main__':
    mds = get_all_files(SOURCE_PATH)
    print(len(mds),'->',mds)
    for k,v in mds.items():
        md_2_html(k,v,CSS_PATH)

