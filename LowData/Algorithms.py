class dictionary_dimension_conversion():
    def __init__(self, dictionary=None):
        self.dictionary = dictionary

    def dict_conversion(self):
        new_dict = {}
        if self.dictionary == None:
            print("Invalid Dictionary Entry")
            return 
        for key, val in self.dictionary.items():
            summation = sum(list(val.values()))
            new_dict[key] = summation
        return new_dict

    def dict_total(self):
        dictionary = self.dict_conversion()
        return sum(list(dictionary.values()))
    



if __name__ == "__main__":
    dictionary = {"Dresses": {"I hate this product": 889, "I love this product": 1, "I recommend this product to my friends": 449, "I do not recommend this product to my friends": 1345, "The quality of this product is very bad": 1, "The quality of this product is very good": 709, "I waste a lot of money purchasing this product": 1, "The design is very good": 1, "I hate the design of this product": 545, "Do not try this ": 621, "I am very unhappy about this product": 76, "I am very happy about this product": 1, "The style is very good": 116, "I like the color": 94, "excellent design": 295}, "Jackets": {"The quality of this product is very bad": 904, "Do not try this ": 700, "The quality of this product is very good": 444, "I like the color": 432, "I do not recommend this product to my friends": 504, "I recommend this product to my friends": 676}, "Jeans": {"I am very unhappy about this product": 453, "I waste a lot of money purchasing this product": 414, "I do not recommend this product to my friends": 1624, "I hate this product": 520, "Do not try this ": 588, "The quality of this product is very good": 954, "I like the color": 723, "I recommend this product to my friends": 1089}, "Shirts & Tops": {"The quality of this product is very bad": 346, "I hate this product": 730, "Do not try this ": 945, "The quality of this product is very good": 685, "I like the color": 537, "I do not recommend this product to my friends": 720, "I recommend this product to my friends": 896}, "Shorts": {"I do not recommend this product to my friends": 341, "I love this product": 451, "The quality of this product is very bad": 264, "Do not try this ": 489, "The quality of this product is very good": 332, "I like the color": 304, "I recommend this product to my friends": 420}, "Sweaters": {"I hate this product": 528, "Do not try this ": 428, "The quality of this product is very good": 260, "I do not recommend this product to my friends": 473, "I recommend this product to my friends": 228}}
    test = dictionary_dimension_conversion(dictionary)
    test.dict_conversion()
    test.dict_total()
