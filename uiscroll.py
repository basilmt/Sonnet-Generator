import pygame
import sys
import time


from backend import main, generate


# Colors
BLACK = (0, 0, 0)
GRAY = (198, 138, 9)
WHITE = (255, 255, 255)

# Create ui
pygame.init()
size = width, height = 1200, 600
screen = pygame.display.set_mode(size)

# Fonts
# Can be changed to DMSerif if required 
OLD_LONDON = "assets/fonts/OldLondon.ttf"
# OPEN_SANS = "assets/fonts/DMSerif.ttf"
smallFont = pygame.font.Font(OLD_LONDON, 20)
mediumFont = pygame.font.Font(OLD_LONDON, 28)
largeFont = pygame.font.Font(OLD_LONDON, 40)

# Add image as Background
scroll = pygame.image.load("assets/images/scroll.png")
scroll = pygame.transform.scale(scroll, (600, 450))


model = main()
lines = []
wait = ["","","","","","","Please Wait","Loading..."]
lines = wait
newSonnet = True

while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)

    # Draw the scroll
    recta = pygame.Rect(300,50,600, 400)
    screen.blit(scroll, recta)

    # Show Title
    title = largeFont.render("Sonnet Generator", True, WHITE)
    titleRect = title.get_rect()
    titleRect.center = ((width / 2), 25)
    screen.blit(title, titleRect)
    
    # Print Lines of Sonnet
    for i, linex in enumerate(lines):
        line = smallFont.render(linex, True, BLACK)
        lineRect = line.get_rect()
        lineRect.center = ((width / 2), 75 + 30 * i)
        screen.blit(line, lineRect)
    


    # Generate button
    # For new Sonnet 
    buttonRect = pygame.Rect( (3 / 8) * width , (6 / 7) * height, width / 4, 50)
    buttonText = mediumFont.render("Generate", True, BLACK)
    buttonTextRect = buttonText.get_rect()
    buttonTextRect.center = buttonRect.center
    pygame.draw.rect(screen, GRAY, buttonRect)
    screen.blit(buttonText, buttonTextRect)

    pygame.display.flip()

    if newSonnet:
        newSonnet = False
        lines = generate(model)

    # Check if Generate button clicked
    click, _, _ = pygame.mouse.get_pressed()
    if click == 1:
        mouse = pygame.mouse.get_pos()
        if buttonRect.collidepoint(mouse):
            newSonnet = True
            lines = wait


    #sleep 300ms for lowering processing
    time.sleep(0.3)