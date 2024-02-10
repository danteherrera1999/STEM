import matplotlib.pyplot as plt
import numpy as np

# Simple Quaternion class definition and demo to show how quaternion operations work

d2r = np.pi/180

class Q:
    def __init__(self,w,x,y,z):
        self.w = w
        self.v = np.array([x,y,z])
        self.mag = np.sqrt(self.w**2 + np.sum(self.v**2))
    def __str__(self):
        return "{"+f" {self.w}| {' '.join(self.v.astype(str).tolist())}"+" }"
    def __mul__(self,b):
        if isinstance(b,Q):
            return Q(self.w * b.w - np.dot(self.v,b.v),*(self.w*b.v)+b.w*self.v+np.cross(self.v,b.v))
        else:
            return Q(self.w*b,*self.v*b)
    def __add__(self, b):
        return Q(self.w+b.w,*self.v+b.v)
    def get_unit(self):
        return Q(self.w / self.mag, *self.v / self.mag)
    def get_theta(self):
        return np.arccos(self.w)*2
    def get_axis(self):
        return self.v / np.sin(self.get_theta()/2)
    def get_DCM(self):
        q1, q2, q3, q4 = *self.v,self.w
        return np.array([[q1 ** 2 - q2 ** 2 - q3 ** 2 + q4 ** 2, 2 * (q1 * q2 + q3 * q4), 2 * (q1 * q3 - q2 * q4)],
                        [2 * (q2 * q1 - q3 * q4), -q1 ** 2 + q2 ** 2 - q3 ** 2 + q4 ** 2,2*(q2*q3+q1*q4)],
                        [2 * (q3 * q1 + q2 * q4), 2 * (q3 * q2 - q1 * q4),-q1 ** 2 - q2 ** 2 + q3 ** 2 + q4 ** 2]])
gq = lambda theta,x,y,z: Q(np.cos(d2r*theta/2),x*np.sin(d2r*theta/2),y*np.sin(d2r*theta/2),z*np.sin(d2r*theta/2))

q1 = gq(90,0,0,1)
q2 = gq(90,0,1,0)
q3 = gq(90,1,0,0)
q4 = q1 * q2 * q3

print(q4)
print(q4.get_DCM())
print(q4.get_theta()/d2r)
print(q4.get_axis())

v = np.array([1,0,0])
print(np.matmul(q4.get_DCM(),v))
