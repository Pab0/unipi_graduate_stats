## Extracting CS department graduate statistics from PDF announcements

I've been wondering for some time what the average time to graduate from my Bachelor's department (University of Piraeus, Department of Informatics) is. This information isn't published anywhere; however, the department's graduation announcements contain the IDs of the graduating students. Since the ID at the department is formatted as _"Π{year of enrollment}{3-digit serial number}"_, it should be possible to extract the enrollment year of the graduating students, and thus some crude statistics about average completion time of the Bachelor's.

This quickly became a big technical challenge, and the project evolved from curiosity about graduating statistics to interest in data extraction in general. Interestingly enough to warrant this write-up, at the very least. Read on, then, to share in my frustrations and triumphs, or skip to the end if you're just interested in the results.


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
