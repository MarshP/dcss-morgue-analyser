import argparse
import operator
from enum import Enum
from os import listdir, remove, path
from os.path import isfile, join


class DeathStats:
    """
    Class that parses morgue folder and generate a stat structure
    that can be interrogated through get... methods
    """

    MorguePath = ''

    Verbose = True

    MorgueFiles = []

    """
    Example of line in Stats :
    {'dungeon': 'Dungeon',
    'background': 'Ice Elementalist',
    'name': 'Awutz',
    'hp': '30',
    'surname': 'the Chiller',
    'duration': '00:11:56',
    'dun+lev': 'Dungeon:1',
    'level': '4',
    'turns': '2120',
    'god': 'None',
    'religion_rank': 'None',
    'filename': 'morgue-Awutz-20160912-104224.txt',
    'species': 'Merfolk',
    'version': '0.18.1 (tiles)',
    'death_cause': 'giant frog',
    'dungeon_level': '1',
    'score': 63}
    """

    Stats = []

    def __init__(self, morguepath):
        """
        Constructor
        :param morguepath: Path to crawl morgue files (ex: C:\dcss\morgue )
        """
        self.MorguePath = morguepath
        self.MorgueFiles = []
        for f in listdir(self.MorguePath):
            if isfile(join(self.MorguePath, f)) and f[:6] == "morgue" and f[-3:] == "txt":
                self.MorgueFiles.append(f)

    def analyze(self):

        """
        Analyze morgue files in :MorguePath and fill :Stats
        """
        self.Stats = []

        for morgue in self.MorgueFiles:
            print(morgue)
            with open(join(self.MorguePath, morgue)) as file:
                content = file.readlines()

            stat = self.get_information(content)
            stat['filename'] = morgue
            self.Stats.append(stat)

    def get_number_of_game(self, stat=None):
        """
        :return: the number of game played in global or param stat structure
        """
        if stat is None:
            stat = self.Stats

        return len(stat)

    def get_filtered_stat(self, character):
        """
        returns a stat structure filtered for character
        :param character: the character (race+job) to filter
        :return: stat structure
        """
        filtstat = []
        for s in self.Stats:
            sb = s['species'] + ' ' + s['background']
            if sb == character:
                filtstat.append(s)
        return filtstat

    def get_character_list(self):

        list_char = []
        for s in self.Stats:
            sb = s['species'] + ' ' + s['background']
            if sb not in list_char:
                list_char.append(sb)

        return list_char

    def get_stat_basic(self, param, stat=None):
        if stat is None:
            stat = self.Stats
        simplestat = {}
        for s in stat:
            if s[param] in simplestat:
                simplestat[s[param]] += 1
            else:
                simplestat[s[param]] = 1
        sorted_simplestat = sorted(simplestat.items(), key=operator.itemgetter(1), reverse=True)
        if self.Verbose:
            s = "\n"
            for k in sorted_simplestat:
                s = s + "{} ({} times)\n".format(k[0], simplestat[k[0]])
            return s
        else:
            return sorted_simplestat[1] + " (" + simplestat[sorted_simplestat[1]] + " times)"

    def get_best_game(self, stat=None):
        if stat is None:
            stat = self.Stats
        bestgame = {'score': 0}
        for s in stat:
            if s['score'] > bestgame['score']:
                bestgame = s
        return bestgame['score']

    def get_averagescore(self,stat=None):
        if stat is None:
            stat = self.Stats
        avg = 0.0
        if len(stat)==0:
            return 0
        for s in stat:
            avg=avg+s['score']
        return int(avg/len(stat))

    def get_information(self, morgue):
        stat = {}
        line = 0
        stat['version'] = self.get_version(morgue[line])

        # Score & main Stats
        # example string :
        # 64 Olivier the Skirmisher (level 3, -1/34 HPs)
        line = line + 2
        curline = morgue[line]
        stat['score'] = int(curline[:curline.find(' ')])
        stat['name'] = curline[curline.find(' ') + 1:curline.find('the') - 1]
        stat['surname'] = curline[curline.find('the '):curline.find('(') - 1]
        stat['level'] = curline[curline.find('level ') + 6:curline.find(',')]
        stat['hp'] = curline[curline.find('/') + 1:curline.find('HP') - 1]

        # Race & Background
        # example string :
        # Began as a Minotaur Berserker on Aug 19, 2016.
        line = line + 1
        curline = morgue[line]
        linetab = curline.strip().split(' ')
        stat['species'] = linetab[3]
        stat['background'] = linetab[4]
        if len(linetab) > 9:
            stat['background'] = stat['background'] + ' ' + linetab[5]

        # Find religion
        line = line + 1
        curline = morgue[line].strip()
        if curline.startswith('Was'):
            if curline.find('Was an') > -1:
                stat['religion_rank'] = curline[curline.find('Was an') + 6: curline.find(' of ')]
            elif curline.find('Was the') > -1:
                stat['religion_rank'] = curline[curline.find('Was the') + 6: curline.find(' of ')]
            else:
                stat['religion_rank'] = curline[curline.find('Was a') + 6: curline.find(' of ')]

            stat['god'] = curline[curline.find(' of ') + 4:curline.find('.')]
        else:
            stat['religion_rank'] = 'None'
            stat['god'] = 'None'
            line = line - 1

        # Cause of death
        line = line + 1
        curline = morgue[line]

        if morgue[line + 1].strip().startswith("... invoked"):
            linetab = morgue[line + 1].strip().split(' ')
            stat['death_cause'] = ' '.join(linetab[4:])
        else:
            # write_file(curline)
            linetab = curline.strip().split(' ')
            if linetab[len(linetab) - 1].endswith(")"):
                del linetab[len(linetab) - 1]
                del linetab[len(linetab) - 1]

            if linetab[2] == "afar":
                del linetab[1]
                del linetab[1]

            if linetab[1] == "with":
                while linetab[1] != "by":
                    del linetab[1]

            if linetab[0].startswith('...'):
                stat['death_cause'] = 'Not Dead'
            else:
                if linetab[1] == "by" or linetab[1] == "to":
                    if linetab[2] == "a" or linetab[2] == "an":
                        stat['death_cause'] = ' '.join(linetab[3:])
                    else:
                        stat['death_cause'] = ' '.join(linetab[2:])
                if stat['death_cause'].find('\'s ghost') > -1:
                    stat['death_cause'] = "Player" + stat['death_cause'][stat['death_cause'].find('\'s ghost'):]

        # dungeon & level
        while not (morgue[line].strip().startswith('... on level') or morgue[line].strip().startswith('... in a')):
            line = line + 1

        linetab = morgue[line].strip().split(' ')
        if len(linetab) > 4:
            stat['dungeon_level'] = linetab[3]
            stat['dungeon'] = linetab[6]
        else:
            stat['dungeon'] = linetab[3]
            stat['dungeon_level'] = '(/na)'

        if stat['dungeon'].endswith('.'):
            stat['dungeon'] = stat['dungeon'][:-1]
        stat['dun+lev'] = stat['dungeon'] + ":" + stat['dungeon_level']
        # Game duration
        line = 4
        while not morgue[line].strip().startswith('The game lasted'):
            line = line + 1

        linetab = morgue[line].strip().split(' ')
        stat['duration'] = linetab[3]
        stat["turns"] = linetab[4][1:]

        return stat

    @staticmethod
    def get_version(line):
        # Dungeon Crawl Stone Soup version 0.18.1 (tiles) character file.
        idxv = line.find('version ') + 8
        idxc = line.find(' character')
        return line[idxv:idxc]


###############
# MAIN Stuff
################

class OutputType(Enum):
    Console = 1
    File = 2


# TODO manage output type
Output = OutputType.Console
OUTPUTFILE = r'death_stats.txt'


def write_file(data):
    """
    this function write data to file
    :param data:
    :return:
    """
    # TODO manage output type
    file_name = OUTPUTFILE
    with open(file_name, 'a') as x_file:
        x_file.write(data + "\n")


def write_percharacter_stats(deathstats, list_character):
    for lc in list_character:
        lcstat = deathstats.get_filtered_stat(lc)
        write_file("-" * 50)
        write_file("Statistic for : {}".format(lc))
        write_file("Number of games played : {}".format(deathstats.get_number_of_game(lcstat)))
        write_file("Killed most by : {}".format(deathstats.get_stat_basic("death_cause", lcstat)))
        write_file("Killed most in : {}".format(deathstats.get_stat_basic("dun+lev", lcstat)))
        write_file("Best game : {}".format(deathstats.get_best_game(lcstat)))
        write_file("Average Score : {}".format(deathstats.get_averagescore(lcstat)))


def main():
    """
    Main function (heh :)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, help="DCSS path", default=path.dirname(path.abspath(__file__)))
    args = parser.parse_args()

    crawl_path = args.path
    morgue_path = join(crawl_path, 'morgue')

    if isfile(OUTPUTFILE):
        remove(OUTPUTFILE)

    ds = DeathStats(morgue_path)

    ds.analyze()

    write_file("-" * 50)
    write_file("Number of games played : {}".format(ds.get_number_of_game()))
    write_file("-" * 50)
    write_file("Killed most by : {}".format(ds.get_stat_basic("death_cause")))
    write_file("Killed most in : {}".format(ds.get_stat_basic("dun+lev")))
    write_file("Best game : {}".format(ds.get_best_game()))
    write_file("Average Score : {}".format(ds.get_averagescore()))
    write_file("-" * 50)

    list_character = ds.get_character_list()
    write_percharacter_stats(ds, list_character)


if __name__ == "__main__":
    main()
