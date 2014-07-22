#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8 (standalone edition) on Sat Jul 19 12:08:25 2014
#

import wx
import wx.grid

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

import codecs
import operator


class MyNGram:
    
    cutlist = "<>/:：;；,、＂’，.。！？｢\"\'\\\n\r《》“”!@#$%^&*()「」『』—–©®™¶…‘’“”﹁﹂﹃﹄︻︼‹›․‧﹛﹜﹝﹞﹟﹠﹡﹤﹥︽︾︿﹀｢｣～".decode("utf-8")  

    def cutSentence(self, text_path, keywords): ##放入原始文章路徑, 增加斷詞的list
        text = codecs.open(text_path,"r","utf-8")   #開檔
        sentence = ""
        textList = []
           
        for line in text.readlines():
            line = line.strip() ##清除空白
            
            for keyword in keywords:  #清除關鍵字
                line = "".join(line.split(keyword))
                
            for word in line:
                if word not in self.cutlist: #如果文字不是標點符號，就把字加到句子中
                    sentence += word
                    #print sentence
                else:
                    textList.append(sentence) #如果遇到標點符號，把句子加到 text list中
                    sentence = ""
                    #print textList
        return textList#傳回一個文字陣列

    def ngram(self, textLists,n,minFreq): #第一個參數放處理好的文章(LIST檔，utf-8編碼)，第二個參數放字詞的長度單位，第三個參數放至少要幾次以上
     
        words=[]     #存放擷取出來的字詞
        words_freq={}#存放字詞:計算個數 
        result= []
        for textList in textLists:
            for w in range(len(textList)-(n-1)): #要讀取的長度隨字詞長度改變
                words.append(textList[w:w+n])    #抓取長度w-(n-1)的字串

        for word in words:
            if word not in words_freq:               #如果這個字詞還沒有被放在字典檔中
                words_freq[word] = words.count(word) #就開一個新的字詞，裡面放入字詞計算的頻次
     
        words_freq = sorted(words_freq.iteritems(),key=operator.itemgetter(1),reverse=True) #change words_freq from dict to list 
        
        for word in words_freq:
            if word[1] >= minFreq:
                result.append(word)
                
        return result ##回傳一個陣列[詞,頻次]

    def longTermPriority(self, path, maxTermLength, minFreq):
        self.longTerms=[]          #長詞
        self.longTermsFreq=[]      #長詞+次數分配
        print "def longTermPriority",path 
        
        for i in range(maxTermLength,1,-1): ##字詞數由大至小
            print "in for loop", path
            text_list = self.cutSentence(path,self.longTerms)  #呼叫cutSentence function
            #print len(text_list)
            words_freq = self.ngram(text_list,i, minFreq) #呼叫 ngram function
            #print i

        
            for word_freq in words_freq:
                self.longTerms.append(word_freq[0])  #將跑出來的長詞加入 longTerms list 做為下次切割檔案的基礎
                #print word_freq[0]
                self.longTermsFreq.append(word_freq) #將長詞和次數加入另外一個list  分成兩個檔儲存的用意是減少迴圈次數
                #print word_freq
        
    def GetTermsFreq(self):
        return self.longTermsFreq
 

    

class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):

        for file in filenames:
            self.window.Clear()
            self.window.WriteText(file)
            #print filePath
           

class MyNotebook(wx.Notebook):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyNotebook.__init__
        kwds["style"] = 0
        wx.Notebook.__init__(self, *args, **kwds)
        self.notebook_2_pane_1 = wx.Panel(self, wx.ID_ANY)
        self.text_FileName = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, _("File Name"))
        self.text_ctrl_DropTarget = wx.TextCtrl(self.notebook_2_pane_1, wx.ID_ANY, _("Drop .txt file here"), style=wx.TE_READONLY)
        self.text_MaxStringLength = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, _("Max String\nLength"))
        self.combo_box_MaxStringLength = wx.ComboBox(self.notebook_2_pane_1, wx.ID_ANY, choices=[_("2"), _("3"), _("4"), _("5(recommand)"), _("6"), _("7"), _("8"), _("9"), _("10")], style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY)
        self.text_MinStringFreq = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, _("Min Terms\nFreq"))
        self.combo_box_MinStringFreq = wx.ComboBox(self.notebook_2_pane_1, wx.ID_ANY, choices=[_("2"), _("3(recommand)"), _("4"), _("5"), _("6"), _("7"), _("8"), _("9"), _("10")], style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY)
        self.text_colID = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, _("which col\n(for Excel file)"),size=(0,0))
        self.text_ctrl_ColID = wx.TextCtrl(self.notebook_2_pane_1, wx.ID_ANY, _("Enter \"Col ID\"!"),size=(0,0))
        self.text_MaxList = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, _("Max Result List"),size=(0,0))
        self.text_ctrl_MaxListLength = wx.TextCtrl(self.notebook_2_pane_1, wx.ID_ANY, _("Enter a \"NUM\"!"),size=(0,0))
        self.button_Confirm = wx.Button(self.notebook_2_pane_1, wx.ID_ANY, _("Confirm"))
        self.button_Clear = wx.Button(self.notebook_2_pane_1, wx.ID_ANY, _("Clear"),size=(0,0))
        self.label_ResultPreview = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, _("\nResult Previw\n"))
        self.grid_Result = wx.grid.Grid(self.notebook_2_pane_1, wx.ID_ANY, size=(1, 1))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

        # make the text control be a drop target
        dt = MyFileDropTarget(self.text_ctrl_DropTarget)
        self.text_ctrl_DropTarget.SetDropTarget(dt)

        # Bind function on button
        self.Bind(wx.EVT_BUTTON, self.OnConfirm, self.button_Confirm)

    def __set_properties(self):
        # begin wxGlade: MyNotebook.__set_properties
        self.AddPage(self.notebook_2_pane_1, _("Main"))
        self.text_FileName.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.text_ctrl_DropTarget.SetToolTipString(_("only accept .txt file"))
        self.text_MaxStringLength.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.combo_box_MaxStringLength.SetToolTipString(_("max string length for N-GRAM "))
        self.combo_box_MaxStringLength.SetSelection(3)
        self.text_MinStringFreq.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.combo_box_MinStringFreq.SetToolTipString(_("minimum frequency of the terms"))
        self.combo_box_MinStringFreq.SetSelection(1)
        self.text_colID.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.text_ctrl_ColID.SetToolTipString(_("Enter the Excel Col ID in \"English\""))
        self.text_MaxList.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.text_ctrl_MaxListLength.SetToolTipString(_("limit amount of the result"))
        self.button_Confirm.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.button_Confirm.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.button_Clear.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.label_ResultPreview.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.grid_Result.CreateGrid(0, 2)
        self.grid_Result.EnableEditing(0)
        self.grid_Result.SetColLabelValue(0, _("Terms"))
        self.grid_Result.SetColLabelValue(1, _("Freq"))
        self.grid_Result.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyNotebook.__do_layout
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1.Add(self.text_FileName, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((10, 20), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_DropTarget, 2, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_4.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        grid_sizer_2.Add(self.text_MaxStringLength, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_2.Add((10, 20), 2, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_2.Add(self.combo_box_MaxStringLength, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_4.Add(grid_sizer_2, 1, wx.EXPAND, 0)
        grid_sizer_3.Add(self.text_MinStringFreq, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_3.Add((10, 20), 2, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_3.Add(self.combo_box_MinStringFreq, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_4.Add(grid_sizer_3, 1, wx.EXPAND, 0)
        grid_sizer_4.Add(self.text_colID, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_4.Add((10, 20), 2, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_4.Add(self.text_ctrl_ColID, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_4.Add(grid_sizer_4, 1, wx.EXPAND, 0)
        grid_sizer_6.Add(self.text_MaxList, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_6.Add((10, 20), 2, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_6.Add(self.text_ctrl_MaxListLength, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_4.Add(grid_sizer_6, 1, wx.EXPAND, 0)
        grid_sizer_5.Add(self.button_Confirm, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_5.Add((20, 20), 2, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_5.Add(self.button_Clear, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_4.Add(grid_sizer_5, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_2.Add((50, 20), 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_5.Add(self.label_ResultPreview, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_5.Add(self.grid_Result, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_5, 1, wx.EXPAND, 0)
        self.notebook_2_pane_1.SetSizer(sizer_2)
        # end wxGlade

    def OnConfirm(self,e):
        filePath = self.text_ctrl_DropTarget.GetLineText(0)
        maxStringLength = self.combo_box_MaxStringLength.GetSelection()+ 2
        minStringFreq = self.combo_box_MinStringFreq.GetSelection()+ 2
        myNG = MyNGram()
        #print filePath, maxStringLength, minStringFreq

        myNG.longTermPriority(filePath, maxStringLength,minStringFreq)

        self.termsFreq = myNG.GetTermsFreq()
        # set grid value
        self.grid_Result.InsertRows(0,len(self.termsFreq))
        for i in range(len(self.termsFreq)):
            self.grid_Result.SetCellValue(i,0,self.termsFreq[i][0])
            self.grid_Result.SetCellValue(i,1,str(self.termsFreq[i][1]))        

# end of class MyNotebook

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        # Menu Bar
        self.MyApp_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        menuSave = wxglade_tmp_menu.Append(wx.ID_ANY, _("Save"), _("Save the file"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        menuQuit = wxglade_tmp_menu.Append(wx.ID_ANY, _("Quit"), _("Bye Bye!"), wx.ITEM_NORMAL)
        self.MyApp_menubar.Append(wxglade_tmp_menu, _("File"))
        wxglade_tmp_menu = wx.Menu()
        menuHelp = wxglade_tmp_menu.Append(wx.ID_ANY, _("How to Use"), _("It is easy to use"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        menuAbout = wxglade_tmp_menu.Append(wx.ID_ANY, _("About"), _("About the Author"), wx.ITEM_NORMAL)
        self.MyApp_menubar.Append(wxglade_tmp_menu, _("Help"))
        self.SetMenuBar(self.MyApp_menubar)
        # Menu Bar end
        self.MyApp_statusbar = self.CreateStatusBar(1, 0)
        self.notebook_2 = MyNotebook(self, wx.ID_ANY)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

        #Bind function with Menu
        self.Bind(wx.EVT_MENU, self.OnQuit, menuQuit)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnHelp, menuHelp)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        
    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(_("My N-GRAM Analyst"))
        self.SetSize((756, 485))
        self.MyApp_statusbar.SetStatusWidths([-1])
        # statusbar fields
        MyApp_statusbar_fields = [_("For your service")]
        for i in range(len(MyApp_statusbar_fields)):
            self.MyApp_statusbar.SetStatusText(MyApp_statusbar_fields[i], i)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.notebook_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def OnQuit(self,e):
        self.Close()

    def OnSave(self,e):
        try:    
            f = open("C:\\N-gram.txt","w") 
            for terms in self.notebook_2.termsFreq:
                f.write(terms[0].encode("utf-8")+',')
                f.write(str(terms[1]).encode("utf-8")+'\n')
            f.close()
            self.ShowMessage_Save()
        except AttributeError:
            self.ShowMessage_NoFile()        

    def OnHelp(self,e):
        wx.MessageBox('1. Drog a ".txt" file to File Name\n2. Select the max string length for N-GRAM\n3. Select the minimum frequency of the terms', 'Info', 
            wx.OK | wx.ICON_INFORMATION)

    def OnAbout(self,e):
        description =""u"以N-GLAM演算法打造的文本分析工具，本工具僅支援中文文章。\n本工具同時採用標點緞斷句及長詞優先演算法。""" 
        info = wx.AboutDialogInfo()
        info.SetName('About N-GRAM Analyst')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2014 Bryan Yang')
        info.SetWebSite('http://bryannotes.blogspot.tw/')
        info.SetLicence('GPLv3')


        wx.AboutBox(info)


    def ShowMessage_Save(self):
        wx.MessageBox('File Saved at \"c:\\N-gram.txt\"', 'Info', 
            wx.OK | wx.ICON_INFORMATION)

    def ShowMessage_NoFile(self):
        wx.MessageBox('Please analysis the file first', 'Info', 
            wx.OK | wx.ICON_INFORMATION)

   

# end of class MyFrame
class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        MyApp = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(MyApp)
        MyApp.Show()
        return 1

# end of class MyApp

if __name__ == "__main__":
    gettext.install("app") # replace with the appropriate catalog name

    app = MyApp(0)
    app.MainLoop()
