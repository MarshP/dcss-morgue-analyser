## DCSS Morgue Analyser 

A Python program to analyse your [Dungeon Crawl Stone Soup](https://github.com/crawl/crawl) morgue folder, collate metrics, spot patterns and give hints.

* **Version:** 0.1 'mucking about with python'
* **Release date:** tba
* **Maintainer:** MarshP (marshp.vcs@gmail)

**This tool is in pre-pre-nascent-alpha** I'm doing this to help me learn Python, though other contributions may make it somewhat useful.

### Documentation

This readme contains only a quickstart, but that should be enough for most users. 

More detailed user docs are on the [project documentation pages](https://marshp.github.io/dcss-morgue-analyser/)

Contributor docs and discussions are in the [project wiki](https://github.com/MarshP/dcss-morgue-analyser/wiki).

### Quick start

1. Ensure Python 3 [(download)](https://www.python.org/downloads/) is installed
2. Copy the `.py` files in the `dcss_morgue_analyser/` directory to your DCSS `crawl/morgue/` directory
  * On Windows look in `%AppData%` for the crawl directory
  * If you intend to analyse a subset of your morgue, such as characters of one species/profession, copy those files to a new directory and use that in place of the morgue
3. In the morgue directory open a shell or command prompt: `$ Python ./morgue-analyser.py`
4. Look for an output file called `dcssma-analysis.txt`. This will look prettier if opened in a mardown-enabled reader.

#### Issues and sugestions ####

If you spot something, [raise an issue](https://github.com/MarshP/dcss-morgue-analyser/issues/new) or -- as you can almost certainly code better than I can -- fork and fix. :0)
### Plans for DCSSMA

DCSSMA will start life as a simple script which takes the morgue folder location as a command line arg. It will parse the morgue .txt files and use some pretty blunt regex work to produce some metrics and report them.

Later I hope to add more efficient data handling, more refined analysis, and maybe a gui or interactive file selection shell. Maybe some link to webtiles...

#### Metrics

The plan is for min, max and useful derived figures -- median, mean, SD and so forth -- for a variety of metrics. But we're guided by useful questions.

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

### Copyright and License

No copyright claimed on top of whatever arises naturally from publishing the repo contents in any given jurisdiction .

License is [WTFPL](https://en.wikipedia.org/wiki/WTFPL).
