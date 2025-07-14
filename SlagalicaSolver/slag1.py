import time
import itertools

def load_dictionary(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f.readlines())

def find_longest_word(letters, dictionary):
    start_time = time.time()
    max_word = ""
    
    #for length in range(1, len(letters) + 1):
    for length in range(len(letters), 0, -1):
        for perm in itertools.permutations(letters, length):
            word = ''.join(perm)
            
            if word in dictionary and len(word) > len(max_word):
                max_word = word
           
            if time.time() - start_time > 50:
                return max_word
    
    return max_word

def main():
    dictionary = load_dictionary('recnik.txt')
    
    print("Унеси 12 слова, ћирилица!:")
    letters = input().strip()
    
    if len(letters) != 12:
        print("Треба 12 слова мајмуне!.")
        return
    
    longest_word = find_longest_word(letters, dictionary)
    
    print(f"Најдужа реч: {longest_word}")

if __name__ == "__main__":
    main()



