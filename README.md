# 3D Rubik's Cube
I made a 3D functioning Rubik's Cube with Projection and Rotation Matrix.
![rubiks-video](example.gif)
(quality and frame rate are low due to the GIF format)
## How it works
The pygame library is used only to draw lines and polygons on the screen, all the logic and maths required for the 3D cube was done in my code.

To represent the 8 corners of the 3 dimensional cube I used 3-dimensional vectors, then I used Projection Matrix to Project the 3D dots to the 2D plane.

To rotate the entire cube a certain angle on a specific axis I multiplied each vector that represents a corner with the correct Rotation Matrix (each axis has it's own Rotation Matrix). 

To calculate and to differ the 9 colors of each face I used simple algebra of subtracting two vectors(corners) in order to find the distance between them and that way I could find the third and two-thirds points between the two corners.

## Controls 
* For a 90 degree rotation of the cube there is 4 arrows on screen to click on.
* For free hand rotation use the Arrow keys , Z and X. (note that you will need to press the center button that appears before keep turning the faces of the cube).
* To turn each face use the letters that are commonly used in the Rubik's Cube terminology:
  * F - turn the forward face clockwise (f key)
  * B - turn the back face clockwise (b key)
  * R - turn the right face clockwise (r key)
  * L - turn the left face clockwise (l key)
  * U - turn the up face clockwise (u key)
  * D - turn the down face clockwise (d key)
  * F' - turn the forward face counterclockwise (F key)
  * B' - turn the back face counterclockwise (B key)
  * R' - turn the right face counterclockwise (R key)
  * L' - turn the left face counterclockwise (L key)
  * U' - turn the up face counterclockwise (U key)
  * D' - turn the down face counterclockwise (D key)

## Little optimization
* Only rendering the 3 faces of the cube that are "closest" to the user, if we look at the cube we can see that no matter what position the cube is at, we can only see 3 faces of the cube (the 3 faces that are "closest" to the user), because rendering to the screen has one of the higher computational cost render only half the faces optimize the code and improve the performance.
* I used python dictionaries a lot because to my knowledge they have good performance and are superior to using a lot of if-else statements.
