"""Org-mode module providing facilities to export Org documents or 
   parts of Org documents to a variety of other formats.

   This exports:
   - org2any.org2html: Export as a HTML-formatted data. 

"""

# Imports required
from tempfile import NamedTemporaryFile
from subprocess import call
import urllib

###########################################################################

def org2html(org_content, file_prefix="", file_delete=True):
    """org2html(org_content[, file_prefix=""[, file_delete=True]])

    Description: 
    Creates a temporary org-file with given content having default 
    file-name and extension ".org"; and if file_prefix provided it's prefixed 
    to the default file-name. Based on that file, a temporary html file is 
    created and from that file only the content between the "body" element 
    tag, is stripped off and returned to the calling function.

    NOTE: This function deletes "org" file (only when 'file_delete' is set 
    to 'True'), and not the "Html" file.

    Example: 
    For an Org file [myfile-]temp2.org, the HTML file will be 
    [myfile-]temp2.html. The file will be overwritten without warning.

    Arguments:
    org_content - a string representing org-mode content
    file_prefix[optional] - required to create temporary file with the given prefix
    file_delete[optional] - whether to delete the temporary file once it is closed or not 

    Returns: a unicode representing org-mode content exported to HTML-formatted content. 

    """
            
    # org editor content manipulation for temporary file (".org")
    org_content_header_for_file = "#+OPTIONS: timestamp:nil author:nil creator:nil ^:{} H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t" + "\n#+BIND: org-export-html-auto-postamble nil" + "\n#+TITLE: \n"

    org_content_for_file = org_content.replace("\r", "")

    # Creating a temporary file with ".org" extension 
    file_suffix=".org"        # ".org" suffix must; otherwise emacs command won't work!
    org_file_obj = NamedTemporaryFile('w+t', suffix=file_suffix, prefix=file_prefix, delete=file_delete)

    filename_org = org_file_obj.name
    # Example (filename_org): "/tmp/wikiname-usrname-tmptCd4aq.org"

    org_file_obj.write((org_content_header_for_file + org_content_for_file).encode('utf-8'))
    # NOTE: Don't close this file till the time, html file is created

    # Move the cursor - pointing to start of the file
    # Must, otherwise cursor remains @ end (as this file isn't closed after writing data into it) and you won't get any data
    org_file_obj.seek(0)

    # Exporting the above created ".org" file to html
    
    ext_html = ".html"
    filename_html = filename_org[:-4] + ext_html
    # Example (filename_html): "/tmp/wiliname-usrname-tmptCd4aq.html"
    
    cmd = "emacs --batch " + filename_org + " --eval '(org-export-as-html nil)'"
    # (org-export-as-html nil)
    # (setq org-export-html-postamble nil) 
    cmd_res = call((cmd + ' </dev/null'), shell=True)
            
    # Close ".org" temporary file
    org_file_obj.close()
            
    if cmd_res <= 0:
        print "\n\n Html file created @ {0}\n".format(filename_html)
    else:
        # TODO: Throw error, may be I/O
        print "\n\n Some error occurred!!!\n"
        
    # Reading data from ".html" file and pasting it in wikipage object's "content" variable 
    with open(filename_html, 'r') as html_file_obj:
        html_data = html_file_obj.readlines()

    # Stripping and storing html data i.e. between <body>...</body> (Both elements are not included)
    strip_html_data = ""
    start_index = html_data.index("<body>\n") + 1         # Start copying data after <body>\n element
    end_index = html_data.index("</body>\n")              # Copy data until you reach before </body>\n element
    for line in html_data[start_index:end_index]:
        strip_html_data += line.decode('utf-8').lstrip()

    return strip_html_data
