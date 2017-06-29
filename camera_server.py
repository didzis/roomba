#!/usr/bin/env python3

import io
import socket
import struct
from PIL import Image
import picamera
import time

import traceback

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

camera = None

# Accept a single connection and make a file-like object out of it
while True:
    try:
        conn,addr = server_socket.accept()
        # connection = server_socket.accept()[0].makefile('wb')
        # connection = conn
        # connection = conn.makefile('wb')
        connection = conn.makefile('wb')
        # connection_in = conn.makefile('rb')
        print('new connection accepted')
        try:
            if not camera:
                camera = picamera.PiCamera()
            camera.resolution = (640, 480)
            # camera.resolution = (320, 240)
            # Start a preview and let the camera warm up for 2 seconds
            camera.start_preview()
            time.sleep(2)
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                print('.', end='', flush=True)
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                # Rewind the stream and send the image data over the wire
                stream.seek(0)
                connection.write(stream.read())
                # If we've been capturing for more than 30 seconds, quit
                # if time.time() - start > 30:
                #     break
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()

                conn.recv(1)
                # connection_in.read(1)
            # Write a length of zero to the stream to signal we're done
            # connection.write(struct.pack('<L', 0))

            # while True:
            #     # Read the length of the image as a 32-bit unsigned int. If the
            #     # length is zero, quit the loop
            #     image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            #     if not image_len:
            #         break
            #     # Construct a stream to hold the image data and read the image
            #     # data from the connection
            #     image_stream = io.BytesIO()
            #     image_stream.write(connection.read(image_len))
            #     # Rewind the stream, open it as an image with PIL and do some
            #     # processing on it
            #     image_stream.seek(0)
            #     image = Image.open(image_stream)
            #     print('Image is %dx%d' % image.size)
            #     image.verify()
            #     print('Image is verified')
        finally:
            camera.stop_preview()
            # Write a length of zero to the stream to signal we're done
            connection.write(struct.pack('<L', 0))
            connection.close()
    except KeyboardInterrupt:
        server_socket.close()
        print('Interrupted!')
        break
    except BrokenPipeError:
        print('Broken pipe')
    except:
        traceback.print_exc()

