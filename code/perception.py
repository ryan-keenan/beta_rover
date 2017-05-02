import numpy as np
import cv2

# Define a function to perform a perspective transform
# I've used the example_grid1.jpg image (in calibration images folder)
# to choose source points for the
# grid cell in front of the rover (each grid cell is 1 square meter in the sim)
def perspect_transform(img, src, dst):
       
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))# keep same size as input image
    return warped

# Identify pixels above the threshold
# Threshold of RGB > 160 does a nice job of identifying ground pixels only
def color_thresh(img, rgb_thresh=(160, 160, 160)):
    # Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:,:,0])
    # Require that each pixel be above all three threshold values in RGB
    # above_thresh will now contain a boolean array with "True"
    # where threshold was met
    above_thresh = (img[:,:,0] > rgb_thresh[0]) \
                & (img[:,:,1] > rgb_thresh[1]) \
                & (img[:,:,2] > rgb_thresh[2])
    # Index the array of zeros with the boolean array and set to 1
    color_select[above_thresh] = 1
    # Return the binary image
    return color_select

# Define a function to convert to rover-centric coordinates
def rover_coords(binary_img):
    # Identify nonzero pixels
    ypos, xpos = binary_img.nonzero()
    # Calculate pixel positions with reference to the rover position being at the 
    # center bottom of the image.  
    y_pixel = np.absolute(ypos - binary_img.shape[0]).astype(np.float)
    x_pixel = (xpos - binary_img.shape[1]/2).astype(np.float)
    return x_pixel, y_pixel

# Define a function to convert to radial coords in rover space
def to_polar_coords(x_pixel, y_pixel):
    # Convert (x_pixel, y_pixel) to (distance, angle) 
    # in polar coordinates in rover space
    # Calculate distance to each pixel
    dist = np.sqrt(x_pixel**2 + y_pixel**2)
    # Calculate angle away from vertical for each pixel
    angles = np.arctan2(x_pixel, y_pixel)
    return dist, angles

# Define a function to map rover space pixels to world space
def pix_to_world(dist, angles, x_rover, y_rover, yaw_rover):
    # Map pixels from rover space to world coords
    pix_angles = angles + (yaw_rover * np.pi/180)    
    # Assume a worldmap size of 200 x 200
    world_size = 200
    # Assume factor of 10 scale change between rover and world space
    scale = 10
    x_pix_world = np.clip(np.int_((dist/scale * np.sin(pix_angles)) + (x_rover)), 0, world_size - 1)
    y_pix_world = np.clip(np.int_((dist/scale * np.cos(pix_angles)) + (y_rover)), 0, world_size - 1)
    return x_pix_world, y_pix_world

# Apply the above functions in succession and update the Rover state accordingly
def perception_step(Rover):
    # Perform perception steps to update Rover()
    # TODO: 
    # NOTE: camera image is coming to you in Rover.img
    # 1) Define source and destination points for perspective transform
    # 2) Apply perspective transform
    # 3) Apply color threshold to identify navigable terrain/obstacles/rock samples
    # 4) Update Rover.vision_image (this will be displayed on left side of screen)
        # Example: Rover.vision_image[:,:,0] = obstacle color-thresholded binary image
        #          Rover.vision_image[:,:,1] = rock_sample color-thresholded binary image
        #          Rover.vision_image[:,:,2] = navigable terrain color-thresholded binary image

    # 5) Convert rover-centric pixel values to world coordinates
    # 6) Update Rover worldmap (to be displayed on right side of screen)
        # Example: Rover.worldmap[obstacle_y_world, obstacle_x_world, 0] += 1
        #          Rover.worldmap[rock_y_world, rock_x_world, 0] += 1
        #          Rover.worldmap[navigable_y_world, navigable_x_world, 0] += 1

    # 7) Convert rover-centric pixel positions to polar coordinates
    # Update Rover pixel distances and angles
        # Rover.nav_dists = rover_centric_pixel_distances
        # Rover.nav_angles = rover_centric_angles
    
 
    
    
    return Rover