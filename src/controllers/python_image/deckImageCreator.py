from PIL import Image
import json
import os
import uuid
from data import data
import math
import io
import urllib.request
from time import sleep
from ratelimit import limits as ratelimits
import sys


class CardData:
    name = ''
    imageUrl = ''
    backFaceImageUrl = ''
    isDoubleFaced = False
    quantity = 0

    def __init__(self, cardData):
        try:
            self.name = cardData['cardJson']['name']
            self.id = cardData['cardJson']['id']
            self.imageUrl = cardData['cardJson']['image_uris']['png']
            self.quantity = int(cardData['quantity'])
            self.backFaceImageUrl = ''
            self.isDoubleFaced = False
        except KeyError:
            self.name = cardData['cardJson']['name']
            self.id = cardData['cardJson']['id']
            self.imageUrl = cardData['cardJson']['card_faces'][0]['image_uris']['png']
            self.backFaceImageUrl = cardData['cardJson']['card_faces'][1]['image_uris']['png']
            self.quantity = int(cardData['quantity'])
            self.isDoubleFaced = True

    def __str__(self):
        return str([self.imageUrl, self.backFaceImageUrl,
               self.isDoubleFaced, self.quantity])


class DeckImageCreator:
    cardImageRealWidth = 63.0
    cardImageRealHeight = 88.0
    cardImageWidth = 745
    cardImageHeight = 1040
    ppi = 300
    columns = 0
    maxPrintWidth = 0
    pixelsBetweenCards = 0

    storageFolder = './python_image/'

    def __init__(self, maxPrintWidth=900, pixelsBetweenCards=10):
        self.setImageSettings(maxPrintWidth, pixelsBetweenCards)

    def setImageSettings(self, maxPrintWidth, pixelsBetweenCards):
        conversionRate = self.cardImageRealWidth/self.cardImageWidth
        cardSeparationRealSize = pixelsBetweenCards*conversionRate
        columns = (maxPrintWidth - cardSeparationRealSize) / \
            (self.cardImageRealWidth + cardSeparationRealSize)
        if columns <= 0:
            raise Exception('Print area is not wide enough')
        self.columns = int(columns)
        self.maxPrintWidth = maxPrintWidth
        self.pixelsBetweenCards = pixelsBetweenCards

    def loadJsonData(self, jsonData):
        cardsData = json.loads(jsonData, strict=False)
        return [CardData(card) for card in cardsData]

    def checkForImageInCache(self, id):
        return os.path.isfile(self.storageFolder + 'cache/' + id + '.png')

    def storeImageInCache(self, image, id):
        if not os.path.exists(self.storageFolder + 'cache/'):
            os.makedirs(self.storageFolder + 'cache/')
        image.save(self.storageFolder + 'cache/' + id + '.png')

    def retrieveImageInCache(self, id):
        return Image.open(self.storageFolder + 'cache/' + id + '.png')

    def retrieveImage(self, url, id, cache=True):
        try:
            return self.requestImage(url, id, cache)
        except:
            sleep(0.1)
            return self.requestImage(url, id, cache)

    @ratelimits(calls=1, period=0.1)
    def requestImage(self, url, id, cache=True):
        if (self.checkForImageInCache(id) and cache):
            return self.retrieveImageInCache(id)
        image = Image.open(io.BytesIO(urllib.request.urlopen(url).read()))
        if (cache):
            self.storeImageInCache(image, id)
        return image

    def pasteCardOnCanvas(self, canvas, card, lastPosition):

        def calculateNextPosition(lastPosition, canvasWidth):
            offsetX = self.cardImageWidth + self.pixelsBetweenCards
            offsetY = self.cardImageHeight + self.pixelsBetweenCards
            nextPosition = (lastPosition[0] + offsetX, lastPosition[1])
            if nextPosition[0] + offsetX > canvasWidth:
                nextPosition = (self.pixelsBetweenCards,
                                lastPosition[1] + offsetY)
            return nextPosition

        if (card.isDoubleFaced):
            frontFaceimage = self.retrieveImage(card.imageUrl, card.id)
            backFaceImage = self.retrieveImage(
                card.backFaceImageUrl, card.id, cache=False)
            position = lastPosition
            for j in range(card.quantity):
                canvas.paste(frontFaceimage, position)
                position = calculateNextPosition(position, canvas.size[0])
                canvas.paste(backFaceImage, position)
                position = calculateNextPosition(position, canvas.size[0])
        else:
            position = lastPosition
            image = self.retrieveImage(card.imageUrl, card.id)
            for j in range(card.quantity):
                canvas.paste(image, position)
                position = calculateNextPosition(position, canvas.size[0])
        return position

    def calculateCanvasSize(self, cardsData):
        numberOfCards = 0
        for card in cardsData:
            if card.isDoubleFaced:
                numberOfCards += card.quantity * 2
            else:
                numberOfCards += card.quantity
        if self.columns > numberOfCards:
            width = int(self.cardImageWidth*numberOfCards +
                        self.pixelsBetweenCards*(numberOfCards + 1))
        else:
            width = int(self.cardImageWidth*self.columns +
                        self.pixelsBetweenCards*(self.columns + 1))
        rows = math.ceil(numberOfCards/self.columns)
        height = int(self.cardImageHeight*rows +
                     self.pixelsBetweenCards*(rows + 1))
        return (width, height)

    def createDeckImage(self, jsonData, saveOnDisk=True):
        if not os.path.exists(self.storageFolder + '/decks'):
            os.makedirs(self.storageFolder + 'decks')
        cardsData = self.loadJsonData(jsonData)
        canvas = Image.new('RGBA', self.calculateCanvasSize(
            cardsData), (255, 255, 255, 255))
        lastPosition = (self.pixelsBetweenCards, self.pixelsBetweenCards)
        for card in cardsData:
            lastPosition = self.pasteCardOnCanvas(canvas, card, lastPosition)
        deckId = str(uuid.uuid4())
        deckFile = self.storageFolder + 'decks/' + deckId + '.png'
        if (saveOnDisk):
            canvas.save(deckFile, dpi=(self.ppi, self.ppi))
        print(deckId)
        sys.stdout.flush()
    

if __name__ == '__main__':
    jsonData = open(sys.argv[1], encoding="utf8").read()
    mtg = DeckImageCreator()
    if (sys.argv[2] == 'img'):
        mtg.createDeckImage(jsonData)
    elif (sys.argv[2] == 'pdf'):
        mtg.createDeckPdf(jsonData, 'letter')

