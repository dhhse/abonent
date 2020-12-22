## Let's all be honest: when scientists write code, aesthetics and
## software engineering principles take a back seat to having running,
## working code before a deadline.

## So, let's release the ugly.  And, let's be proud of that.


import re
import os


PATH_TO_FOLDER = 'pages_plain' # путь к папке с txt-файлами, в которых нужно сделать разметку

def parse_folder (path_to_folder):
    for path, dirs, filenames in os.walk (path_to_folder):
        for filename in filenames:
            print (filename)
            if '.txt' in filename:
                
                path_to_file = os.path.join (path,filename)
                parse_file (path_to_file)


def surround_with_tag (text, tag):
    opener = '<'+tag +'>'
    closer = '</'+tag +'>'
    return (opener + text + closer) 

def parse_file (path_to_file):
    with open (path_to_file, 'r',encoding='utf-8') as openfile:
        path_to_new_file = re.sub ('.txt','_segmented.xml', path_to_file)
        with open (path_to_new_file, 'w',encoding='utf-8') as writefile:
            writefile.write ('<root>\n')
            for line in openfile:
                newline = parse_line(line)
                writefile.write (newline)
            writefile.write ('</root>\n')

def parse_line (line):
    line = re.sub('<', '&lt;', line)
    line = re.sub('>', '&gt;', line)
    line = re.sub(r'^([А-ЯA-Z]{3,})\s+([А-ЯA-Z][а-яa-z]+\.?)\s+([А-ЯA-Z][а-яa-z]+\.?)'
                  ,surround_with_tag(r'\1','surname')
                  +surround_with_tag(r'\2','firstname')
                  +surround_with_tag(r'\3','patronym'),
                  line)
    line = re.sub(r'^([А-ЯA-Z]{3,})',surround_with_tag(r'\1','surname'), line)
    line = re.sub(r'([ТГT]\.?\s+\d{4,5})',surround_with_tag(r'\1','phone_number'), line)
    line = re.sub (r'(—\s+)([А-ЯA-Z][а-яa-z]+\.?)\s+([А-ЯA-Z][а-яa-z]+\.?)',
                   r'\1'+surround_with_tag(r'\2','firstname')
                   +surround_with_tag(r'\3','patronym'),
                   line)
    line = re.sub(r'(Д\s+\d+\.)(\n)',
                  surround_with_tag(r'\1','household_property')+r'\2',
                  line)
    return (line)


if __name__ == "__main__":
    print ('working')
    parse_folder (PATH_TO_FOLDER)

        
        
