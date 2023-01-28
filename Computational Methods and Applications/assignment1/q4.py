import random

class TextGenerator:
    def __init__(self):
        self.prefix_dict = {}
        self.assimilated = False
        
    def assimilateText(self, file_name):
        if self.assimilated == True:
            print("Warning: Already assimilated once.")
            # return                                                                    # Kill or pass?
        
        try:                                                                            # trying to open and read text from file
            with open(file_name, 'r') as f:
                text = f.read()
        except FileNotFoundError:
            raise Exception("Requested file not found!")
        except:
            raise Exception("An error occurred while trying to read file!")
        
        words = text.split()                                                            # split based on any whitespace character (including \n \r \t \f and ' ')
        if len(words) < 3:
            raise Exception("Assimilation failed: at least 3 words required in the file.")
        
        for i in range(len(words) - 2):                                                 # *** creating prefix dictionary ***
            prefix = (words[i], words[i+1])
            if prefix not in self.prefix_dict:
                self.prefix_dict[prefix] = []
            self.prefix_dict[prefix].append(words[i+2])
        self.assimilated = True
                
    def generateText(self, num_words, start_word=None):
        if not self.assimilated:                                                        # If not assimilated before, the self.prefix_dict will 
            raise Exception("It was not assimilated before generation.")                # be empty, and it does not make sense to generateText
        
        if start_word:
            prefix = None
            candidates=[]
            for key in self.prefix_dict:                                                # creating candidates of starting prefix
                if start_word == key[0]:
                    candidates.append(key)
                    
            if candidates!=[]:
                prefix = candidates[int((random.random()*len(candidates))//1)]          # randomly choosing a prefix from candidates
            # print("candidates =",candidates)
            # print("prefix =",prefix)
            if not prefix and num_words!=1:
                raise Exception("Unable to produce text with the specified start word.")
        else:
            prefix = random.choice(list(self.prefix_dict.keys()))
        
        if num_words==1:                                                                # Corner case: If we want to generate just one word,
            if not start_word:                                                          #   and start_word isn't specified,
                return random.choice(list(prefix))                                      #     we choose randomly from the random prefix chosen.
            else:                                                                       #   and start_word is specified,
                return start_word                                                       #     the generated text is the start_word itself.
        
        output = list(prefix)
        for _ in range(num_words - 2):                                                  # (num_words - 2) because 2 words already added
            if prefix not in self.prefix_dict:
                raise Exception("KeyError - Unable to generate next word after "+str(prefix[0])+" "+str(prefix[1]))
            
            # print("self.prefix_dict[prefix] =",self.prefix_dict[prefix])              
            next_word = random.choice(self.prefix_dict[prefix])                         # randomly choosing from possible next words
            output.append(next_word)
            prefix = (prefix[1], next_word)
        return ' '.join(output)
    
    def print_prefdict(self, flag=False):                                               # helper funtion to help debugging
        if(not flag):
            print(self.prefix_dict)
        else:
            for k in self.prefix_dict:
                if len(self.prefix_dict[k])>1:
                    print(str(k)+': '+str(self.prefix_dict[k]))

tg = TextGenerator()
# tg.print_prefdict()
tg.assimilateText('sherlock.txt')
print(tg.generateText(100, 'Holmes'))

# tg.assimilateText('shk.txt')
# print(tg.generateText(1, 'yz'))
# print(tg.generateText(10, 'a'))