import re
from collections import defaultdict
import rich
from rich import console
from itertools import chain
import pyinspect as pi

aliases = {
    'Admin Interface':            'Admin/Security',
    'Admin':                      'Admin/Security',
    'Security':                   'Admin/Security',
    'Content Management Systems': 'Cms',
    'E-Commerce':                 'Ecommerce',
    'File Transfers':             'Files/Images',
    'Image Handling':             'Files/Images',
    'Model Extensions':           'Fields/Models',
    'Fields':                     'Fields/Models',
    'Models':                     'Fields/Models',
    'Search Engine Optimisation': 'Seo',
    'Task Queues':                'Task Queue',
    'Drf Resources':              'Django Rest Framework',
    'Drf Tutorials':              'Django Rest Framework',
    'Testing':                    'Debugging/Performance',
    'Debugging':                  'Debugging/Performance',
    'Performance':                'Debugging/Performance',
    'General':                    'Other',
    'Settings':                   'Configuration',
    'Educational':                'External Documentation',
    'Websites':                   'External Documentation',
    'Static Assets':              'Asset Management',
    'Users':                      'Authentication',
    'Blog Management':            'Cms',
    'Wysiwyg Editors':            'Editors',
    
    }


def have_common_url(lib1, lib2):
    for url in lib1['urls']:
        for otherurl in lib2['urls']:
            if url == otherurl:
                return True
    return False


def have_same_name(lib1, lib2):
    return lib1['name'] == lib2['name']


def parse_file(filename) -> dict:
    filedict = {}
    current_title = ""
    with open(f'./dev/{filename}') as f:
        lines = f.readlines()
    for line in map(str.strip, lines):
        match = re.search(r"\[(?P<name>[^]]+)]\((?P<url>https?://[^)]+)\)[ -]*(?P<description>.*)", line)
        if not match:
            if 'http' in line:
                raise ValueError(f"Should have matched, but no match: {line}")
            titlematch = re.search(r'###? (.+)', line)
            if titlematch:
                current_title = titlematch.group(1).title()
                if current_title in aliases:
                    current_title = aliases[current_title]
            continue
        linedict = match.groupdict()
        name = linedict['name'].lower()
        url = linedict['url'].lower()
        url = url[:-1] if url.endswith('/') else url
        description = linedict['description']
        if current_title == 'Apis' and ('rest' in name.lower() or 'rest' in url or 'rest' in description.lower()):
            current_title = 'Django Rest Framework'
        if name in filedict:
            if any(fileurl != url for fileurl in filedict[name]['urls']):
                # same name, different url. e.g. name='official documentation', urls can be different because under different titles
                print(f'"{filename}" duplicate: "{name}":\n\t{filedict[name]}\n\tvs\n\t{linedict} ({current_title = })')
                newname = f'{next(iter(filedict[name]["titles"]))}: {name}'
                filedict[newname] = filedict[name]
                del filedict[name]
                name = f'{current_title} : {name}'
        filedict[name] = dict(urls={url}, description=description, titles={current_title})
    return filedict


def main():
    jbwolfe = parse_file('jbwolfe-awesome-django.md')
    wsvincent = parse_file('wsvincent-awesome-django.md')
    shahraizali = parse_file('shahraizali-awesome-django.md')
    keys = set(jbwolfe.keys()) | set(wsvincent.keys()) | set(shahraizali.keys())
    merged = dict()
    bytitle = defaultdict(list)
    
    con = console.Console()
    # populate merged
    for key in keys:
        merged[key] = dict(titles=set(), urls=set(), description='')
        for val in (jbwolfe.get(key), wsvincent.get(key), shahraizali.get(key)):
            if not val:
                continue
            merged[key]['titles'].update(val['titles'])
            merged[key]['urls'].update(val['urls'])
            merged[key]['description'] = val['description']
    
    # popuplate bytitle
    for key, value in merged.items():
        for title in value['titles']:
            if title == 'Other' and len(value['titles']) > 1:
                continue
            if title == 'Python Packages' and len(value['titles']) > 1:
                continue
            if title == 'Restful Api' and len(value['titles']) > 1:
                continue
            
            lib = dict(urls=frozenset(merged[key]['urls']), description=merged[key]['description'], name=key)
            normalized_title = aliases.get(title) or title
            existing_lib = next((otherlib for otherlib in bytitle[normalized_title] if have_same_name(otherlib, lib) or have_common_url(otherlib, lib)), None)
            if existing_lib:
                print(f"\nskipping duplicate lib under {normalized_title}:\n\tlib:\n\t\t{lib}\n\texisting:\n\t\t{existing_lib}")
            else:
                bytitle[normalized_title].append(lib)
    for title, libs in bytitle.items():
        for l1 in libs:
            duplicates = list(otherlib for otherlib in chain(*bytitle.values()) if have_same_name(otherlib, l1) or have_common_url(otherlib, l1))
            if len(duplicates) > 1:
                print('\nduplicates:')
                titles = [key for key in bytitle.keys() if any(duplicate in bytitle[key] for duplicate in duplicates)]
                con.print(titles, duplicates, width=1000, no_wrap=False, crop=False, soft_wrap=False)
                # pretty.pprint(f"duplicates: {duplicates}")
    
    bytitle_str = ""
    for title, libs in sorted(bytitle.items()):
        bytitle_str += f"\n\n## {title}\n\n"
        for lib in sorted(libs, key=lambda k: k['name']):
            bytitle_str += f"- [{lib['name']}]({next(iter(lib['urls']))}) - {lib['description']}\n"
    
    with open('./dev/merged-awesome-django.md', mode='w') as f:
        f.write(bytitle_str)


if __name__ == '__main__':
    main()
