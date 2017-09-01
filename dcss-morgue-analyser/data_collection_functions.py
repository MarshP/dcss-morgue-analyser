import re

def collect_data(buffer, directory_path):
    with open((directory_path + '\\' + 'dcssma-analysis.txt'), 'w') as myfile:
        myfile.write("# DCSS Morgue Analyser Output #\n\n"
                     "**Note:** 'Average' means 'arithmetic mean' throughout.\n\n")
    get_gold_stats(buffer, directory_path)

# TODO How far does the player usually progress, in terms of dungeon exploration, time/turns played, XP/XL and skills?
# TODO What usually kills the characters, and how, and where?
# TODO Are there avoidable issues? Including:
    # TODO unidentified items while i.d scrolls are available,
    # TODO unused heal wounds pots at HP death,
    # TODO under-used god abilities with high piety,
    # TODO unspent gold
    # TODO enchant armour/weaps scrolls gained early and unused
# TODO ...and other gameplay smells to be added
# TODO What is the progress on primary skills for the background and species, or the skills with best species aptitude?
# TODO Later convert all this to some NLP or parsing library made for the job



def get_gold_stats(buffer, directory_path):
    gold_at_death_sum = 0
    gold_at_death_avg = 0
    gold_spent_sum = 0
    gold_spent_avg = 0
    gold_spent_pc = 0

    gold_at_death_regex = re.compile(r'(Gold:(\s+))(\d+)')
    gold_at_death_matches = re.findall(gold_at_death_regex, buffer)
    for match in gold_at_death_matches:
        gold_at_death_sum += int(match[2])
    gold_at_death_avg = gold_at_death_sum/len(gold_at_death_matches)

    gold_spent_regex = re.compile(r'(spent(\s+))(\d+)')
    gold_spent_matches = re.findall(gold_spent_regex, buffer)
    for match in gold_spent_matches:
        gold_spent_sum += int(match[2])
    gold_spent_avg = gold_spent_sum/len(gold_spent_matches)

    gold_spent_pc = (gold_spent_avg/(gold_spent_avg+gold_at_death_avg))*100
    print("At death ",gold_at_death_sum, gold_at_death_avg)
    print("Spent ", gold_spent_sum, gold_spent_avg)
    print("%.0f" % gold_spent_pc+"%")

    with open((directory_path + '\\' + 'dcssma-analysis.txt'), 'a') as myfile:
        myfile.writelines(["## Gold ##\n\n",
                           "Avg. gold at death: " + str(gold_at_death_avg)+"\n",
                           "Avg. gold spent: " + str(gold_spent_avg) + "\n\n"
                           "Gold only helps you win if you spend it.\nYou spent on average "+ str(round(gold_spent_pc,))+"% "+
                           "of the gold you collected.\n\n"])

                     # "Avg. gold spent: ", gold_spent_avg, "\n")
                     # "Gold only helps you win if you spend it. You spent on average ", gold_spent_pc, "%"
                     # "of the gold you collect. You cannott take it with you.\n")
                     #


    # do someting meaningful later
    # ANOTHER_THING
    ##AnotherCountRegex = re.compile(r'Gold:(\s+)\d+')
    ##another_match = AnotherCountRegex.search(buffer)
    ##print('Another amount: ' + another_match.group())
    # do someting meaningful later





