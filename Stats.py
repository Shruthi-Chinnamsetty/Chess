import matplotlib
import matplotlib.backends.backend_agg as agg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pygame

def stats():

    matplotlib.use("Agg")

    df = pd.read_csv('Stats.csv')

    fig, ax = plt.subplots(figsize=(8, 6))

    names = df['Name']
    x = np.arange(len(names))

    # The width of the bars (1 = the whole width of the person)
    width = 0.20

    # Create the bar charts!
    ax.bar(x - 3*width/2, df['Win'], width, label='Wins', color='#0343df')
    ax.bar(x - width/2, df['Lose'], width, label='Losses', color='#e50000')

    ax.set_ylabel('No of Win and Losses')
    ax.set_title('Player winning Stats')

    ax.set_xticks(x)    # This ensures we have one tick per [player], otherwise we get fewer.
    ax.set_xticklabels(names.astype(str).values, rotation='horizontal')

    ax.legend()

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()

    pygame.init()

    pygame.display.set_mode((800, 600))
    screen = pygame.display.get_surface()

    size = canvas.get_width_height()

    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(surf, (0, 0))
    pygame.display.flip()

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
