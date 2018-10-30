from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import Tkinter
import ttk

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
introQuestionImport = []
questionImport = []
SPREADSHEET_ID = '14A7zY6u4FhIJ1Y9R8gCHlO3svMcfscemPb4vYyzX4xw'
INTRO_QUESTIONS_RANGE_NAME = 'IntroQuestions'
QUESTIONS_RANGE_NAME = 'Questions'
ANSWER_TYPES = ["TextField", "Picker"]
def main():
    
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    store = file.Storage('token.json')
    creds = store.get()
    print("Checking Credentials")
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    global service
    
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=INTRO_QUESTIONS_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
      #  data = values
        print('Name, Major:')
        i = 0
        for row in values:
            if i != 0: {introQuestionImport.append(row)}
            i+=1

    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 range = QUESTIONS_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
      #  data = values
        print('Name, Major:')
        i = 0
        for row in values:
            if i != 0: {questionImport.append(row)}
            i+=1

    print(questionImport)
if __name__ == '__main__':
    main()

class GUI():
    def __init__(self, master):
        self.master = master
        self.master.title = ("Data Collection")

        self.notebook = ttk.Notebook(master)

        # INTRO QUESTION #
        self.introQuestionFrame = Tkinter.Frame()
        
        # INTRO QUESTION - DATA FRAME #
        self.introQuestionDataFrame = Tkinter.Frame(self.introQuestionFrame)

        # INTRO QUESTION - DATA FRAME - QUESTION FRAME #
        self.introQuestionQuestionFrame = Tkinter.Frame(self.introQuestionDataFrame)
        introQuestionsIndex = 0
        print(introQuestionImport)
        for x in introQuestionImport:
            self.question = Tkinter.Label(self.introQuestionQuestionFrame, text = introQuestionImport[introQuestionsIndex][0])
            introQuestionsIndex+=1
            self.question.pack()

        self.introQuestionQuestionFrame.grid(row = 0, column = 0)

        # INTRO QUESTION - DATA FRAME - ANSWERTYPE FRAME
        self.introQuestionAnswerFrame = Tkinter.Frame(self.introQuestionDataFrame)
        self.answerType = Tkinter.Label(self.introQuestionAnswerFrame, text = "HELP")
        introAnswersIndex = 0
        self.introAnswerLabels = []
        for x in introQuestionImport:
            self.answer = Tkinter.Label(self.introQuestionAnswerFrame, text = introQuestionImport[introAnswersIndex][1])
            self.answer.grid(row=introAnswersIndex, column=0)
            self.introAnswerLabels.append(self.answer)
            self.answer.bind("<Enter>", self.on_enter)
            self.answer.bind("<Leave>", self.on_leave)
            introAnswersIndex+=1
        self.answerType.grid(row = 0, column=1)

        self.introQuestionAnswerFrame.grid(row=0, column=1)
        self.introQuestionDataFrame.grid(row = 0, column=0)

        # INTRO QUESTION - ADD FRAME #
        self.answerTypeMenuLabel = Tkinter.StringVar(master)
        self.answerTypeMenuLabel.set(ANSWER_TYPES[0])
        self.introQuestionAddFrame = Tkinter.Frame(self.introQuestionFrame)
        self.addQuestionLabel = Tkinter.Label(self.introQuestionAddFrame, text = "Add Question: ")
        self.addQuestionEntry = Tkinter.Entry(self.introQuestionAddFrame)
        self.addAnswerTypeLabel = Tkinter.Label(self.introQuestionAddFrame, text = "Select Answer Type")
        self.addAnswerTypeDrop = Tkinter.OptionMenu(self.introQuestionAddFrame, self.answerTypeMenuLabel, *ANSWER_TYPES)
        self.addQuestionButton = Tkinter.Button(self.introQuestionAddFrame, text = "Add", command = self.AddIntroQuestion)
        self.addQuestionLabel.grid(row = 0, column = 0)
        self.addAnswerTypeLabel.grid(row = 0, column = 1)
        self.addQuestionEntry.grid(row = 1, column = 0)
        self.addAnswerTypeDrop.grid(row = 1, column = 1)
        self.addQuestionButton.grid(row = 2, column = 1)

        self.introQuestionAddFrame.grid(row = 1, column = 0)

        ## QUESTION ##
        self.questionFrame = Tkinter.Frame()
        self.questionList = Tkinter.Listbox(self.questionFrame, width = 50)
        for x in questionImport:
            self.questionList.insert(Tkinter.END, x[0])
        self.questionList.pack()
        self.notebook.add(self.introQuestionFrame, text = "Intro Questions")
        self.notebook.add(self.questionFrame, text = "Test Questions")
        
        self.notebook.pack()

    def AddIntroQuestion(self):
        introQuestionExport = [self.addQuestionEntry.get(), self.answerTypeMenuLabel.get()]
        body = {
            "majorDimension":"ROWS",
            "values": [introQuestionExport]
        }
        exporter = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, 
                                                                range=INTRO_QUESTIONS_RANGE_NAME, 
                                                                valueInputOption="RAW", 
                                                                body=body)
        exporter.execute()

    def on_enter(self, event):
        for x in self.introAnswerLabels:
            if x == event.widget: 
                for y in introQuestionImport:
                    if y[0] == x.cget("text"):
                     self.answerType.configure(text = x[1])
                    else: self.answerType.configure(text = "none")

    def on_leave(self, event):
        self.answerType.configure(text = "N/A")

    

root = Tkinter.Tk()
my_gui = GUI(root)
root.mainloop()

