import re

def path(file):
    # file to resource_location path
    l = re.split(r'[/\\".]',str(file))
    del l[-1]
    s = ''
    for value in l :
        if not value == '' :
            s += value + '/'
    return s[:-1]

def get(namespace,file):
    # namespace & file to resource_location
    return str(namespace) + ':' + path(file)

def separate(file):
    # get path from resource_location
    l = str(file).split(':',1)
    if l.__len__() > 1 :
        del l[0]
    s = ''
    for value in l :
            s += value
    return s

def split(file):
    # get (namespace, path) from resource_location
    file = str(file)
    tags_flag = False
    if file.startswith('#'):
        tags_flag = True
        file = file[1:]
    l = str(file).split(':',1)
    if l.__len__() <= 1 :
        l = ['minecraft', l[-1]]
    if tags_flag :
        l[0] = '#' + l[0]
    return l

def namespaced(file):
    # get namespaced id
    namespace, resource_path = split(file)
    return namespace + ':' + resource_path
