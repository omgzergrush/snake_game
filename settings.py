WHITE = (252, 252, 252)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 220)

SPEED = 1
FPS_NORMAL = 30
FPS_INTRO = 30

INITIAL_SNAKE_LENGTH = 2

BOARD_WIDTH = 800
BOARD_HEIGHT = 600

MUSIC_VOLUME = 0.2
AUDIOFREQUENCY = 44100
AUDIOSIZE = 16
AUDIOCHANNELS = 2
AUDIOBUFFERSIZE = 4096

# Resources:

RESOURCES_FOLDER = './resources/'
AUDIO_FOLDER = './audio/'

FONT_NAME = RESOURCES_FOLDER + "ARCADE.TTF"

SNAKE_HEAD = RESOURCES_FOLDER + 'snake_head.png'
APPLE = RESOURCES_FOLDER + 'apple.png'
ICON = RESOURCES_FOLDER + 'apple_icon.bmp'

BITE = AUDIO_FOLDER + 'bite.wav'
PUNCH = AUDIO_FOLDER + 'sharp_punch.wav'

INTRO_SONG = AUDIO_FOLDER + 'Noisewaves_-_04_-_Horses_With_Fake_Legs.mp3'
SONGS = ['Noisewaves_-_01_-_If_Im_A_Baker_Youre_A_Homewrecker.mp3', 'Noisewaves_-_02_-_Someone_Unique.mp3', 'Noisewaves_-_03_-_Voice_Recognition_Everything.mp3', 'Noisewaves_-_04_-_Horses_With_Fake_Legs.mp3', 'Noisewaves_-_05_-_Do_I_Look_Like_I_Want_To_Play_Volleyball.mp3']
SONGS = [AUDIO_FOLDER + song for song in SONGS]