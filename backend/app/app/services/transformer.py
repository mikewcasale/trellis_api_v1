from app.db.number_map import number_map, number_units

class NumberToEnglishTransformer(object):
    """Transforms a number to its written english equivalent
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
    
    def combine_remaining(self, number:str, iter_split:int) -> str:
        """Combines the remaining units in the number-split-on-commas (e.g. combines "000" and "000" in ex. "100,000,000" --> ["100","000","000"])

        Args:
            number: The number to be converted into english
            iter_split: The current iteration while looping through the number-split-on-commas (e.g. ["100","000","000"] iterating from 0-2 because length==3)
        """
        combined_number = ''
        for n in number.split(',')[iter_split:]:
            combined_number += n
        return combined_number
    
    def preprocess_remaining(self, number:str, iter_split:int) -> str:
        """Preprocesses the remaining units in the number-split-on-commas into a standard comma formatted string (e.g. "1,234,567" --> "234,567")

        Args:
            number (int): The number to be converted into english
            iter_split (int): The current iteration while looping through the number-split-on-commas (e.g. ["100","000","000"] iterating from 0-2 because length==3)
        """
        return self.preprocess_number(int(self.combine_remaining(number, iter_split)))

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

    def preprocess_number(self, number:int) -> str:
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
            raise ValueError(payload)

        formatted_number = self.preprocess_number(payload)
        for iter_split in range(len(formatted_number.split(','))):
            formatted_number_remaining = self.preprocess_remaining(formatted_number, iter_split)
            number_in_english += self.map_english_number(formatted_number_remaining) + ' '
        return self.cleanup_response(number_in_english)