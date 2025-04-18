""" Sprite Sample Program """

import arcade

# --- Constants ---
SPRITE_SCALING_BOX = 0.5
SPRITE_SCALING_PLAYER = 0.5

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

MOVEMENT_SPEED = 7*1.6

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.01

g_x = 1000
g_y = 0

#import numpy as np
import random
def gen_plane():

    ### Ob wir nach links oder rechts gehen
    #tmp = np.random.randint(2)
    tmp = random.randrange(2)
    side = 1
    if tmp == 1:
        side = -1

    box_size = 64

    ### Anzahl der Boxen
    #Nb = np.random.randint(1, 11)
    Nb = random.randrange(1, 11)

    global g_x
    global g_y

    ### X dist
    dx = side * random.randrange(5, 15)


    ### Y dist
    dy = random.randrange(0, 5)

    ### Update global position
    g_x += dx * box_size
    g_y += dy * box_size

    ### Richtung der Boxen (horizontal oder vertical)
    #tmp = np.random.randint(2)
    tmp = random.randrange(2)

    # Liste mit den neuen Boxen
    xpos = []
    ypos = []


    for i in range(Nb):
        x = g_x
        y = g_y
        xpos.append(x)
        ypos.append(y)

        if tmp == 0:  ## Boxen sind horizontal
            g_x += box_size
        elif tmp == 1: ## Boxen sind vertical
            g_y += box_size

    return xpos, ypos




class MyGame(arcade.Window):
    """ This class represents the main window of the game. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")

        # Sprite lists
        self.player_list = None
        self.wall_list = None

        # Set up the player
        self.player_sprite = None

        # This variable holds our simple "physics engine"
        self.physics_engine = None
        self.player_speed_x = 0
        self.available_jumps = 2
        self.player_speed_x_factor = 1

        

        # Create the cameras. One for the GUI, one for the sprites.
        # We scroll the 'sprite world' but not the GUI.
        self.camera_for_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_for_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    def setup(self):

        # Set the background color
        arcade.set_background_color(arcade.color.BRIGHT_GREEN)

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Reset the score
        self.score = 0

        # Create the player
        self.player_sprite = arcade.Sprite("images/character2.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 64
        self.player_list.append(self.player_sprite)

        # --- Manually place walls

        # Manually create and position a box at 300, 200
        wall = arcade.Sprite("images/boxCrate_double_neon_black.png", SPRITE_SCALING_BOX)
        wall.center_x = 300
        wall.center_y = 200
        self.wall_list.append(wall)

        # Manually create and position a box at 364, 200
        wall = arcade.Sprite("images/boxCrate_double_neon_black.png", SPRITE_SCALING_BOX)
        wall.center_x = 364
        wall.center_y = 200
        self.wall_list.append(wall)

        # --- Place boxes inside a loop
        for x in range(173, 650, 64):
            wall = arcade.Sprite("images/boxCrate_double_neon_black.png", SPRITE_SCALING_BOX)
            wall.center_x = x
            wall.center_y = 350
            self.wall_list.append(wall)

        for x in range(-6400, 6400*10, 64):
            wall = arcade.Sprite("images/boxCrate_double_neon_black.png", SPRITE_SCALING_BOX)
            wall.center_x = x
            wall.center_y = 0
            self.wall_list.append(wall)

        # --- Place walls with a list
        coordinate_list = [[400, 500],
                           [470, 500],
                           [400, 570],
                           [470, 570]]

        # Loop through coordinates
        for coordinate in coordinate_list:
            wall = arcade.Sprite("images/boxCrate_double_neon_black.png", SPRITE_SCALING_BOX)
            wall.center_x = coordinate[0]
            wall.center_y = coordinate[1]
            self.wall_list.append(wall)


        for coordinate in coordinate_list:
            wall = arcade.Sprite("images/boxCrate_double_neon_black.png", SPRITE_SCALING_BOX)
            wall.center_x = coordinate[0] + 3*64
            wall.center_y = coordinate[1] + 4*64
            self.wall_list.append(wall)

        for coordinate in coordinate_list:
            wall = arcade.Sprite("images/boxCrate_double_neon_black.png", SPRITE_SCALING_BOX)
            wall.center_x = coordinate[0] + 13 * 64
            wall.center_y = coordinate[1] + 9 * 64
            self.wall_list.append(wall)


        for x in range(173 + 7 * 64, 650  + 25 * 64, 64):
            wall = arcade.Sprite("images/boxCrate_double_neon_black.png", SPRITE_SCALING_BOX)
            wall.center_x = x
            wall.center_y = 570 +  16 * 64
            self.wall_list.append(wall)


        for i in range(300):
            xpos, ypos = gen_plane()
            for x,y in zip(xpos, ypos):
                wall = arcade.Sprite("images/boxCrate_double_neon_black.png", SPRITE_SCALING_BOX)
                wall.center_x = x
                wall.center_y = y
                self.wall_list.append(wall)

        # Create the physics engine. Give it a reference to the player, and
        # the walls we can't run into.
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

    def on_draw(self):
        arcade.start_render()

        # Select the scrolled camera for our sprites
        self.camera_for_sprites.use()

        # Draw the sprites
        self.wall_list.draw()
        self.player_list.draw()

        # Select the (unscrolled) camera for our GUI
        self.camera_for_gui.use()
        global g_y
        arcade.draw_text(f"Completion: {100*self.score/g_y:.1f} %", 10, 50, arcade.color.BLACK, 24)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        hit_list = self.physics_engine.update()

        if len(hit_list) > 0:
            self.available_jumps = 2



        # Scroll the screen to the player
        self.scroll_to_player()

        self.player_sprite.change_y -= 1
        self.player_sprite.change_x = self.player_speed_x

        player_y = self.player_sprite.center_y
        if self.score < player_y:
            self.score = player_y

        # Scroll the window to the player.
        #
        # If CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        # Anything between 0 and 1 will have the camera move to the location with a smoother
        # pan.
        CAMERA_SPEED = 1
        lower_left_corner = (self.player_sprite.center_x - self.width / 2,
                             self.player_sprite.center_y - self.height / 2)
        self.camera_for_sprites.move_to(lower_left_corner, CAMERA_SPEED)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            if self.player_speed_x >= 0:
                self.player_speed_x = -MOVEMENT_SPEED*self.player_speed_x_factor
                #self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            if self.player_speed_x <= 0:
                self.player_speed_x = MOVEMENT_SPEED*self.player_speed_x_factor
                #self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            if self.available_jumps > 0:
                self.player_sprite.change_y = 3*MOVEMENT_SPEED
                self.available_jumps -= 1
        elif key == arcade.key.LSHIFT:
            if self.player_speed_x < 1.5*MOVEMENT_SPEED:
                self.player_speed_x *= 2.2
            self.player_speed_x_factor = 2.2

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A and self.player_speed_x < 0:
            self.player_speed_x = 0
        elif key == arcade.key.D and self.player_speed_x > 0:
            self.player_speed_x = 0
        elif key == arcade.key.LSHIFT:
            self.player_speed_x_factor = 1
            if abs(self.player_speed_x) > 1.5*MOVEMENT_SPEED:
                self.player_speed_x /= 2.2



    def scroll_to_player(self):
        """
        Scroll the window to the player.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a smoother
        pan.
        """

        position = (self.player_sprite.center_x - self.width / 2,
                        self.player_sprite.center_y - self.height / 2)
        self.camera_for_sprites.move_to(position, CAMERA_SPEED)

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_for_sprites.resize(int(width), int(height))
        self.camera_for_gui.resize(int(width), int(height))


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()