# pyExamScan Usage Instructions

pyExamScan has several modules, all accessible from the main control window. Currently, the software is not packaged as an app, so it must be started from the terminal. If you followed the Installation instructions carefully, you can start the app as follows:

1. Open your terminal or command line (on mac, cmd-space to search, find "terminal" and open the app).
2. in Terminal, navigate to the folder you installed, 
    
    ```bash
    cd ~/Desktop/pyexamscan_v2
    ```
    
3. Run the program with 

    ```bash
    python pyExamScan_v2.py
    ```
    
4. That will open a control window to load files and run the scanner.

## Making your key
### Option 1 - fill in the bubbles:
1. Print out one of the answer sheets and fill it out as the key. Scan it with the exams as the first sheet in the stack **OR...**

### Option 2 - let the software fill in the bubbles:
1. Make a .csv file of your answers. You can do this in a spreadsheet or text editor. 
    + All answers go in one column without a header, each row is another question
    + to leave a row blank, enter IGNORE
    + Enter letters as capital letters, multiple answers not separated by spaces or commas. 
    + Export the file (or save as) and select .csv as your file format
    + For example, your table might look like
    
||
|:---|
|A|
|C|
|IGNORE|
|ABD|
|D|
|FD|

2. Launch pyExamScan using the instructions above
3. In the bottom panel, you can load the jpg of the blank answer sheet and select csv file you just created
    + If you have multiple versions of the test, enter the appropriate version letter (or leave it as A)
4. Click the Make Key button. In the folder containing your key, you will now see a new jpg file. The Last Name should be filled in as "KEY" and the first name as "A" or whatever you changed the version to, and all of the bubbles should be filled in appropriately!
5. Print this out for your records, and add it as the first page in your scan after you collect the student exams.

## Scanning bubbles  
Assuming have made a key by filling out an answer sheet by hand or the Key Maker function, and the students are done with their exam.  

1. Scan all of the students' answer sheets and the key, with the key as the first page, into a single pdf or a bunch of jpgs. I recommend at least 200 dpi, color, for the scanner settings. If you can't scan all at once, scan as jpgs because pdfs cannot be easily modified after being created
2. Make a folder on your computer containing nothing but the scanned file(s).
3. In the control window, click on the `Choose pdf of scans or jpg of key` button.
4. In the file selection window, select either the pdf, or the jpg of the key, and click Ok.
5. In the control window, enter the number of the last question you want graded.
6. If you used "select all that apply" questions, where the correct answer could be none to all of the possibilities, click the `Any select all that apply?` checkbox.
7. Click `Run Scan`, and wait for completion!

## Open ended questions  
If you want to include any fill in the blank kinds of questions, and you want to grade/mark them while scanning:
1. Modify the answer sheet as mentioned below.
2. Select the scans as mentioned above.
3. If the open ended question is in the middle of the exam (not stacked at the end), that set of bubbles needs to be "ignored" by the bubble scanner. Enter that question's number (or multiple numbers separated by commas) in the appropriate box in the control window.
4. Check the box for `any open ended questions to grade on the fly?`
4. Click `Run Scan`.
5. An image of the key will appear. 
    1. On that image, use the mouse to draw a box around the answer area for the first open ended question. 
    2. Draw boxes around the answer areas for other questions. At this time, there is no way to delete a drawn box! If you make an error, you have to close everything and start again.
    3. When you have drawn all of your boxes (one per open ended question), hit the `g` key. And the window will disappear.
6. After the bubbles have been scanned (a short wait), a small window will open for grading the open ended questions:
    1. The top of the window shows what was in the first box you drew on the key, and the bottom shows what was in the box on the first student's sheet.
    2. To award full credit, hit the 'c' key twice. The next student's answer should appear.
    3. To award half credit, hit the 'c' key then the 'x' key (or 'x' then 'c', it doesn't matter). The next student's answer should appear.
    4. To award no credit, hit the 'x' key twice. The next student's answer should appear.
    5. To go back a student (or to a previous question), hit the 'b' key as many times as needed. Note that this requires that you regrade everything you reload. For example, if you hit 'b' five times to back through the last five students, you have to repeat the grading on all of those five students for that answer.
    6. When you've graded the last question for the last student, the image window will close and the software will finish grading.
    
## Using select all that apply questions

If you check the `select all that apply questions` box on the control window, *all* questions will be graded as select all that apply. What does this mean for grading?:
+ Partial credit can be awarded for select all that apply questions. For example, if a question has 3 correct answers (A, B, and C), each correct answer is worth 1/3 points. If a student picks two correct (A, B), they get 0.66 points for that question. Each incorrect answer is penalized with the same fraction, so if a student put two correct on one incorrect answer (A, B, D), they get 0.66 - 0.33 = 0.33 points. If *n* is the number of correct answers, *c* is the number of correct answers selected by the student, and *i* is the number of incorrect answers, the points received by the student is calculated as *c(1/n)-i(1/n)*. Also note that that this value will not be less than zero.
+ If there is only one correct answer, though, it is effectively graded as a one-answer question. E.g., if the correct answer is A, and a student puts A *and* B, they get zero points. Each correct answer is 1/n, which is 1/1, or 1. Each incorrect answer is a penalty of 1/n, or 1/1, or 1. The student effectively gets 1 point for putting A, but is then penalized 1 point for putting B, so they get zero.

## Outputs and what they mean
The software outputs a number of files, some of which are essentially temporary files the software uses, and can be deleted if desired once you get the outputs. 
1. `results.csv` file (can open in a spreadsheet app) contains the grades, student answers, and basic statistics. The right most columns contain the points possible:
    + all questions are worth 1 point, including open ended questions
    + open ended question receiving a 'CX' will get 0.5 points.
    + the "score" column is the score without partial credit. "partialscore" includes all partial credit.
    + The bottom row displays how many students selected the correct answer.
    + if you have select all that apply questions, partial credit is awarded based on the number of correct answers on the key as mentioned above. 
2. The `resultsperquestion.csv`file is laid out similarly to the results file, but instead of student answers it displays the (partial) points received by each student for each question (for transparency of calculations)
3. The `marked.pdf` file contains all of the marked scans, including the key. This is for archival purposes. For the marking:
    + a green 'C' indicates a correct answer
    + a red 'X' indicates an incorrect answer
    + a red 'M' near a question number indicates that a correct answer was "missing" from the student's answers. This is important to mark for select-all-that-apply questions, and so only appears if that check box was selected (but then appears on questions that have only one correct answer). Students may get confused by the M. If there was one correct answer, and they didn't pick it, they will get a red X on their incorrect answer, and a red M because they missed the correct answer. On a select all that apply question, they could get green C's on correct answers, red X's on incorrect answers, and a red M if they didn't select all the correct answers...all on the same question!
4. The "marked" folder contains jpgs files (one per student, file name based on the student name and ID), each marked as in the pdf file above. These files are created to be electronically distributed to each student. I'm not sure what will happen if two students have the same name and no ID entered (I think the first file would be overwritten).
    + The best way I have found to electronically distribute marked exams: In Canvas, you should have an "assignment" where you are entering the exam grades. Open that assignment in SpeedGrader. For each student, find the comment box, under that you should have an option to attach a file, click that. Either click the "choose" button, or on a Mac drag the desired file from the finder onto that button (has to be on the button). You should then see the path to the file, and click attach. Move to the next student.
4. The "aligned" folder contains scans that have been corrected for skew. This are temporary files and can be deleted, or kept if you want to delete the original scans and have some unmarked sheets for future regrading.
5. If you loaded a pdf of answers, you will also see a bunch of jpgs in the main folder. With a pdf, the software saves out all of the images as separate files and then works on those. You can delete all of the jpgs if you want.

    
## Modifying the answer sheet
Included in the download folder is a folder called "images". This contains several things:
1. An Adobe Illustrator file for the answer sheet.
2. Pre-made pdfs of the answer sheet with various numbers of questions.

The scanning software depends on precise locations of bubbles and the three black circles (registration marks). So, you can modify by blocking questions off, but don't move anything around, and you can't add bubbles where they don't exist.  

### Some options:
All modification can be done in most pdf editors, without needing to use Illustrator
+ If I have a 50 question exam, I use the 60 question file. I leave the outlined box on the right, and just use a white box to cover up questions 51-60.
+ For open ended questions, put the number and a blank line in the answer box. To use the scanner to grade the open ended questions, the answers for all students must be in the same place!
+ If an open ended question occurs in the middle of an exam (say, \#14), make the answer blank in space on the right, but also cover up the bubbles for question 14. I draw a white box to cover the bubbles, then add a black arrow facing right. Don't forget to tell the scanner to "ignore" that question when you run the scans!
+ You can block out and overwrite anything at the top. E.g. you can cover up the Honor Pledge with a white box, then add a text box of anything else in that space. You can cover up all but the first four columns for the ID numbers and use assigned 4 digit IDS, or cover up the ID numbers all together.
+ In general, you (or the students) can make marks anywhere on the answer sheet as long as it doesn't interfere with the three big black registration marks, the four 'B' bubbles around the outside, or the bubbles for questions (unless those question numbers are listed as ignored, or after the max number of questions to grade).

### Other Scenarios
You can get creative with how to use this. For example, let's say you want to have the students draw and label a graph on the answer sheet in the box on the right. That might be difficult to grade with the open ended question grader, so you can score it manually, then grade it with the bubble grader. Let's say you had 20 multiple choice questions, but want to allow up to 10 points for the drawing. Instead of covering up questions 21-30 on the answer sheet leave them there. Make 21-30 all 'A' on your key. After you collect the answer sheets grade the graphs by hand. To award 10 points, *you* fill in 'A' for questions 21-30. To award 6 points, just fill in six A's. You may leave "wrong" answers blank. A rubric could be used to delineate that 21 is for labeling the x-axis, 22 for the y-axis, 23 for one curve, 24 for another, etc. Then scan the answer sheets and let the software do the math. 