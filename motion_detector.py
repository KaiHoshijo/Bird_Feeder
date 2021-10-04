# using the opencv library to develop the motion detector for the birds
import cv2
# using the time module to keep track of photo tacking
import time
# adding the motion images to be searched and find
import get_bird_name
# getting the constants of the birdfeeder_constants
import birdfeeder_constants as bfc

def get_camera():
    """
        Returns the camera object for the python script to use
            Parameters:
                None
            Returns:
                A camera object from opencv
    """
    return cv2.VideoCapture(0)

def get_frame(cam):
    """
        Gets a current frame from the camera.
        Parameters:
            cam (opencv object): The camera to use for taking a photo
        Returns:
            A photo from the camera
    """
    # set initial color to read in a colored image
    color = cv2.IMREAD_COLOR
    # read in the frame
    ret1, frame1 = cam.read()
    # change color if necessary
    colored_image = cv2.cvtColor(frame1, color)
    return colored_image

def detect_motion(initial_frame, new_frame):
    """
        This function compares the initial frame and new frame to check
        if there has been motion.
        Parameters:
            initial_frame (cv2 frame): The frame to base the motion off of.
            new_frame (cv2 frame): The frame to check if there has been motion
        Returns:
            motion_frames (list): A list of sniped sections of the frame with
                                motion
    """
    # create the motion_frames list
    motion_frames = []
    # convert both to grayscale
    initial_frame = cv2.cvtColor(initial_frame, cv2.COLOR_BGR2GRAY)
    new_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
    
    # smooth out both images
    initial_frame = cv2.GaussianBlur(initial_frame, (25, 25), 0)
    new_frame = cv2.GaussianBlur(new_frame, (25, 25), 0)

    # get the absolute difference between the two
    deltaframe = cv2.absdiff(initial_frame, new_frame)

    # get the threshold of the difference
    threshold = cv2.threshold(deltaframe, 25, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=2)

    # find the contours of the threshold
    contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)

    # iterating through the contours
    for contour in contours:
        if cv2.contourArea(contour) < 50:
            continue
        
        # get a bounded rectangle
        (x, y, w, h) = cv2.boundingRect(contour)
        # append that new rectangle
        motion_frames.append((x, y, w, h))

    # return the motion_frames list
    return motion_frames

def find_bird():
    """
        This is the the overhead function that detects if there is motion or
        not in the current frame. Works by taking an initial frame at the
        beginning of a certain time line. If motion is detected, determined
        by having enough differences from the original photo, that the new
        photo is then processed and ran through the email_bird_photos script.
        Parameters:
            None
        Return:
            None
    """
    # get the camera
    cam = get_camera()
    while True:
        # initialize the initial frame timer
        INITIAL_FRAME_TIMER = 1800
        # get the initial time of the initial frame
        previous_initial_timer = time.time()
        while INITIAL_FRAME_TIMER >= 0:
            # get the initial frame once every 30 minutes (1800 seconds)
            initial_frame = get_frame(cam)
            # get the initial time of this scene
            MOTION_TIMER = 5
            previous_motion_time = time.time()
            # read frame every five seconds
            while MOTION_TIMER >= 0:
                # get the new frame
                new_frame = get_frame(cam)
                # get the current time
                current_motion_time = time.time()
                # compare initial time to initial time
                if current_motion_time - previous_motion_time >= 1:
                    # update previous time to be the current time
                    previous_motion_time = current_motion_time
                    # subtact motion timer by 1 second
                    MOTION_TIMER -= 1
                # compare new frame to initial frame
                motion_frames = detect_motion(initial_frame, new_frame)
                # if different, run get_bird_name.py script
                if (len(motion_frames) > 0) :
                    # write the new frame into the bird_images_locations directory
                    file_name = bfc.DIRECTORY_LOCATION + str(current_motion_time)
                    cv2.imwrite(file_name, new_frame)
                    # run get_bird_name.py script
                    get_bird_name.search_bird(file_name)
            # check the current initial time to the previous initial time
            current_initial_timer = time.time()
            if current_initial_timer - previous_initial_timer >= 0:
                # update the previous initial timer to the current timer
                previous_initial_timer = current_initial_timer
                INITIAL_FRAME_TIMER -= 1