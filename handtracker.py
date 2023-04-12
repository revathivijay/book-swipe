import cv2
import mediapipe as mp
from pdftoimage import save_pdf_as_image
import os
import shutil


def detect_swipe_right(landmarks, x_displacements, max_frames=15, swipe_right_count=0) -> bool:
  if len(x_displacements) == max_frames:
    x_displacements.pop(0)
  
  if landmarks:
    x_displacements.append(landmarks[0].landmark[0].x)
  else:
      x_displacements.append(None)

  if len(x_displacements) > 1 and all(x_displacements):
      print(f"actual displacement={x_displacements[-1] - x_displacements[0]}")
      x_disp = x_displacements[-1] - x_displacements[0]
  else:
      x_disp = None

  if x_disp is not None and x_disp > 0.02:
    swipe_right_count += 1
    if swipe_right_count >= 3:
      print(f"RIGHT SWIPED={swipe_right_count}")
      return True
  else:
      swipe_right_count = 0
      return False


def detect_swipe_left(landmarks, x_displacements, max_frames=15, swipe_left_count=0) -> bool:
  if len(x_displacements) == max_frames:
    x_displacements.pop(0)
  
  if landmarks:
    x_displacements.append(landmarks[0].landmark[0].x)
  else:
      x_displacements.append(None)

  if len(x_displacements) > 1 and all(x_displacements):
      print(f"actual displacement={x_displacements[-1] - x_displacements[0]}")
      x_disp = x_displacements[-1] - x_displacements[0]
  else:
      x_disp = None

  if x_disp is not None and x_disp < -0.2:
    swipe_left_count += 1
    if swipe_left_count >= 3:
      print(f"RIGHT SWIPED={swipe_left_count}")
      return True
  else:
      swipe_left_count = 0
      return False
  

def display_text_on_image(image, text):
  font = cv2.FONT_HERSHEY_SIMPLEX
  font_scale = 1
  thickness = 2

  # Get text size
  text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)

  # Define position of text (top right corner)
  x = image.shape[1] - text_size[0] - 10
  y = text_size[1] + 10

  # Write text on image
  cv2.putText(image, text, (x, y), font, font_scale, (0, 0, 255), thickness)


def main():
  mp_drawing = mp.solutions.drawing_utils
  mphands = mp.solutions.hands
  max_frames = 10
  x_displacements = []
  swipe_right_count = 0
  swipe_left_count = 0
  hands= mphands.Hands()
  cap = cv2.VideoCapture(0)


  page_map = {}

  output_path = os.path.join(os.getcwd(), 'output')
  save_pdf_as_image(os.path.join(os.getcwd(), 'test.pdf'), output_path)
  max_pages = len(os.listdir(output_path))
  all_files = os.listdir(output_path)
  for i in range(max_pages):
     page_map[i + 1] = output_path + '/page' + str(i + 1) + '.jpg'

  page_number = 1
  screen_width, screen_height = 1080, 720

  window_width = screen_width // 2
  window_height = screen_height

  while True:
    data, image = cap.read()
    #Flip the image
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image, hand_landmarks, mphands.HAND_CONNECTIONS)

    if len(x_displacements) == max_frames:
      x_displacements.pop(0)
  
    
    landmarks = results.multi_hand_landmarks

    if landmarks:
      x_displacements.append(landmarks[0].landmark[0].x)
    else:
        x_displacements.append(None)

    if len(x_displacements) > 2 and all(x_displacements):
        print(f"actual displacement={x_displacements[-1] - x_displacements[1]}")
        x_disp = x_displacements[-1] - x_displacements[0]
    else:
        x_disp = None

    if x_disp is not None and x_disp > 0.01:
      swipe_right_count += 1
      if swipe_right_count >= 3:
        print(f"RIGHT SWIPED={swipe_right_count}")
        display_text_on_image(image, 'Swiped Right')
        if page_number > 1:
          page_number -= 1
          print(f"Page Number={page_number}")
          x_displacements = []
    else:
        swipe_right_count = 0

    if x_disp is not None and x_disp < -0.01:
      swipe_left_count += 1
      if swipe_left_count >= 3:
        print(f"LEFT SWIPED={swipe_left_count}")
        if page_number < max_pages:
          page_number += 1
          print(f"Page Number={page_number}")
          x_displacements = []
        display_text_on_image(image, 'Swiped Left')
    else:
        swipe_left_count = 0

    img_to_display = cv2.imread(page_map[page_number])
    display_text_on_image(img_to_display, f'Page {page_number}')

    # cv2.namedWindow('Camera')
    # cv2.resizeWindow('Camera', window_width, window_height)
    # cv2.moveWindow('Camera', 0, 0)
    
    cv2.namedWindow('Book')
    cv2.resizeWindow('Book', window_width, window_height)
    cv2.moveWindow('Book', window_width, 0)
    
    
    
    cv2.imshow('Book', img_to_display)
    # cv2.imshow('Camera', image) 
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break





if __name__ == '__main__':
  main()