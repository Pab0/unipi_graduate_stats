## Extracting CS department graduate statistics from PDF announcements

I've been wondering for some time what the average time to graduate from my Bachelor's department (University of Piraeus, Department of Informatics) is. This information isn't published anywhere; however, the department's graduation announcements contain the IDs of the graduating students. Since the ID at the department is formatted as _"Π{year of enrollment}{3-digit serial number}"_, it should be possible to extract the enrollment year of the graduating students, and thus some crude statistics about average completion time of the Bachelor's.

This quickly became a big technical challenge, and the project evolved from curiosity about graduating statistics to interest in data extraction in general. Interestingly enough to warrant this write-up, at the very least. Read on, then, to share in my frustrations and triumphs, or skip to the end if you're just interested in the results.

_Note: While the write-up will be in English, the data will be in Greek (before we get to strictly numerical data, that is). This shouldn't make any difference code-wise though, so you can ignore the few Greek occurences below and in the code._

### Problems

There were two main problems:

#### 1. Data absence
The announcements archive only goes back to 2015, so a lot of data before that is lost. This means that naturally, older student generations will only have their longer-studying students in the announcements, skewing the data. On the other hand though, newer generations haven't had time yet to reach a longer study period, which skews data in the opposite direction.

Given that the number of students per year is very roughly similar, and (naively) assuming that the distribution of students over years studying is about the same, those two factors should balance each other out to a degree. Of course, the only cohorts with moderately accurate results will the ones from ~2011 to ~2013 so far (given that this is a 4-year degree), with older generations missing their large head and younger generations missing their long tail.

#### 2. Data is locked in unwieldy formats
The data is theoretically out there, but very hard to access. Some of the reasons are:
- **Problem 1**: The graduation announcements are posted on the website, mixed with all of the department's other announcements.
- **Problem 2**: Additionally, both Bachelor's and Master's graduations are announced, with no obvious way to filter for either.
- **Problem 3**: Even for Bachelor's graduation announcements, not all of them include the list of graduating students, some just contain general information about the venue etc.
- **Problem 4**: The announcement's content isn't posted on the website itself, but in linked documents. What is more, those documents are different file-types (.doc, .docx or .pdf), even if they have a similar content.
- **Problem 5**: The list of students is a table from a Word template, which means that is split over multiple pages, with inconsistent layout and line-wrapping where the cell's content exceeds the cell's width (a common occurence with Greek names).

Yet despite all those problems, there is also one advantage: The template mentioned above is consistent. The files types generated might be different, but the template that generated the initial Word content has stayed the same. This one consistency will be the anchor that helps us overcome most of the above problems.

### Solution

We will be using a number of tools/languages, trying to stick with the best tool for each job (and naturally, choosing from among the small pool that I'm familiar with; I'm certain more efficient ways for many of these steps). It will all be duct-taped together via the main [Bash script](https://github.com/Pab0/unipi_graduate_stats/blob/master/unipi_grades.sh).

#### Problem 1: All Announcements are posted together on the website

(_script: [get_docs.py](https://github.com/Pab0/unipi_graduate_stats/blob/master/get_docs.py)_)

Okay, this one is easy. The department's [website](http://www.cs.unipi.gr/) thankfully includes a search function. Searching for _"ορκωμοσία" ("graduation")_ ought to return everything related, and then some. We can download the results page with Python's `requests` package, and parse it with Python's [BeautifulSoup](https://code.launchpad.net/beautifulsoup/) package. We can then look over all links, navigate to each page and download the attached file, where available (it turns out it is always available for the announcements we're interested in).

We now have a collection of 40+ .doc, .docx anc .pdf documents about various announcements. Manually opening some of the announcements we're interested in, we notice that they indeed share the same text template.


#### Problem 4: Documents are in different formats

(_script: [Bash script, paragraph #2](https://github.com/Pab0/unipi_graduate_stats/blob/master/unipi_grades.sh#L9)_)

Having a separate workflow for each data-type is not very efficient, so let's tackle Problem 4 first: Let's convert everything into the same format. The one that is most easy to convert to from all three is PDF. This is done easily with LibreOffce, which we can call headless-ly (ie. no need to boot up the whole suite, we'll just use their writer `lowriter`).

We now have a bunch of PDF files, but it's time to actually look at the contents.


#### Problems 2&3: Only some announcements are for the Bachelor's graduation, and not all of those include the students' list

(_script: [Bash script, paragraphs #3 & #4](https://github.com/Pab0/unipi_graduate_stats/blob/master/unipi_grades.sh#L30)_)

We've noticed that the files we want (lists of Bachelor's graduates) all (and only those) use the same template, so if we can extract the text from the PDF, searching for the pattern is straight-forward. There are many tools available for that, and while some of them will butcher the table, we only care about the text template in the beginning at this point. The command-line package `pdf2txt` is good enough for that, so we do a regular `grep` over its output and remove any PDF files that don't match.

While we're at it, let's extract the year of graduation from the template (another straight-forward `grep`) and set the file's title to this.

We're left with only the PDF files we want, with each of them including a few paragraphs of rich text and the list (that's the part we're actually interested in, we can forget the text prelude from now on).

#### Problem 5: Extract list data from PDF

(_script: [pdf_to_csv.py](https://github.com/Pab0/unipi_graduate_stats/blob/master/pdf_to_csv.py)_)

Unfortunately, the Word template messes with the layout of the table, which results in `pdf2txt` butchering the order of rows. Same with `pdftotext`, even including the `-layout` option (in newer versions a `-table` option is available, this was not included in my distribution's offered version though). We'll have to turn to something more powerful then - and [camelot](https://github.com/camelot-dev/camelot) is designed for exactly this: Extracting tabular data from PDFs. It not only looks at the PDF data, but also uses computer vision to ensure it isn't thrown off by weird layouts.

Sure enough, this did the job. The extracted tables can easily be exported to [pandas](https://github.com/pandas-dev/pandas), which is very handy when working with tables. After some moderate table operations, we write the result into a .csv file.

For the first time, our data is stored in a code-friendly format. A note to data maintainers/publishers: Publishing the data (also) in such formats helps save a _lot_ of time to other people; with a 2-click "Export to CSV" this write-up would've just started here.


### Results
