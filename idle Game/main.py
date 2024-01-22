import pygame
import time
import random
pygame.init()

COLORSCHEME = {'BG':(255,255,255),'MG':(155,155,155),'FG':(0,0,0),'AC':(0,150,210)}
COLORSCHEME = {'BG':(25,25,25),'MG':(155,155,155),'FG':(250,167,32),'AC':(24,0,128)}

SCREENSIZE = (1600,800)
realScreen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)
SCREEN = pygame.surface.Surface((1600,800))

pygame.display.set_caption('Idle Game', "Idle")

iconSurface = pygame.surface.Surface((50,50))
iconSurface.fill((255,255,255))
pygame.draw.circle(iconSurface, (0,0,0), (25,25), 20)
pygame.display.set_icon(iconSurface)

dirtTiers = ('Dirt', 'Soil', 'Mud', 'Loamy Dirt', 'freash Topsoil', 'Sandy Soil', 'Clay Rich Ground', 'Silty Soil', 'Peat', 'rich topsoil', 'Fertile Earth', 'nourishing ground', 'Composted Soil', 'organic dirt', 'Flourishing Loam', 'Enriched Earth', 'Lush Soil', 'Nutrient-Rich Dirt', 'Iron Inffused', 'vitalized earth', 'Ambered Loam', 'Golden Soil', 'Pristine Dirt', 'Crystallized Earth', 'Stellar Soil', 'Diamond Dirt', 'Quantum Mud', 'Nebula Loam', 'Legendary Dirt', 'Astral Soil', 'Cosmic Mud', 'Galaxy Dirt', 'Celestial Soil', 'Elven earth', 'Mythical Mud', 'Sacred Loam', 'Divine Dirt', 'Ascended Earth', 'Immortal Soil', 'Eternity Dirt')


def updateScreen():
    realScreen.blit(pygame.transform.scale(SCREEN, realScreen.get_size()), (0,0))
    pygame.display.update()

textRenderList = []
def addText(text, size : int, location : tuple, col=COLORSCHEME['FG']) -> None:
    fontText = pygame.font.SysFont('Calibri', size).render(text, True, col)
    textRenderList.append([fontText, location, 0])

class buttonClass:
    def __init__(self, rect, textObject):
        self.rect = rect
        self.text = textObject
        self.textSize = textObject.get_size()
    
    def render(self):
        pygame.draw.rect(SCREEN, COLORSCHEME['MG'], self.rect)
        pygame.draw.rect(SCREEN, COLORSCHEME['FG'], self.rect, 5)
        SCREEN.blit(self.text, (self.rect.centerx - self.textSize[0]//2, self.rect.centery - self.textSize[1]//2))
    
    def isClicked(self, mouse):
        return self.rect.collidepoint(mouse)

class wormClass:
    def __init__(self, name, amountOf, maxPopulation, soilPerFrame, price, soilQuality, breedingSpeed, moveSpeed, wiggleSpeed, direction, upgradeBasePrice, upMaxlvl, upPricelvl, upBreedlvl, upDirtSpeedlvl):
        self.amountOf = amountOf
        self.maxPopulation = maxPopulation
        self.name = name
        self.soilPerFrame = soilPerFrame
        self.price = price
        self.soilQuality = soilQuality
        self.breedingSpeed = breedingSpeed
        self.moveSpeed = moveSpeed
        self.wiggleSpeed = wiggleSpeed
        self.direction = direction
        self.upgradeBasePrice = upgradeBasePrice
        self.upMaxlvl = upMaxlvl
        self.upPricelvl = upPricelvl
        self.upBreedlvl = upBreedlvl
        self.upDirtSpeedlvl = upDirtSpeedlvl

def newWorm(name, tier):
    rarity = int(5*random.random()**2*random.random())
    points = rarity*12 + tier*5
    wormStats = [1]*6 # soil, price, soilquality, breedingSpeed, moveSpeed, direction
    for i in points:
        wormStats[random.randint(0,5)] += 1
    return wormClass(name, 1, 16, 0.0001*wormStats[0]*random.randint(5,9), random.randint(2,5)*wormStats[1], wormStats[2]//6, wormStats[3], wormStats[4], random.randint(1,10), wormStats[5], points-2*tier, 0, 0, 0, 0)

def newRandomName():
    with open('Assets\\wormNameList.txt') as names:
        nameString = names.read()
        nameString = nameString.replace('\n','').split('|')
        part1 = random.choice(nameString[0].split(','))
        part2 = random.choice(nameString[1].split(','))
        prefix  = random.choice(nameString[2].split(',')) if random.randint(1,3) == 1 else ''
        mid = random.choice(nameString[2].split(',')) if random.randint(1, 3) == 1 else ''
        if mid == prefix:
            [mid, prefix][random.randint(0, 1)]  = ''
    name = prefix  + part1 + mid + part2
    return name.lstrip().title()

def dig(tier):
    soilCount[currentSoilTier] -= 1
    item = random.randint(0,2)
    if item == 1:
        addText('+1 dirt', 50, (mouseCoords[0]-30, mouseCoords[1]-40))
        soilCooldownList[currentSoilTier] += random.random()*2/3
        return
    elif item == 2:
        addText('+1 rock', 50, (mouseCoords[0]-30, mouseCoords[1]-40))
        return
        

soilPicture = pygame.transform.scale(pygame.image.load('Assets\\shovel.png'),(350,400))

digButton = buttonClass(pygame.rect.Rect(1270, 420, 310, 60), pygame.font.SysFont('ariel', 70).render('Dig', True, COLORSCHEME['AC']))
nextSoilButton = buttonClass(pygame.rect.Rect(1140, 160, 60, 60), pygame.font.SysFont('ariel', 70).render('>', True, COLORSCHEME['AC']))
preSoilButton = buttonClass(pygame.rect.Rect(820, 160, 60, 60), pygame.font.SysFont('ariel', 70).render('<', True, COLORSCHEME['AC']))

soilCooldownList = [0]*len(dirtTiers)
soilCount = [0]*len(dirtTiers)
currentSoilTier = 0

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseCoords = pygame.mouse.get_pos()
            if digButton.isClicked(mouseCoords) and soilCount[currentSoilTier] > 0:
                dig(currentSoilTier)
            elif preSoilButton.isClicked(mouseCoords) and currentSoilTier > 0:
                currentSoilTier -= 1
            elif nextSoilButton.isClicked(mouseCoords) and currentSoilTier < 39:
                currentSoilTier += 1

    SCREEN.fill(COLORSCHEME['BG'])
    SCREEN.blit(soilPicture, (1250,0))

    # soil counter and tiers
    pygame.draw.rect(SCREEN, COLORSCHEME['MG'], (820, 20, 380*soilCooldownList[currentSoilTier], 60))
    pygame.draw.rect(SCREEN, COLORSCHEME['AC'], (820, 20, 380, 60), 5)
    SCREEN.blit(pygame.font.SysFont('ariel', 60).render('Amount: ' + str(soilCount[currentSoilTier]), True, COLORSCHEME['FG']), (840, 35))
    SCREEN.blit(pygame.font.SysFont('ariel', 60).render('Soil Tier', True, COLORSCHEME['FG']), (930, 105))
    pygame.draw.rect(SCREEN, COLORSCHEME['MG'], (900, 160, 220, 60))
    pygame.draw.rect(SCREEN, COLORSCHEME['FG'], (900, 160, 220, 60), 5)
    soilNamePicture = pygame.font.SysFont('ariel', 60).render(dirtTiers[currentSoilTier].title(), True, COLORSCHEME['AC'])
    if soilNamePicture.get_size()[0] >= 200:
        soilNamePicture = pygame.transform.scale(soilNamePicture, (200, soilNamePicture.get_size()[1]))
    SCREEN.blit(soilNamePicture, (910, 170))


    digButton.render()
    if currentSoilTier < 39: nextSoilButton.render()
    if currentSoilTier > 0: preSoilButton.render()

    soilCooldownList[currentSoilTier] += 0.01
    if soilCooldownList[currentSoilTier] >= 1: 
        soilCooldownList[currentSoilTier] -= 1
        soilCount[currentSoilTier] += 1

    for i in textRenderList:
        SCREEN.blit(i[0], (i[1][0],i[1][1]-i[2]))
        i[2] += 3
        if i[2] > 150:
            textRenderList.remove(i)
    updateScreen()
    clock.tick(60)

for i in range(100):
    print(newRandomName())