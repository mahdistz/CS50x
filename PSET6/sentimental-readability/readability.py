from cs50 import get_string


def calculate_coleman_liau(text):
    # Count the number of letters, words, and sentences in the text
    num_letters = sum(1 for char in text if char.isalpha())
    num_words = len(text.split())
    num_sentences = text.count(".") + text.count("!") + text.count("?")

    # Calculate the average number of letters per 100 words
    L = float(num_letters) / float(num_words) * 100

    # Calculate the average number of sentences per 100 words
    S = float(num_sentences) / float(num_words) * 100

    # Calculate the Coleman-Liau index
    coleman_liau_index = 0.0588 * L - 0.296 * S - 15.8

    # Round the index to the nearest integer
    grade_level = round(coleman_liau_index)

    # Return the calculated grade level
    return grade_level


def main():
    string = get_string("Text: ")
    grade_level = calculate_coleman_liau(string)

    if grade_level < 1:
        print("Before Grade 1")
    elif grade_level >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {grade_level}")


if __name__ == '__main__':
    main()
