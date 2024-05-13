import PIL
import sacn

if __name__ == '__main__':
    from PIL import ImageGrab

    sender = sacn.sACNsender()
    sender.start()
    sender.activate_output(1)
    sender[1].multicast = True
    sender.manual_flush = True

    # Capture a specific region (x1 :left, y1:top, x2: right,y2:  bottom)
    first = ImageGrab.grab(bbox=(0, 0, 1920, 1080), include_layered_windows=True)

    rgb = first.load()[10, 10]
    print(rgb)

    # screenshot.save("screenshot.png")

    size = first.size
    print("x/y", size)

    numbersChunkX = 10

    chunkY = 100
    chunkX = size[1] / 10
    chunk = chunkX, chunkY
    pixelInChunk = chunkX * chunkY
    chunkCount = 16

    while True:
        screenshot = ImageGrab.grab(bbox=(0, 0, 1920, 1080), include_layered_windows=True)
        data = []
        for i in range(chunkCount):
            r = 0
            g = 0
            b = 0
            for x in range(int(chunkX)):
                for y in range(int(chunkY)):
                    rgb = screenshot.load()[x + (i * chunkX), y]
                    r += rgb[0]
                    g += rgb[1]
                    b += rgb[2]

            averageRed = int((r / pixelInChunk))
            averageGreen = int((g / pixelInChunk))
            averageBlue = int((b / pixelInChunk))
            data.append(averageRed)
            data.append(averageGreen)
            data.append(averageBlue)

        #print(data)
        sender[1].dmx_data = data
        sender.flush()

    sender.manual_flush = False

    # sender.stop()
    screenshot.close()
