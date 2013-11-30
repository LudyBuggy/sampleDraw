from Tkinter import Frame, Canvas, YES, BOTH
import Leap

class TouchPointListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"
        self.size = 5

    def on_connect(self, controller):
        print "Connected"

    def convertLeepCordsToCanvas(self,position,frame):
        interactionBox = frame.interaction_box
        normalizedPosition = interactionBox.normalize_point(position)
        return normalizedPosition.x * self.paintCanvas.winfo_width(), self.paintCanvas.winfo_height()  - normalizedPosition.y * self.paintCanvas.winfo_height()

    def on_frame(self, controller):
        if len(self.paintCanvas.find_withtag('pre')) != 0:
            self.paintCanvas.delete("all")

        frame = controller.frame()

        linetest = self.paintCanvas.find_withtag('touch')
        if len(linetest) > 0:
            list_of_screen_coods=[]
            for point in linetest[-4:-1]:
                corrds = self.paintCanvas.coords(point)
                list_of_screen_coods.append([corrds[0],corrds[1]])
            #print list_of_screen_coods

            for (x0,y0,x1,y1) in self.linemaker(list_of_screen_coods):
                self.paintCanvas.create_line(x0,y0,x1,y1, width=self.size,fill="red")


        for pointable in frame.pointables:

            posX,posY = self.convertLeepCordsToCanvas(pointable.tip_position,frame)
            self.draw(posX,posY, self.size, self.size, pointable)

    def linemaker(self,screen_points):
    # Function to take list of points and make them into lines
    #    http://stackoverflow.com/a/16495875
    #
        is_first = True
        # Set up some variables to hold x,y coods
        x0 = y0 = 0
        # Grab each pair of points from the input list
        for (x,y) in screen_points:
            # If its the first point in a set, set x0,y0 to the values
            if is_first:
                x0 = x
                y0 = y
                is_first = False
            else:
                # If its not the fist point yeild previous pair and current pair
                yield x0,y0,x,y
                # Set current x,y to start coords of next line
                x0,y0 = x,y

    def draw(self, x, y, width, height, pointable):
        tag = ''
        if(pointable.touch_distance > 0 and pointable.touch_zone != Leap.Pointable.ZONE_NONE):
            color = self.rgb_to_hex((0, 255 - 255 * pointable.touch_distance, 0))
            tag='hover'

        elif(pointable.touch_distance <= 0):
            color = self.rgb_to_hex((-255 * pointable.touch_distance, 0, 0))
            #color = '#FFFFFF'
            tag='touch'
            width = 0
            height = 0

        else:
            color = self.rgb_to_hex((0,0,200))
            tag='pre'

        if (pointable.is_tool)  :
            tool = Leap.Tool(pointable)
            self.paintCanvas.create_oval( x, y, x + width, y + height, fill = color, outline = "", tag=tag)
        else:
            finger = Leap.Finger(pointable)
            self.paintCanvas.create_oval( x, y, x + width, y + height, fill = color, outline = "", tag=tag)

    def set_canvas(self, canvas):
        self.paintCanvas = canvas

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

class PaintBox(Frame):

    def __init__( self ):
        Frame.__init__( self )
        self.leap = Leap.Controller()
        self.painter = TouchPointListener()
        self.leap.add_listener(self.painter)
        self.pack( expand = YES, fill = BOTH )
        self.master.title( "Touch Points" )
        self.master.geometry( "800x600" )

        # create Canvas component
        self.paintCanvas = Canvas( self, width = "800", height = "600" )
        self.paintCanvas.pack()
        self.painter.set_canvas(self.paintCanvas)

def main():
    PaintBox().mainloop()

if __name__ == "__main__":
    main()