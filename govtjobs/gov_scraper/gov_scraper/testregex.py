import re

path_txt = '/home/urmi/Documents/govtjobs/govtjobs/downloaded_text/full/0c1c0212b150c60a1a8ffaeaaf284116684315ce.pdf.txt'
file = open(path_txt, "r")

text = file.read()
print (text)

result = re.search(r"CEN(\s|-)[0-9]{2}\/[0-9]{4}", text)

print (result.group(0))

