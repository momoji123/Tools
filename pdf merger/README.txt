cover file: File will be merged at first page of every merge result files
pattern: Pattern to seperate unrelevant filename with part of file name to be used as key

example:

SOURCE FILES:
- cover.pdf
- filename PATTERN 01.pdf
- filename PATTERN 02.pdf
- filename_2 PATTERN 01.pdf
- filename_2 PATTERN 02.pdf

INPUT:
- cover file: cover.pdf
- pattern: PATTERN

result files:
1.pdf --> merge: 
	- cover.pdf
	- filename PATTERN 01.pdf
	- filename_2 PATTERN 01.pdf 
2.pdf --> merge: 
	- cover.pdf
	- filename PATTERN 02.pdf
	- filename_2 PATTERN 02.pdf