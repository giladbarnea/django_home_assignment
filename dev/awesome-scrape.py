import re
from collections import defaultdict

from rich import pretty
from itertools import chain

aliases = {
    'Admin Interface':            'Admin',
    'Content Management Systems': 'Cms',
    'E-Commerce':                 'Ecommerce',
    'File Transfers':             'Files/Images',
    'Image Handling':             'Files/Images',
    'Model Extensions':           'Models',
    'Search Engine Optimisation': 'Seo',
    'Task Queues':                'Task Queue',
    'Drf Resources':              'Django Rest Framework',
    'Drf Tutorials':              'Django Rest Framework',
    'Testing':                    'Debugging',
    
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
    
    # populate merged
    for key in keys:
        merged[key] = dict(titles=set(), urls=set(), name='', description='')
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
            lib = dict(urls=frozenset(merged[key]['urls']), description=merged[key]['description'], name=key)
            normalized_title = aliases.get(title) or title
            existing_lib = next((otherlib for otherlib in bytitle[normalized_title] if have_same_name(otherlib, lib) or have_common_url(otherlib, lib)), None)
            if existing_lib:
                print(f"\nskipping duplicate lib under {normalized_title}:\n\tlib:\n\t\t{lib}\n\texisting:\n\t\t{existing_lib}")
            else:
                bytitle[normalized_title].append(lib)
    
    
    bytitle_str = ""
    for title, libs in sorted(bytitle.items()):
        bytitle_str += f"\n\n## {title}\n\n"
        for lib in sorted(libs, key=lambda k: k['name']):
            bytitle_str += f"- [{lib['name']}]({next(iter(lib['urls']))}) - {lib['description']}\n"
    
    with open('./dev/merged-awesome-django.md', mode='w') as f:
        f.write(bytitle_str)


if __name__ == '__main__':
    main()
