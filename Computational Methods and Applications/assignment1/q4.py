import random

class TextGenerator:
    def __init__(self):
        self.prefix_dict = {}
        
    def assimilateText(self, file_name):
        with open(file_name, 'r') as f:
            text = f.read()
        words = text.split()
        for i in range(len(words) - 2):
            prefix = (words[i], words[i+1])
            if prefix not in self.prefix_dict:
                self.prefix_dict[prefix] = []
            self.prefix_dict[prefix].append(words[i+2])
                
    def generateText(self, num_words, start_word=None):
        if start_word:
            prefix = None
            candidates=[]
            for key in self.prefix_dict:
                if start_word == key[0]:
                    candidates.append(key)
                    
            if candidates!=[]:
                prefix = candidates[int((random.random()*len(candidates))//1)]
            # print("candidates =",candidates)
            # print("prefix =",prefix)
            if not prefix:
                raise Exception("Unable to produce text with the specified start word.")
        else:
            prefix = random.choice(list(self.prefix_dict.keys()))
        output = list(prefix)
        for i in range(num_words - 2):
            next_word = random.choice(self.prefix_dict[prefix])
            output.append(next_word)
            prefix = (prefix[1], next_word)
        return ' '.join(output)
    
    # def print_prefdict(self):
    #     print(self.prefix_dict)

tg = TextGenerator()
tg.assimilateText('sherlock.txt')

print(tg.generateText(50,"girl"))