import pygame

pygame.font.init()
BASE_FONT = pygame.font.SysFont("Segoe UI", 28)
TITLE_FONT = pygame.font.SysFont("Segoe UI Black", 48, bold=True)

def draw_button(screen, text, center_pos, font=BASE_FONT, button_color=(30,144,255), hover_color=(65,105,225)):
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    text_surf = font.render(text, True, (255, 255, 255))
    rect = text_surf.get_rect(center=center_pos)
    padding_x, padding_y = 30, 15
    button_rect = pygame.Rect(rect.left - padding_x, rect.top - padding_y, rect.width + padding_x*2, rect.height + padding_y*2)
    
    if button_rect.collidepoint(mouse_pos):
        color = hover_color
        if mouse_pressed[0]:
            return True
    else:
        color = button_color
    pygame.draw.rect(screen, color, button_rect, border_radius=12)
    pygame.draw.rect(screen, (255, 255, 255), button_rect, 2, border_radius=12)  
    screen.blit(text_surf, rect)
    return False

def input_box(screen, x, y, w, h, text='', font=BASE_FONT, active_color=(65,105,225), inactive_color=(100,100,100)):
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    active = False
    done = False
    input_text = text

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 20:
                        input_text += event.unicode

        color = active_color if active else inactive_color
        pygame.draw.rect(screen, color, rect, 3, border_radius=8)
        text_surf = font.render(input_text, True, (255, 255, 255))
        screen.fill((0, 0, 0), rect.inflate(-6, -6))  
        screen.blit(text_surf, (rect.x + 5, rect.y + (h - text_surf.get_height()) // 2))
        pygame.display.flip()
    return input_text
