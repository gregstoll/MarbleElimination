import pymunk
import pygame
import pymunk.pygame_util

def addMarble(space : pymunk.Space, x : int, y : int):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
    body.position = (x, y)
    shape = pymunk.Circle(body, 15)
    shape.elasticity = 0.9
    space.add(body, shape)


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    space = pymunk.Space()
    space.gravity = (0, 900)  # gravity pointing down

    # Create a marble
    addMarble(space, 102, 50)
    addMarble(space, 202, 50)
    addMarble(space, 302, 50)
    addMarble(space, 402, 50)

    # Add a floor
    floor = pymunk.Segment(space.static_body, (0, 580), (600, 580), 5)
    floor.elasticity = 0.9
    space.add(floor)

    # Bounds
    left = pymunk.Segment(space.static_body, (0, 0), (0, 580), 5)
    left.elasticity = 1.0
    space.add(left)
    right = pymunk.Segment(space.static_body, (0, 580), (600, 580), 5)
    right.elasticity = 1.0
    space.add(right)

    # Add slopes
    slope1 = pymunk.Segment(space.static_body, (50, 150), (150, 250), 5)
    slope1.elasticity = 0.9
    space.add(slope1)
    slope2 = pymunk.Segment(space.static_body, (100, 400), (200, 500), 5)
    slope2.elasticity = 0.9
    space.add(slope2)
    slope3 = pymunk.Segment(space.static_body, (400, 500), (500, 400), 5)
    slope3.elasticity = 0.9
    space.add(slope3)
    slope4 = pymunk.Segment(space.static_body, (300, 250), (400, 150), 5)
    slope4.elasticity = 0.9
    space.add(slope4)
    flat1 = pymunk.Segment(space.static_body, (200, 380), (350, 385), 5)
    flat1.elasticity = 0.9
    space.add(flat1)



    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        space.step(1/60)
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
