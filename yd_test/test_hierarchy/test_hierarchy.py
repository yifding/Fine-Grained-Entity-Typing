def count_level(line):
    i = 0
    while(i < len(line) and line[i] == '\t'):
        i += 1
    return i

def extract_hierarchy(filename):
    child_dict = {}
    parent_dict = {}
    level_dict = {}
    current_parent = {}

    child_dict['name'] = 'root'
    with open(filename) as f:
        for line in f:
            level = count_level(line)
            level_dict[line.strip()] = level
            print(f'line: {repr(line)}; level:{level}')
            # print(eval(line))
            if level == 0:
                child_dict[line.strip()] = {}
                child_dict[line.strip()]['name'] = line.strip()
                parent_dict[line.strip()] = child_dict
                current_parent[level] = child_dict[line.strip()]
            else:
                parent_dict[line.strip()] = current_parent[level-1]
                parent_dict[line.strip()][line.strip()] = {}
                current_dict = parent_dict[line.strip()][line.strip()]
                current_dict['name'] = line.strip()
                current_parent[level] = current_dict

    return child_dict, parent_dict, level_dict



if __name__ == '__main__':
    filename = 'test_hierarchy.txt'
    child_dict, parent_dict, level_dict = extract_hierarchy(filename)
    print(f'child_dict: {child_dict}')
    print(f'parent_dict: {parent_dict}')
    print(f'level_dict: {level_dict}')