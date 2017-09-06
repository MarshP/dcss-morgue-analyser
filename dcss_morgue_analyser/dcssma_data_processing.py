import re
import shutil
import logging

log_format = "%(levelname)s - %(message)s - %(asctime)s - %(name)s"
logging.basicConfig(filename=".\\morgue-analyser.log",
                    level=logging.INFO,
                    format=log_format,
                    filemode='w')
logger = logging.getLogger(__name__)
logger.info('Import module.')
logger.info('Set logging level ' + logging.getLevelName(logger.getEffectiveLevel()) + ' in this module.')

def process_data(buffer, directory_path):
    logger.info('Start data processing functions.')
    with open((directory_path + '\\' + 'dcssma-analysis.txt'), 'w') as myfile:
        myfile.write("# DCSS Morgue Analyser Output #\n\n"
                     "Open this file in a markdown-enabled reader for a prettier experience. A .md copy is provided in the same directory.\n\n"
                     "**Note:** 'Average' means 'arithmetic mean' throughout.\n\n")
    progress_stats(buffer, directory_path)
    gold_stats(buffer, directory_path)
    shutil.copy((directory_path + '\\' + 'dcssma-analysis.txt'), (directory_path + '\\' + 'dcssma-analysis.md'))

# TODO What usually kills the characters, and how, and where?
# TODO unidentified items while i.d scrolls are available,
# TODO unused heal wounds pots at HP death,
# TODO under-used god abilities with high piety,
# TODO enchant armour/weaps scrolls gained early and unused
# TODO ...and other gameplay smells to be added
# TODO What is the progress on primary skills for the background and species, or the skills with best species aptitude?
# TODO Later convert all this to some NLP or parsing library made for the job

def progress_stats(buffer, directory_path):
    # TODO Docstrings throughout.
    count_games = 0
    xl_at_death_sum = 0
    xl_at_death_avg = 0
    branches_visited_sum = 0
    branches_visited_avg = 0
    lvls_seen_sum = 0
    lvls_seen_avg = 0
    main_dungeon_floors_sum = 0
    main_dungeon_floors_avg = 0
    runes_sum = 0
    runes_avg = 0
    three_runes_sum = 0
    three_runes_avg = 0

    count_games_regex = re.compile(r'(Began\sas\sa)')
    count_games_matches = re.findall(count_games_regex, buffer)
    # print(count_games_matches)
    # for match in count_games_matches:
    count_games += len(count_games_matches)

    xl_at_death_regex = re.compile(r'(Str:(\s*)(\d+)(.+)XL:(\s*)(\d+))')
    xl_at_death_matches = re.findall(xl_at_death_regex, buffer)
    logger.debug(xl_at_death_matches)
    for match in xl_at_death_matches:
        xl_at_death_sum += int(match[5])
    xl_at_death_avg = xl_at_death_sum / len(xl_at_death_matches)
    # print(xl_at_death_sum, xl_at_death_avg)

    main_dungeon_regex = re.compile(r'(Dungeon\s\((\d+)/(\d+)\))')
    main_dungeon_matches = re.findall(main_dungeon_regex, buffer)
    print(main_dungeon_matches)
    for match in main_dungeon_matches:
        main_dungeon_floors_sum += int(match[1])
    main_dungeon_floors_avg = main_dungeon_floors_sum / len(main_dungeon_matches)
    print(main_dungeon_floors_sum, main_dungeon_floors_avg)
    # FIXME Prints need to become logs

    branches_regex = re.compile(r'(visited\s(\d+)\sbranches)')
    branches_matches = re.findall(branches_regex, buffer)
    # print(branches_matches)
    for match in branches_matches:
        branches_visited_sum += int(match[1])
    branches_visited_avg = branches_visited_sum / len(branches_matches)
    # print(branches_visited_sum, branches_visited_avg)

    lvls_seen_regex = re.compile(r'(saw\s(\d+)\sof\sits\slevels)')
    lvls_seen_matches = re.findall(lvls_seen_regex, buffer)
    # print(lvls_seen_matches)
    for match in lvls_seen_matches:
        lvls_seen_sum += int(match[1])
    lvls_seen_avg = lvls_seen_sum / len(lvls_seen_matches)
    # print(lvls_seen_sum, lvls_seen_avg)

    runes_regex = re.compile(r'((\d+)/(\d+)\srunes:)')
    runes_matches = re.findall(runes_regex, buffer)
    print(runes_matches)
    for match in runes_matches:
        runes_sum += int(match[1])
    runes_avg = runes_sum / len(runes_matches)
    games_per_rune = count_games/len(runes_matches)
    print(len(runes_matches), runes_sum, runes_avg)

    three_runes_regex = re.compile(r'((3)/(\d+)\srunes:)')
    three_runes_matches = re.findall(three_runes_regex, buffer)
    print(three_runes_matches)
    for match in three_runes_matches:
        three_runes_sum += int(match[1])
    three_runes_avg = three_runes_sum / len(three_runes_matches)
    games_per_three_rune = count_games / len(three_runes_matches)
    print(len(three_runes_matches), three_runes_sum, three_runes_avg)

    with open((directory_path + '\\' + 'dcssma-analysis.txt'), 'a') as myfile:
        myfile.writelines(["## Progress ##\n\n",
                           "DCSSMA analysed " + str(
                               count_games) + " morgue files (completed games). Here is your **average** progress:\n\n",
                           "* Your average level (XL) at death was " + str(round(xl_at_death_avg, )) + "\n",
                           "  * For reference, characters can be expected to survive banishment to the abyss more often than not from around XL 15\n",
                           "  * For reference, in XP terms XL 22 is halfway to the maximum XL 27\n",
                           "* You reached " + str(
                               round(main_dungeon_floors_avg, )) + " floors of the main dungeon per game (out of 15)\n",
                           "* You explored " + str(round(branches_visited_avg, )) + " dungeon branches per game\n",
                           "* You explored " + str(round(
                               lvls_seen_avg, )) + " levels overall per game (main dungeon, vaults and branches)\n\n",
                           "### Runes ###\n\n",
                           "You obtained at least a single rune on " + str(
                               len(runes_matches)) + " ocassions; that's once every " + str(
                               round(games_per_rune, 1)) + " games.\n\n",
                           "You obtained three runes on " + str(
                               len(three_runes_matches)) + " ocassions; that's once every " + str(
                               round(games_per_three_rune, 1)) + " games.\n\n"])


def gold_stats(buffer, directory_path):
    gold_at_death_sum = 0
    gold_at_death_avg = 0
    gold_spent_sum = 0
    gold_spent_avg = 0
    gold_spent_pc = 0

    gold_at_death_regex = re.compile(r'(Gold:(\s+))(\d+)')
    gold_at_death_matches = re.findall(gold_at_death_regex, buffer)
    for match in gold_at_death_matches:
        gold_at_death_sum += int(match[2])
    gold_at_death_avg = gold_at_death_sum / len(gold_at_death_matches)

    gold_spent_regex = re.compile(r'(spent(\s+))(\d+)')
    gold_spent_matches = re.findall(gold_spent_regex, buffer)
    for match in gold_spent_matches:
        gold_spent_sum += int(match[2])
    gold_spent_avg = gold_spent_sum / len(gold_spent_matches)

    gold_spent_pc = (gold_spent_avg / (gold_spent_avg + gold_at_death_avg)) * 100

    with open((directory_path + '\\' + 'dcssma-analysis.txt'), 'a') as myfile:
        myfile.writelines(["## Gold ##\n\n",
                           "Gold only helps you win if you spend it.\n\n"
                           "* Avg. gold at death: " + str(round(gold_at_death_avg, )) + "\n",
                           "* Avg. gold spent: " + str(round(gold_spent_avg, )) + "\n",
                           "* You spent on average " + str(round(gold_spent_pc, )) + "% " +
                           "of the gold you collected.\n\n"])

