import json
import os

folders = []

for root, dirs, files in os.walk('.'):
    if 'manifest.json' in files:
        folders.append(root)

print('These folders have a manifest.json file:')
for i, folder in enumerate(folders, 1):
    print(f'{i}. {folder}')

choice = int(input('Enter the number of the folder you want to update: '))

if 1 <= choice <= len(folders):
    folder = folders[choice - 1]
    with open(f'{folder}/manifest.json', 'r+') as json_file:
        data = json.load(json_file)

        mod_versions = {}
        for item in data['dependencies']:
            author_name, mod_name, version = item.split('-')
            mod_versions[author_name + '-' + mod_name] = version

        with open('dependency.txt', 'r') as txt_file:
            for line in txt_file:
                line = line.strip()
                author_name, mod_name, version = line.split('-')
                fullname = author_name + '-' + mod_name

                if fullname in mod_versions:
                    old_version = mod_versions[fullname]
                    if version > old_version:
                        index = data['dependencies'].index(fullname + '-' + old_version)
                        data['dependencies'][index] = line
                        print(f'updated {mod_name} {old_version} -> {version}')
                else:
                    data['dependencies'].append(line)
                    print(f'added {mod_name}')

        json_file.seek(0)
        json.dump(data, json_file, indent=4)
        json_file.truncate()
else:
    print(f'Invalid folder number: {choice}')


