import argparse
import operator
from os import listdir, remove, path
from os.path import isfile, join
from enum import Enum
import dcss_data


class DeathStats:
    MorguePath = ''

    Verbose = True

    MorgueFiles = []

    stats = []

    def __init__(self, morguepath):
        """
        Constructor
        :param morguepath: Path to crawl morgue files (ex: C:\dcss\morgue )
        """
        self.MorguePath = morguepath
        MorgueFiles = []
        for f in listdir(self.MorguePath):
            if (isfile(join(self.MorguePath, f)) and (f[:6] == "morgue") and (f[-3:] == "txt")):
                self.MorgueFiles.append(f)

    def Analyze(self):

        """
        Analyze morgue files in :MorguePath and fill :stats
        """
        self.stats = []

        for morgue in self.MorgueFiles:
            print(morgue)
            with open(join(self.MorguePath, morgue)) as file:
                content = file.readlines()

            stat = self.getInformation(content)
            stat['filename'] = morgue
            self.stats.append(stat)

    def getNumberOfGame(self):
        return len(self.stats)

    def getFilteredStatChar(self, character):
        filtstat = []
        for s in self.stats:
            sb = s['species'] + ' ' + s['background']
            if sb == character:
                filtstat.append(s)
        return filtstat

    def getCharacterList(self):

        list_char = []
        for s in self.stats:
            sb = s['species'] + ' ' + s['background']
            if sb not in list_char:
                list_char.append(sb)

        return list_char

    def getStatBasic(self, param, stat=None):
        if stat is None:
            stat = self.stats
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
            return (sorted_simplestat[1] + " (" + simplestat[sorted_simplestat[1]] + " times)")

    def getBestGame(self, stat=None):
        if stat is None:
            stat = self.stats
        bestgame = {'score': 0}
        for s in stat:
            if s['score'] > bestgame['score']:
                bestgame = s
        return (bestgame['score'])

    def getInformation(self, morgue):
        stat = {}
        line = 0
        stat['version'] = self.getVersion(morgue[line])

        # Score & main stats
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
        if (curline.startswith('Was')):
            if (curline.find('Was an') > -1):
                stat['religion_rank'] = curline[curline.find('Was an') + 6: curline.find(' of ')]
            elif (curline.find('Was the') > -1):
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

        if (morgue[line + 1].strip().startswith("... invoked")):
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
                while (linetab[1] != "by"):
                    del linetab[1]

            if (linetab[0].startswith('...')):
                stat['death_cause'] = 'Not Dead'
            else:
                if (linetab[1] == "by" or linetab[1] == "to"):
                    if (linetab[2] == "a" or linetab[2] == "an"):
                        stat['death_cause'] = ' '.join(linetab[3:])
                    else:
                        stat['death_cause'] = ' '.join(linetab[2:])
                if (stat['death_cause'].find('\'s ghost') > -1):
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

        if (stat['dungeon'].endswith('.')):
            stat['dungeon'] = stat['dungeon'][:-1]
        stat['dun+lev'] = stat['dungeon'] + ":" + stat['dungeon_level']
        # Game duration
        line = 4
        while (not morgue[line].strip().startswith('The game lasted')):
            line = line + 1

        linetab = morgue[line].strip().split(' ')
        stat['duration'] = linetab[3]
        stat["turns"] = linetab[4][1:]

        return stat

    @staticmethod
    def getVersion(line):
        # Dungeon Crawl Stone Soup version 0.18.1 (tiles) character file.
        idxv = line.find('version ') + 8
        idxc = line.find(' character')
        return (line[idxv:idxc])


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
        lcstat = deathstats.getFilteredStatChar(lc)
        write_file("-" * 50)
        write_file("Statistic for : {}".format(lc))
        write_file("Number of games played : {}".format(len(lcstat)))
        write_file("Killed most by : {}".format(deathstats.getStatBasic("death_cause", lcstat)))
        write_file("Killed most in : {}".format(deathstats.getStatBasic("dun+lev", lcstat)))
        write_file("Best game : {}".format(deathstats.getBestGame(lcstat)))


def main():
    """
    Main function (heh :)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, help="DCSS path", default=path.dirname(path.abspath(__file__)))
    args = parser.parse_args()

    CRAWL_PATH = args.path
    MORGUE_PATH = join(CRAWL_PATH, 'morgue')

    if isfile(OUTPUTFILE):
        remove(OUTPUTFILE)

    ds = DeathStats(MORGUE_PATH)

    ds.Analyze()

    write_file("-" * 50)
    write_file("Number of games played : {}".format(ds.getNumberOfGame()))
    write_file("-" * 50)
    write_file("Killed most by : {}".format(ds.getStatBasic("death_cause")))
    write_file("Killed most in : {}".format(ds.getStatBasic("dun+lev")))
    write_file("Best game : {}".format(ds.getBestGame()))
    write_file("-" * 50)

    list_character = ds.getCharacterList()
    write_percharacter_stats(ds, list_character)


if __name__ == "__main__":
    main()
