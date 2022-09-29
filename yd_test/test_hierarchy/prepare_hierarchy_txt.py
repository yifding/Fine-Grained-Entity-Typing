file_name = 'test_hierarchy.txt'

with open(file_name, 'w') as writer:
    writer.write('root' + '\n')
    writer.write('\tart' + '\n')
    writer.write('\t\tart-music' + '\n')
    writer.write('\t\tart-writtenart')