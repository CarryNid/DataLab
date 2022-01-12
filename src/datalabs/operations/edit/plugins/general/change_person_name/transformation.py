import numpy as np
import spacy
from checklist.perturb import Perturb
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from edit.editing import *

@editing(name = "change_person_name", contributor = "xl_augmenter",
         task = "Any", description="this function is used to ")
def change_person_name(text:str, max_outputs = 1):

    spacy_nlp = spacy.load("en_core_web_sm")
    perturbed = Perturb.perturb(
        [spacy_nlp(text)], Perturb.change_names, nsamples=1)

    # print(perturbed.data)
    perturbed_texts = (
        perturbed.data[0][1: max_outputs+1]
        if len(perturbed.data) > 0
        else [text]
    )
    return perturbed_texts

# sentence = "Andrew finally returned the French book to Chris that I bought last week"
# perturbed = change_person_name(text=sentence)
# print(perturbed)