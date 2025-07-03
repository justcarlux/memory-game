class SettingsManager:
    def __init__(self):
        self.music_enabled = True
        self.sfx_enabled = True
        self.transitions_enabled = True
        
    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        
    def toggle_sfx(self):
        self.sfx_enabled = not self.sfx_enabled
        
    def toggle_transitions(self):
        self.transitions_enabled = not self.transitions_enabled