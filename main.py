import PIL
import sacn


def captureSingleChunk(screenshot, singleChunkXStart, singleChunkXStop, singleChunkYStart, singleChunkYStop):
    """ Captures one single chunk from the screenshot.
    Square: Upper Left Point -> singleChunkXStart/singleChunkYStart |
    Lower Right Point -> singleChunkXStop/singleChunkYStop"""
    singleChunkData = []
    r = 0
    g = 0
    b = 0
    for x in range(int(singleChunkXStart), int(singleChunkXStop)):
        for y in range(int(singleChunkYStart), int(singleChunkYStop)):
            chunkRGB = screenshot.load()[x, y]
            r += chunkRGB[0]
            g += chunkRGB[1]
            b += chunkRGB[2]
    averageRed = int((r / pixelInChunk))
    averageGreen = int((g / pixelInChunk))
    averageBlue = int((b / pixelInChunk))
    singleChunkData.append(averageRed)
    singleChunkData.append(averageGreen)
    singleChunkData.append(averageBlue)
    return singleChunkData


def captureChunksTop(screenshot1):
    chunkData = []
    for i in range(1, chunkCount + 1):
        cordX1 = (i - 1) * chunkX
        cordX2 = i * chunkX
        chunkData.extend(captureSingleChunk(screenshot1, cordX1, cordX2, 0, chunkY))
    #print(chunkData)
    return chunkData


def captureChunksBottom(screenshot1, height):
    chunkData = []
    for i in range(1, chunkCount + 1):
        cordX1 = (i - 1) * chunkX
        cordX2 = i * chunkX
        chunkData.extend(captureSingleChunk(screenshot1, cordX1, cordX2, (height - chunkY), height))
    #print(chunkData)
    return chunkData


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

    chunkY = 10
    chunkX = size[1] / 10
    chunk = chunkX, chunkY
    pixelInChunk = chunkX * chunkY
    chunkCount = 10

    while True:
        screenshot = ImageGrab.grab(bbox=(0, 0, 1920, 1080), include_layered_windows=True)
        data = captureChunksBottom(screenshot, 1080)
        sender[1].dmx_data = data
        sender.flush()

    sender.manual_flush = False

    # sender.stop()
    screenshot.close()
