import os
import random
import collections
import jsonlines
from tqdm import tqdm
from create_ontology import ori_onto2use_onto

SEED = 19940802
SHOT = 5

def process_example(words, labels):
    assert len(words) == len(labels)
    examples = []
    for index, (word, label) in enumerate(zip(words, labels)):
        if label != 'O':
            if index == 0 or labels[index] != labels[index - 1]:
                end_index = index
                while end_index < len(words) - 1 and labels[end_index] == labels[end_index + 1]:
                    end_index += 1
                left_context = words[: index]
                mention = words[index: end_index + 1]
                right_context = words[end_index + 1:]
                example = {
                    'left_context': left_context,
                    'mention': mention,
                    'right_context': right_context,
                    'entity_type': [ori_onto2use_onto(labels[index])],
                }
                examples.append(example)
    return examples


input_dir = '/nfs/yding4/Entity_Typing/dataset/FEW-NERD'
output_dir = '/nfs/yding4/Entity_Typing/Fine-Grained-Entity-Typing/data/FEW-NERD'
os.makedirs(output_dir, exist_ok=True)
splits = ['train', 'dev', 'test']

for split in splits:
    input_file = os.path.join(input_dir, split + '.txt')
    output_file = os.path.join(output_dir, split + '.json')
    examples = []
    words = []
    labels = []
    with open(input_file) as reader:
        for line in tqdm(reader):
            if line.startswith("-DOCSTART-") or not line.strip():
                if words:
                    examples.extend(process_example(words, labels))
                words = []
                labels = []
            else:
                parts = line.rstrip().split('\t')
                assert len(parts) == 2
                words.append(parts[0])
                labels.append(parts[1])
        if words:
            examples.extend(process_example(words, labels))
    examples = sorted(examples, key=lambda x: (x['entity_type'], x['left_context']))
    with jsonlines.open(output_file, 'w') as writer:
        writer.write_all(examples)

    if split == 'train':
        few_shot_examples = []
        few_shot_output_file = os.path.join(output_dir, split + '_' + str(SHOT) + '_shot.json')
        random.Random(SEED).shuffle(examples)
        label2shot = collections.defaultdict(int)
        label2mention = collections.defaultdict(list)
        for example in examples:
            entity_type = example['entity_type'][0]
            mention = ' '.join(example['mention']).lower()
            if label2shot[entity_type] < SHOT and mention not in label2mention[entity_type]:
                few_shot_examples.append(example)
                label2mention[entity_type].append(mention)
                label2shot[entity_type] += 1
        with jsonlines.open(few_shot_output_file, 'w') as writer:
            writer.write_all(few_shot_examples)
