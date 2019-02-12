from mod_lib import *

pygame.init()
screen = pygame.display.set_mode(screen_size)
fps = 60
clock = pygame.time.Clock()

dp = DataProvider()
if dp.get_value("isNew"):
    generate_map()
    del dp

dp = DataProvider()
world_map = dp.get_value("map")
player = None


def init():
    global player
    Border(0, 0, width, 0, "up")
    Border(0, height, width, height, "down")
    Border(0, 0, 0, height, "left")
    Border(width, 0, width, height, "right")
    player = Player(creatures_group, 9, 4, 20, 20)
    if not dp.get_value("isNew"):
        set_block(dp.get_value("Active_Block"))
        player.restore_from_save(dp.get_value("Player"))


def start_screen():
    init()
    game()
    pass


def pause():
    pass


def game():
    re_render(world_map)
    while pygame.sprite.spritecollideany(player, water_group):
        player.move(random.randint(0, width), random.randint(0, width))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dp.set_value("Player", player.generate_save())
                dp.set_value("Active_Block", get_block())
                dp.save()
                running = False
        clock.tick(fps)
        tile_group.draw(screen)
        creatures_group.draw(screen)
        creatures_group.update(world_map)
        borders.draw(screen)
        pygame.display.flip()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pause()


start_screen()

pygame.quit()
