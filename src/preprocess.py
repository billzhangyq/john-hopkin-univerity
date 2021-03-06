#!/usr/bin/env python3

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Synopsis: converts the {train,test}.json files to a vector list
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import csv
from random import shuffle, choice, gauss, random
from collections import namedtuple

Patient = namedtuple('Patient', ['age', 'gender', 'face', 'arm', 'leg',
    'dysphasia', 'hemianopia', 'visuospatial', 'cerebellar', 'aspirin',
    'carotid', 'thromb', 'stroke_14', 'haem_14', 'pulm_14'])
# noncebheam is major non-cerebral haemoraging
# thromb is thrombolosis

# reads the data from the filename and returns the input data and the correct
# labels
# @param n: how many more patients to have in the final output
def open_data(filename, n=0):
    patients = [] # patient vectors
    patients_survived = []

    # generate the named tuples
    # the file is in Latin-1, not UTF-8
    with open(filename, 'r', encoding='latin-1') as patients_file:
        # we ignore the first line because it defines the headers, not a
        # patient
        patients_file.__next__() # intentionally ignored

        for patient in csv.reader(patients_file):
            patients.append([
                int(patient[4]),
                int(patient[3] == 'Female'), # 0 for male, 1 for female
                int(patient[12] == 'yes'),
                int(patient[13] == 'yes'),
                int(patient[14] == 'yes'),
                int(patient[15] == 'yes'),
                int(patient[16] == 'yes'),
                int(patient[17] == 'yes'),
                int(patient[18] == 'yes'),
                int(patient[25] == 'true'),
                int(patient[41] == 'yes'),
                int(patient[42] == 'yes'),
                int(patient[106] == 'true'),
                int(patient[107] == 'true'),
                int(patient[108] == 'true'),
                ])
            patients_survived.append(int(patient[93] == 'false'))

    data = list(zip(patients, patients_survived))
    shuffle(data)

    if len(data) > n:
        data = data[n:]

    while len(data) < n:
        patient, survived = choice(data)[:] # don't change the original
        patient[0] *= gauss(1, 0.01) # randomly slightly change their age

        prob_switching = 0.05
        for i in range(1, len(patient)):
            if random() < prob_switching:
                patient[i] = 1 - patient[i]
        data.append((patient, survived))

    return list(zip(*data))
