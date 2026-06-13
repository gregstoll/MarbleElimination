# /// script
# dependencies = [
#  "pygame-ce",
#  "cffi",
#  "pymunk",
# ]
# ///
import pymunk
import pygame
from pymunk.vec2d import Vec2d
import asyncio
import math
import typing as t
import pymunk.pygame_util
import random
import sys
import time

IS_EMSCRIPTEN = sys.platform == 'emscripten'
if IS_EMSCRIPTEN:
    import js

FRAMES_PER_SECOND = 60.0

WIDTH : int = 1500
HEIGHT : int = 750

def sign(x):
    return int(math.copysign(1, x)) if x != 0 else 0

def rgb_colors_too_close(rgb1, rgb2) -> bool:
    # CieLAB or CieXYZ are more accurate but are complicated
    # Just use redmean
    # https://en.wikipedia.org/wiki/Color_difference#cite_ref-euc_1-1
    rmean = (rgb1[0] + rgb2[0]) / 2.0
    rpart = (2 + (rmean / 256.0)) * (rgb1[0] - rgb2[0]) * (rgb1[0] - rgb2[0])
    gpart = 4 * (rgb1[1] - rgb2[1]) * (rgb1[1] - rgb2[1])
    bpart = (2 + ((255 - rmean) / 256.0)) * (rgb1[2] - rgb2[2]) * (rgb1[2] - rgb2[2])
    distance_squared = rpart + gpart + bpart
    log(f"distance_squared between {rgb1} and {rgb2} : {distance_squared}")
    return distance_squared < 60000

def add_marble(space : pymunk.Space, x : int, y : int, colors: t.List[tuple]) -> pymunk.Shape:
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
    body.position = (x, y)
    shape = pymunk.Circle(body, 15)
    shape.elasticity = 0.9
    #shape.color = pygame.Color(50, 200, 50, 1)
    too_close = True
    while too_close:
        color = (random.randint(10, 250), random.randint(10, 250), random.randint(10, 250)) # RGB random color
        too_close = False
        for c in colors:
            if rgb_colors_too_close(color, c):
                log(f"colors too close: {color} and {c}")
                too_close = True
                break
    colors.append(color)
    log(f"adding color: {color}")
    shape.color = (color[0], color[1], color[2], 1)
    shape.collision_type = 1
    shape.is_rainbow = False
    space.add(body, shape)
    return shape

def create_marble_from_winner(space : pymunk.Space, winner : pymunk.Shape) -> pymunk.Shape:
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
    body.position = (random.randint(50, WIDTH-50), 50)
    shape = pymunk.Circle(body, 15)
    shape.elasticity = 0.9
    shape.color = winner.color
    shape.collision_type = 1
    shape.is_rainbow = winner.is_rainbow
    space.add(body, shape)
    return shape

def on_red_segment_hits_marble(arbiter : pymunk.Arbiter, space: pymunk.Space, data):
    for b in arbiter.bodies:
        if b.body_type == pymunk.Body.DYNAMIC:
            b.position = (100, 50)
    return True  # Continue with normal physics

def create_level1(space: pymunk.Space) -> t.List[pymunk.Segment]:
    segments = []

    # Add grills
    grill_x : int = 0
    while (grill_x < WIDTH-70):
        grill = pymunk.Segment(space.static_body, (grill_x, 600), (grill_x+50, 605), 5)
        grill.elasticity = 0.9
        segments.append(grill)
        grill_x = grill_x + 105

    # Add slopes
    slope1 = pymunk.Segment(space.static_body, (50, 120), (150, 220), 5)
    slope1.elasticity = 0.9
    segments.append(slope1)
    slope2 = pymunk.Segment(space.static_body, (100, 370), (200, 470), 5)
    slope2.elasticity = 0.9
    segments.append(slope2)
    slope3 = pymunk.Segment(space.static_body, (400, 470), (500, 370), 5)
    slope3.elasticity = 0.9
    segments.append(slope3)

    segments.extend(drawRotor(300, 350, 180))
    space.add(*segments)
    return segments


def drawRotor(x_pos: int, y_pos: int, velocity: int) -> t.List[pymunk.Segment]:
    rotor_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    rotor_body.position = (x_pos, y_pos)
    rotor_body.angular_velocity = math.radians(velocity)  # 180 degrees per second

    # Segment from center to +100 units on x-axis (local coordinates)
    rotor_segment = pymunk.Segment(rotor_body, (-100, 0), (100, 0), 5)
    rotor_segment.elasticity = 0.9
    rotor_segment2 = pymunk.Segment(rotor_body, (0, -100), (0, 100), 5)
    rotor_segment2.elasticity = 0.9
    return [rotor_body, rotor_segment, rotor_segment2]

def create_level2(space: pymunk.Space) -> t.List[pymunk.Segment]:
    segments = []
    # Add grills
    grill_x : int = 0
    while (grill_x < WIDTH-70):
        grill = pymunk.Segment(space.static_body, (grill_x, 600), (grill_x+50, 605), 5)
        grill.elasticity = 0.9
        segments.append(grill)
        grill_x = grill_x + 100

    # Add slopes
    slope1 = pymunk.Segment(space.static_body, (50, 120), (150, 220), 5)
    slope1.elasticity = 0.9
    segments.append(slope1)
    slope2 = pymunk.Segment(space.static_body, (100, 370), (200, 470), 5)
    slope2.elasticity = 0.9
    segments.append(slope2)

    segments.extend(drawRotor(200, 200, 180))
    segments.extend(drawRotor(400, 200, 185))
    segments.extend(drawRotor(600, 200, 190))
    segments.extend(drawRotor(800, 200, 195))
    segments.extend(drawRotor(1000, 200, 170))
    segments.extend(drawRotor(1200, 200, 175))
    segments.extend(drawRotor(250, 400, 180))
    segments.extend(drawRotor(450, 400, 185))
    segments.extend(drawRotor(650, 400, 190))
    segments.extend(drawRotor(850, 400, 195))
    segments.extend(drawRotor(1050, 400, 170))
    segments.extend(drawRotor(1250, 400, 175))
    space.add(*segments)
    return segments


def drawWinner(space : pymunk.Space, shape : pymunk.Shape, winner_index: int) -> pymunk.Shape:
    body = pymunk.Body(0, 0, pymunk.Body.STATIC)
    body.position = (WIDTH-50, 50 * (winner_index + 1))
    new_shape = pymunk.Circle(body, 15)
    new_shape.elasticity = 0.9
    new_shape.color = shape.color
    new_shape.is_rainbow = shape.is_rainbow
    space.add(body, new_shape)
    return new_shape

def addRedSegment(space : pymunk.Space, collision_segments : t.List[pymunk.Segment], endpoint1 : tuple[float, float], endpoint2 : tuple[float, float]):
    red_segment = pymunk.Segment(space.static_body, endpoint1, endpoint2, 10)
    red_segment.elasticity = 1.0
    red_segment.collision_type = 2
    red_segment.color = pygame.Color("Red")
    space.add(red_segment)
    if IS_EMSCRIPTEN:
        collision_segments.append(red_segment)

def log(s):
    print(s)
    if IS_EMSCRIPTEN:
        js.console.log(s)

async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    collision_segments = []

    if IS_EMSCRIPTEN:
        seed = time.monotonic_ns()
        #print("seed is " + str(seed))
        random.seed(seed)
        log(f"seed is {seed}")

    space = pymunk.Space()
    space.gravity = (0, 900)  # gravity pointing down

    # Create marbles
    marbles : t.List[pymunk.Shape] = []
    colors : t.List[tuple] = []
    marbles.append(add_marble(space, random.randint(50, WIDTH-50), 50, colors))
    marbles.append(add_marble(space, random.randint(50, WIDTH-50), 50, colors))
    marbles.append(add_marble(space, random.randint(50, WIDTH-50), 50, colors))
    marbles.append(add_marble(space, random.randint(50, WIDTH-50), 50, colors))
    if random.randint(0, 1) == 0:
        marbles[0].is_rainbow = True

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
    space.add(right)
    right.elasticity = 1.0

    # Create level
    segments = create_level2(space)
    lastLevel = 2

    # Create red segment on left
    addRedSegment(space, collision_segments, (10, HEIGHT-100), (10, HEIGHT-20))

    # emscripten version uses pymunk 6.4, which doesn't
    # have on_collision :-(
    if not IS_EMSCRIPTEN:
        space.on_collision(1, 2, on_red_segment_hits_marble)

    platform_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    platform_body.position = (700, 350)
    slope4 = pymunk.Segment(platform_body, (-50, 50), (50, -50), 5)
    slope4.elasticity = 0.9
    space.add(platform_body, slope4)

    running = True
    winners : t.List[pymunk.Shape] = []
    platform_direction = 1
    frame_num = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        space.step(1/FRAMES_PER_SECOND)
        if not IS_EMSCRIPTEN:
            space.debug_draw(draw_options)
        pygame.display.flip()
        if IS_EMSCRIPTEN:
            for shape in space.shapes:
                body = shape.body
                if body:
                    pos = int(body.position.x), int(body.position.y)
                    
                    if isinstance(shape, pymunk.Circle):
                        # Draw circle
                        pygame.draw.circle(screen, shape.color, pos, int(shape.radius))

                        #     # Draw a line to show rotation
                        #     angle = body.angle
                        #     end_pos = (
                        #         int(pos[0] + math.cos(angle) * shape.radius),
                        #         int(pos[1] + math.sin(angle) * shape.radius)
                        #     )
                        #     pygame.draw.line(screen, BLACK, pos, end_pos, 2)
                    elif isinstance(shape, pymunk.Poly):
                        # Draw polygon (box)
                        vertices = []
                        for v in shape.get_vertices():
                            x, y = v.rotated(body.angle) + body.position
                            vertices.append((int(x), int(y)))
                        pygame.draw.polygon(screen, shape.color, vertices)
                    if isinstance(shape, pymunk.Segment):
                        start = shape.a.rotated(body.angle) + body.position
                        end = shape.b.rotated(body.angle) + body.position
                        # use green if moving, gray if not
                        if hasattr(shape, 'color'):
                            color = shape.color
                        else:
                            color = (0, 200, 0) if body.body_type == pymunk.Body.KINEMATIC else (140, 140, 140)
                        pygame.draw.line(screen, color, start, end, int(shape.radius))

            pygame.display.update()
            await asyncio.sleep(0)

        clock.tick(60)

        # Move platform back and forth
        if platform_body.position.y > HEIGHT-100:
            platform_direction = -1
        elif platform_body.position.y < 100:
            platform_direction = 1
        speed = 100
        platform_body.velocity = Vec2d(0, platform_direction * speed)

        for marblesToCheck in (marbles, winners):
            for m in marblesToCheck:
                if m.is_rainbow:
                    #m.color = (random.randint(10, 250), random.randint(10, 250), random.randint(10, 250), 1)  # RGB random color
                    base_value = frame_num / 12.0
                    # fancy rainbow cycle
                    m.color = (0.5 * (math.sin(base_value - 2) + 1) * 256,
                               0.5 * (math.sin(base_value + 2) + 1) * 256,
                               0.5 * (math.sin(base_value) + 1) * 256,
                               1)
                    #log(f"new rainbow color: {m.color}")

        beforeWinners = len(winners)
        for m in marbles:
            if m.body.position.x > WIDTH:
                log(f"before remove marble: len(marbles)={len(marbles)}, len(winners)={len(winners)}")
                space.remove(m)
                marbles.remove(m)
                new_marble = drawWinner(space, m, len(winners))
                winners.append(new_marble)
                log(f"after remove marble: len(marbles)={len(marbles)}, len(winners)={len(winners)}")
            elif IS_EMSCRIPTEN:
                # have to do on_collision check here
                for segment in collision_segments:
                    contact_info = segment.shapes_collide(m)
                    if contact_info.points:
                        m.body.position = (100, 50)
                        continue
                    # this is not really general for segments that aren't vertical
                    #if segment.a.y - 10 <= m.body.position.y and m.body.position.y <= segment.b.y + 10:
                    #    # we're in the bottom "channel"
                    #    old_x = m.body.position.x
                    #    new_x = old_x + m.body.velocity.x/FRAMES_PER_SECOND
                    #    # check if it's moving really really fast and would "go through" the segment
                    #    if abs(new_x - segment.a.x) <= (m.radius + 10) or (sign(old_x - segment.a.x) != sign(new_x - segment.a.x)):
                    #        #print(f"m.body.position.x = {m.body.position.x} m.body.velocity.x = {m.body.velocity.x} segment.a.x = {segment.a.x}, m.radius={m.radius}")
                    #        m.body.position = (100, 50)
                    #        continue
        if len(winners) != beforeWinners:
            log(f"transition from {beforeWinners} winners to {len(winners)}, len(marbles) is {len(marbles)}")
            if len(marbles) == 1:
                log("marble eliminated!")
                space.remove(*marbles)
                marbles = []
                if len(winners) != 1:
                    marbles = [create_marble_from_winner(space, w) for w in winners]
                    space.remove(*winners)
                    winners = []

                    # Create red segment on right
                    #addRedSegment(space, collision_segments, (WIDTH-20, HEIGHT-100), (WIDTH-20, HEIGHT-20))
                    space.remove(*segments)
                    if lastLevel == 2:
                        segments = create_level1(space)
                        lastLevel = 1
                    else:
                        segments = create_level2(space)
                        lastLevel = 2
        frame_num = frame_num + 1

    pygame.quit()

if IS_EMSCRIPTEN or __name__ == "__main__":
    asyncio.run(main())