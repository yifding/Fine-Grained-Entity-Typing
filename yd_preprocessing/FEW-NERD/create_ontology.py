import os
import collections


KEY_WORDS_MAPPING = {
    'broadcastprogram': 'broadcast program',
    'writtenart': 'written art',
    'sportsfacility': 'sports facility',
    'sportsevent': 'sports event',
    'militaryconflict': 'military conflict',
    'bodiesofwater': 'bodies of water',
    'GPE': 'geopolitical entity',
    'governmentagency': 'government agency',
    'politicalparty': 'political party',
    'showorganization': 'show organization',
    'sportsleague': 'sports league',
    'sportsteam': 'sports team',
    'astronomything': 'astronomy thing',
    'biologything': 'biology thing',
    'chemicalthing': 'chemical thing',
    'educationaldegree': 'educational degree',
    'livingthing': 'living thing',
    'education': 'education institution',
}


def ori_onto2use_onto(ori_onto):
    use_onto = '/' + ori_onto.replace('/', '|').replace('-', '/')
    return use_onto


input_file = 'labels.txt'
output_dir = '/nfs/yding4/Entity_Typing/Fine-Grained-Entity-Typing/data/FEW-NERD'
os.makedirs(output_dir, exist_ok=True)
old_hier_file = os.path.join(output_dir, 'old_hier.txt')
new_hier_file = os.path.join(output_dir, 'new_hier.txt')

old_hier = dict()
new_hier = collections.defaultdict(list)

with open(input_file) as reader:
    for line in reader:
        line = line.rstrip('\n')
        if line == 'O':
            continue
        first_level, second_level = line.split('-')
        raw_second_level_key_words = second_level.split('/')
        second_level_key_words = []
        for raw_second_level_key_word in raw_second_level_key_words:
            if raw_second_level_key_word in KEY_WORDS_MAPPING:
                second_level_key_words.append(KEY_WORDS_MAPPING[raw_second_level_key_word])
            else:
                second_level_key_words.append(raw_second_level_key_word)

        print(f'first_level: {first_level}')
        print(f'second_level: {second_level_key_words}')

        first_level_str = first_level

        if len(second_level_key_words) == 1:
            second_level_str = second_level_key_words[0]
        else:
            second_level_str = ', '.join(second_level_key_words[:-1]) + ' or ' + second_level_key_words[-1]
        # 1. old_hier: dictionary of original line to new name.
        # 2. new_hier: \t split of hierarchical classes
        assert line not in old_hier
        if second_level_str == 'other':
            old_hier[line] = first_level_str
        else:
            old_hier[line] = second_level_str

        assert line not in new_hier[first_level_str]
        new_hier[first_level_str].append(line)

print(f'old_hier: {old_hier}')
print(f'new_hier: {new_hier}')

with open(old_hier_file, 'w') as writer:
    for index, (k, v) in enumerate(old_hier.items()):
        writer.write(ori_onto2use_onto(k) + ':' + v)
        if index != len(old_hier.items()) - 1:
            writer.write('\n')

with open(new_hier_file, 'w') as writer:
    for index, (k, v) in enumerate(new_hier.items()):
        writer.write(ori_onto2use_onto(k) + '\n')
        for second_index, second_level in enumerate(v):
            writer.write('\t' + ori_onto2use_onto(second_level))
            if index == len(new_hier.items()) - 1 and second_index == len(v) - 1:
                continue
            else:
                writer.write('\n')
