
from psychopy import gui
        
def show_gui():

    myDlg = gui.Dlg(title="Search & Match Task")
    myDlg.addText('Participant Info')
    myDlg.addText('')
    myDlg.addField('ID:', 1)
    myDlg.addField('Age:', 00)
    myDlg.addField('Gender:', choices=["Female", "Male", "Other"])
    myDlg.addField('Handedness:', choices=["Right", "Left", "Ambidexter"])

    myDlg.addText('')
    myDlg.addText('Task Settings')
    myDlg.addText('')
    myDlg.addField('Color Schemes:', choices=["Discriminable Color Palette", "Color-blind friendly Palette"])
    # For the color trials, each square had one of the eight highly discriminable colors
    myDlg.addField('Difficulty Levels:', choices=["Short", "Medium", "Long"])
    myDlg.addField('Parallel Version:', choices=["A", "B"])
    myDlg.addField('Level Order:', choices=["Random Order", "Order in file"])
    myDlg.addField('Repetitions per Level:', 1)
    myDlg.addField('Match presentation time (seconds) :', 0.5)
    
    ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
    if myDlg.OK:  # or if ok_data is not None
        return ok_data

    else:
        print('user cancelled')
        return ok_data
