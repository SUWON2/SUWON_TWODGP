import math
from pico2d import*

import core
from player import Player

class GameState:
    def init(self):
        hide_cursor()

        background = core.sprite.Sprite('./res/background.png')
        background.camera_ignorer = True
        background.x = core.const.SCREEN_WIDTH / 2
        background.y = core.const.SCREEN_HEIGHT / 2
        core.renderer.Add(background)

        boundary = core.sprite.Sprite('./res/boundary.png')
        core.renderer.Add(boundary)

        self.player = Player()

        self.zoom_point = core.sprite.Sprite('./res/zoom_point.png')
        self.zoom_point.camera_ignorer = True
        core.renderer.Add(self.zoom_point)

        self.zoom_outer = core.sprite.Sprite('./res/zoom_outer.png')
        self.zoom_outer.camera_ignorer = True
        core.renderer.Add(self.zoom_outer)

        self.zoom_scale = 0.7

        self.bgm = load_music('./res/Metallic Mistress.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()

    def update(self):
        if core.eh.get_key_down(SDLK_ESCAPE):
            core.pop_state()
            return

        view_dir_x = self.zoom_point.x + core.camera.x - self.player.spr.x
        view_dir_y = self.zoom_point.y + core.camera.y - self.player.spr.y
        view_dis = math.sqrt(view_dir_x ** 2 + view_dir_y ** 2)

        if view_dis != 0.0:
            view_dir_x /= view_dis
            view_dir_y /= view_dis

        self.player.update(view_dir_x, view_dir_y)
        self.__update_zoom(view_dir_x, view_dir_y, view_dis)
        self.__update_camera()

    def exit(self):
        core.renderer.clear()

    def pause(self):
        pass

    def resume(self):
        pass

    def __update_zoom(self, view_dir_x, view_dir_y, zoom_dis):
        self.zoom_point.x = core.eh.mouse_pos[0]
        self.zoom_point.y = core.eh.mouse_pos[1]
        self.zoom_outer.x = core.eh.mouse_pos[0]
        self.zoom_outer.y = core.eh.mouse_pos[1]

        self.zoom_scale = min(max(1.0, zoom_dis / 300.0), 1.5)
        self.zoom_outer.scaleX = self.zoom_scale
        self.zoom_outer.scaleY = self.zoom_scale

    def __update_camera(self):
        CAMERA_VELOCITY = 8
        target_x = self.player.spr.x - core.const.SCREEN_WIDTH / 2
        target_y = self.player.spr.y - core.const.SCREEN_HEIGHT / 2
        core.camera.x += (target_x - core.camera.x) * CAMERA_VELOCITY * core.delta_time
        core.camera.y += (target_y - core.camera.y) * CAMERA_VELOCITY * core.delta_time

if __name__ == '__main__':
    core.init(GameState())
    core.run()