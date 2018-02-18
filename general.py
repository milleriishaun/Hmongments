import os

# Each website crawled is a separate project(folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating project ' + directory)
        os.makedirs(directory)

# Create queued and crawled files(if not already made)
def create_data_files(project_name, base_url):
    queue = os.path.join(project_name, 'queue.txt')
    crawled = os.path.join(project_name, 'crawled.txt')
    if not os.path.isfile(queue):
        write_file(queue, base_url)
        if not os.path.isfile(crawled):
            write_file(crawled, '')

# Create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)

# Add data onto and existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')

# this is creating a new file which will delete it
# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()

# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

# Iterate through a set. Eache item will be a new line in the file
def set_to_file(links, file_name):
    with open(file_name, 'w') as f:
        for l in sorted(links):
            f.write(l+"\n")
