from app.db.number_map import number_map, number_units

class NumberToEnglishTransformer(object):
    """Transforms a number to its written english equivalent following the process
        1. Reformat integer number as a comma-formatted string, (e.g. 123456 --> "123,456")
        2. Split the string found in step 1 on each comma to create a list of strings (e.g. "123,456" --> ["123","456"])
        3. Iterate through the list found in step 2, on each iteration:
            3a. Map the leftmost number (e.g. ["123","456"] --> "one hundred twenty three")
            3b. Map the leftmost number's units (e.g. ["123","456"] --> "thousand")
            3c. Combine & return outputs from 3a and 3b (e.g. "one hundred twenty three thousand")
        4. Combine the iterative outputs of step 3 (e.g. "one hundred twenty three thousand" + "four hundred fifty six")
    """

    def __init__(self):
        super().__init__()

    def cleanup_response(self, number_in_english:str) -> str:
        """Cleans up response

        Args:
            number_in_english (str): The API response
        Returns:
            number_in_english (str): The cleaned number in english
        """
        if 'zero  ' in number_in_english and number_in_english != 'zero  ':
            number_in_english = number_in_english.replace('zero  ', '')
        return number_in_english
    
    def combine_remaining(self, formatted_number:str, comma_split_ct:int) -> str:
        """Combines the remaining number-split-on-commas (e.g. combines "000" and "000" in ex. "100,000,000" --> ["100","000","000"])

        Args:
            formatted_number: The number to be converted into english
            comma_split_ct: The current comma_split_ct
        """
        combined_number = ''
        for n in formatted_number.split(',')[comma_split_ct:]:
            combined_number += n
        return combined_number
    
    def reformat_remaining_with_commas(self, formatted_number:str, comma_split_ct:int) -> str:
        """Preprocesses the remaining units in the number-split-on-commas into a standard comma formatted string (e.g. "1,234,567" --> "234,567")

        Args:
            formatted_number (int): The number to be converted into english
            comma_split_ct (int): The current iteration while looping through the number-split-on-commas (e.g. ["100","000","000"] iterating from 0-2 because length==3)
        """
        number_remaining = int(self.combine_remaining(formatted_number, comma_split_ct))
        return self.reformat_with_commas(number_remaining)

    def map_english_units(self, formatted_number_remaining:str) -> str:
        """Maps the English units of the number to the left of the leftmost comma
            (e.g. hundreds, thousands, millions, billions, etc...)
        Args:
            formatted_number_remaining: The number formatted as str with commas
        Returns:
            mapped_english_units: English units of the number to the left of the leftmost comma in formatted_number_remaining
        """
        units = ''
        split_num = formatted_number_remaining.split(',')
        for n in [x for x in split_num if x != split_num[0]]:
            units += n
        mapped_english_units = number_units[len(units)]
        return mapped_english_units

    def map_english_number(self, formatted_number_remaining:str) -> str:
        """Maps the English number to the left of the leftmost comma
            (e.g. hundreds, thousands, millions, billions, etc...)
        Args:
            formatted_number_remaining: The number formatted as str with commas
        Returns:
            mapped_english_units: English units of the number to the left of the leftmost comma in formatted_number_remaining
        """
        mapped_english_units = self.map_english_units(formatted_number_remaining)
        mapped_english_number = number_map[formatted_number_remaining.split(',')[0]]
        mapped_english_number = mapped_english_number + ' ' + mapped_english_units
        return mapped_english_number

    def reformat_with_commas(self, number:int) -> str:
        """Preprocesses the number into a standard comma formatted string (e.g. 1000 --> "1,000")
        """
        return '{:,}'.format(number)

    def transform(self, payload:int) -> str:
        """Main transformation logic

        Args:
            payload (int): The number to be converted into english
        Returns:
            number_in_english (str): The transformed number in english
        """
        number_in_english = ''

        try:
            payload = int(payload.number)
        except:
            try:
                payload = int(payload['number'])
            except:
                raise ValueError(payload)

        formatted_number = self.reformat_with_commas(payload)
        comma_iterations = range(len(formatted_number.split(',')))
        for comma_split_ct in comma_iterations:
            formatted_number_remaining = self.reformat_remaining_with_commas(formatted_number, comma_split_ct)
            number_in_english += self.map_english_number(formatted_number_remaining) + ' '
        return self.cleanup_response(number_in_english)