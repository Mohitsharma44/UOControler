from __future__ import division, print_function
from controller_imports import *

class RootWidget(ScreenManager, Screen):
    # Total number of screens:
    SCREENS = 3
    FILES = 15
    # Set Control Button Properties Here:
    _COLORS = [(232/255,153/255, 96/255, 1),(168/255, 159/255, 152/255, 1),
               (112/255, 149/255, 194/255, 1),(163/255, 200/255, 130/255, 1)]
    CTRL_BTN_COLORS = cycle(_COLORS[:SCREENS])
    CTRL_BTN_HEIGHT = 0.10
    CTRL_BTN_WIDTH = 'auto' # Pass float between 0 and 1
    
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        # Ask for Password
        self.loginPopup()
        
    def loginPopup(self, **kwargs):
        '''
        Plain String based password Login System.
        If password entered incorrectly, the popup will
        not go away.
        '''
        flayout = FloatLayout()
        image = AsyncImage(source='./city_520.png',
                           allow_stretch=True,
                           #size=(100,50),
                           #size_hint=(0,0.5),
                           pos_hint={'x':0, 'y':-0.35})
        txtinput = TextInput(text='', multiline=False,
                             password=True, size=(200,50),
                             size_hint=(None, None),
                             pos_hint={'center_x':0.5, 'center_y':0.7}
        )
        txtinput.bind(on_text_validate=self.on_enter)
        label = Label(text='Login to access Controller', size=(100, 50),
                      size_hint=(0,0.5),
                      pos_hint={'center_x':0.5, 'center_y':0.85})
        flayout.add_widget(txtinput)
        flayout.add_widget(label)
        flayout.add_widget(image)
        self.popup = Popup(title='Login', content=flayout,
                           auto_dismiss=False)
        self.popup.open()

    def on_enter(self,value):
        '''
        Check for the login input. If correct, provide access to controller
        '''
        if value.text == 'Mohit':
            self.popup.dismiss()
            Window.clearcolor = get_color_from_hex('#212121')
            print('Starting Controller UI')
            self.controllerUI()
        
    def controllerUI(self, **kwargs):
        self.transition = NoTransition()
        try:
            for i in range(self.SCREENS):
                screen = Screen(id='Screen %d'%i, name='Screen %d'%i)
                for cntrl_button in self._ctrlButtons():
                    screen.add_widget(cntrl_button)
                for vid_button in self._vidButtons():
                    screen.add_widget(vid_button)
                #screen.add_widget(Label(text='Screen %d'%i))
                screen.add_widget(AsyncImage(id='TV1',
                                             source='city.png',
                                             size_hint=(0.48,1.2),
                                             pos_hint={'x':0., 'y':0}
                ))
                screen.add_widget(AsyncImage(id='TV1',
                                             source='city.png',
                                             size_hint=(0.48,1.2),
                                             pos_hint={'x':0.52, 'y':0}
                ))
                screen.add_widget(Label(id='status',
                                        markup=True,
                                        text='[b]Controller Ready.. [/b]',
                                        font_size='13sp',
                                        size_hint=(0.1, 0.05),
                                        pos_hint={'x':0.05, 'y':0}
                ))
                self.add_widget(screen)
            self.current = 'Screen 0'
        except Exception, e:
            print('Exception in Screen: ',e)
            pass
            
    def _ctrlButtons(self):
        ctrlbuttons = []
        for i in range(self.SCREENS):
            ctrlbuttons.append(ToggleButton(id='Control %d'%i,
                                      name = 'Control %d'%i,
                                      group='control',
                                      text='Go to Screen: %d'%i,
                                      size_hint=(1/self.SCREENS if self.CTRL_BTN_WIDTH == 'auto' else self.CTRL_BTN_WIDTH,
                                                 self.CTRL_BTN_HEIGHT),
                                      on_press=self._ctrlBtnPress,
                                      on_release=self._ctrlBtnRelease,
                                      background_color=self.CTRL_BTN_COLORS.next(),
                                      pos_hint={'x': i/self.SCREENS, 'y': 1-self.CTRL_BTN_HEIGHT}
            ))
        return ctrlbuttons
    
    def _vidButtons(self):
        vidbuttons = []
        # Enumerate here.. ind, val
        for i in range(self.FILES):
            vidbuttons.append(Button(id='Video %d'%i,
                                           name='Video %d'%i,
                                           group='video',
                                           text='Vid %d'%i,# Replace by fname
                                           size_hint=(0.2,self.CTRL_BTN_HEIGHT),
                                           on_press=self._vidBtnPress,
                                           on_release=self._vidBtnRelease,
                                           pos_hint=self._yPositions(i)
            ))
        return vidbuttons

    def _yPositions(self, i):
            j = i % 5
            if i < 5:
                return {'x':j/5, 'y':0.25}
            elif i >= 5 and i < 10: 
                return {'x':j/5, 'y':0.25-0.1}
            elif i >= 10 and i < 15:
                return {'x':j/5, 'y':0.25-0.2}
            
    def _ctrlBtnPress(self, value):
        self.current = 'Screen %d'%(int(value.id[-1::]))
        print(self.current)
        # Turn of Bold Text for all Buttons
        for i in range(self.SCREENS+self.FILES):
            if self.get_screen(self.current).children[i].id[:-1] == 'Control ':
                self.get_screen(self.current).children[i].bold = False
        # Turn on Bold for the selected button
        value.bold = True
        '''
        #~~ Do Not Remove ~~#
        #-- HOW TO ACCESS WIDGETS FROM OTHER WIDGETS --#
        print(self.get_screen(self.current).ids)
        for i in range(self.SCREENS+self.FILES):
            print(self.get_screen(self.current).children[i].id)
        '''    
    def _vidBtnPress(self, value):
        print(value.pos_hint)
        
    def _ctrlBtnRelease(self, value):
        pass

    def _vidBtnRelease(self, value):
        pass


    
class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    MainApp().run()
