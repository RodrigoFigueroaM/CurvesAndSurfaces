#!/usr/bin/env python
'''
DrawingWindow
----------
**DrawingWindow*** creates a GLStandardDrawingWindow from QGLWidget.
Implements : mousePressEvent
             mouseMoveEvent
             mouseReleaseEvent
             paintGL
attributes
----------
    *colorCounter to decide the color of the lines.
'''
import math
import array
import numpy
from PyQt5.QtGui import (QColor, QImage, QMatrix4x4, QOpenGLShader,
        QOpenGLShaderProgram, QOpenGLContext, QOpenGLTexture, QSurfaceFormat, QVector3D, QMouseEvent)
from PyQt5 import QtCore, QtGui
from PyQt5.QtOpenGL import QGLFormat
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import  QWidget
from MyPackages.qtPackage.GLStandardDrawingWindow3D import *
from OpenGL.arrays import vbo
from OpenGL.GL import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray
from OpenGL.arrays import vbo
from NURBSSurface import NURBSSurface
from camera import Camera

from enum import Enum
class axis(Enum):
    x = 1
    y = 2
    z = 3


class DrawingWindow(GLStandardDrawingWindow3D):

    vertexShaderSource= """
#version 120\n
uniform highp mat4 projectionMatrix;
uniform highp mat4 modelViewMatrix;
uniform highp mat4 normalMatrix; 

attribute highp vec4 vertexAtr; //.posAttr
attribute vec3 normalAttr; // .normals

varying vec3 normal;
varying vec4 vertex;

void main() 
{
    gl_Position =  projectionMatrix * modelViewMatrix * vertexAtr;
    
    normal = normalAttr;
    vertex = vertexAtr;
}

"""

    fragmentShaderSource ="""
#version 120\n

uniform highp mat4 projectionMatrix;
uniform highp mat4 modelViewMatrix;
uniform highp mat4 normalMatrix; 


varying vec3 normal;
varying vec4 vertex;

const vec3 lightPos = vec3(0.0, 20.0, 0.0);
const vec3 lightColor = vec3(1.0, 1.0, 1.0);

const vec3 ambientColor = vec3(0.3, 0.0, 0.3);
const vec3 diffuseColor = vec3(0.5, 0.5, 0.5);
const vec3 specularColor = vec3(1.0, 1.0, 1.0);
const vec3 emitColor = vec3(0.5, 0.0, 0.5);

const float shininess = 160.0;

const vec3 eyePos = vec3 (0,0,0);


void main() 
{
    vec4 tempVertex = modelViewMatrix * vertex;
    vec3 vrtx = tempVertex.xyz / tempVertex.w;

    vec4 tempNormal = normalMatrix * vec4(normal,0.0);
    vec3 nrml =  normalize(tempNormal.xyz);



    vec3 eyeDir = normalize(eyePos - vrtx); // V
    vec3 lightDir = normalize(lightPos - vrtx); //L
    vec3 halfVector = normalize(lightDir + eyeDir); //H

    //DIFFUSE 
    float NdotL = dot(nrml, lightDir );
    vec3 lambert = NdotL * diffuseColor * lightColor * max(NdotL ,0.0);

    //SPECULAR
    float NdotH = dot(nrml, halfVector);
    vec3  blinnPhong = lightColor * specularColor * pow( max(NdotH,0.0 ), shininess );


    gl_FragColor = vec4(lambert + blinnPhong + ambientColor , 1.0);
}
"""

    def __init__(self):
        super(DrawingWindow,self).__init__()
        self.history=[]
        self.userDefinedPoints = []
        self.setMouseTracking(True)

        #SURFACE setup
        self.ctrPnt = [
                    [ QVector3D( 10,0,10 ), QVector3D( 5,0,10 ), QVector3D( -5,0,10 ), QVector3D( -10,0,10 ) ],
                    [ QVector3D( 10,0,5), QVector3D( 5,10,5 ), QVector3D( -5,10,5 ), QVector3D( -10,0,5 ) ],
                    [ QVector3D( 10,0,-5 ), QVector3D(  5,10,-5  ), QVector3D( -5,10,-5  ), QVector3D( -10,0,-5 ) ],
                    [ QVector3D( 10,0,-10 ), QVector3D( 5,0,-10 ), QVector3D( -5,0,-10 ), QVector3D( -10,0,-10 ) ]
                    ] 

        self.vtr = []
        self.vertices = []
        self.indices =[]

        self.controlPoints = []
        self.rotationAxis = None


        for row in self.ctrPnt:
            for vector in row:
                self.controlPoints.append( float(vector.x()) )
                self.controlPoints.append( float(vector.y()) )
                self.controlPoints.append( float(vector.z()) )

        self.surface = NURBSSurface(
                controlNet = self.ctrPnt,
                Udegree = 3,
                Wdegree = 3,
                Uknots = [0, 0, 0, 0, 1, 1, 1, 1],
                Wknots = [0, 0, 0, 0, 1, 1, 1, 1])

        self.surface.setWeights([[1.0,1.0,1.0,1.0],[1.0,1.0,1.0,1.0],[1.0,1.0,1.0,1.0],[1.0,1.0,1.0,1.0]])
        self.surface.compute()
        self.vtr = self.surface.surfacePoints


        self.indices = triangleRenderer( row = 12, col = 11 )
        normalsList = normalsPerTriangle(self.vtr, self.indices)
        self.surfaceNormals = []
        self.normals = normalsPerVertex(normalsList, len(self.vtr))

        for value in self.vtr :
            self.vertices.append( float(value.x()) )
            self.vertices.append( float(value.y()) )
            self.vertices.append( float(value.z()) )

        for value in self.normals:
            self.surfaceNormals.append( float(value.x()) )
            self.surfaceNormals.append( float(value.y()) )
            self.surfaceNormals.append( float(value.z()) )

        #QTsetting
        glFormat  = QGLFormat()
        glFormat.setVersion( 3, 2 )
        glFormat.setProfile( QGLFormat.CoreProfile )
        QGLFormat.setDefaultFormat(glFormat)
        print(glFormat)

        #camera
        self.camera = Camera(  position = QVector3D (0,7,20),
                        direction =  QVector3D(0, 0, 0),
                        up = QVector3D(0,1,0) )

        self.normalMatrix = QMatrix4x4()

        #interaction
        self.selectedPoint = None
        self.editFlag = False
        self.showControlPoints = False


    def initializeGL(self):
        GL.glClearColor(0.15, 0.15, 0.15, 1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_LIGHTING)
        
        self.program = QOpenGLShaderProgram(self)
        self.program.addShaderFromSourceCode(QOpenGLShader.Vertex, self.vertexShaderSource)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, self.fragmentShaderSource)
        self.program.link()
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.vertexAtr = self.program.attributeLocation("vertexAtr")
        self.colAttr = self.program.attributeLocation("colAttr")

        self.projectionMatrixAttr = self.program.uniformLocation("projectionMatrix")
        self.modelViewMatrixAttr = self.program.uniformLocation("modelViewMatrix")
        self.normalMatrixAttr = self.program.uniformLocation("normalMatrix")

        self.normalAttr =  self.program.attributeLocation("normalAttr")

        self.controlPtsAttr = self.program.attributeLocation("controlPtsAttr")
        self.pressClick = QVector3D( 0, 0, 0)
        self.releaseClick = QVector3D( 0, 0, 0)
        self.programid = 0


      
       
    def paintGL(self):
        '''
        paintGL
        Updates the current object that is being drawn in screen.
        Draws whatever is on the history stack as a set of Vector3Ds
        '''
        GL.glClear(GL.GL_COLOR_BUFFER_BIT| GL.GL_DEPTH_BUFFER_BIT)
        GL.glViewport(0, 0,  self.width, self.height)
        GL.glMatrixMode(GL.GL_PROJECTION)
    
        ratio = self.width / self.height
        self.camera.setPerspective(self.fov, ratio, 1.0, 50.0)
        

        self.camera.lookAtCenter()   
        self.camera.rotate(self.xRot,0,0)
        self.camera.rotate(0,self.yRot,0)
        self.camera.rotate(0,0,self.zRot)


        self.normalMatrix = self.camera.modelViewMatrix.inverted()[0].transposed()
        
        self.program.bind()
        self.program.setUniformValue('modelViewMatrix', self.camera.modelViewMatrix)
        self.program.setUniformValue('normalMatrix', self.normalMatrix)
        self.program.setUniformValue('projectionMatrix', self.camera.projectionMatrix) 

        GL.glPointSize(5)
     

        GL.glEnableVertexAttribArray( self.vertexAtr)

        # GL.glPolygonMode( GL.GL_FRONT_AND_BACK ,GL.GL_LINE)
        GL.glVertexAttribPointer(self.vertexAtr, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, self.vertices)
        GL.glDrawElements(GL.GL_TRIANGLE_STRIP, len(self.indices) ,  GL_UNSIGNED_BYTE, self.indices)
  
        GL.glVertexAttribPointer(self.vertexAtr, 3, GL_FLOAT, GL_FALSE, 0, self.controlPoints)
        GL.glEnableVertexAttribArray(self.vertexAtr)
        GL.glDrawArrays(GL.GL_LINE_LOOP, 0, (len(self.controlPoints)//3) )

        GL.glVertexAttribPointer(self.vertexAtr, 3, GL_FLOAT, GL_FALSE, 0, self.controlPoints)
        GL.glEnableVertexAttribArray(self.vertexAtr)
        GL.glDrawArrays(GL.GL_POINTS, 0, (len(self.controlPoints)//3) )
           
        GL.glEnableVertexAttribArray( self.normalAttr)
        GL.glVertexAttribPointer(self.normalAttr, 3, GL_FLOAT, GL_FALSE, 0, self.surfaceNormals)   
       
        # GL.glDisableVertexAttribArray(self.colAttr)
        GL.glDisableVertexAttribArray(self.vertexAtr)
        # GL.glDisableVertexAttribArray(self.normalAttr)

        self.program.release()


    def mousePressEvent(self,  event):    
        if self.editFlag == False:
            self.pressClick = QVector3D(event.x(), self.height - event.y(), 1)
        else:
            begin, end = self.camera.mouseRay( event.x(), self.height - event.y(), 
                                              self.width, self.height)
            t = 0.0
            ray = begin
            while t < 100.0:
                ray = begin + t * (end - begin)
                for row in self.ctrPnt: 
                    self.selectedPoint = rayCollision(ray, row, 0.5)
                    if self.selectedPoint :
                        print('collision at {}'.format( self.selectedPoint ))
                        break
                else:
                    t += 0.1
                    continue
                break   

       
    def mouseMoveEvent(self, event):
        if self.editFlag == False:
            sensitivity = 0.05
            if event.buttons() == Qt.LeftButton:
                self.releaseClick = QVector3D(event.x(), self.height - event.y(), 1)

                angle = angleBetweenTwoVectors(self.pressClick, self.releaseClick)
              
                if self.rotationAxis is axis.x :
                    if  self.pressClick.y() < self.releaseClick.y():
                        angle *= -1 
                    self.xRot += angle * sensitivity
                    self.xRot %= 360

                elif self.rotationAxis is axis.z :
                    if  self.pressClick.x() < self.releaseClick.x():
                        angle *= -1 
                    self.zRot += angle * sensitivity
                    self.zRot %= 360

                elif self.rotationAxis is axis.y :
                    if  self.pressClick.x() < self.releaseClick.x():
                        angle *= -1 
                    self.yRot += angle * sensitivity
                    self.yRot %= 360
        else:
            if self.selectedPoint and event.buttons() == QtCore.Qt.LeftButton:
                one, two = self.camera.mouseRay( event.x(), self.height - event.y(), 
                                              self.width, self.height)
                two =  QVector3D(two.x(), two.y(), two.z()) / two.w()
                self.selectedPoint += (two - self.selectedPoint) 
                print(self.selectedPoint)
                self._updateControlPoints()
                self._updateSurface()
        self.update()

    def mouseReleaseEvent(self,  event):
        self.pressClick = self.releaseClick

        if self.editFlag == True:
            self.pressClick = QVector3D(0, 0, 1)
            self.releaseClick = QVector3D(0, 0,1)
            if self.selectedPoint:
                self.selectedPoint = None
        self.update()
          
    def setRotationAxis(self, rotationAxis = None):
        self.rotationAxis = rotationAxis


    def setEditFlag(self, status = None ):
        self.editFlag = status
        self.selectedPoint = None

        
    def setContontrolPoinsFalg(self, status = None ):
       self.showControlPoints = status

    def _updateControlPoints(self):
        for row in self.ctrPnt:
            i = 0 
            for vector in row:
                self.controlPoints[i * 3] = ( float(vector.x()) ) # 0,3,6
                self.controlPoints[(i * 3) + 1] = ( float(vector.y()) ) # 1,4,7
                self.controlPoints[(i * 3) + 2] = ( float(vector.z()) ) # 2,5,8
                i += 1

    def _updateSurface(self):
        self.vtr = [] 
        self.vertices = []
        self.surfaceNormals = []
        self.normals = [] 
        self.surface.compute()
        self.vtr = self.surface.surfacePoints


        self.indices = triangleRenderer( row = 12, col = 11 )
        normalsList = normalsPerTriangle(self.vtr, self.indices)
        self.normals = normalsPerVertex(normalsList, len(self.vtr))

        for value in self.vtr :
            self.vertices.append( float(value.x()) )
            self.vertices.append( float(value.y()) )
            self.vertices.append( float(value.z()) )

        for value in self.normals:
            self.surfaceNormals.append( float(value.x()) )
            self.surfaceNormals.append( float(value.y()) )
            self.surfaceNormals.append( float(value.z()) )
        pass

'''***************************************
*           HELPER FUNCTION
***************************************'''
def rayCollision(rayPoint, points, bounds):
    for point in points:
        if ( point.x() > rayPoint.x() - bounds
        and  point.x() < rayPoint.x() + bounds
        and  point.y() < rayPoint.y() + bounds
        and  point.y() > rayPoint.y() - bounds
        and  point.z() > rayPoint.z() - bounds
        and  point.z() < rayPoint.z() + bounds):
            return point
    return None

def triangleRenderer( row = 0 , col = 0):
    '''function to calculate the indices for a triangle strip based shader'''
    indices = []
    beg = 0
    end  = row -1
    for i in range(0, col - 1):#len(vertices)//3 - triangleStep):
        for j in range( beg, end ):
            indices.append( j )
            indices.append( j + row)
        indices.append( j + row)
        indices.append( (i + 1) * row )
        beg += row
        end += row
    return indices

def normalsPerTriangle(vertices = None, indices = None):
        triangleNormals = []
        i = 0
        for index in range( 0, len(indices) - 1 , 1):
            if indices[ index ] != indices[ index - 1] and  indices[ index ] != indices[ index + 1] and indices[ index - 1 ] != indices[ index + 1]:
                a = (vertices[indices[ index - 1 ]] - vertices[indices[ index ]])
                b = (vertices[indices[ index + 1 ]] - vertices[indices[ index ]])
                if index % 2 == 0: 
                    normal = QVector3D.crossProduct(b, a)
                else:
                    normal = QVector3D.crossProduct(a, b)
                triangleNormals.append([ i ,(indices[ index],indices[ index - 1],indices[ index + 2 ]), normal])
                i += 1
        return triangleNormals

def normalsPerVertex(faces = None, numberOfVertices = 0):
    # make sublist of vertices and triangles tahta affect the
    li =[]
    for index in range(0, numberOfVertices, 1):
        inli = []
        for face in faces:
            if index == face[1][0]:
                inli.append(face[0])
            if index == face[1][1]:
                 inli.append(face[0])
            if index == face[1][2]:
                 inli.append(face[0])
        li.append([index, inli])

    verticesNormals = []
    for row in li:
        normalsAvg = QVector3D(0,0,0)
        for index in row[1]:
            normalsAvg += faces[index][2]
        normalsAvg = normalsAvg / len(row[1]) 
        normalsAvg = normalsAvg.normalized()
        verticesNormals.append( normalsAvg )
    return verticesNormals



def angleBetweenTwoVectors(A = None, B = None):
    ABoverABmag = QVector3D.dotProduct(A, B) / (A.length() * B.length())
    if ABoverABmag > 0.999999:
        ABoverABmag = 1.0
    elif ABoverABmag < - 0.99999:
            ABoverABmag = -1.0
    return math.degrees( math.acos( ABoverABmag ))

