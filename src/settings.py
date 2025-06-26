class GameSettings:
    def __init__(self):
        self.transitions_enabled = True
        self.music_enabled = True
        self.sfx_enabled = True
        
    def toggle_transitions(self):
        self.transitions_enabled = not self.transitions_enabled
        
    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        
    def toggle_sfx(self):
        self.sfx_enabled = not self.sfx_enabled