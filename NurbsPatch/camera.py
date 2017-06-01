from PyQt5.QtGui import (  QMatrix4x4, QSurfaceFormat, QVector3D, QVector4D)

class Camera(object):
	"""docstring for Camera"""
	def __init__(self, position = QVector3D (0,0,1),
						direction =  QVector3D(0, 0, 0),
						up = QVector3D(0,1,0)):
		super(Camera, self).__init__()
		self._pos = position
		self._dir = direction
		self._up = up
		self._projectionMatrix = QMatrix4x4()
		self._modelViewMatrix = QMatrix4x4()

	def setPerspective(self, fov = 90 , ratio = 100, near = 1.0, far = 2.0 ):
		self._projectionMatrix.setToIdentity()
		self._projectionMatrix.perspective(fov, ratio, near, far)

	def setFrustum(self, left = -1 , right= 1, bottom = -1, top = 1, near = 1, far = 2.0):
		self._projectionMatrix.setToIdentity()
		self._projectionMatrix.frustum( left , right, bottom, top, near, far)    

	def setProjectionMatrixToIdentity(self):
		self._projectionMatrix.setToIdentity()

	def setModelViewMatrixToIdentityt(self):
		self._modelViewMatrix.setToIdentity()

	def lookAtCenter(self):
		self._modelViewMatrix.setToIdentity()
		direction =  self._dir - self._pos
		self._modelViewMatrix.lookAt( self._pos, direction, self._up)

	def lookAt(self, position, direction , up):
		direction =  self.dir - self.pos
		self._pos = position
		self._dir = direction
		self._up = up
		self._modelViewMatrix.setToIdentity()
		self._modelViewMatrix.lookAt( self._pos, self._dir, self._up)

	def rotate(self, xangle, yangle, zangle):
		self._modelViewMatrix.rotate( xangle, 1, 0, 0)
		self._modelViewMatrix.rotate( yangle, 0, 1, 0)
		self._modelViewMatrix.rotate( zangle, 0, 0, 1)

	def translate(self, x, y, z):
		self._modelViewMatrix.transale( x, y, z)

	def mouseRay(self, xin, yin, width, height):
		near = -1.0
		far = 0.0
		rayBegin = self._rayDirection(xin, yin, width, height, near)
		rayEnd = self._rayDirection(xin, yin, width, height, far)
		return rayBegin, rayEnd 

	def _rayDirection(self, xin, yin, width, height, plane):
		x,y,z = self._devicePortCoordinates(xin, yin, width, height)
		clipCoord = QVector4D (x, y, plane, 1.0)
		eyeCoord = self._eyeSpace(clipCoord)
		ray = self._worldCoord(eyeCoord)
		return ray

	def _devicePortCoordinates(self, x, y, width, height):
		#bring mouse to device coordinates to opengl cordinates ranges [-1:1,xy]
		x -=  width / 2
		y -= height / 2

		y /= (height  / 2)
		x /= (width / 2)
		return x, y, -1.0

	def _eyeSpace(self, clipCoord):
		invertedProjectionMatrix = self.projectionMatrix.inverted()[0]
		eye = invertedProjectionMatrix * clipCoord
		return eye/eye.w()
		# return QVector4D (eye.x(), eye.y(), plane, 1.0)

	def _worldCoord(self, eyeCoord):
		invertedViewMatrix = self.modelViewMatrix.inverted()[0]
		worldCoord = invertedViewMatrix * eyeCoord
		return worldCoord/ worldCoord.w()
		# return QVector3D( worldCoord.x(), worldCoord.y(), worldCoord.z()) #try - somethin 

	def mouseWorld(self, xin, yin, width, height):
		mouse = self._mouseDirection(xin, yin, width, height, -1.0)
		return mouse

	def _mouseDirection(self, xin, yin, width, height, plane):
		x,y,z = self._devicePortCoordinates(xin, yin, width, height)
		clipCoord = QVector4D (x, y, plane, 0.0)
		eyeCoord = self._mouseEyeSpace(clipCoord)
		ray = self._mouseWorldCoord(eyeCoord)
		return ray

	def _mouseEyeSpace(self, clipCoord):
		invertedProjectionMatrix = self.projectionMatrix.inverted()[0]
		eye = invertedProjectionMatrix * clipCoord
		return QVector4D (eye.x(), eye.y(), -1.0, 0.0)

	def _mouseWorldCoord(self, eyeCoord):
		invertedViewMatrix = self.modelViewMatrix.inverted()[0]
		worldCoord = invertedViewMatrix * eyeCoord
		# return worldCoord/ worldCoord.w()
		return QVector3D( worldCoord.x(), worldCoord.y(), worldCoord.z()) #try - somethin 


	@property
	def position (self):
		return self._pos

	@position.setter
	def position (self, position):
		self._pos = position

	@property
	def direction (self):
		return self._dir

	@direction.setter
	def direction (self, direction):
		self._dir = direction

	@property
	def up (self):
		return self._up

	@up.setter
	def up (self, up):
		self._up = up

	@property
	def projectionMatrix(self):
		return self._projectionMatrix

	@projectionMatrix.setter
	def projectionMatrix (self, projectionMatrix):
		self._projectionMatrix.setToIdentity()
		self._projectionMatrix = projectionMatrix

	@property
	def modelViewMatrix(self):
		return self._modelViewMatrix

	@modelViewMatrix.setter
	def modelViewMatrix (self, modelViewMatrix):
		self._modelViewMatrix.setToIdentity()
		self._modelViewMatrix = modelViewMatrix

	def __str__(self):
		return 'position:{}\ndirection: {}\nup:{}\n'.format( self._pos, self._dir, self._up)

if __name__ == '__main__':
	camera = Camera()
	print(camera)
	camera.rotate(60,60,60)
	print(camera)


