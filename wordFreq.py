import wordfreq

def get_top_2000_five_letter_words():
    word_list = wordfreq.top_n_list('en', 50000)  # Assuming we start with a large list
    real = []
    f = open("beep/case.txt", "r")
    for x in f:
        var = x.split(' ', 1)[0]
        if var.isalnum():
            if len(var) == 5:
                real.append(var)
    print(real)
    five_letter_words = [word.upper() for word in word_list if len(word) == 5 and word.isalnum() and word.upper() in real][:2000]
    return five_letter_words

def write_to_file(words, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for word in words:
            file.write(word + '\n')

def main():
    top_2000_five_letter_words = get_top_2000_five_letter_words()
    file_path = 'top2000.txt'
    write_to_file(top_2000_five_letter_words, file_path)
    print(f"Top 2000 five-letter English words written to '{file_path}'.")
def check():
    f = open("beep/case.txt", "r")
    real = []
    for x in f:
        var = x.split(' ', 1)[0]
        if var.isalnum():
            if len(var) == 5:
                real.append(var)

    with open("trys.txt", 'r') as file:
        numbers = [float(line.strip()) for line in file]
        total = sum(numbers)
        arg =total / len(numbers)
        print(arg)
    f = open("beep/case.txt", "r")



if __name__ == "__main__":
    main()

if __name__ == "__main__":
    check()