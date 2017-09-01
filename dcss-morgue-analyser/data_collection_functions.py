import re

def get_gold_stats(buffer):
    # GOLD_COUNT
    gold_total = 0
    GoldCountRegex = re.compile(r'(Gold:(\s+))(\d+)')
    gold_match = GoldCountRegex.search(buffer)
    print('Gold amount: ' + gold_match.group(3))
    gold_total += int(gold_match.group(3))
    print(gold_total)
    # do someting meaningful later
    # ANOTHER_THING
    ##AnotherCountRegex = re.compile(r'Gold:(\s+)\d+')
    ##another_match = AnotherCountRegex.search(buffer)
    ##print('Another amount: ' + another_match.group())
    # do someting meaningful later





def collect_data(buffer):
    get_gold_stats(buffer)