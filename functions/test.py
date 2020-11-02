# file for testing 
from functions.textprocessing import TextProcessor

text = """Antibodies are a key part of our immune defences and stop the virus from getting inside the body's cells.
The Imperial College London team found the number of people testing positive for antibodies has fallen by 26% 
between June and September. They say immunity appears to be fading and there is a risk of catching the virus multiple
times. The news comes as figures from the Office for National Statistics show that the number of Covid-19 deaths in
the UK rose by 60% in the week of 16 October. More than 350,000 people in England have taken an antibody test as part
of the REACT-2 study so far. In the first round of testing, at the end of June and the beginning of July, about
60 in 1,000 people had detectable antibodies. But in the latest set of tests, in September, only 44 per 1,000
people were positive. It suggests the number of people with antibodies fell by more than a quarter between summer and autumn."""

processor = TextProcessor()
tokens = processor.create_tokens_from_text(text)
print(tokens)
tokens = processor.clean_tokens(tokens)
print(tokens)
key_words = processor.calculate_key_words(tokens, 5) 
print(key_words)
