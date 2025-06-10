import pygame
from queue import Queue
import random, time


# Створюємо клас клієнтів, що будуть робити запити адміністраторам сервічного центру
class Client:
    id = 0
    def __init__(self):
        self.operations = random.randint(3, 8) # час на вирішення запиту клієнта
        self.image = pygame.image.load("src/client_small.png")
        Client.id += 1 
        self.id = Client.id


# Створюємо клас адміністраторів, що будуть обслуговувати запити клієнтів
class Server:
    def __init__(self):
        self.status = "Free" # статус адміністратора 'Free" - вільний; 'Busy' - з клієнтом; 'time_out" - замінює клієнта; 'Break' -  перерва.
        self.image = pygame.image.load("src/server_small.png")
        self.client = None # клієнт в роботі
        self.time = None # час початку роботи з клієнтом або початку перерви


# Створюємо клас нашого ЦНАПУ, який має чергу з клієнтів та певну кількість адміністраторів
class CNAP:
    def __init__(self):
        self.clients = Queue(maxsize = 12)
        self.servers = [Server() for _ in range(3)]

    def new_client(self, client):
        if self.clients.full():
            return "Queue is full!"
        self.clients.put(client)

    def serve_clients(self):
        if self.clients.empty():
            return "Queue is empty!"
        return self.clients.get()
    

def generate_client():
    '''
    Функція генерації клієнтів
    '''
    if random.randint(1, 6) > 3:
        cnap.new_client(Client())


if __name__ == "__main__":
    # Ініціюємо бібліотеку pygame та встановлюємо іконку
    pygame.init()
    screen = pygame.display.set_mode((300, 500))
    pygame.display.set_caption("Queue solver")
    icon = pygame.image.load("src/icon.png")
    pygame.display.set_icon(icon)

    my_font = pygame.font.Font('src/GOST_Type_BU.ttf', 16)

    bg = pygame.image.load("src/area.png")
    pause = pygame.image.load("src/pause.png")
    red_lamp = pygame.image.load("src/red_lamp.png")
    green_lamp = pygame.image.load("src/green_lamp.png")

    action = True
    cnap = CNAP()
    seconds = 0
    served_clients = 0

    # Безпосередній цикл роботи
    while action:
        screen.blit(bg, (0, 0))

        if not cnap.clients.empty():
            text = my_font.render('Last client', True, 'black')
            screen.blit(text, (201, 150))
            text = my_font.render('in Queue:' + str(Client.id), True, 'black')
            screen.blit(text, (201, 165))      

        text = my_font.render('SERVING:', True, 'blue')
        screen.blit(text, (16, 60))

        # Цикл роботи адміністраторів
        for i, server in enumerate(cnap.servers):
            if server.status == "Free":
                screen.blit(server.image, (33 + 105 * i, 455))
                screen.blit(green_lamp, (62 + 105 * i, 383))
                if not cnap.clients.empty():
                    server.client = cnap.serve_clients() # вільний приймає клієнта з черги
                    server.status = "Busy"
                    screen.blit(server.client.image, (33 + 105 * i, 353))
                    pygame.draw.circle(screen, 'white', (32 + 105 * i, 347), 10)
                    text = my_font.render(str(server.client.id), True, 'black')
                    if 0 < server.client.id < 10:
                        x = 0
                    elif 9 > server.client.id < 100:
                        x = -2
                    else:
                        x = -4
                    screen.blit(text, (28 + 105 * i + x, 338))
                    text = my_font.render(str(server.client.operations), True, 'red')
                    screen.blit(text, (50 + 105 * i, 338))
                    screen.blit(red_lamp, (62 + 105 * i, 383))     
                    server.time = seconds     
                    
                else:
                    text = my_font.render("Queue is empty!", True, 'red')
                    screen.blit(text, (1, 5))                

            elif server.status == "Busy":
                screen.blit(server.image, (33 + 105 * i, 455))
                screen.blit(red_lamp, (62 + 105 * i, 383))    
                if server.client:
                    screen.blit(server.client.image, (33 + 105 * i, 353))
                    pygame.draw.circle(screen, 'white', (32 + 105 * i, 347), 10)
                    text = my_font.render(str(server.client.id), True, 'black')
                    if 0 < server.client.id < 10:
                        x = 0
                    elif 9 > server.client.id < 100:
                        x = -2
                    else:
                        x = -4
                    screen.blit(text, (28 + 105 * i + x, 338))
                    text = my_font.render(str(server.client.operations - (seconds - server.time)), True, 'red')
                    screen.blit(text, (50 + 105 * i, 338))
                    if seconds - server.time == server.client.operations:
                        server.status = "time_out"                    

            elif server.status == "time_out":            
                screen.blit(server.image, (33 + 105 * i, 455))
                screen.blit(green_lamp, (62 + 105 * i, 383))
                server.status = "Free"
                served_clients += 1
                if random.randint(1, 10) == 10:
                    server.status = "Break"
                    server.time = seconds 
            # випадкова перерва на 20 секунд
            elif server.status == "Break":
                screen.blit(pause, (23 + 105 * i, 360))
                if seconds - server.time == 20:
                    server.status = "Free"

        # Вивід інформації щодо обслуговування
        count = 0
        for i, server in enumerate(cnap.servers):        
            if server.status == "Busy":
                count += 1
                text = my_font.render(f'SERVER {i + 1}:{server.client.id}', True, 'blue')
                screen.blit(text, (16, 60 + 20 * count))

        # Анімація заповнення черги до адміністраторів
        for i in range(cnap.clients.qsize()):
            client = cnap.serve_clients()
            if i < 6:
                x = 49 * i
                y = 0
            else:
                x = 49 * i - 294
                y = 55
            screen.blit(client.image, (19 + x, 253 - y))
            pygame.draw.circle(screen, 'white', (18 + x, 247 - y), 10)
            text = my_font.render(str(client.id), True, 'black')
            if 9 < client.id < 100:
                x -= 2
            elif client.id > 99:
                x -= 4
            screen.blit(text, (14 + x, 238 - y))
            cnap.new_client(client)

        # Інформуємо про переповнення черги
        if cnap.clients.full():
            text = my_font.render("Queue is full!", True, 'red')
            screen.blit(text, (1, 5))
        else:    
            generate_client()

        text = my_font.render('SERVED: ' + str(served_clients), True, 'blue')
        screen.blit(text, (16, 160))
        text = my_font.render('In process: ' + str(seconds) + ' sec', True, 'black')
        screen.blit(text, (165, 5))
        seconds += 1
                
        time.sleep(1)
        pygame.display.update()

        # Завершення програми при натисканні на кнопку виходу
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                action = False
                pygame.quit()