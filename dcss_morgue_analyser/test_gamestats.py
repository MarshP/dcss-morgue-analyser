import csv
from os import  remove, path
from enum import Enum
from os.path import isfile, join
import argparse
from configuration import Configuration
from game_stats import GameStats,StatColumn

###############
# MAIN Stuff
################

class OutputType(Enum):
    Console = 1
    File = 2


# TODO manage program output type
Output = OutputType.Console
OutputFile = r'game_stats.txt'


def write_file(data):
    """
    this function write data to file
    :param data:
    :return:
    """
    # TODO manage program output type
    file_name = OutputFile
    with open(file_name, 'a') as x_file:
        x_file.write(data + "\n")


def write_percharacter_stats(gamestats, list_character):
    for lc in list_character:
        lcstat = gamestats.get_filtered_stat(lc)
        write_file("-" * 50)
        write_file("Statistic for : {}".format(lc))
        write_file("Number of games played : {}".format(gamestats.get_number_of_game(lcstat)))
        sorted_simplestat = gamestats.get_stat_basic(StatColumn.death_cause, lcstat)
        s = "\n"
        for k in sorted_simplestat:
            s = s + "{} ({} times)\n".format(k[0], k[1])
        write_file("Killed most by : {}".format(s))

        sorted_simplestat = gamestats.get_stat_basic(StatColumn.dun_lev, lcstat)
        s = "\n"
        for k in sorted_simplestat:
            s = s + "{} ({} times)\n".format(k[0], k[1])
        write_file("Killed most in : {}".format(s))

        write_file("Best game : {}".format(gamestats.get_best_game(lcstat)))
        write_file("Average Score : {}".format(gamestats.get_averagescore(lcstat)))



def main():
    """
    Main function (heh :)
    """

    configuration = Configuration()

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, help="DCSS path", default=path.dirname(path.abspath(__file__)))
    args = parser.parse_args()

    crawl_path = args.path
    configuration.morgue_path = join(crawl_path, 'morgue')

    if isfile(OutputFile):
        remove(OutputFile)

    gamestats = GameStats(configuration)

    gamestats.analyze()

    write_file("-" * 50)
    write_file("Number of games played : {}".format(gamestats.get_number_of_game()))
    write_file("-" * 50)

    stat = gamestats.get_stat_basic(StatColumn.death_cause)
    s = "\n"
    for k in stat:
        s = s + "{} ({} times)\n".format(k[0], k[1])
    write_file("Killed most by : {}".format(s))

    stat = gamestats.get_stat_basic(StatColumn.dun_lev)

    s = "\n"
    for k in stat:
        s = s + "{} ({} times)\n".format(k[0], k[1])
    write_file("Killed most in : {}".format(s))

    write_file("Best game : {}".format(gamestats.get_best_game()))
    write_file("Average Score : {}".format(gamestats.get_averagescore()))
    write_file("-" * 50)

    list_character = gamestats.get_character_list()
    write_percharacter_stats(gamestats, list_character)

    scorevol = gamestats.get_scoreevolution(type='day')

    with open('scorevol.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Date","Score"])
        writer.writerows(scorevol)



if __name__ == "__main__":
    main()
