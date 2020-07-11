DESKTOP = True
import project4
import urllib2
import math
import random
import matplotlib.pyplot as plt

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"


###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict


def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)

    # read in files as string
    words = word_file.read()

    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list

# Question 1
"""
human_eyeless_protein = read_protein(HUMAN_EYELESS_URL)
fruit_fly_eyeless_protein = read_protein(FRUITFLY_EYELESS_URL)
PAM50_scoring_matrix = read_scoring_matrix(PAM50_URL)

#human_fruit_fly_alignment_matrix = project4.compute_alignment_matrix(human_eyeless_protein, fruit_fly_eyeless_protein, PAM50_scoring_matrix, False)

#print project4.compute_local_alignment(human_eyeless_protein, fruit_fly_eyeless_protein, PAM50_scoring_matrix, human_fruit_fly_alignment_matrix)

# score = 875
# local alignment for Human Eyeless Protein: 'HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEK-QQ'
# local alignment for Fruit Fly Eyeless Protein: 'HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ')

# Question 2
consensus_pax_domain = read_protein(CONSENSUS_PAX_URL)
# comparing with Human Eyeless Protetin
human_eyeless_protein = 'HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEKQQ'
human_pax_alignment_matrix = project4.compute_alignment_matrix(human_eyeless_protein, consensus_pax_domain, PAM50_scoring_matrix, True)
human_pax_alignment = project4.compute_global_alignment(human_eyeless_protein, consensus_pax_domain, PAM50_scoring_matrix, human_pax_alignment_matrix)
number_of_corresponding_elements = 0
for idx in range(len(human_pax_alignment[1])):
    if(human_pax_alignment[1][idx] == human_pax_alignment[2][idx]):
        number_of_corresponding_elements += 1
print float(number_of_corresponding_elements)/float(len(human_pax_alignment[1])) * 100
# similarity = 72.9323308271%
# comparing with fruit fly eyeless protein
fruit_fly_eyeless_protein = 'HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ'
ff_pax_alignment_matrix = project4.compute_alignment_matrix(fruit_fly_eyeless_protein, consensus_pax_domain, PAM50_scoring_matrix, True)
ff_pax_alignment = project4.compute_global_alignment(fruit_fly_eyeless_protein, consensus_pax_domain, PAM50_scoring_matrix, ff_pax_alignment_matrix)
number_of_corresponding_elements = 0
for idx in range(len(ff_pax_alignment[1])):
    if(ff_pax_alignment[1][idx] == ff_pax_alignment[2][idx]):
        number_of_corresponding_elements += 1
print float(number_of_corresponding_elements)/float(len(ff_pax_alignment[1])) * 100
# similarity = 70.1492537313%

# Question 3
# No, not at all. The similarity/agreement percentages are both around 70%, which is extremely unlikely if generated randomly.
# There are 23 possible characters not including the dashes, so a random generation would produce a far lower agreement
# percentage.
"""

# Question 4
def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    Takes as input two sequences seq_x and seq_y, a scoring matrix scoring_matrix, and a number of trials num_trials.
    This function should return a dictionary scoring_distribution that represents an un-normalized distribution generated
    by performing the following process num_trials times
    """
    scoring_distribution = dict()
    scores = dict()
    for idx in range(num_trials):
        print idx
        rand_y = ''.join(random.sample(seq_y, len(seq_y)))
        alignment_matrix = project4.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        score = project4.compute_local_alignment(seq_x, rand_y, scoring_matrix, alignment_matrix)[0]
        if score not in scoring_distribution:
            scoring_distribution[score] = 1
        else:
            scoring_distribution[score] += 1
        scores[idx] = score
    return scoring_distribution, scores


def normalize_distribution(distribution):
    count = sum(distribution.values())
    return_value = dict()
    for key in distribution.keys():
        return_value[key] = float(distribution[key]) / float(count)
    return return_value
"""
un_normalized, scores = generate_null_distribution(human_eyeless_protein, fruit_fly_eyeless_protein, PAM50_scoring_matrix, 1000)
normalized = normalize_distribution(un_normalized)

line1 = plt.bar(normalized.keys(), normalized.values())
plt.legend()
plt.xlabel('Scores')
plt.ylabel('Fraction of Trials')
plt.title('Distribution of hypothesis testing over 100 trials')
plt.show()
"""

# Question 5
#mean = float(sum(scores.values())) / 1000.0

def compute_standard_deviation(mean, scores):
    return_value = 0.0
    for score in scores:
        return_value += math.pow((score - mean), 2)
    return_value = return_value / float(len(scores))
    return_value = math.sqrt(return_value)
    return return_value

#standard_deviation = compute_standard_deviation(mean, scores.values())

#print "this is the mean " + str(mean)
#print "this is the standard deviation " + str(standard_deviation)
#print "this is the z score " + str((875.0 - mean) / standard_deviation)
# this is the mean 52.309
# this is the standard deviation 7.28351007413
# this is the z score 112.952545081

# Question 6
# The distribution of the hypothesis testing is roughly bell shaped meaning it aligns pretty well with a
# normal distribution. Since the value of the local alignment between the fruit fly and human eyeless
# genes is more than 10 standard deviations away from the mean, it makes it extremely unlikely.
# Winning the lottery is around one in a trillion, but the chances of this score being random is
# less than that probably by a factor of 50. I found this by looking up standard deviation confidence
# intervals online

# Question 7
# diag_score is 2,
# off_diag_score is 1,
# dash_score is 0

# Question 8
#word_list = read_words(WORD_LIST_URL)

def check_spelling(checked_word, dist, word_list):
    return_value = list()
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']

    score_matrix = project4.build_scoring_matrix(alphabet, 2, 1, 0)

    for word in word_list:
        alignment_matrix = project4.compute_alignment_matrix(word, checked_word, score_matrix, True)
        global_alignment = project4.compute_global_alignment(word, checked_word, score_matrix, alignment_matrix)
        distance = len(word)+len(checked_word)-global_alignment[0]
        if(distance <= dist):
            return_value.append(word)

    return return_value

#print check_spelling("humble", 1, word_list)
#print check_spelling("firefly", 2, word_list)

# ['bumble', 'fumble', 'humble', 'humbled', 'humbler', 'humbles', 'humbly', 'jumble', 'mumble', 'rumble', 'tumble']
# ['direly', 'finely', 'fireclay', 'firefly', 'firmly', 'firstly', 'fixedly', 'freely', 'liefly', 'refly', 'tiredly']

