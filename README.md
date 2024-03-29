# Steganosaurus

![logo](https://github.com/Jonmainhart/cmsc495_final/blob/60704169467b502b7fdbc35e241c96bdf57c6f9f/Steganosaurus/assets/stego.png)

Capstone project for CMSC 495 at [University of Maryland Global Campus](https://www.umgc.edu).

Steganography is an information encoding technique that has been used throughout history to send secret messages without attracting attention. It is the practice of concealing a secret message in something that is not secret; a simple yet powerful technique for safeguarding and transmitting secret information.

*Steganosaurus* is an image-based steganography application written in Python 3.9 that allows users to explore one of the fundamental concepts of steganography by hiding text inside of an image. It allows users to both encode secret conversations and reveal the secret data contained in an image. The result of an encoded image is a seemingly exact replica of the original image imperceptibly changed to contain a secret message. The purpose of this software is to allow users to have fun and experience steganography in a user-friendly way that anyone can enjoy.

Why *Steganosaurus*? Steganosaurus is a portmanteau of *steganography* (which is what the program does) and *stegosaurus* (because dinosaurs are cool).

## How It Works

*Steganosaurus* encodes messages into images by first converting the message into its binary equivalent. Then, the binary message is used to shift the image's pixel values to be either odd for a binary 1, or even for a binary 0. Each character is eight bits and each pixel contains three color values, so each character uses three pixels. The ninth bit of each set of pixels is used as a control value. The ninth bit is set to an odd value (binary 1) at the end of the message. The decoder will stop when it encounters a binary 1 in the ninth position of a set of pixels and then process the message.

The decoder works in a similar way. The pixel data is read three pixels at a time. If the color values of the pixel are odd, a binary 1 is recorded, if it is even, a binary 0. If an even value (binary 0) is encountered in the ninth position of the set, a new set is read. If an odd value is encountered, decoding stops and the binary values are converted into characters.

[This tutorial](https://www.geeksforgeeks.org/image-based-steganography-using-python/) was used as the basis for this project and can provide additional context.

## Why use Steganosaurus?

You can use *Steganosaurus* to:

- Send secret messages to your friends
- Protect your 5th century battle plans
- Hide your grandmother’s secret cookie recipe from prying eyes (a secret worth keeping!)

## Contributors

[Linden Crandall](https://github.com/Crandy9)

[Jonathan Mainhart](https://github.com/Jonmainhart)

[Zhihua Zheng](https://github.com/Chika-KZ)

## User Guide

We think *Steganosaurus* is easy to use, but we created it so we may be a bit biased. Below you will find instructions on how to get started using the various features of *Steganosaurus*.

### Getting Started

1. Download or clone this repository to your local machine.
2. Navigate to the `../Steganosaurus/src` folder. Note that the exact location depends on where you cloned the application.
3. Install the required dependencies with the following:

`python3 -m pip install -r requirements.txt`

4. Type `python3 steganosaurus` and press Enter to launch the application.

Once launched, one of our default images will load and a decoded message will appear in the text area.

### Choose an Image

1. Click the “Open Image” button to open the file browser.
2. Navigate to the image file that you want to use for your steganography. Make sure that the file you select is of a proper image file type.

NOTE: Only image files with .jpg, .jpeg, or .png are allowed. An error will display if you attempt to load any other file type.

Your image will display in the window when successfully loaded.

### Decode an Image

The application will attempt to decode a stored message as soon as an image is loaded. The decoded message will be displayed in the text window below the image. Nothing will be displayed if the image selected does not contain a secret message.

NOTE: You may see a garbled message which does not make sense due to no message being encoded. This is a result of the decoder reading the pixels of the unaltered image which happen to be the binary equivalent of random characters. This is completely okay.

### Encode an Image

1. Open an image file (see Choosing an Image above).
2. Enter your secret message in the text field. The number of characters remaining along with the number of characters allowed will be displayed.

NOTE: The length of the allowed message will be limited by the size of the selected image.

3. Click the “Encode Image” button when you are ready to encode the message into the image.

Congratulations! You have successfully encoded an image using steganography! You may now save the image or reset the image to its original state.

### Reset an Image

If you change your mind, you can start over by removing an encoded message from an image before it is saved.

NOTE: Resetting an image can only be performed on newly encoded images. Saved images cannot be reset.

1. Click the “Reset Image” button.

When selected, any secret messages that you have encoded onto the image will be erased and the image will be restored to its unaltered original form from the time it was opened.

### Save an Image

You may save your image after successfully encoding a message.

1. Click the “Save Image” button. The File Explorer will open.
2. Navigate to the directory where your encoded image is to be saved.

NOTE: You may rename and save the image immediately after opening it before you begin the encoding process to make a copy and preserve the original image file.

Once saved, you can send your secret message as an attachment to an email, text message, or social medial post like any other image.

## To Contribute

Please submit an Issue or a Pull Request if you wish to contribute to this project.

Thank you for your interest in Steganosaurus!
