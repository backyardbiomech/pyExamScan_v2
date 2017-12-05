from fpdf import FPDF
import sys

from dicts import Dicts
from settings import Settings
from image import Image
import init_functions
import scan_functions
import df_functions


class Scanner(object):
    '''
    Scanner is the main class that contains scanner settings from the GUI,
    lists of image files,
    aligment matrices,
    grade sheet file names,
    and panda data tables for grading
    '''
    def __init__(self, input_file, quests, markmissing, openQ, ignores):
        '''
        retrieve values from the gui (or call from command line)
        input_file is path to key jpg or pdf of all scans
        quests is an integer as the number of questions to grade
        markmissing is a boolean - True if select all that apply, False if not
        openQ is a boolean - True if there are any open ended questions to grade on screen
        ignnores is a comma separated string of numbers of questions to not scan (for open ended Q's)
        '''
        self.input_file = input_file
        self.quests = quests
        self.markmissing = markmissing
        self.openQ = openQ
        if len(ignores)>0:
            ignores=ignores+','
            self.ignores=list(ast.literal_eval(ignores))
        else:
            self.ignores=None
        self.scan_settings=Settings()
        # initialize file and pathnames (and split pdfs into jpgs)
        self.path, self.image_list = init_functions.filenames(input_file)
        # intialize the output pdf which the scanner object will write to
        self.outpdf=FPDF('P','pt','Letter')
        # initialize the pandas dataframe to contain results
        self.resdf = init_functions.makeResDf(quests, len(self.image_list))
        # make the dictionaries containing scanning coordinates
        self.qAreas, self.idAreas, self.nAreas = init_functions.makeAreaDict(quests)
        # make the dictionaries to convert coordinates to letters or numbers
        self.Ndict, self.Idict, self.Qdict = init_functions.makeResDict()
        # Start the scanner
        self.rundots()
        #print('here')
        # run the open questions grader
#         if self.openQ:
#             self.runopenQ():
        
    def rundots(self):
        # the main loop for loading images for alignment and dot scanning
        for i in range(len(self.image_list)):
            # create image object, which will load and align image
            img = Image(self.image_list[i], self.scan_settings)
            print('Processing scan {0:1d}'.format(i))
            # scan the aligned image and return a dict of all markers for the image
            self.qRes = scan_functions.scanDots(img.scanimg, self.qAreas, self.ignores, self.Qdict)
            self.idRes = scan_functions.scanDots(img.scanimg, self.idAreas, self.ignores, self.Idict)
            self.nRes = scan_functions.scanDots(img.scanimg, self.nAreas, self.ignores, self.Ndict)
            # if this is the key image, save the results to keyDict
            if i == 0:
                self.keyDict = self.qRes.copy()
            # parse the name and id
            lastName, firstName, studentID = df_functions.getid(self.idRes, self.nRes)
            self.qRes['LastName'] = lastName
            self.qRes['FirstName'] = firstName
            self.qRes['studentID'] = studentID
            # save data to data frame
            for k, v in self.qRes.items():
                self.resdf.loc[i,k]=v
            #save the aligned image for later marking
            scan_functions.saveimg(self.image_list, i, img.scanimg)

        # test write resdf to csv
        fname = self.path + 'results.csv'
        print(fname)
        self.resdf.to_csv(fname, index=True, index_label = 'index')
        sys.exit()

