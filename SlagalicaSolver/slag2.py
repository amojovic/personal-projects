import time
import itertools
import threading

def load_dictionary(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f.readlines())

longest_word_lock = threading.Lock()
longest_word = ""

def find_longest_word_from_short_to_long(letters, dictionary, start_time):
    global longest_word
    for length in range(1, len(letters) + 1):
        for perm in itertools.permutations(letters, length):
            word = ''.join(perm)
            if word in dictionary:
                with longest_word_lock:  
                    if len(word) > len(longest_word):
                        longest_word = word
            if time.time() - start_time > 50:
                return

def find_longest_word_from_long_to_short(letters, dictionary, start_time):
    global longest_word
    for length in range(len(letters), 0, -1):
        for perm in itertools.permutations(letters, length):
            word = ''.join(perm)
            if word in dictionary:
                with longest_word_lock:  
                    if len(word) > len(longest_word):
                        longest_word = word
            if time.time() - start_time > 50:
                return

def main():
    global longest_word
    dictionary = load_dictionary('recnik.txt')
    
    print("Унеси 12 слова, ћирилица!:")
    letters = input().strip()
    
    if len(letters) != 12:
        print("Треба 12 слова мајмуне!.")
        return
    
    start_time = time.time()
    
    thread1 = threading.Thread(target=find_longest_word_from_short_to_long, args=(letters, dictionary, start_time))
    thread2 = threading.Thread(target=find_longest_word_from_long_to_short, args=(letters, dictionary, start_time))
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    
    print(f"Најдужа реч: {longest_word}")
    print(f"Дужина речи: {len(longest_word)}")


if __name__ == "__main__":
    main()
