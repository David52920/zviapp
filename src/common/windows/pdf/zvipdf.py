from reportlab.graphics.shapes import *
from reportlab.lib.pagesizes import A4,letter,landscape,portrait
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin, String
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.legends import Legend
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus.tables import Table
from reportlab.platypus import Paragraph, Table, SimpleDocTemplate, Spacer,TableStyle
from reportlab.lib.units import mm, inch
from reportlab.platypus.flowables import Flowable
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle, TA_CENTER
import threading

class PDF(_DrawingEditorMixin,Drawing):
    def __init__(self,pathList ,width = 400, height = 100, parent = None, *args, **kw):
        Drawing.__init__(self,width,height,*args,**kw)
        print("Initializing PDF properties...")
        self._lock = threading.RLock()
        self._pathList = pathList
        self._yAdd = 5
        self._caselength_dictionary = {'1':5,'2':5,'3':8,'4':10,'5':13,'6':15,'7':18,'8':20,'9':20,'10':25,'11':25,'12':30}
        #self._pathname = pathname
        #self._casename = "CNM_DNM"

        self._drawing_width = 500
        self._drawing_height = 100
        #label title
        self._title_x = 155
        self._title_y = 160
        self._title_maxWidth = 250
        self._title_height = 20
        self._title_fontSize = 10
        #label x-axis
        self._textAnchor = "middle"
        self._labelx_x = 150
        self._labelx_y = 10
        self._labelx_maxWidth = 180
        self._labelx_height = 20
        self._labelx_fontSize = 7
        #label y-axis
        self._labely_x = 10
        self._labely_y = 100
        self._labely_maxWidth = 180
        self._labely_height = 20
        self._labely_fontSize = 7
        #chart
        self._chart_x = self._labely_x + 30
        self._chart_y = 40
        self._chart_height = 100
        self._chart_width = 200
        self._legend_alignment = "right"
        self._legend_x = 50
        self._legend_y = 150
        self._legend_fontSize = 7
        self._legend_dxTextSpace = 5
        self._legend_dy = 2
        self._legend_dx = 8
        self._legend_deltay = 5
        self._legend_deltax = 5
        self._Ps = 0
        self._Pd = 0
        self._visibleGrid = 1
        self._strokeWidth = 0.1
        self._gridColor = colors.lightgrey

        self._pressure_tick = 0
        self._volume_tick = 0
        self._force_tick = 0
        self._force_add = 0
        self._pressure_add = 0
        self._userForceTicks = 0
        self._userPressureTicks = 0
        self._userVolumeTicks = 0
        self._userForceAdd = 0
        self._userPressureAdd = 0
        self._data = []
        self._dataList = []
        self._height = 0
        self._tabley = 300
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER,leading=7)
        print("-> Initializing complete.")

    def getUserPressureTicks (self):
        return self._userPressureTicks
    
    def setUserPressureTicks (self,value):
        self._userPressureTicks = value
        
    def getPressureTicks (self):
        return self._pressure_tick
    
    def setPressureTicks (self,value):
        self._pressure_tick = value
        
    def getUserVolumeTicks (self):
        return self._userVolumeTicks
    
    def setUserVolumeTicks(self,value):
        self._userVolumeTicks = value
        
    def getVolumeTicks (self):
        return self._volume_tick
    
    def setVolumeTicks(self,value):
        self._volume_tick = value
        
    def getUserForceTicks (self):
        return self._userForceTicks
    
    def setUserForceTicks(self,value):
        self._userForceTicks = value

    def getForceTicks (self):
        
        return self._force_tick
    
    def setForceTicks(self,value):
        self._force_tick = value

    def getUserForceAdd (self):
        return self._userForceAdd
    
    def setUserForceAdd(self,value):
        self._userForceAdd = value
        
    def getForceAdd (self):
        return self._force_add
    
    def setForceAdd(self,value):
        self._force_add = value

    def getUserPressureAdd (self):
        return self._userPressureAdd
    
    def setUserPressureAdd(self,value):
        self._userPressureAdd = value
        
    def getPressureAdd (self):
        return self._pressure_add
    
    def setPressureAdd(self,value):
        self._pressure_add = value
        
    def readCylinderData(self, index):
        print("\t\tI. Extracting 'RecipCylinder' data from selected file folder...")
        file = open("{pathname}\\3,5\\RecipCylinder.dat".format(pathname = self._pathList[index][0]))
        dataList = []
        for line in file:
            dataList+=[line.split()]

        theta = [x[0] for x in dataList]
        CrankAngle = [float(i) * 180 / 3.14159 for i in theta[2:]]

        GasForceN = [x[39] for x in dataList]
        GasForceN1 = [float(i) for i in GasForceN[2:]]
        GasForce = [float(i) * 0.224809 for i in GasForceN[2:]]
        #
        InertiaN = [x[40] for x in dataList]
        InertiaN1 = [float(i) for i in InertiaN[2:]]
        Inertia = [float(i) * 0.224809 for i in InertiaN[2:]]

        RodN = [x[41] for x in dataList]
        RodN1 = [float(i) for i in RodN[2:]]
        Rod = [float(i) * 0.224809 for i in RodN[2:]]

        P_HEPA = [x[29] for x in dataList]
        P_HEPA1 = [float(i) for i in P_HEPA[2:]]
        P_HE = [float(i) * 0.000145038 for i in P_HEPA[2:]]

        P_CEPA = [x[30] for x in dataList]
        P_CEPA1 = [float(i) for i in P_CEPA[2:]]
        P_CE = [float(i) * 0.000145038 for i in P_CEPA[2:]]

        V_HE = [x[2] for x in dataList]
        V_HE1 = [float(i) for i in V_HE[2:]]
        HEVolume = [float(i) * 61023.744 for i in V_HE[2:]]

        V_CE = [x[14] for x in dataList]
        V_CE1 = [float(i) for i in V_CE[2:]]
        CEVolume = [float(i) * 61023.744 for i in V_CE[2:]]

        xs_HE = [x[10] for x in dataList]
        xs_HE1 = [float(i) for i in xs_HE[2:]]
        SVHE1 = [float(i) * 39.3701 for i in xs_HE[2:]]

        vs_HE = [x[9] for x in dataList]
        vs_HE1 = [float(i) for i in vs_HE[2:]]
        SVHE2 = [float(i) * 3.28084 for i in vs_HE[2:]]

        xd_HE = [x[12] for x in dataList]
        xd_HE1 = [float(i) for i in xd_HE[2:]]
        DVHE1 = [float(i) * 39.3701 for i in xd_HE[2:]]

        vd_HE = [x[11] for x in dataList]
        vd_HE1 = [float(i) for i in vd_HE[2:]]
        DVHE2 = [float(i) * 3.28084 for i in vd_HE[2:]]

        xs_CE = [x[21] for x in dataList]
        xs_CE1 = [float(i) for i in xs_CE[2:]]
        SVCE1 = [float(i) * 39.3701 for i in xs_CE[2:]]

        vs_CE = [x[20] for x in dataList]
        vs_CE1 = [float(i) for i in vs_CE[2:]]
        SVCE2 = [float(i) * 3.28084 for i in vs_CE[2:]]

        vd_CE = [x[22] for x in dataList]
        vd_CE1 = [float(i) for i in vd_CE[2:]]
        DVCE2 = [float(i) * 3.28084 for i in vd_CE[2:]]

        xd_CE = [x[23] for x in dataList]
        xd_CE1 = [float(i) for i in xd_CE[2:]]
        DVCE1 = [float(i) * 39.3701 for i in xd_CE[2:]]
        file.close()
        data = [CrankAngle,GasForce,Inertia, HEVolume,CEVolume, Rod,P_HE,P_CE,SVHE1, DVHE1, SVCE1, DVCE1,SVHE2, DVHE2, SVCE2, DVCE2,\
                GasForceN1,InertiaN1,RodN1,P_HEPA1,P_CEPA1,V_HE1,V_CE1, xs_HE1, vs_HE1, xd_HE1, vd_HE1, xs_CE1, vs_CE1, xd_CE1, vd_CE1]
        print("\t\t-> Extraction complete.")
        return data
    
    def CreateDataList(self):
        for x in range(len(self._pathList)):
            self.AddDataFromFile((x))
#"""Tables"""
    def CreateValveConfigHeaderTable(self,canvas, width, height):
        text_data = ["Case","Stage", "Valve Type", "(in)<br/>Nose Diameter<br/>S/D","",
                     "(in^2)<br/>Effective Area<br/>S/D","", "(in^3)<br/>Clearance Volume<br/>S/D","",
                     "Module#<br/>S/D", "Suction<br/>Module", "Discharge<br/>Module"]
        d = []
        font_size = 6
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER,leading=7)
        for text in text_data:
            ptext = "<font size='{0}'><b>{1}</b></font>".format(font_size,text)
            p = Paragraph(ptext, centered)
            d.append(p)
        
        data = [d]
        colWidth = [0.4*inch,0.4*inch,0.8*inch,0.45*inch,0.45*inch,0.45*inch,0.45*inch,0.45*inch,0.45*inch,0.6*inch,0.6*inch,0.6*inch]
        table = Table(data,colWidth)
        table.setStyle(TableStyle([('SPAN', (3, 0), (4, 0)),
                                   ('SPAN', (5, 0), (6, 0)),
                                   ('SPAN', (7, 0), (8, 0)),
                                   ]))
        w, h = table.wrapOn(canvas, 0, 0)
        self._height = height - self._tabley
        table.drawOn(canvas, 0, self._height)

    def CreateValveConfigDataTable(self,canvas, width, height):
        line_num = 1 #replace with case ID
        font_size = 6
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER,leading=7)
        formatted_line_data = []

        lineData = []
        for x in range(len(self._pathList)):
            HESND = self._dataList[x][2]
            HEDND = self._dataList[x][3]
            HESEA = self._dataList[x][4]
            HEDEA = self._dataList[x][5]
            HESvclr = self._dataList[x][6]
            HEDvclr = self._dataList[x][7]
            HESNum = self._dataList[x][8]
            HEDNum = self._dataList[x][9]
            HESMod = self._dataList[x][10]
            HEDMod = self._dataList[x][11]
            
            line_data = [str(x+1), "1", "Standard/Standard", 
                         "{0}".format(HESND),"{0}".format(HEDND), "{0}".format(HESEA),"{0}".format(HEDEA),
                         "{0}".format(HESvclr),"{0}".format(HEDvclr), "{0}/{1}".format(HESNum,HEDNum), 
                         "{0}".format(HESMod), "{0}".format(HEDMod)]
        
            for item in line_data:
                ptext = "<font size='{0}'>{1}</font>".format(font_size-1,item)
                p = Paragraph(ptext, centered)
                formatted_line_data.append(p)
            lineData.append(formatted_line_data)
            formatted_line_data = []
            line_num += 1
        colWidth = [0.4*inch,0.4*inch,0.8*inch,0.45*inch,0.45*inch,0.45*inch,0.45*inch,0.45*inch,0.45*inch,0.6*inch,0.6*inch,0.6*inch]
        rowsHeight=[0.1*inch]*len(self._pathList)
        mytable = Table(lineData,colWidth,rowsHeight)

        w, h = mytable.wrapOn(canvas, 0, 0)
        if str(len(self._pathList)) in self._caselength_dictionary:
            self._yAdd = self._caselength_dictionary[str(len(self._pathList))]
        self._height -= (self._yAdd + (len(self._pathList) * 5))
        mytable.drawOn(canvas, 0, self._height)
        
    def CreateOCHeaderTableTop(self,canvas, width, height):
        text_data = ["","","","","","","","","","", #10 items (0-9)
                     "(%)<br/>Fixed Clearance<br/>w/o Valves","", #(10-11)
                     "(%)<br/>Valve Clearance","",#(12-13)
                     "(%)<br/>Added Clearance","",#(14-15)
                     "(%)<br/>Running Clearance",""] #(15-16)
        d = []
        font_size = 6
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER,leading=7)
        for text in text_data:
            ptext = "<font size='{0}'><b>{1}</b></font>".format(font_size,text)
            p = Paragraph(ptext, centered)
            d.append(p)
        
        data = [d]
        colWidth = [0.4*inch,0.4*inch,0.4*inch,0.3*inch,0.4*inch,0.4*inch,1*inch,1*inch,1*inch,0.9*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch]
        table = Table(data,colWidth)
        table.setStyle (TableStyle ([

            ('SPAN',(10,0),(11,0)),
            ('SPAN',(12,0),(13,0)),
            ('SPAN',(14,0),(15,0)),
            ('SPAN',(16,0),(17,0))
            ]))
        w, h = table.wrapOn(canvas, 0, 0)
        self._height -= 20
        table.drawOn(canvas, 0, self._height)
        
    def CreateOCHeaderTableBottom(self,canvas, width, height):
        text_data = ["Case","Stage",
                     "Molecular Weight", "(in)<br/>Cylinder Bore",
                     "(RPM)<br/>Speed","(Psia)<br/>Suction Pressure","(Psia)<br/>Discharge Pressure",
                     "(F)<br/>Suction Temperature","(Psi)<br/>Pressure Differential",
                     "Pressure Ratio","HE","CE","HE","CE","HE","CE","HE","CE"]
        d = []
        font_size = 6
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER,leading=7)
        for text in text_data:
            ptext = "<font size='{0}'><b>{1}</b></font>".format(font_size,text)
            p = Paragraph(ptext, centered)
            d.append(p)
        
        data = [d]
        colWidth = [0.4*inch,0.4*inch,0.7*inch,0.7*inch,0.5*inch,0.7*inch,0.7*inch,0.7*inch,0.7*inch,0.7*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch]
        table = Table(data,colWidth)
        w, h = table.wrapOn(canvas, 0, 0)
        self._height -= 9
        table.drawOn(canvas, 0, self._height)

    def CreateOCDataTable(self,canvas, width, height):
        line_num = 1
        font_size = 6
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER,leading=7)
        formatted_line_data = []
        lineData = []
        for x in range(len(self._pathList)):
            mw = self._dataList[x][0]
            bore = self._dataList[x][1]
            RPM = self._dataList[x][12]
            Ps = self._dataList[x][13]
            Pd = self._dataList[x][14]
            Ts = self._dataList[x][15]
            DiffP = self._dataList[x][16]
            Ratio = self._dataList[x][17]
            FixedClrHE = self._dataList[x][18]
            FixedClrCE = self._dataList[x][19]
            ValveClrHE = self._dataList[x][20]
            ValveClrCE = self._dataList[x][21]
            HEaddclr = self._dataList[x][22]
            CEaddclr = self._dataList[x][23]
            HErunclr = self._dataList[x][24]
            CErunclr = self._dataList[x][25]
            
            line_data = [str(x+1), "1", "{0}".format(mw), "{0}".format(bore),"{0}".format(RPM),
                         "{0}".format(Ps),"{0}".format(Pd),"{0}".format(Ts),"{0}".format(DiffP),
                         "{0}".format(Ratio),"{0}".format(FixedClrHE),"{0}".format(FixedClrCE),
                         "{0}".format(ValveClrHE),"{0}".format(ValveClrCE),
                         "{0}".format(HEaddclr),"{0}".format(CEaddclr),
                         "{0}".format(HErunclr),"{0}".format(CErunclr)]
        
            for item in line_data:
                ptext = "<font size='{0}'>{1}</font>".format(font_size-1,item)
                p = Paragraph(ptext, centered)
                formatted_line_data.append(p)
            lineData.append(formatted_line_data)
            formatted_line_data = []
            line_num += 1
        colWidth = colWidth = [0.4*inch,0.4*inch,0.7*inch,0.7*inch,0.5*inch,0.7*inch,0.7*inch,0.7*inch,0.7*inch,0.7*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch]
        rowsHeight=[0.1*inch]*len(self._pathList)
        table = Table(lineData,colWidth,rowsHeight)
        w, h = table.wrapOn(canvas, 0, 0)
        if str(len(self._pathList)) in self._caselength_dictionary:
            self._yAdd = self._caselength_dictionary[str(len(self._pathList))]
        self._height -= (self._yAdd + (len(self._pathList) * 5))
        table.drawOn(canvas, 0, self._height)
        
    def CreateCylinderInfoHeaderTableTop(self,canvas, width, height):
        text_data = ["","","(lb) Total Rod Load","","","(HP) Indicated Horsepower","","",
                     "Discharge","(MMCSFD) Flow","","","(MMSCFD/HP) Specific Power","","",
                     "(psi) Cylinder Pressure","",""]
        d = []
        font_size = 6
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER,leading=7)
        for text in text_data:
            ptext = "<font size='{0}'><b>{1}</b></font>".format(font_size,text)
            p = Paragraph(ptext, centered)
            d.append(p)
        
        data = [d]
        colWidth = [0.4*inch,0.4*inch,0.6*inch,0.7*inch,0.6*inch,0.5*inch,0.5*inch,0.5*inch,0.6*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.2*inch,0.5*inch]
        table = Table(data,colWidth)
        table.setStyle (TableStyle ([

            ('SPAN',(2,0),(4,0)),
            ('SPAN',(5,0),(7,0)),
            ('SPAN',(9,0),(11,0)),
            ('SPAN',(12,0),(14,0)),
            ('SPAN',(15,0),(17,0))
            ]))
        w, h = table.wrapOn(canvas, 0, 0)
        self._height -= 10
        table.drawOn(canvas, 0, self._height)
        
    def CreateCylinderInfoHeaderTableBottom(self,canvas, width, height):
        text_data = ["Case","Stage","Total","Compression", "Tension",
                     "Total","HE", "CE", #HP
                     "Temp.",
                     "Total","HE","CE",#Flow
                     "Total","HE","CE",#Specific Power
                     "Max","Min"]
        d = []
        font_size = 6
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER,leading=7)
        for text in text_data:
            ptext = "<font size='{0}'><b>{1}</b></font>".format(font_size,text)
            p = Paragraph(ptext, centered)
            d.append(p)
        
        data = [d]
        colWidth = [0.4*inch,0.4*inch,0.6*inch,0.7*inch,0.6*inch,0.5*inch,0.5*inch,0.5*inch,0.6*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.6*inch,0.6*inch]

        table = Table(data,colWidth)

        w, h = table.wrapOn(canvas, 0, 0)
        self._height -= 8
        table.drawOn(canvas, 0, self._height)

    def CreateCylinderInfoDataTable(self,canvas, width, height):
        line_num = 1
        font_size = 6
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER,leading=7)
        formatted_line_data = []
        lineData = []
        for x in range(len(self._pathList)):
            TotalRL = self._dataList[x][26]
            CRL = self._dataList[x][27]
            TRL = self._dataList[x][28]
            TotalHP = self._dataList[x][29]
            HEHP = self._dataList[x][30]
            CEHP = self._dataList[x][31]
            Td = self._dataList[x][32]
            TotalFlow = self._dataList[x][38]
            HEFlow = self._dataList[x][39]
            CEFlow = self._dataList[x][40]
            TotalSP = self._dataList[x][41]
            HESP = self._dataList[x][42]
            CESP = self._dataList[x][43]
            MaxP = self._dataList[x][52]
            MinP = self._dataList[x][53]
            
            line_data = [str(x+1), "{stage}".format(stage = "1"), TotalRL, CRL,TRL,
                TotalHP,HEHP,CEHP,Td,
                TotalFlow,HEFlow,CEFlow,TotalSP,HESP,CESP,
                MaxP,MinP]
        
            for item in line_data:
                ptext = "<font size='{0}'>{1}</font>".format(font_size-1,item)
                p = Paragraph(ptext, centered)
                formatted_line_data.append(p)
            lineData.append(formatted_line_data)
            formatted_line_data = []
            line_num += 1
        colWidth = [0.4*inch,0.4*inch,0.6*inch,0.7*inch,0.6*inch,0.5*inch,0.5*inch,0.5*inch,0.6*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.6*inch,0.6*inch]
        rowsHeight=[0.1*inch]*len(self._pathList)
        table = Table(lineData,colWidth,rowsHeight)
        w, h = table.wrapOn(canvas, 0, 0)
        if str(len(self._pathList)) in self._caselength_dictionary:
            self._yAdd = self._caselength_dictionary[str(len(self._pathList))]
        self._height -= (self._yAdd + (len(self._pathList) * 5))
        table.drawOn(canvas, 0, self._height)
        
    def CreateValveInfoHeaderTableTop(self,canvas, width, height):
        text_data = ["","",
                     "(%) Valve Loses", "", "", "","",
                     "(FPS) Impact Velocities(1,1)", "", "", "",
                     "(FPS) Impact Velocities(3,5)", "", "", "",
                     "Valve DP",""]
        d = []
        font_size = 6
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER,leading=7)
        for text in text_data:
            ptext = "<font size='{0}'><b>{1}</b></font>".format(font_size,text)
            p = Paragraph(ptext, centered)
            d.append(p)
        
        data = [d]
        colWidth = [0.4*inch,0.4*inch,0.5*inch,0.5*inch,0.5*inch,0.4*inch,0.4*inch,0.4*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.6*inch,0.6*inch]
        table = Table(data,colWidth)
        table.setStyle (TableStyle ([

            ('SPAN',(2,0),(6,0)),
            ('SPAN',(7,0),(10,0)),
            ('SPAN',(11,0),(14,0)),
            ('SPAN',(15,0),(16,0))
             ]))
        w, h = table.wrapOn(canvas, 0, 0)
        self._height -= 10
        table.drawOn(canvas, 0, self._height)
        
    def CreateValveInfoHeaderTableBottom(self,canvas, width, height):
        text_data = ["Case","Stage",
                     "HES","CES","HED","CED","Total", #
                     "HES","CES","HED","CED", #
                     "HES","CES","HED","CED", #
                     "Suction","Discharge"]
        d = []
        font_size = 6
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER,leading=7)
        for text in text_data:
            ptext = "<font size='{0}'><b>{1}</b></font>".format(font_size,text)
            p = Paragraph(ptext, centered)
            d.append(p)
        
        data = [d]
        colWidth = [0.4*inch,0.4*inch,0.5*inch,0.5*inch,0.5*inch,0.4*inch,0.4*inch,0.4*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.6*inch,0.6*inch]

        table = Table(data,colWidth)

        w, h = table.wrapOn(canvas, 0, 0)
        self._height -= 10
        table.drawOn(canvas, 0, self._height)

    def CreateValveInfoDataTable(self,canvas, width, height):
        line_num = 1
        font_size = 6
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER,leading=7)
        formatted_line_data = []
        lineData = []
        for x in range(len(self._pathList)):
            HESVL = self._dataList[x][33]
            HEDVL = self._dataList[x][34]
            CESVL = self._dataList[x][35]
            CEDVL = self._dataList[x][36]
            TotalVL = self._dataList[x][37]
            HESIV1 = self._dataList[x][44]
            HEDIV1 = self._dataList[x][45]
            CESIV1 = self._dataList[x][46]
            CEDIV1 = self._dataList[x][47]
            HESIV = self._dataList[x][48]
            HEDIV = self._dataList[x][49]
            CESIV = self._dataList[x][50]
            CEDIV = self._dataList[x][51]
            HESVDP = self._dataList[x][54]
            HEDVDP = self._dataList[x][55]
            
            line_data = [str(x+1), "{stage}".format(stage = "1"),
                HESVL,HEDVL,CESVL,CEDVL,TotalVL,
                HESIV1,HEDIV1,CESIV1,CEDIV1,HESIV,HEDIV,CESIV,CEDIV,HESVDP,HEDVDP]
        
            for item in line_data:
                ptext = "<font size='{0}'>{1}</font>".format(font_size-1,item)
                p = Paragraph(ptext, centered)
                formatted_line_data.append(p)
            lineData.append(formatted_line_data)
            formatted_line_data = []
            line_num += 1
        colWidth = colWidth = [0.4*inch,0.4*inch,0.5*inch,0.5*inch,0.5*inch,0.4*inch,0.4*inch,0.4*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch]
        rowsHeight=[0.1*inch]*len(self._pathList)
        table = Table(lineData,colWidth,rowsHeight)
        w, h = table.wrapOn(canvas, 0, 0)
        if str(len(self._pathList)) in self._caselength_dictionary:
            self._yAdd = self._caselength_dictionary[str(len(self._pathList))]
        self._height -= (self._yAdd + (len(self._pathList) * 5))
        table.drawOn(canvas, 0, self._height)
        
    def AddDataFromFile(self,index):
        print("\t\t\t{0}. Extracting data from .OUT files...".format(chr(index + 97)))
        with open('{pathname}\\3,5\\{casename}.OUT'.format(pathname = self._pathList[index][0], casename = self._pathList[index][1])) as results:
                content = results.readlines()
                for line in content:
                    if line.startswith("Flow@STP(MMCFD)"):
                        column = line.split(")")
                        flows = column[1].split()
                        TotalFlow = round(float(flows[0]), 3)
                        HEFlow = round(float(flows[1]), 3)
                        CEFlow = round(float(flows[2]), 3)
                    if line.startswith("Indicated Power (hp)"):
                        column = line.split(")")
                        HPs = column[1].split()
                        HEHP = round(float(HPs[1])* 1.05, 3)
                        CEHP = round(float(HPs[2])* 1.05, 3)
                        TotalHP = round((HEHP + CEHP), 3)
                    if line.startswith("Max Cylinder Pressure(psi)"):
                        column = line.split(")")
                        maxpress = column[1].split()
                        max1 = round(float(maxpress[0]), 3)
                        max2 = round(float(maxpress[1]), 3)
                        MaxP = max(max1, max2)
                    if line.startswith("Min Cylinder Pressure(psi)"):
                        column = line.split(")")
                        minpress = column[1].split()
                        min1 = round(float(minpress[0]), 3)
                        min2 = round(float(minpress[1]), 3)
                        MinP = min(min1, min2)
                    if line.startswith("Discharge Temperature (F)"):
                        column = line.split(")")
                        dischartemp = column[1].split()
                        Td = round(float(dischartemp[0]), 3)
                    if line.startswith("Valve Loss (hp)"):
                        column = line.split(")")
                        valveloss = column[1].split()
                        HESVL = round(float(valveloss[0]), 3)
                        HEDVL = round(float(valveloss[1]), 3)
                        CESVL = round(float(valveloss[2]), 3)
                        CEDVL = round(float(valveloss[3]), 3)
                        TotalVL = HESVL + HEDVL + CESVL + CEDVL
                    if line.startswith("Open imp vel(fps)"):
                        column = line.split(")")
                        impveloc = column[1].split()
                        HESIV = round(float(impveloc[0]), 2)
                        HEDIV = round(float(impveloc[1]), 2)
                        CESIV = round(float(impveloc[2]), 2)
                        CEDIV = round(float(impveloc[3]), 2)
                    if line.startswith("Max Valve DP(psi)"):
                        column = line.split(")")
                        maxvalvedp = column[1].split()
                        HESVDP = round(float(maxvalvedp[0]), 3)
                        HEDVDP = round(float(maxvalvedp[1]), 3)
                        CESVDP = round(float(maxvalvedp[2]), 3)
                        CEDVDP = round(float(maxvalvedp[3]), 3)
                    if line.startswith("Module Type"):
                        column = line.split("Type")
                        modselect = column[1].split()
                        HESMod = modselect[0]
                        HEDMod = modselect[1]
                        CESMod = modselect[2]
                        CEDMod = modselect[3]
                    if line.startswith("# of valves/Corner"):
                        column = line.split("Corner")
                        valvepercorner = column[1].split()
                        HESVPC = int(float(valvepercorner[0]))
                        HEDVPC = int(float(valvepercorner[1]))
                        CESVPC = int(float(valvepercorner[2]))
                        CEDVPC = int(float(valvepercorner[3]))
                    if line.startswith("# of modules/valve"):
                        column = line.split("valve")
                        nummod = column[1].split()
                        HESNum = (nummod[0])
                        HEDNum = (nummod[1])
                        CESNum = (nummod[2])
                        CEDNum = (nummod[3])
                    if line.startswith("Nose Dia(in)"):
                        column = line.split(")")
                        nosedia = column[1].split()
                        HESND = float(nosedia[0])
                        HEDND = float(nosedia[1])
                        CESND = float(nosedia[2])
                        CEDND = float(nosedia[3])
                    if line.startswith("Cylinder Clearance Percent"):
                        column = line.split("Percent")
                        runclr = column[1].split()
                        HErunclr = round(float(runclr[0]), 3)
                        CErunclr = round(float(runclr[1]), 3)
                    if line.startswith("Max <> RodLoad(lbf)"):
                        column = line.split(")")
                        comploadforces = column[1].split()
                        CRL = round(float(comploadforces[0]), 2)
                    if line.startswith("Max >< RodLoad(lbf)"):
                        column = line.split(")")
                        tenloadforces = column[1].split()
                        TRL = round(float(tenloadforces[0]), 2)
                    if line.startswith("Clearance Volume(in^3)"):
                        column = line.split(")")
                        clrvolvalves = column[1].split()
                        HESvclr = round(float(clrvolvalves[0]), 3)
                        HEDvclr = round(float(clrvolvalves[1]), 3)
                        CESvclr = round(float(clrvolvalves[2]), 3)
                        CEDvclr = round(float(clrvolvalves[3]), 3)
                    if line.startswith("Piston Displacement (in^3)"):
                        column = line.split(")")
                        pistondisplace = column[1].split()
                        HEPD = round(float(pistondisplace[0]), 3)
                        CEPD = round(float(pistondisplace[1]), 3)
                    if line.startswith("Added clearance (in^3)"):
                        column = line.split(")")
                        addclr = column[1].split()
                        addclrHE = round(float(addclr[0]), 3)
                        addclrCE = round(float(addclr[1]), 3)
                    if line.startswith("Cylinder clearance (in^3)"):
                        column = line.split(")")
                        cylinderclr = column[1].split() 
                        HEcylclr = round(float(cylinderclr[0]), 3)
                        CEcylclr = round(float(cylinderclr[1]), 3)
                    if line.startswith("Effective Area(in^2)"):
                        column = line.split(")")
                        effectivearea = column[1].split()
                        HESEA = round(float(effectivearea[0]), 3)
                        HEDEA = round(float(effectivearea[1]), 3)
                        CESEA = round(float(effectivearea[2]), 3)
                        CEDEA = round(float(effectivearea[3]), 3)
                    if line.startswith("Cylinder Diameter (in)"):
                        column = line.split(")")
                        boresize = column[1].split()
                        bore = float(boresize[0])
                    if line.startswith("# of components:"):
                        column = line.split("mixture:")
                        moleweight = column[1].split()
                        mw = round(float(moleweight[0]), 3)
                    if line.startswith("Valve Pocket Factor"):
                        column = line.split("Factor")
                        pocketfactor = column[1].split()
                        HESPF = int(float(pocketfactor[0]))
                        HEDPF = int(float(pocketfactor[1]))
                        CESPF = int(float(pocketfactor[2]))
                        CEDPF = int(float(pocketfactor[3]))
                MainList = content[44].split()
                RPM = round(float(MainList[0]), 3)
                Ps = round(float(MainList[1]), 3)
                Ts = round(float(MainList[2]), 3)
                Pd = round(float(MainList[3]), 3)

                self._Ps = Ps
                self._Pd = Pd
                #Added Clr    

                HEaddclr = round(((addclrHE / HEPD) * 100), 2)
                CEaddclr = round(((addclrCE / CEPD) * 100), 2)
                # Fixed Clr
                FixedClrHE = round((HEcylclr / HEPD) * 100, 3)
                FixedClrCE = round((CEcylclr / CEPD) * 100, 3)
                # Valve Clr
                ValveClrHE = round((((HESvclr * HESVPC) + (HEDvclr * HEDVPC)) / HEPD) * 100, 3)
                ValveClrCE = round((((CESvclr * CESVPC) + (CEDvclr * CEDVPC)) / CEPD) * 100, 3)
                #Specific Power-given as (hp-s/lbm) in .OUT file used below to give HP/MMSCFD
                TotalSP = round(TotalHP/TotalFlow, 3)
                HESP = round(HEHP/HEFlow, 3)
                CESP = round(CEHP/CEFlow, 3)
                
                Ratio = round(Pd / Ps, 3)
                DiffP = round(Pd - Ps, 3)

                TotalRL = round(TRL + CRL,2)
                TotalVL = round(HESVL + HEDVL + CESVL + CEDVL,2)
                
                throwNum = 1

                modList = [HESMod,HEDMod,CESMod,CEDMod]
                modRatioList = ["HESModRat","HEDModRat","CESModRat","CEDModRat"]
                reedDict = {"B":653,"C":1023,"D":1476,"E-N":1500,"E-M":2615,"E-X":2615,"F-N":1500,"F-M":4100,"F-X":4100,"O":1476,"P-N":1500,
                                            "P-M":2615,"P-X":2615,"Q-N":1500,"Q-M":4100,"Q-X":4100}
                    
                for ratio,mod in zip(modRatioList,modList):
                    for reed in reedDict.items():
                        if reed[0] in mod:
                            exec("self._{0}={1}".format(ratio,reed[1])) #creates variables from modRatioList

                HESModRat = self._HESModRat
                HEDModRat = self._HEDModRat
                CESModRat = self._CESModRat
                CEDModRat = self._CEDModRat
                with open('{pathname}\\1,1\\{casename}PF1_1.OUT'.format(pathname = self._pathList[index][0], casename = self._pathList[index][1])) as results:
                    content = results.readlines()
                    for line in content:
                        if line.startswith("Open imp vel(fps)"):
                            column = line.split(")")
                            impveloc = column[1].split()
                            HESIV1 = round(float(impveloc[0]), 2)
                            HEDIV1 = round(float(impveloc[1]), 2)
                            CESIV1 = round(float(impveloc[2]), 2)
                            CEDIV1 = round(float(impveloc[3]), 2)
##                if Data.HESTMod != '0':
##                    Data.suctiontype = 'Stacked'
##                else:
##                    Data.suctiontype = 'Standard'
##                if Data.HEDTMod != '0':
##                    Data.dischargetype = 'Stacked'
##                else:
##                    Data.dischargetype = 'Standard'
                print("\t\t\t-> Extraction complete.")
                self._dataList.append([mw,bore,HESND,HEDND,HESEA,HEDEA,HESvclr,HEDvclr,HESNum,HEDNum,HESMod,HEDMod,RPM,Ps,Pd,Ts,\
                    DiffP, Ratio,FixedClrHE,FixedClrCE,ValveClrHE,ValveClrCE,HEaddclr, CEaddclr,\
                    HErunclr,CErunclr, TotalRL, CRL, TRL, TotalHP,HEHP,CEHP,Td,HESVL,HEDVL,CESVL,CEDVL,TotalVL,\
                    TotalFlow,HEFlow,CEFlow,TotalSP,HESP,CESP, HESIV1,HEDIV1,CESIV1,CEDIV1,HESIV,HEDIV,CESIV,CEDIV,\
                    MaxP,MinP,HESVDP,HEDVDP])
        
    def initForce(self, ymax):
        if(self._userForceTicks == 0):
            if(ymax > 0 and ymax < 100):
                self.setForceTicks(10)
            elif(ymax >= 100 and ymax <= 1000):
                self.setForceTicks(100)
            elif(ymax > 1000 and ymax < 10000):
                self.setForceTicks(1000)
            elif(ymax >= 10000 and ymax <= 100000):
                self.setForceTicks(10000)
        if(self._userForceAdd == 0):
            if(ymax > 0 and ymax < 100):
                self.setForceAdd(10)
            elif(ymax >= 100 and ymax <= 1000):
                self.setForceAdd(100)
            elif(ymax > 1000 and ymax < 10000):
                self.setForceAdd(100)
            elif(ymax >= 10000 and ymax <= 100000):
                self.setForceAdd(1000)
        
    def initPressure(self, ymax):
        if(self._userPressureTicks == 0):
            if(ymax > 0 and ymax < 100):
                self.setPressureTicks(10)
            elif(ymax >= 100 and ymax <= 1000):
                self.setPressureTicks(50)
            elif(ymax > 1000 and ymax < 5000):
                self.setPressureTicks(100)
            elif(ymax >= 5000 and ymax <= 10000):
                self.setPressureTicks(1000)
        if(self._userPressureAdd == 0):
            if(ymax > 0 and ymax < 100):
                self.setPressureAdd(10)
            elif(ymax >= 100 and ymax <= 1000):
                self.setPressureAdd(10)
            elif(ymax > 1000 and ymax < 5000):
                self.setPressureAdd(100)
            elif(ymax >= 5000 and ymax <= 10000):
                self.setPressureAdd(1000)
                
    def initVolume(self, xmax):
        if(self._userVolumeTicks == 0):
            if(xmax > 0 and xmax < 100):
                self.setVolumeTicks(10)
            elif(xmax >= 100 and xmax <= 1000):
                self.setVolumeTicks(50)
            elif(xmax > 1000 and xmax < 5000):
                self.setVolumeTicks(500)
            elif(xmax >= 5000 and xmax < 10000):
                self.setVolumeTicks(1000)
                
    def ForceVsAngle(self):
        print("\t\t\t1. Creating chart 1 of 5 : 'Force Vs. Crank Angle'...")
        drawing = Drawing(self._drawing_width,self._drawing_height)
        lp = LinePlot()
        #Title
        lp_label = Label()
        lp_label._text = "FORCES VS CRANK ANGLE"
        lp_label.x = self._title_x
        lp_label.y = self._title_y
        lp_label.maxWidth = self._title_maxWidth
        lp_label.height = self._title_height
        lp_label.textAnchor = self._textAnchor
        lp_label.fontSize = self._title_fontSize
        #XAxis Label
        lp_labelx = Label()
        lp_labelx._text = "CRANK ANGLE(DEG)"
        lp_labelx.x = self._labelx_x
        lp_labelx.y = self._labelx_y
        lp_labelx.maxWidth = self._labelx_maxWidth
        lp_labelx.height = self._labelx_height
        lp_labelx.textAnchor = self._textAnchor
        lp_labelx.fontSize = self._labelx_fontSize
        #YAxis Label
        lp_labely = Label()
        lp_labely._text = "FORCE(LBF)"
        lp_labely.x = self._labely_x
        lp_labely.y = self._labely_y
        lp_labely.maxWidth = self._labely_maxWidth
        lp_labely.height = self._labely_height
        lp_labely.textAnchor = self._textAnchor
        lp_labely.fontSize = self._labely_fontSize
        lp_labely.angle = 90
        #Chart settingss
        lp.x = self._chart_x
        lp.y = self._chart_y
        lp.height = self._chart_height
        lp.width = self._chart_width
        
        lp.xValueAxis.valueMin = 0
        lp.xValueAxis.valueMax = 360
        lp.xValueAxis.valueStep = 45

        ymin = min(min(self._data[1]),min(self._data[2]),min(self._data[5]))
        ymax = max(max(self._data[1]),max(self._data[2]),max(self._data[5]))

        self.initForce(ymax)

        if(self._userForceAdd != 0):
            lp.yValueAxis.valueMin = min(min(self._data[1]),min(self._data[2]),min(self._data[5])) - self.getUserForceAdd()
            lp.yValueAxis.valueMax = max(max(self._data[1]),max(self._data[2]),max(self._data[5])) + self.getUserForceAdd()
        else:
            lp.yValueAxis.valueMin = min(min(self._data[1]),min(self._data[2]),min(self._data[5])) - self.getForceAdd()
            lp.yValueAxis.valueMax = max(max(self._data[1]),max(self._data[2]),max(self._data[5])) + self.getForceAdd()
        if(self._userForceTicks != 0):
            lp.yValueAxis.valueStep = self.getUserForceTicks()
        else:
            lp.yValueAxis.valueStep = self.getForceTicks()
        lp.yValueAxis.gridStrokeWidth = lp.xValueAxis.gridStrokeWidth = self._strokeWidth
        lp.yValueAxis.visibleGrid = lp.xValueAxis.visibleGrid = self._visibleGrid
        lp.yValueAxis.gridStrokeColor = lp.xValueAxis.gridStrokeColor = self._gridColor
        #Legend Settings
        lp_legend = Legend()
        lp_legend.colorNamePairs =  [(colors.blue, "Gas Force"),(colors.red, "Inertia Force"),(colors.green, "Rod Load")]

        lp_legend.alignment = self._legend_alignment
        lp_legend.x = self._legend_x
        lp_legend.y = self._legend_y
        lp_legend.fontSize = self._legend_fontSize
        lp_legend.dxTextSpace = self._legend_dxTextSpace
        lp_legend.dy = self._legend_dy
        lp_legend.dx = self._legend_dx
        lp_legend.deltay = self._legend_deltay
        lp_legend.deltax = self._legend_deltax
        lp_legend.columnMaximum = lp_legend.variColumn = 1
        
        lp.data = [[],[],[]]
        for x,y in zip(self._data[0],self._data[1]):
            test = (x,y)
            lp.data[0].append(test)
        for x,y in zip(self._data[0],self._data[5]):
            test = (x,y)
            lp.data[1].append(test)
        for x,y in zip(self._data[0],self._data[2]):
            test = (x,y)
            lp.data[2].append(test)
            
        lp.lines[0].strokeColor = colors.blue
        lp.lines[1].strokeColor = colors.red
        lp.lines[2].strokeColor = colors.green
     
        drawing.add(lp)
        drawing.add(lp_label)
        drawing.add(lp_labelx)
        drawing.add(lp_labely)
        drawing.add(lp_legend)
        print("\t\t\t-> 'Force Vs. Crank Angle' chart completely drawn with initial properites.")
        return drawing
                
    def CylinderPressureVsAngle(self):
        print("\t\t\t2. Creating chart 2 of 5: 'Cylinder Pressure Vs. Crank Angle'...")
        drawing = Drawing(self._drawing_width,self._drawing_height)
        lp = LinePlot()
        #Title
        lp_label = Label()
        lp_label._text = "CYLINDER PRESSURE VS CRANK ANGLE"
        lp_label.x = self._title_x
        lp_label.y = self._title_y
        lp_label.maxWidth = self._title_maxWidth
        lp_label.height = self._title_height
        lp_label.textAnchor = self._textAnchor
        lp_label.fontSize = self._title_fontSize
        #XAxis Label
        lp_labelx = Label()
        lp_labelx._text = "CRANK ANGLE(DEG)"
        lp_labelx.x = self._labelx_x
        lp_labelx.y = self._labelx_y
        lp_labelx.maxWidth = self._labelx_maxWidth
        lp_labelx.height = self._labelx_height
        lp_labelx.textAnchor = self._textAnchor
        lp_labelx.fontSize = self._labelx_fontSize
        #YAxis Label
        lp_labely = Label()
        lp_labely._text = "PRESSURE (PSIA)"
        lp_labely.x = self._labely_x
        lp_labely.y = self._labely_y
        lp_labely.maxWidth = self._labely_maxWidth
        lp_labely.height = self._labely_height
        lp_labely.textAnchor = self._textAnchor
        lp_labely.fontSize = self._labely_fontSize
        lp_labely.angle = 90
        #Chart settingss
        lp.x = self._chart_x
        lp.y = self._chart_y
        lp.height = self._chart_height
        lp.width = self._chart_width
        lp.xValueAxis.valueMin = 0
        lp.xValueAxis.valueMax = 360
        lp.xValueAxis.valueStep = 45

        ymin = min(min(self._data[6]), min(self._data[7]))
        ymax = max(max(self._data[6]), max(self._data[7]))

        self.initPressure(ymax)
        
        if(self._userPressureAdd !=0):
            lp.yValueAxis.valueMin = ymin - self.getUserPressureAdd()
            lp.yValueAxis.valueMax = ymax + self.getUserPressureAdd()
        else:
            lp.yValueAxis.valueMin = ymin - self.getPressureAdd()
            lp.yValueAxis.valueMax = ymax + self.getPressureAdd()
            
        if(self._userPressureTicks != 0):
            lp.yValueAxis.valueStep = self.getUserPressureTicks()
        else:
            lp.yValueAxis.valueStep = self.getPressureTicks()
        lp.yValueAxis.gridStrokeWidth = lp.xValueAxis.gridStrokeWidth = self._strokeWidth
        lp.yValueAxis.visibleGrid = lp.xValueAxis.visibleGrid = self._visibleGrid
        lp.yValueAxis.gridStrokeColor = lp.xValueAxis.gridStrokeColor = self._gridColor
        #Legend Settings
        lp_legend = Legend()
        lp_legend.colorNamePairs =  [(colors.blue, "HE"),(colors.red, "CE"),(colors.green, "Suction Pressure"),(colors.orange, "Discharge Pressure")]
        lp_legend.alignment = self._legend_alignment
        lp_legend.x = self._legend_x
        lp_legend.y = self._legend_y
        lp_legend.fontSize = self._legend_fontSize
        lp_legend.dxTextSpace = self._legend_dxTextSpace
        lp_legend.dy = self._legend_dy
        lp_legend.dx = self._legend_dx
        lp_legend.deltay = self._legend_deltay
        lp_legend.deltax = self._legend_deltax
        lp_legend.columnMaximum = lp_legend.variColumn = 1
        lp.data = [[],[],[],[]]
        #Crank vs PHE
        for x,y in zip(self._data[0],self._data[6]):
            test = (x,y)
            pressureSuction = (x,self._Ps)
            pressureDischarge = (x,self._Pd)
            lp.data[0].append(test)
            lp.data[2].append(pressureSuction)
            lp.data[3].append(pressureDischarge)
        #Crank vs PCE
        for x,y in zip(self._data[0],self._data[7]):
            test = (x,y)
            lp.data[1].append(test)

        lp.lines[0].strokeColor = colors.blue
        lp.lines[1].strokeColor = colors.red
        lp.lines[2].strokeColor = colors.green
        lp.lines[3].strokeColor = colors.orange
     
        drawing.add(lp)
        drawing.add(lp_label)
        drawing.add(lp_labelx)
        drawing.add(lp_labely)
        drawing.add(lp_legend)
        print("\t\t\t-> 'Cylinder Pressure Vs. Crank Angle' chart completely drawn with initial properites.")
        return drawing
    
    def CylinderPressureVsVolume(self):
        print("\t\t\t3. Creating chart 3 of 5: 'Cylinder Pressure Vs. Cylinder Volume'...")
        drawing = Drawing(self._drawing_width,self._drawing_height)
        lp = LinePlot()
        #Title
        lp_label = Label()
        lp_label._text = "CYLINDER PRESSURE VS VOLUME"
        lp_label.x = self._title_x
        lp_label.y = self._title_y
        lp_label.maxWidth = self._title_maxWidth
        lp_label.height = self._title_height
        lp_label.textAnchor = self._textAnchor
        lp_label.fontSize = self._title_fontSize
        #XAxis Label
        lp_labelx = Label()
        lp_labelx._text = "VOLUME(IN^3)"
        lp_labelx.x = self._labelx_x
        lp_labelx.y = self._labelx_y
        lp_labelx.maxWidth = self._labelx_maxWidth
        lp_labelx.height = self._labelx_height
        lp_labelx.textAnchor = self._textAnchor
        lp_labelx.fontSize = self._labelx_fontSize
        #YAxis Label
        lp_labely = Label()
        lp_labely._text = "PRESSURE (PSIA)"
        lp_labely.x = self._labely_x
        lp_labely.y = self._labely_y
        lp_labely.maxWidth = self._labely_maxWidth
        lp_labely.height = self._labely_height
        lp_labely.textAnchor = self._textAnchor
        lp_labely.fontSize = self._labely_fontSize
        lp_labely.angle = 90
        #Chart settingss
        lp.x = self._chart_x
        lp.y = self._chart_y
        lp.height = self._chart_height
        lp.width = self._chart_width
        lp.xValueAxis.valueMin = 0
        xmax = max(max(self._data[3]),max(self._data[4]))
        lp.xValueAxis.valueMax = xmax
        self.initVolume(xmax)

        if(self._userPressureAdd !=0):
            lp.xValueAxis.valueStep = self.getUserVolumeTicks()
        else:
            lp.xValueAxis.valueStep = self.getVolumeTicks()
            
        ymin = min(min(self._data[6]), min(self._data[7]))
        ymax = max(max(self._data[6]), max(self._data[7]))
        
        self.initPressure(ymax)
        
        if(self._userPressureAdd !=0):
            lp.yValueAxis.valueMin = ymin - self.getUserPressureAdd()
            lp.yValueAxis.valueMax = ymax + self.getUserPressureAdd()
        else:
            lp.yValueAxis.valueMin = ymin - self.getPressureAdd()
            lp.yValueAxis.valueMax = ymax + self.getPressureAdd()
            
        if(self._userPressureTicks != 0):
            lp.yValueAxis.valueStep = self.getUserPressureTicks()
        else:
            lp.yValueAxis.valueStep = self.getPressureTicks()
        lp.yValueAxis.gridStrokeWidth = lp.xValueAxis.gridStrokeWidth = self._strokeWidth
        lp.yValueAxis.visibleGrid = lp.xValueAxis.visibleGrid = self._visibleGrid
        lp.yValueAxis.gridStrokeColor = lp.xValueAxis.gridStrokeColor = self._gridColor
        #Legend Settings
        lp_legend = Legend()
        lp_legend.colorNamePairs =  [(colors.blue, "HE"),(colors.red, "CE"),(colors.green, "Suction Pressure"),(colors.orange, "Discharge Pressure")]
        lp_legend.alignment = self._legend_alignment
        lp_legend.x = self._legend_x
        lp_legend.y = self._legend_y
        lp_legend.fontSize = self._legend_fontSize
        lp_legend.dxTextSpace = self._legend_dxTextSpace
        lp_legend.dy = self._legend_dy
        lp_legend.dx = self._legend_dx
        lp_legend.deltay = self._legend_deltay
        lp_legend.deltax = self._legend_deltax
        lp_legend.columnMaximum = lp_legend.variColumn = 1
        lp.data = [[],[],[],[]]
        #HEVolume vs PHE
        for x,y in zip(self._data[3],self._data[6]):
            test = (x,y)
            lp.data[0].append(test)
        #CEVolume vs PCE
        for x,y in zip(self._data[4],self._data[7]):
            test = (x,y)
            lp.data[1].append(test)

        for x in range(0,int(xmax)):
            pressureSuction = (x,self._Ps)
            pressureDischarge = (x,self._Pd)
            lp.data[2].append(pressureSuction)
            lp.data[3].append(pressureDischarge)
            

        lp.lines[0].strokeColor = colors.blue
        lp.lines[1].strokeColor = colors.red
        lp.lines[2].strokeColor = colors.green
        lp.lines[3].strokeColor = colors.orange
     
        drawing.add(lp)
        drawing.add(lp_label)
        drawing.add(lp_labelx)
        drawing.add(lp_labely)
        drawing.add(lp_legend)
        print("\t\t\t-> 'Cylinder Pressure Vs. Cylinder Volume' chart completely drawn with initial properites.")
        return drawing
    
    def ValveLiftVsAngle(self):
        print("\t\t\t4. Creating chart 4 of 5: 'Valve Lift Vs. Crank Angle'...")
        drawing = Drawing(self._drawing_width,self._drawing_height)
        lp = LinePlot()
        #Title
        lp_label = Label()
        lp_label._text = "VALVE LIFT VS CRANK ANGLE"
        lp_label.x = self._title_x
        lp_label.y = self._title_y
        lp_label.maxWidth = self._title_maxWidth
        lp_label.height = self._title_height
        lp_label.textAnchor = self._textAnchor
        lp_label.fontSize = self._title_fontSize
        #XAxis Label
        lp_labelx = Label()
        lp_labelx._text = "CRANK ANGLE (DEG)"
        lp_labelx.x = self._labelx_x
        lp_labelx.y = self._labelx_y
        lp_labelx.maxWidth = self._labelx_maxWidth
        lp_labelx.height = self._labelx_height
        lp_labelx.textAnchor = self._textAnchor
        lp_labelx.fontSize = self._labelx_fontSize
        #YAxis Label
        lp_labely = Label()
        lp_labely._text = "VALVE LIFT (IN) "
        lp_labely.x = self._labely_x
        lp_labely.y = self._labely_y
        lp_labely.maxWidth = self._labely_maxWidth
        lp_labely.height = self._labely_height
        lp_labely.textAnchor = self._textAnchor
        lp_labely.fontSize = self._labely_fontSize
        lp_labely.angle = 90
        #Chart settingss
        lp.x = self._chart_x
        lp.y = self._chart_y
        lp.height = self._chart_height
        lp.width = self._chart_width
        lp.xValueAxis.valueMin = 0
        lp.xValueAxis.valueMax = 360
        lp.xValueAxis.valueStep = 45

        lp.yValueAxis.gridStrokeWidth = lp.xValueAxis.gridStrokeWidth = self._strokeWidth
        lp.yValueAxis.visibleGrid = lp.xValueAxis.visibleGrid = self._visibleGrid
        lp.yValueAxis.gridStrokeColor = lp.xValueAxis.gridStrokeColor = self._gridColor

        lp.yValueAxis.valueMin = 0
        lp.yValueAxis.valueMax = 0.2
        lp.yValueAxis.valueStep = 0.04
        #Legend Settings
        lp_legend = Legend()
        lp_legend.colorNamePairs =  [(colors.blue, "SVHE"),(colors.red, "DVHE"),(colors.green, "SVCE"),(colors.orange, "DVCE")]
        lp_legend.alignment = self._legend_alignment
        lp_legend.x = self._legend_x
        lp_legend.y = self._legend_y
        lp_legend.fontSize = self._legend_fontSize
        lp_legend.dxTextSpace = self._legend_dxTextSpace
        lp_legend.dy = self._legend_dy
        lp_legend.dx = self._legend_dx
        lp_legend.deltay = self._legend_deltay
        lp_legend.deltax = self._legend_deltax
        lp_legend.columnMaximum = lp_legend.variColumn = 1
        lp.data = [[],[],[],[]]
        #Crank vs SVHE1
        for x,y in zip(self._data[0],self._data[8]):
            test = (x,y)
            lp.data[0].append(test)
        #Crank vs DVHE1
        for x,y in zip(self._data[0],self._data[9]):
            test = (x,y)
            lp.data[1].append(test)
        #Crank vs SVCE1
        for x,y in zip(self._data[0],self._data[10]):
            test = (x,y)
            lp.data[2].append(test)
        #Crank vs DVCE1
        for x,y in zip(self._data[0],self._data[11]):
            test = (x,y)
            lp.data[3].append(test)  
        lp.lines[0].strokeColor = colors.blue
        lp.lines[1].strokeColor = colors.red
        lp.lines[2].strokeColor = colors.green
        lp.lines[3].strokeColor = colors.orange
     
        drawing.add(lp)
        drawing.add(lp_label)
        drawing.add(lp_labelx)
        drawing.add(lp_labely)
        drawing.add(lp_legend)
        print("\t\t\t-> 'Valve Lift Vs. Crank Angle' chart completely drawn with initial properites.")
        return drawing
    
    def ValveVelocityVsAngle(self):
        print("\t\t\t5. Creating chart 5 of 5: 'Valve Velocity Vs. Crank Angle'...")
        drawing = Drawing(self._drawing_width,self._drawing_height)
        lp = LinePlot()
        #Title
        lp_label = Label()
        lp_label._text = "VALVE ELEMENT VELOCITY VS CRANK ANGLE"
        lp_label.x = self._title_x
        lp_label.y = self._title_y
        lp_label.maxWidth = self._title_maxWidth
        lp_label.height = self._title_height
        lp_label.textAnchor = self._textAnchor
        lp_label.fontSize = self._title_fontSize
        #XAxis Label
        lp_labelx = Label()
        lp_labelx._text = "CRANK ANGLE (DEG)"
        lp_labelx.x = self._labelx_x
        lp_labelx.y = self._labelx_y
        lp_labelx.maxWidth = self._labelx_maxWidth
        lp_labelx.height = self._labelx_height
        lp_labelx.textAnchor = self._textAnchor
        lp_labelx.fontSize = self._labelx_fontSize
        #YAxis Label
        lp_labely = Label()
        lp_labely._text = "ELEMENT VELOCITY (FPS) "
        lp_labely.x = self._labely_x
        lp_labely.y = self._labely_y
        lp_labely.maxWidth = self._labely_maxWidth
        lp_labely.height = self._labely_height
        lp_labely.textAnchor = self._textAnchor
        lp_labely.fontSize = self._labely_fontSize
        lp_labely.angle = 90
        #Chart settingss
        lp.x = self._chart_x
        lp.y = self._chart_y
        lp.height = self._chart_height
        lp.width = self._chart_width
        lp.xValueAxis.valueMin = 0
        lp.xValueAxis.valueMax = 360
        lp.xValueAxis.valueStep = 45

        lp.yValueAxis.valueMin = -80
        lp.yValueAxis.valueMax =  80
        lp.yValueAxis.valueStep = 10
        lp.yValueAxis.gridStrokeWidth = lp.xValueAxis.gridStrokeWidth = self._strokeWidth
        lp.yValueAxis.visibleGrid = lp.xValueAxis.visibleGrid = self._visibleGrid
        lp.yValueAxis.gridStrokeColor = lp.xValueAxis.gridStrokeColor = self._gridColor        
        #Legend Settings
        lp_legend = Legend()
        lp_legend.colorNamePairs =  [(colors.blue, "SVHE"),(colors.red, "DVHE"),(colors.green, "SVCE"),(colors.orange, "DVCE")]
        lp_legend.alignment = self._legend_alignment
        lp_legend.x = self._legend_x
        lp_legend.y = self._legend_y
        lp_legend.fontSize = self._legend_fontSize
        lp_legend.dxTextSpace = self._legend_dxTextSpace
        lp_legend.dy = self._legend_dy
        lp_legend.dx = self._legend_dx
        lp_legend.deltay = self._legend_deltay
        lp_legend.deltax = self._legend_deltax
        lp_legend.columnMaximum = lp_legend.variColumn = 1
        lp.data = [[],[],[],[]]
        #Crank vs SVHE1
        for x,y in zip(self._data[0],self._data[12]):
            test = (x,y)
            lp.data[0].append(test)
        #Crank vs DVHE1
        for x,y in zip(self._data[0],self._data[13]):
            test = (x,y)
            lp.data[1].append(test)
        #Crank vs SVCE1
        for x,y in zip(self._data[0],self._data[14]):
            test = (x,y)
            lp.data[2].append(test)
        #Crank vs DVCE1
        for x,y in zip(self._data[0],self._data[15]):
            test = (x,y)
            lp.data[3].append(test)  
        lp.lines[0].strokeColor = colors.blue
        lp.lines[1].strokeColor = colors.red
        lp.lines[2].strokeColor = colors.green
        lp.lines[3].strokeColor = colors.orange
     
        drawing.add(lp)
        drawing.add(lp_label)
        drawing.add(lp_labelx)
        drawing.add(lp_labely)
        drawing.add(lp_legend)
        print("\t\t\t-> 'Valve Velocity Vs. Crank Angle' chart completely drawn with initial properites.")
        return drawing
        
    def CreateCanvas(self,index):
        print("Creating PDF...")
        canvas = Canvas("PDF_{0}_Cases.pdf".format(index), pagesize = landscape(letter))
        width, height = letter
        print("\tI. Creating page 1 of 2...")
        x,y = 0, 0
        self.CreateDataList()
        self.CreateValveConfigHeaderTable(canvas,width,height)
        self.CreateValveConfigDataTable(canvas,width,height)
        self.CreateOCHeaderTableTop(canvas,width,height)
        self.CreateOCHeaderTableBottom(canvas,width,height)
        self.CreateOCDataTable(canvas,width,height)
        self.CreateCylinderInfoHeaderTableTop(canvas,width,height)
        self.CreateCylinderInfoHeaderTableBottom(canvas,width,height)
        self.CreateCylinderInfoDataTable(canvas,width,height)
        self.CreateValveInfoHeaderTableTop(canvas,width,height)
        self.CreateValveInfoHeaderTableBottom(canvas,width,height)
        self.CreateValveInfoDataTable(canvas,width,height)
        canvas.rect(0.2*inch, 0.2*inch, 7*inch, 2*inch)
        
        canvas.showPage()
##        print("\t-> Page 1 of 2 created.")
##        print("\tII. Creating page 2 of 2...")    
##        for index in range(len(self._pathList)):
##            self._data.clear()
##            print("\t\t Chart {indexNum} of {listLength}".format(indexNum = index + 1, listLength = len(self._pathList)))
##            self._data = self.readCylinderData(index)
##            forces = self.ForceVsAngle()
##            pressureA = self.CylinderPressureVsAngle()
##            pressureV = self.CylinderPressureVsVolume()
##            lift = self.ValveLiftVsAngle()
##            velocity = self.ValveVelocityVsAngle()
##            #reverse order
##            renderPDF.draw(velocity, canvas, x, y, showBoundary = False)
##            renderPDF.draw(lift, canvas, x, y+160, showBoundary = False)
##            renderPDF.draw(pressureV, canvas, x, y+320, showBoundary = False)
##            renderPDF.draw(pressureA, canvas, x, y+480, showBoundary = False)
##            renderPDF.draw(forces, canvas, x, y+640, showBoundary = False)
##            canvas.showPage()
        print("-> PDF is complete: now saving to selected location...")
        canvas.save()
        print("Save complete.")
        print("You can now access the PDF.")
#pathList = [["./Cases/CNM_DNM", "/CNM_DNM"],["./Cases/DNM_ONM", "/DNM_ONM"],["./Cases/CNM_DNM", "/CNM_DNM"],["./Cases/DNM_ONM", "/DNM_ONM"],["./Cases/CNM_DNM", "/CNM_DNM"],["./Cases/DNM_ONM", "/DNM_ONM"],["./Cases/DNM_ONM", "/DNM_ONM"],["./Cases/DNM_ONM", "/DNM_ONM"]]
pathList = []
for i in range(1):
    pathList.append(["./Cases/CNM_DNM", "/CNM_DNM"])
    newPDF = PDF(pathList)
    newPDF.CreateCanvas(i+1)
