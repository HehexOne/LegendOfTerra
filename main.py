from mod_lib import *

pygame.init()
screen = pygame.display.set_mode(screen_size)
fps = 60
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('Century Gothic', 25)

render_ui = True
dp = DataProvider()
if dp.get_value("isNew"):
    generate_map()
    del dp

dp = DataProvider()
world_map = dp.get_value("map")
player = None


def init():
    global player
    [Raccoon(i) for i in dp.get_value("creatures")]
    [Bush(i) for i in dp.get_value("foliage")]
    Border(0, 0, width, 0, "up")
    Border(0, height, width, height, "down")
    Border(0, 0, 0, height, "left")
    Border(width, 0, width, height, "right")
    player = Player(player_group, 9, 4, 20, 20)
    if not dp.get_value("isNew"):
        set_block(dp.get_value("Active_Block"))
        player.restore_from_save(dp.get_value("Player"))


def start_screen():
    global render_ui, world_map, player, dp
    is_running = True
    init()
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    is_running = False
                if event.key == pygame.K_p:
                    init()
                    game()
                if event.key == pygame.K_r:
                    reset()
                    render_ui = True
                    dp = DataProvider()
                    if dp.get_value("isNew"):
                        generate_map()
                        del dp

                    dp = DataProvider()
                    world_map = dp.get_value("map")
                    player = None
                if event.key == pygame.K_e:
                    return
            if event.type == pygame.QUIT:
                dp.set_value("Player", player.generate_save())
                dp.set_value("Active_Block", get_block())
                dp.save()
                is_running = False
                pygame.quit()
        screen.fill(pygame.Color('black'))
        header = pygame.font.SysFont('Century Gothic', 70)
        textsurface = header.render('Legend of Terra', False, (70, 100, 150))
        screen.blit(textsurface, (30, 50))
        menu = pygame.font.SysFont('Century Gothic', 40)
        textsurface = menu.render('Press P to play.', False, (70, 100, 150))
        screen.blit(textsurface, (30, 200))
        textsurface = menu.render('Press R to reset saves.', False, (70, 100, 150))
        screen.blit(textsurface, (30, 250))
        textsurface = menu.render('Press E to exit.', False, (70, 100, 150))
        screen.blit(textsurface, (30, 300))
        textsurface = menu.render(f'Your last score: {player.score}', False, (255, 255, 150))
        screen.blit(textsurface, (30, 600))
        pygame.display.flip()


def pause():
    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    is_running = False
            if event.type == pygame.QUIT:
                dp.set_value("Player", player.generate_save())
                dp.set_value("Active_Block", get_block())
                dp.save()
                is_running = False
                pygame.quit()
        try:
            screen.fill(pygame.Color('black'))
            font_tmp = pygame.font.SysFont('Century Gothic', 40)
            textsurface = font_tmp.render(f'Pause. Press Q to play or Cross to exit.', False, (255, 255, 255))
            screen.blit(textsurface, (30, 600))
            pygame.display.flip()
        except Exception:
            pass


def dead():
    pass


def draw_interface():
    pygame.draw.rect(screen, (0, 0, 0), (20, 20, 200, 40))
    pygame.draw.rect(screen, (0, 0, 0), (237, 20, 200, 40))
    pygame.draw.rect(screen, (0, 0, 0), (455, 20, 200, 40))
    pygame.draw.rect(screen, (200, 0, 0), (30, 30, abs(int(180 * (player.hp / player.max_hp))), 20))
    textsurface = font.render(f'Coins: {player.coins} / Potions: {player.num_of_potions}', False, (255, 255, 255))
    screen.blit(textsurface, (460, 30))
    textsurface = font.render(f'Score: {player.score}', False, (255, 255, 255))
    screen.blit(textsurface, (245, 30))


def game():
    global render_ui
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
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    player.use_potion()
                if event.key == pygame.K_F1:
                    render_ui = not render_ui
                if event.key == pygame.K_ESCAPE:
                    pause()
                if event.key == pygame.K_e:
                    player.check_bush_raccoon()
                if event.key == pygame.K_SPACE:
                    enemy = pygame.sprite.spritecollideany(player, enemies_group)
                    if enemy:
                        Particle(player.rect.x, player.rect.y)
                        enemy.cast_damage(player.get_damage(), player)
        clock.tick(fps)
        tile_group.draw(screen)
        sparkle_group.update()
        enemies_group.update(world_map)
        enemies_group.draw(screen)
        foliage_group.update(world_map)
        raccoons_group.update(world_map)
        creatures_group.draw(screen)
        player_group.update(world_map)
        player_group.draw(screen)
        creatures_group.update(world_map)
        borders.draw(screen)
        sparkle_group.draw(screen)
        if player.hp <= 0:
            dead()
        if render_ui:
            draw_interface()
        pygame.display.flip()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pause()


start_screen()
pygame.quit()
