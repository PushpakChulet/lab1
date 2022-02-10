from OpenGL.GL import *
from OpenGL.GLUT import *

from geometry import *
from camera import *

camera = Camera('camera.txt')
geometry = Geometry('geometry.d.txt')
geometry.world_to_screen(camera)


def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(5.0)
    for polygon in geometry.polygon_list:
        if polygon[2]:
            glBegin(GL_LINE_LOOP)
            for index in polygon[0]:
                glVertex2f(geometry.screen_point_list[index][0], geometry.screen_point_list[index][1])
            glEnd()
    glFlush()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowSize(1280, 720)
    glutCreateWindow("LAB1")
    glutDisplayFunc(draw)
    glutMainLoop()
    return


if __name__ == '__main__':
    main()
