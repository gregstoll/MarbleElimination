from pymunk.vec2d import Vec2d
import math
import pymunk
import typing as t
import pygame
import pymunk.pygame_util
import random

WIDTH : int = 1500
HEIGHT : int = 750

def addMarble(space : pymunk.Space, x : int, y : int) -> pymunk.Shape:
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
    body.position = (x, y)
    shape = pymunk.Circle(body, 15)
    shape.elasticity = 0.9
    #shape.color = pygame.Color(50, 200, 50, 1)
    shape.color = (random.randint(10, 250), random.randint(10, 250), random.randint(10, 250), 1)  # RGB random color
    space.add(body, shape)
    return shape

def create_level1(space: pymunk.Space) -> None:
    # Add a floor
    floor = pymunk.Segment(space.static_body, (0, 590), (600, 590), 5)
    floor.elasticity = 0.9
    space.add(floor)

    # Add a ceiling
    ceiling = pymunk.Segment(space.static_body, (0, 5), (600, 5), 5)
    ceiling.elasticity = 0.9
    space.add(ceiling)

    # Bounds
    left = pymunk.Segment(space.static_body, (0, 0), (0, 590), 5)
    left.elasticity = 1.0
    space.add(left)
    right = pymunk.Segment(space.static_body, (595, 0), (595, 520), 5)
    right.elasticity = 1.0
    space.add(right)

    # Add grill
    #grill1 = pymunk.Segment(space.static_body, (0, 540), (600, 540), 5)
    grill1 = pymunk.Segment(space.static_body, (0, 540), (50, 540), 5)
    grill1.elasticity = 0.9
    space.add(grill1)
    grill2 = pymunk.Segment(space.static_body, (100, 540), (150, 540), 5)
    grill2.elasticity = 0.9
    space.add(grill2)
    grill3 = pymunk.Segment(space.static_body, (200, 540), (250, 540), 5)
    grill3.elasticity = 0.9
    space.add(grill3)
    grill4 = pymunk.Segment(space.static_body, (300, 540), (350, 540), 5)
    grill4.elasticity = 0.9
    space.add(grill4)
    grill5 = pymunk.Segment(space.static_body, (400, 540), (450, 540), 5)
    grill5.elasticity = 0.9
    space.add(grill5)
    grill6 = pymunk.Segment(space.static_body, (500, 540), (550, 540), 5)
    grill6.elasticity = 0.9
    space.add(grill6)


    # Add slopes
    slope1 = pymunk.Segment(space.static_body, (50, 120), (150, 220), 5)
    slope1.elasticity = 0.9
    space.add(slope1)
    slope2 = pymunk.Segment(space.static_body, (100, 370), (200, 470), 5)
    slope2.elasticity = 0.9
    space.add(slope2)
    slope3 = pymunk.Segment(space.static_body, (400, 470), (500, 370), 5)
    slope3.elasticity = 0.9
    space.add(slope3)


    rotor_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    rotor_body.position = (300, 350)
    rotor_body.angular_velocity = math.radians(180)  # 180 degrees per second

    # Segment from center to +100 units on x-axis (local coordinates)
    rotor_segment = pymunk.Segment(rotor_body, (-100, 0), (100, 0), 5)
    rotor_segment.elasticity = 0.9
    rotor_segment2 = pymunk.Segment(rotor_body, (0, -100), (0, 100), 5)
    rotor_segment2.elasticity = 0.9
    space.add(rotor_body, rotor_segment, rotor_segment2)

def drawRotor(space : pymunk.Space, x_pos: int, y_pos: int, velocity: int) -> None:
    rotor_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    rotor_body.position = (x_pos, y_pos)
    rotor_body.angular_velocity = math.radians(velocity)  # 180 degrees per second

    # Segment from center to +100 units on x-axis (local coordinates)
    rotor_segment = pymunk.Segment(rotor_body, (-100, 0), (100, 0), 5)
    rotor_segment.elasticity = 0.9
    rotor_segment2 = pymunk.Segment(rotor_body, (0, -100), (0, 100), 5)
    rotor_segment2.elasticity = 0.9
    space.add(rotor_body, rotor_segment, rotor_segment2)


def create_level2(space: pymunk.Space) -> None:
    # Add a floor
    floor = pymunk.Segment(space.static_body, (0, HEIGHT-20), (WIDTH, HEIGHT-10), 10)
    floor.elasticity = 0.9
    space.add(floor)

    # Add a ceiling
    ceiling = pymunk.Segment(space.static_body, (0, 10), (WIDTH, 10), 10)
    ceiling.elasticity = 0.9
    space.add(ceiling)

    # Bounds
    left = pymunk.Segment(space.static_body, (0, 0), (0, HEIGHT), 10)
    left.elasticity = 1.0
    space.add(left)
    right = pymunk.Segment(space.static_body, (WIDTH-10, 0), (WIDTH-10, HEIGHT-100), 10)
    right.elasticity = 1.0
    space.add(right)

    # Add grill
    grill_x : int = 0
    while (grill_x < WIDTH-50):
        grill = pymunk.Segment(space.static_body, (grill_x, 600), (grill_x+50, 605), 5)
        grill.elasticity = 0.9
        space.add(grill)
        grill_x = grill_x + 100

    # Add slopes
    slope1 = pymunk.Segment(space.static_body, (50, 120), (150, 220), 5)
    slope1.elasticity = 0.9
    space.add(slope1)
    slope2 = pymunk.Segment(space.static_body, (100, 370), (200, 470), 5)
    slope2.elasticity = 0.9
    space.add(slope2)

    drawRotor(space, 200, 200, 180)
    drawRotor(space, 400, 200, 185)
    drawRotor(space, 600, 200, 190)
    drawRotor(space, 800, 200, 195)
    drawRotor(space, 1000, 200, 170)
    drawRotor(space, 1200, 200, 175)
    drawRotor(space, 250, 400, 180)
    drawRotor(space, 450, 400, 185)
    drawRotor(space, 650, 400, 190)
    drawRotor(space, 850, 400, 195)
    drawRotor(space, 1050, 400, 170)
    drawRotor(space, 1250, 400, 175)


def drawWinner(space : pymunk.Space, shape : pymunk.Shape, winner_index: int) -> pymunk.Shape:
    body = pymunk.Body(0, 0, pymunk.Body.STATIC)
    body.position = (WIDTH-50, 50 * (winner_index + 1))
    new_shape = pymunk.Circle(body, 15)
    new_shape.elasticity = 0.9
    new_shape.color = shape.color
    space.add(body, new_shape)
    return new_shape

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    space = pymunk.Space()
    space.gravity = (0, 900)  # gravity pointing down

    # Create marbles
    marbles : t.List[pymunk.Shape] = []
    marbles.append(addMarble(space, random.randint(50, WIDTH-50), 50))
    marbles.append(addMarble(space, random.randint(50, WIDTH-50), 50))
    marbles.append(addMarble(space, random.randint(50, WIDTH-50), 50))
    marbles.append(addMarble(space, random.randint(50, WIDTH-50), 50))

    # Create level
    create_level2(space)

    platform_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    platform_body.position = (700, 350)
    slope4 = pymunk.Segment(platform_body, (-50, 50), (50, -50), 5)
    slope4.elasticity = 0.9
    space.add(platform_body, slope4)

    running = True
    winners : t.List[pymunk.Shape] = []
    random_marble : pymunk.Shape = marbles[0]
    direction = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        space.step(1/60)
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(60)

        # Move platform back and forth
        if platform_body.position.y > HEIGHT-100:
            direction = -1
        elif platform_body.position.y < 100:
            direction = 1
        speed = 100
        platform_body.velocity = Vec2d(0, direction * speed)

        random_marble.color = (random.randint(10, 250), random.randint(10, 250), random.randint(10, 250), 1)  # RGB random color
        for m in marbles:
            if m.body.position.x > WIDTH:
                space.remove(m)
                marbles.remove(m)
                new_marble = drawWinner(space, m, len(winners))
                winners.append(new_marble)
                if random_marble == m:
                    random_marble = new_marble


    pygame.quit()

if __name__ == "__main__":
    main()
