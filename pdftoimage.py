from pdf2image import convert_from_path
import os


def save_pdf_as_image(pdf_file_path, output_folder):
    images = convert_from_path(pdf_file_path)
    if not os.path.exists(output_folder):
      os.mkdir(output_folder)
    
      for i in range(len(images)):  
        images[i].save('output/page'+ str(i + 1) +'.jpg', 'JPEG')


def test():
    save_pdf_as_image('test.pdf', 'output')


if __name__ == '__main__':
    test()

