from storage import StorageDriver

class SettingsManager:
    def __init__(self, storage: StorageDriver):
        self.storage = storage
        self.music_enabled = storage.get_setting("music_enabled", True)
        self.sfx_enabled = storage.get_setting("sfx_enabled", True)
        self.transitions_enabled = storage.get_setting("transitions_enabled", True)
        
    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        self.storage.set_setting("music_enabled", self.music_enabled)
        
    def toggle_sfx(self):
        self.sfx_enabled = not self.sfx_enabled
        self.storage.set_setting("sfx_enabled", self.sfx_enabled)
        
    def toggle_transitions(self):
        self.transitions_enabled = not self.transitions_enabled
        self.storage.set_setting("transitions_enabled", self.transitions_enabled)
        
