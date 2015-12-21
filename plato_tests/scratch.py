'''
Created on Dec 20, 2015

@author: mike
'''

class A(object):
    def __init__(self, yuck=''):
        print 'A: ' + yuck

class B(A):
    pass

if __name__ == '__main__':
    B('yolo')
    print 'done'