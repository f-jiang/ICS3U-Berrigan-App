from kivy.app import App
from kivy.graphics import BorderImage
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, BoundedNumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.settings import *
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.storage.jsonstore import JsonStore
from kivy.core.audio import Sound, SoundLoader
from kivy.uix.progressbar import ProgressBar
#from kivy.lang import Builder


import random
import json
import os

'''
how ScreenManagers work:
-each screen gets its own class
-you add screens to the screen manager using the add_widget function
-you set the screen being displayed by setting the "current" property to the name of the desired screen
-you can set the direction of the transition animation by setting the "transition.direction" property to either "up",
"down", "left", or "right"
'''

class SplashScreen(Screen):
    bar = ObjectProperty(None)

    def on_enter(self, *args):
        bar = self.ids["loading_bar"]
        animation = Animation(value=bar.max, duration=2.0)
        animation.start(bar)
        animation.bind (on_complete=SplashScreen.complete)

    def complete(self, *args):
        FranSons.screen_manager.transition.direction = "left"
        FranSons.screen_manager.current = "main"


class MainMenuScreen(Screen):
    def on_enter(self, *args):
        if Assets.sounds['backgroundmusic.wav'].state == 'stop':
            Assets.sounds['backgroundmusic.wav'].play()
            Assets.sounds['backgroundmusic.wav'].loop = True


class CreditsScreen(Screen):
    shitter = 0
    def ericEaster(self, *args): # Eric's Easter Egg. Click his name three times in credits to have the time of your life.
        self.shitter += 1
        if self.shitter==6:
            self.shitter = 0
            Assets.sounds['lel.wav'].play()


'''class GameConfigScreen(Screen):

    # feilan: because ingame is a part of the playscreen, ingame.go should be called in playscreen class
    def go(self, *args):
        Assets.sounds['backgroundmusic.wav'].stop()
        InGame().go(2, 5)'''


class PlayScreen(Screen):
    global box1
    global box3
    global box3data
    global promptE
    global ib
    global timerbar
    
    def __init__(self, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)
        
        # self.add_widget(Image(source="assets/textures/bg2.png"))
        global box1
        global box3
        global box3data
        global promptE
        global ib
        global timerbar
        global timerholder
        box0 = BoxLayout(orientation="vertical")
        box1 = BoxLayout(orientation="horizontal", size_hint_y=0.9)
        box2 = BoxLayout(orientation="vertical",
                         size_hint_x=0.5,
                         size_hint_y=1.0,
                         padding=50,
                         spacing=25)
        
        ib=GridLayout(cols=2) # input stuffs go here
        box2.add_widget(ib)
        bb=Button(size_hint_x=1.0,
                  size_hint_y=0.25,
                  text="Quit"
                  )
        bb.bind(on_release=PlayScreen.toMenu)
        box2.add_widget(bb)
        box1.add_widget(box2)
        
        promptE = Image(source="")
        box1.add_widget(promptE)
        timerbar = ProgressBar(max=100,
                               size_hint_y=1.0,
                               size_hint_x=0.8,
                               pos_hint={'right': 0.9}
                               )
        timerholder = GridLayout(cols=1,
                                 size_hint_y=0.1,
                                 size_hint_x=0.8,
                                 pos_hint={'right': 0.9}
                                 )
        timerholder.add_widget(timerbar)
        box0.add_widget(timerholder)
        box0.add_widget(box1)
        self.add_widget(box0)

    def on_pre_enter(self, *args):
        InGame().go(2, 5)

    def on_enter(self, *args):
        animation = Animation(volume=0.0, duration=0.5)
        animation.start(Assets.sounds['backgroundmusic.wav'])
        animation.bind(on_complete=PlayScreen.on_mute)

    def on_mute(self, *args):
        Assets.sounds['backgroundmusic.wav'].stop()
        Assets.sounds['backgroundmusic.wav'].volume = 1.0

    def toMenu(self): # go to menu
        InGame.stop(self)

        FranSons.screen_manager.transition.direction = "down"
        FranSons.screen_manager.current = "main"

        Assets.sounds['backgroundmusic.wav'].play()
        Assets.sounds['backgroundmusic.wav'].loop = True

    def toEndScreen(self):
        InGame.stop(self)

        FranSons.screen_manager.transition.direction = "left"
        FranSons.screen_manager.current = "end"

        Assets.sounds['backgroundmusic.wav'].play()
        Assets.sounds['backgroundmusic.wav'].loop = True

    def updatePrompt(self, hint, input_data, correct_answer, type, tl, **kwargs):
        global box1
        global box3
        global box3data
        global promptE
        global ib
        global timerbar
        global timeholder

        ib.clear_widgets(children=None)

        # if input_data is of mc format
        # newSource = args[0]
        # potentialAnswers = args[1]
        # correctAnswer = args[2]
        box1.remove_widget(promptE)
        timerholder.remove_widget(timerbar)
        box3 = []
        box3data = []
        timerbar = None
        for pa in input_data:
            box3.append(Button(text=str(pa),
                               size_hint_x=0.5,
                               size_hint_y=0.5))
            box3data.append(pa)
        for i in range(0,4):
            if box3data[i]==correct_answer:
                box3[i].bind(on_press=InGame.takeCorrect)
            else:
                box3[i].bind(on_press=InGame.takeWrong)
            ib.add_widget(box3[i])

        # if the hint provided is an image
        promptE = Image(source=hint, size_hint_x=0.5)
        box1.add_widget(promptE)
        timerbar = ProgressBar(max=100,
                               size_hint_y=1.0,
                               size_hint_x=1.0
                               )
        timerholder.add_widget(timerbar)
        timerO = Animation(value=timerbar.max, duration=tl)
        timerO.start(timerbar)
        timerO.bind(on_complete = InGame.takeWrong)
        
    def level(self, *args): # feilan: could remove because not being used anywhere
        InGame.level(InGame)


class EndScreen(Screen):

    def on_enter(self, *args):
        Assets.sounds['backgroundmusic.wav'].play()
        Assets.sounds['backgroundmusic.wav'].loop = True

class StatsScreen(Screen):
    pass

# feilan: for this class we need to decide whether we should use it as a static (would use InGame instead of self)
# class or an instance (would use self) because using both conventions at the same time will cause us a lot of problems
# for now ive made it so that we use ingame as a static class
# also if we choose not to use instances, we may as well go procedural and move all the code in this class back into
# playscreen (i say we do it)
class InGame(): # host for functions relating to gameplay

    health = 3
    progress = -1
    goal = 0    # the value progress needs to be if we want to win
    difficulty = 1  # TODO: to be user-defined
    banged = [] # each word's face value that was banged is put into this array

    def go(self, starting_health, goal):
        #BackgroundScreenManager.background_image = ObjectProperty(Image(source='assets/textures/bg1.png'))

        InGame.health = starting_health
        InGame.progress = 0
        InGame.goal = goal

        print('starting values for health, progress, and goal: ', InGame.health, InGame.progress, InGame.goal)

        InGame.level()

    def stop(self):
        GameSave.save()
        InGame.banged = []

    def level(*args):
        global time
        """feilan: BASIC GAMEFLOW DESCRIPTION:
        -progress increases when answer correct
        -health decreases when answer incorrect
        -win by getting progress to certain value
        -lose by losing all health"""

        # self.progress += 1

        # making a list of words that can be asked
        possibilities = [] # creates list of possible prompts, picks random one from this later
        for p in Assets.words:
            if not (p in InGame.banged):
                possibilities.append(p)
        if len(possibilities) > 0 or InGame.progress < InGame.goal or InGame.health > 0:
            # selecting a word
            t = random.randrange(0, len(possibilities))
            InGame.currentWord = Assets.words[possibilities[int(t)]].definition # sets the level's current word
            (InGame.banged).append(InGame.currentWord) # adds to list of already used words, so as not to use it in the future

            # here: add code for picking answer format, hint format
            opts = ["mc","wp"]
            random.shuffle(opts)
            # if mc is the chosen answer format
            hint = Assets.words[InGame.currentWord].assets["texture"]
            pa0 = Assets.words[InGame.currentWord].inputs["mc"] # possible answers
            random.shuffle(pa0)
            inputData = [pa0[0], # here, add 3 of the bs answers and then the actual answer, then shuffle that shit up
                   pa0[1],
                   pa0[2],
                   InGame.currentWord]
            random.shuffle(inputData)
            timeLength = ((0.5**((4/InGame.goal)*InGame.progress)/(4 - InGame.difficulty))*9)+(7 - InGame.difficulty)
            # feilan: suggestion: move updateprompt into this class
            PlayScreen.updatePrompt(PlayScreen, hint, inputData, InGame.currentWord, opts[0], timeLength)
        else:
            InGame.end()

    def takeCorrect(*args):
        # update stat
        GameSave.total_correct += 1

        InGame.progress += 1
        print("Correct")
        print('current values for health, progress, and goal: ', InGame.health, InGame.progress, InGame.goal)

        if InGame.progress >= InGame.goal:
            InGame.end()
        else:
            InGame.level()

        Assets.sounds['correctanswer.wav'].play()

    def takeWrong(*args):
        # update stat
        GameSave.total_wrong += 1

        InGame.health -= 1
        print("Incorrect")
        print('current values for health, progress, and goal: ', InGame.health, InGame.progress, InGame.goal)

        if InGame.health > 0:
            InGame.level()
        else:
            InGame.end()

        Assets.sounds['surprise.wav'].play()

    def end(*args):
        InGame.stop(None)
        print('game over')

        # go to end screen instead
        PlayScreen.toEndScreen(None)


# TODO: determine what needs to be saved
class GameSave():
    source = JsonStore('save.json')

    total_correct = 0
    total_wrong = 0
    total_unanswered = 0    # TODO: find a place to update this stat
    time_played_s = 0       # TODO: find a place to update this stat
    av_question_time = 0

    # loads game save
    def load(*args):
        # sets up json if it has no values yet
        # if GameSave.source.count() == 0:
        GameSave.set_to_default()

        # writes json values to class variables
        GameSave.total_correct = GameSave.source.get('answers')['total_correct']
        GameSave.total_wrong = GameSave.source.get('answers')['total_wrong']
        GameSave.total_wrong = GameSave.source.get('answers')['total_unanswered']
        GameSave.time_played_s = GameSave.source.get('time_played_s')

    # overwrites game save
    def save(*args):
        # writes class variables to json values
        GameSave.source.put('answers',
                            total_correct=GameSave.total_correct,
                            total_wrong=GameSave.total_wrong,
                            total_unanswered=GameSave.total_unanswered)
        GameSave.source.put('time_played_s', value=GameSave.time_played_s)

    # resets game save
    def reset(*args):
        GameSave.source.clear()     # clear the json
        GameSave.set_to_default()   # set to default values
        GameSave.load()             # load default values

    # resets game save json to default values
    def set_to_default(*args):
        GameSave.source.put('answers', total_correct=0, total_wrong=0, total_unanswered=0)
        GameSave.source.put('time_played_s', value=0)
        print(GameSave.source.get('answers'))


class Assets():
    word_source = JsonStore('assets/words.json')
    sound_sources = JsonStore('assets/sounds/index.json')
    texture_sources = JsonStore('assets/textures/index.json')
    
    words = {}
    sounds = {}
    textures = {}

    # loads all assets and writes them to class variables
    def load(*args):
        # Loading the words
        Assets.words = {word['definition']:Word(word['definition'],
                                                word['difficulty'],
                                                word['inputs'],
                                                word['hints']
                                                )
                        for word in Assets.word_source.get('words')}
        
        # Loading the sounds
        Assets.sounds = {file_name:SoundLoader.load(filename=os.path.join('assets/sounds/', file_name))
                         for file_name in Assets.sound_sources.get('files')}

        # Loading the textures
        # for some reason this dict appears to be empty when accessed from the .kv file
        # TODO: find out why this is empty in kv file
        Assets.textures = {file_name:os.path.join('assets/textures/', file_name)
                           for file_name in Assets.texture_sources.get('files')}

# to access: Assets.words['the word you're looking for'].definition
class Word:

    def __init__(self, word, diff, inputs, hints, *args):
        self.definition = word                              # the actual word
        self.difficulty = diff                              # the word's difficulty
        self.inputs = inputs                                 # multiple choice possible answers
        self.assets = hints  # the texture and sound that go with the word (use these in the InGame class)
        

class BackgroundScreenManager(ScreenManager):
    background_image = ObjectProperty(Image(source='assets/textures/bg1.png'))

    """def __init__(self, **kwargs):    # TODO: fix sm size problems in python code
        super(BackgroundScreenManager, self).__init__(**kwargs)

        with self.canvas.before: # TODO: size of the screenmanager is wrong
            BorderImage(texture=BorderImage(source=Assets.textures['bg1.png']).texture, pos=self.pos, size=self.size)"""


class FranSons(App):
    screen_manager = None
    settings = None

    def build(self):
        # TODO: make a function for setting up game-related stuff?
        GameSave.load()
        Assets.load()
        
        # configure Settings panel
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False

        # initialize ScreenManager, set transition, add screens, and set current to splash screen
        FranSons.screen_manager = BackgroundScreenManager(transition=SlideTransition())
        FranSons.screen_manager.add_widget(SplashScreen(name="splash"))      # splash screen; loading occurs here
        FranSons.screen_manager.add_widget(MainMenuScreen(name="main"))      # main menu
        FranSons.screen_manager.add_widget(CreditsScreen(name="credits"))    # credits
        # FranSons.screen_manager.add_widget(GameConfigScreen(name="conf"))    # more specific settings
        FranSons.screen_manager.add_widget(PlayScreen(name="play"))          # gameplay occurs here
        FranSons.screen_manager.add_widget(EndScreen(name="end"))            # end screen, with score breakdown
        FranSons.screen_manager.add_widget(StatsScreen(name="stats"))        # players stats
        FranSons.screen_manager.current = "splash"

        ''' the app's settings can now be accessed through this variable
            how to access this from an outside class:
            print(FranSons.settings.get('gameplay', 'difficulty'))
        '''
        FranSons.settings = self.config

        return FranSons.screen_manager

    def build_config(self, config):
        config.setdefaults("settings", {
            "music": True,
            "sfx": True
        })
        config.setdefaults("gameplay", {
            "difficulty": 'Normal',
            "nature": True,
            "food": True,
            "machines": True
        })

    def build_settings(self, settings):
        settings.add_json_panel("App",
                                self.config,
                                data=json.dumps([
                                    {'type': 'bool',
                                     'title': 'Music',
                                     'desc': 'Toggle Music',
                                     'section': 'app',
                                     'key': 'music',
                                     'values': ['False', 'True']},
                                    {'type': 'bool',
                                     'title': 'Sound Effects',
                                     'desc': 'Toggle Sound Effects',
                                     'section': 'app',
                                     'key': 'sfx',
                                     'values': ['False', 'True']}])
                                )
        settings.add_json_panel("Gameplay",
                                self.config,
                                data=json.dumps([
                                    {'type': 'options',
                                     'title': 'Difficulty',
                                     'section': 'gameplay',
                                     'key': 'difficulty',
                                     'options': ['Easy', 'Normal', 'Hard']},
                                    {'type': 'title',
                                     'title': 'Word Categories'},
                                    {'type': 'bool',
                                     'title': 'Nature',
                                     'section': 'gameplay',
                                     'key': 'nature',
                                     'values': ['False', 'True']},
                                    {'type': 'bool',
                                     'title': 'Food',
                                     'section': 'gameplay',
                                     'key': 'food',
                                     'values': ['False', 'True']},
                                    {'type': 'bool',
                                     'title': 'Machines',
                                     'section': 'gameplay',
                                     'key': 'machines',
                                     'values': ['False', 'True']}])
                                )

if __name__ == "__main__":
    FranSons().run()
