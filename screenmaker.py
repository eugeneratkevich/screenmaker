import custTray
import wx
from PIL import ImageGrab
import time
from time import sleep
import win32con #for the VK keycodes
 
 # http://stackoverflow.com/questions/8263513/show-another-window-wxpython
 # http://stackoverflow.com/questions/11200703/showing-another-window-frame-in-wxpython
 
########################################################################
class MainFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="create screenshot", size=(400, 330))
        self.imagescreenpath = ''
        self.imagescreenXs = 0
        self.imagescreenYs = 0
        self.imagescreenXf = 0
        self.imagescreenYf = 0
        self.PhotoMaxSize = 340
        self.lastMousePos = wx.Point(0, 0)



        # panel = wx.Panel(self)
        panel = wx.Panel(self, -1, (20, 20), (self.PhotoMaxSize, 200))
        self.panel = panel
        self.tbIcon = custTray.CustomTaskBarIcon(self)
 
        self.Bind(wx.EVT_ICONIZE, self.onMinimize)
        self.Bind(wx.EVT_CLOSE, self.onClose)
 
        self.imageCtrl = wx.StaticBitmap(panel)
        # panel.SetBackgroundColour(wx.WHITE)

        # panel.CaptureMouse()

        # myCursor= wx.StockCursor(wx.CURSOR_CROSS)
        # self.SetCursor(myCursor)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDownTestWin)



        wx.Button(self, 1, 'create screenshot', (140, 240), (120, 28))
        self.Bind(wx.EVT_BUTTON, self.OnScreen, id=1)
        self.Hide()
        # self.Centre()
        # self.Show()

        self.regHotKey()
        self.Bind(wx.EVT_HOTKEY, self.handleHotKey, id=self.hotKeyId)



    def OnLeftDownTestWin(self, event):
        self.imagescreenXs, self.imagescreenYs = wx.GetMousePosition()
        self.panel.SetPosition(wx.Point(self.imagescreenXs, self.imagescreenYs))

        self.Bind(wx.EVT_MOTION, self.OnFrame1Motion)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUpTestWin)

        print 'start'
        # print x
        # print y

    def OnLeftUpTestWin(self, event):
        self.imagescreenXf, self.imagescreenYf = wx.GetMousePosition()
	
        self.OnScreen(event)
        # print 'end'
        # print x
        # print y

    def OnFrame1Motion(self, event):
        if event.LeftIsDown():
            x, y = event.GetPosition()

            self.panel.SetPosition(wx.Point(self.imagescreenXs, self.imagescreenYs))
            self.panel.SetSize(wx.Size(x-self.imagescreenXs, y-self.imagescreenYs))
            print 'move main'
            print self.imagescreenXs
            print self.imagescreenXs - x
            print x

            deltaX = x - self.lastMousePos[0]
            deltaY = y - self.lastMousePos[1]
            self.lastMousePos = wx.Point(x, y)
            x, y = self.GetPosition()
            # self.Move(wx.Point(x + deltaX, y + deltaY))
        event.Skip()


    def regHotKey(self):
        """
        This function registers the hotkey Alt+C with id=101
        """
        self.hotKeyId = 101
        self.RegisterHotKey(
            self.hotKeyId, #a unique ID for this hotkey
            win32con.MOD_ALT, #the modifier key
            # win32con.MOD_CONTROL, #the modifier key
            ord('C'),
            # win32con.VK_F1,
            ) #the key to watch for

    def handleHotKey(self, event):
        self.child = ScreenFrame(self)
        self.child.Show()
        # self.OnScreen(event)
        """
        Prints a simple message when a hotkey event is received.
        """
        # x, y = wx.GetMousePosition()
        # print x
        print "do hot key main actions"






    def OnScreen(self, event):
        self.Hide()
        sleep(0.3)
        # im = ImageGrab.grab()

        print self.imagescreenXs
        print self.imagescreenYs
        print self.imagescreenXf
        print self.imagescreenYf

        if (
            (self.imagescreenXs == 0 or self.imagescreenYs == 0)
            or (self.imagescreenXf == 0 or self.imagescreenYf == 0)
            or (self.imagescreenXs == self.imagescreenXf)
            or (self.imagescreenYs == self.imagescreenYf)
            ):
            self.Show()
            return

        self.SetBackgroundColour('#4f5049')


        #self.panel.SetPosition(wx.Point(self.imagescreenXs, self.imagescreenYs))
        #self.panel.SetSize(wx.Size(self.imagescreenXf - self.imagescreenXs, self.imagescreenYf - self.imagescreenYs))


        im=ImageGrab.grab(bbox=(
            self.imagescreenXs, self.imagescreenYs,
            self.imagescreenXf, self.imagescreenYf
        )) # X1,Y1,X2,Y2
        # f=open(os.path.normpath(os.path.join(self.dirname+os.sep,self.filename)),'r')
        self.imagescreenpath = 'screen/screenshot' +time.strftime('%Y%m%d%H%M%S')+'.png'
        im.save(self.imagescreenpath)
        self.imageCtrl.SetFocus()
        self.imageCtrl.SetBitmap(wx.Bitmap(self.imagescreenpath))

        
        img = wx.Image(self.imagescreenpath, wx.BITMAP_TYPE_ANY)
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW,NewH)
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))

        self.Show()
        # self.Restore()
        self.Show()








    #----------------------------------------------------------------------
    def onClose(self, evt):
        """
        Destroy the taskbar icon and the frame
        """
        self.tbIcon.RemoveIcon()
        self.tbIcon.Destroy()
        self.Destroy()
 
    #----------------------------------------------------------------------
    def onMinimize(self, event):
        """
        When minimizing, hide the frame so it "minimizes to tray"
        """
        self.Hide()
 






















class ScreenFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Frame.__init__(self, None, title="create screenshot", size=(400, 330),  style = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.imagescreenpath = ''
        self.imagescreenXs = 0
        self.imagescreenYs = 0
        self.imagescreenXf = 0
        self.imagescreenYf = 0
        self.PhotoMaxSize = 340
        self.lastMousePos = wx.Point(0, 0)
        self.parent = parent

        self.ToggleWindowStyle(wx.STAY_ON_TOP)

        # panel = wx.Panel(self)
        self.panel = wx.Panel(self, -1, (20, 20), (self.PhotoMaxSize, 200))
        self.SetTransparent(200)
        self.Maximize(True)
        # self.tbIcon = custTray.CustomTaskBarIcon(self)
        self.imageCtrl = wx.StaticBitmap(self.panel)
        self.panel.SetBackgroundColour(wx.WHITE)

        # panel.CaptureMouse()

        myCursor= wx.StockCursor(wx.CURSOR_CROSS)
        self.SetCursor(myCursor)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDownScreenWin)

        # self.Bind(wx.EVT_LEFT_UP, self.OnLeftUpTestWin)

        # myCursor= wx.StockCursor(wx.CURSOR_CROSS)
        # self.SetCursor(myCursor)
        # self.CaptureMouse()
        # self.WarpPointer(100, 100)

        

        # wx.Button(self, 1, 'create screenshot', (140, 240), (120, 28))
        # wx.Button(self, 2, 'Close', (260, 240))

        # self.Bind(wx.EVT_BUTTON, self.OnScreen, id=1)
        # self.Bind(wx.EVT_BUTTON, self.OnClose, id=2)

        self.Centre()
        self.Show()
        self.parent.Hide()


        # self.regHotKey()
        # self.Bind(wx.EVT_HOTKEY, self.handleHotKey, id=self.hotKeyId)



    def OnLeftDownScreenWin(self, event):
        print 'OnLeftDownScreenWin'

        self.imagescreenXs, self.imagescreenYs = wx.GetMousePosition()
        self.panel.SetPosition(wx.Point(self.imagescreenXs, self.imagescreenYs))
        
        self.Bind(wx.EVT_MOTION, self.OnScreenCursorMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUpScreenWin)

        print 'start'
        print x
        print y

    def OnLeftUpScreenWin(self, event):
        self.imagescreenXf, self.imagescreenYf = wx.GetMousePosition()
    
        self.OnScreen(event)
        print 'end'
        print x
        print y

    def OnScreenCursorMotion(self, event):
        if event.LeftIsDown():
            x, y = event.GetPosition()

            self.panel.SetPosition(wx.Point(self.imagescreenXs, self.imagescreenYs))
            self.panel.SetSize(wx.Size(x-self.imagescreenXs, y-self.imagescreenYs))
            print 'move screen'
            print self.imagescreenXs
            print self.imagescreenXs - x
            print x

            deltaX = x - self.lastMousePos[0]
            deltaY = y - self.lastMousePos[1]
            self.lastMousePos = wx.Point(x, y)
            x, y = self.GetPosition()
            # self.Move(wx.Point(x + deltaX, y + deltaY))
        event.Skip()


    # def regHotKey(self):
    #     """
    #     This function registers the hotkey Alt+C with id=101
    #     """
    #     self.hotKeyId = 101
    #     self.RegisterHotKey(
    #         self.hotKeyId, #a unique ID for this hotkey
    #         win32con.MOD_ALT, #the modifier key
    #         # win32con.MOD_CONTROL, #the modifier key
    #         ord('C'),
    #         # win32con.VK_F1,
    #         ) #the key to watch for

    # def handleHotKey(self, event):
    #     self.OnScreen(event)
    #     """
    #     Prints a simple message when a hotkey event is received.
    #     """
    #     # x, y = wx.GetMousePosition()
    #     # print x
    #     print "do hot key actions"






    def OnScreen(self, event):
        self.Hide()
        sleep(0.3)
        # im = ImageGrab.grab()

        print self.imagescreenXs
        print self.imagescreenYs
        print self.imagescreenXf
        print self.imagescreenYf

        if (
            (self.imagescreenXs == 0 or self.imagescreenYs == 0)
            or (self.imagescreenXf == 0 or self.imagescreenYf == 0)
            or (self.imagescreenXs == self.imagescreenXf)
            or (self.imagescreenYs == self.imagescreenYf)
            ):
            self.Show()
            return

        self.SetBackgroundColour('#4f5049')


        #self.panel.SetPosition(wx.Point(self.imagescreenXs, self.imagescreenYs))
        #self.panel.SetSize(wx.Size(self.imagescreenXf - self.imagescreenXs, self.imagescreenYf - self.imagescreenYs))


        im=ImageGrab.grab(bbox=(
            self.imagescreenXs, self.imagescreenYs,
            self.imagescreenXf, self.imagescreenYf
        )) # X1,Y1,X2,Y2
        # f=open(os.path.normpath(os.path.join(self.dirname+os.sep,self.filename)),'r')
        self.imagescreenpath = 'screen/screenshot' +time.strftime('%Y%m%d%H%M%S')+'.png'
        im.save(self.imagescreenpath)
        self.imageCtrl.SetFocus()
        self.imageCtrl.SetBitmap(wx.Bitmap(self.imagescreenpath))

        
        img = wx.Image(self.imagescreenpath, wx.BITMAP_TYPE_ANY)
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW,NewH)
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))

        self.Show()
        # self.Restore()
        self.Show()







 
    #----------------------------------------------------------------------
    def onClose(self, evt):
        """
        Destroy the taskbar icon and the frame
        """
        self.tbIcon.RemoveIcon()
        self.tbIcon.Destroy()
        self.Destroy()
 



#----------------------------------------------------------------------
def main():
    """"""
    app = wx.App(False)
    frame = MainFrame()
    # frame.ShowFullScreen(True,wxFULLSCREEN_ALL)
    app.MainLoop()
 
if __name__ == "__main__":
    main()