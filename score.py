import pygame, os, sys

pygame.init()
pygame.font.init()

score = 0
score_increment = 10

# Set up the game loop
while True:
    font = pygame.font.Font(None, 36)
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x -= 10
            elif event.key == pygame.K_RIGHT:
                player.x += 10

    # Update the game state
    if player.colliderect(obstacle):
        score += score_increment

    # Draw the game
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), player)
    pygame.draw.rect(screen, (0, 255, 0), obstacle)

    # Draw the score to the screen
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)