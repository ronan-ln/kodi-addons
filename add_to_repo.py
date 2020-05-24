import sys
import os
import requests
import zipfile
from xml.etree import ElementTree

addon_name = sys.argv[1]
addon_version = sys.argv[2]
addon_url = sys.argv[3]


destination_folder = './download/' + addon_name + '/'
zip_path = destination_folder + addon_name + '-' + addon_version + '.zip'

print('Creating destination folder...')
try:
    os.mkdir(destination_folder)
except FileExistsError:
    print('Skipping, it already exists')

print('Downloading zip file from ' + addon_url +'...')
res = requests.get(addon_url, stream=True)
with open(zip_path, 'wb') as fd:
    for chunk in res.iter_content(chunk_size=128):
        fd.write(chunk)

print('Reading zip file details...')
zip = zipfile.ZipFile(zip_path)
for name in zip.namelist():
    if name.endswith('/addon.xml'):
        with zip.open(name) as addon_xml:
            addon_node = ElementTree.parse(addon_xml).getroot()
            break

addons = ElementTree.parse('./addons.xml')
addons_root = addons.getroot()
addons_root.insert(len(addons_root), addon_node)

addons.write('./addons.xml', encoding='utf-8', xml_declaration=True)
print('\nYou can now run:'
      '\n\tgit add', zip_path, ' addons.xml',
      '\n\tgit commit -m "Adding', addon_name, 'version', addon_version, 'from', addon_url, '"'
      '\n\tgit push')