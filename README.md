# DCSS Morgue Analyser
A Python program to analyse your [Dungeon Crawl Stone Soup](https://github.com/crawl/crawl) morgue folder, collate metrics, spot patterns and give hints.

**If you're here for a useful tool, best turn back now.** I'm doing this to help me learn Python; it won't be in any way useful for a long time. Then I'll remove this note.

## Plans for DCSSMA
DCSSMA will start life as a simple script which takes the morgue folder location as a command line arg. It will parse the morgue .txt files and use some pretty blunt regex work to produce some metrics and report them.

Later I hope to add more efficient data handling, more refined analysis, and maybe a gui or interactive file selection shell. Maybe some link to webtiles...

## Metrics
We want min, max and useful derived figures -- median, mean, SD and so forth -- for a variety of metrics. But we're guided by useful questions.

* How far does the player usually progress, in terms of dungeon exploration, time/turns played, XP/XL and skills?
* What usually kills the characters, and how, and where?
* Are there avoidable issues? Including:
  * unidentified items while i.d scrolls are available, 
  * unused heal wounds pots at HP death, 
  * under-used god abilities with high piety, 
  * unspent gold
  * enchant armour/weaps scrolls gained early and unused
  * ...and other gameplay smells to be added
* What is the progress on primary skills for the background and species, or the skills with best species aptitude?

And how does all that differ when the player plays different species, backgrounds and classes of background like warrior, zealot or mage?



