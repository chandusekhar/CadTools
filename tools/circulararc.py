# -*- coding: latin1 -*-
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import math

class CircularArc: 
    def getInterpolatedArc(ptStart,  ptArc, ptEnd,  method,  interValue):
        
        coords = []
        coords.append(ptStart)
        
        arcIncr = 1
        
        center = CircularArc.getArcCenter(ptStart,  ptArc, ptEnd)
        
        print str(center.toString())
    
        cx = center.x()
        cy = center.y()
        
        px = ptArc.x() 
        py = ptArc.y()
        r = ( ( cx-px ) * ( cx-px ) + ( cy-py ) * ( cy-py ) ) ** 0.5;      

        ## If the method is "pitch" (=Pfeilh�he) then
        ## we need to calculate the corresponding
        ## angle.
        if method == "pitch":
            myAlpha = 2.0 * math.acos( 1.0 - ( interValue / 1000 ) / r );
            arcIncr = myAlpha
            print "myAlpha: " + str(myAlpha)


        a1 = math.atan2( ptStart.y() - center.y(), ptStart.x() - center.x() );
        a2 = math.atan2( ptArc.y() - center.y(), ptArc.x() - center.x() );
        a3 = math.atan2( ptEnd.y() - center.y(), ptEnd.x() - center.x() );

        # Clockwise
        if a1 > a2 and a2 > a3:
            sweep = a3 - a1;

        # Counter-clockwise
        elif a1 < a2 and a2 < a3: 
            sweep = a3 - a1

        # Clockwise, wrap
        elif (a1 < a2 and a1 > a3) or (a2 < a3 and a1 > a3):
            sweep = a3 - a1 + 2*math.pi

        # Counter-clockwise, wrap
        elif (a1 > a2 and a1 < a3) or (a2 > a3 and a1 < a3):
            sweep = a3 - a1 - 2*math.pi

        else:
            sweep = 0.0;

        ptcount = math.ceil( math.fabs ( sweep / arcIncr ) )

        if sweep < 0: 
            arcIncr *= -1.0;

        angle = a1;

        for i in range(0,  ptcount-1):
            angle += arcIncr;

            if arcIncr > 0.0 and angle > math.pi:
                angle -= 2*math.pi
                
            if arcIncr < 0.0 and angle < -1*math.pi:
                angle -= 2*math.pi

            x = cx + r * math.cos(angle);
            y = cy + r * math.sin(angle);

            point = QgsPoint(x,  y)
            coords.append(point)
            print str(point.toString())
            
            if angle < a2 and (angle +arcIncr) > a2:
                coords.append(ptArc)

            if angle > a2 and (angle + arcIncr) < a2:
                coords.append(ptArc)

        coords.append(ptEnd)
        g = QgsGeometry.fromPolyline(coords)
        return g


    def getArcCenter(ptStart,  ptArc,  ptEnd):
        bx = ptStart.x()
        by = ptStart.y()
        cx = ptArc.x()
        cy = ptArc.y()
        dx = ptEnd.x()
        dy = ptEnd.y()
        
        temp = cx * cx + cy * cy
        bc = (bx * bx + by * by - temp) / 2.0
        cd = (temp - dx * dx - dy * dy) / 2.0
        det = (bx - cx) * (cy - dy) - (cx - dx) * (by - cy)

        det = 1 / det

        x = (bc * (cy - dy) - cd * (by - cy)) * det
        y = ((bx - cx) * cd - (cx - dx) * bc) * det

        return QgsPoint(x, y); 

        
#        if dist == 0:
#            points = [p1,  p2]
#            g = QgsGeometry.fromPolyline(points)
#            return g
#    
#        dn = ( (p1.x()-p2.x())**2 + (p1.y()-p2.y())**2 )**0.5
#        x3 = p1.x() + dist*(p1.y()-p2.y()) / dn
#        y3 = p1.y() - dist*(p1.x()-p2.x()) / dn  
#        p3 = QgsPoint(x3,  y3)       
#      
#        x4 = p2.x() + dist*(p1.y()-p2.y()) / dn
#        y4 = p2.y() - dist*(p1.x()-p2.x()) / dn  
#        p4 = QgsPoint(x4,  y4)       
#        
#        points =  [p3,  p4]
#        g = QgsGeometry.fromPolyline(points)
#        
#        return g


        
    getInterpolatedArc = staticmethod(getInterpolatedArc)
    getArcCenter = staticmethod(getArcCenter)
