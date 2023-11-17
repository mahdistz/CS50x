from cs50 import get_int


def luhn_algorithm(card_number):
    """
    Implements Luhn's Algorithm to validate a credit card number.
    Returns True if the card number is valid, False otherwise.
    """
    card_number = str(card_number)
    card_number = card_number.replace(" ", "")  # Remove any spaces
    if not card_number.isdigit():  # Check if the number contains only digits
        return False

    # Step 1: Double the value of every second digit from the right
    doubled_digits_sum = 0
    for i in range(len(card_number) - 2, -1, -2):
        digit = int(card_number[i])
        doubled_digit = digit * 2
        if doubled_digit > 9:
            doubled_digit = (
                    doubled_digit - 9
            )  # Subtract 9 from doubled digit if it's greater than 9
        doubled_digits_sum += doubled_digit

    # Step 2: Add the digits together
    total_sum = doubled_digits_sum + sum(int(digit) for digit in card_number[-1::-2])

    # Step 3: Check if the sum is divisible by 10
    return total_sum % 10 == 0


def check_card_type(card_number):
    """
    return type of credit card: AmericanExpress or MasterCard or Visa
    """
    card_number = str(card_number)

    if len(card_number) == 15 and (
            card_number.startswith("34") or card_number.startswith("37")
    ):
        return "AmericanExpress"
    elif len(card_number) == 16 and card_number[:2] in ["51", "52", "53", "54", "55"]:
        return "MasterCard"
    elif (len(card_number) == 13 or len(card_number) == 16) and card_number[0] == "4":
        return "Visa"
    else:
        return None


def main():
    while True:
        card_number = get_int("Number: ")
        if card_number >= 0:
            break

    if len(str(card_number)) not in [13, 15, 16]:
        print("INVALID")

    elif luhn_algorithm(card_number):
        if check_card_type(card_number) == "AmericanExpress":
            print("AMEX")
        elif check_card_type(card_number) == "MasterCard":
            print("MASTERCARD")
        elif check_card_type(card_number) == "Visa":
            print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")


if __name__ == '__main__':
    main()
