from snake import App
import random
import time
import csv


def random_games(fname):
    with open(fname, 'a') as f:
        writer = csv.writer(f)
        choices_int = list(range(4))
        choices = ['up', 'right', 'down', 'left']
        # app.on_execute()
        app = App()
        app.on_init()
        while True:
            choice = random.choice(choices_int)
            inputs = app.get_relevant_inputs()
            _, reward = app.do_step(choices[choice])
            inputs.append(choice)
            inputs.append(reward)
            print(f'Inputs: {inputs}')
            print(f'reward: {reward}')
            writer.writerow(inputs)
            # time.sleep(1)
            if app.is_quit:
                app = App()
                app.on_init()

def play_games():
    choices_int = list(range(4))
    choices = ['up', 'right', 'down', 'left']
    # app.on_execute()
    app = App()
    app.on_init()
    while True:
        inputs = app.get_relevant_inputs()
        choice = dumb_choice(inputs)
        print(f'Inputs: {inputs}')
        _, reward = app.do_step(choice)
        inputs.append(choice)
        inputs.append(reward)
        print(f'reward: {reward}')
        # time.sleep(1)
        if app.is_quit:
            app = App()
            app.on_init()
        # time.sleep(.05)

def dumb_choice(inputs):
    choices = ['up', 'right', 'down', 'left']
    x = inputs[0]
    y = inputs[1]
    direction = inputs[6]
    go = None
    avail = inputs[2:6]
    if any(avail):
        pass
    else:
        return 'right'
    if abs(x) > abs(y):
        if x > 0:
            go = 'right'
        else:
            go = 'left'
    else:
        if y > 0:
            go = 'down'
        else:
            go = 'up'
    opp = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
    if opp[go] == direction:
        go = random.choice(choices)
    go_index = choices.index(go)
    while not avail[go_index]:
        go = random.choice(choices)
        go_index = choices.index(go)
    return go

def shortest_path_games():
    choices_int = list(range(4))
    choices = ['up', 'right', 'down', 'left']
    # app.on_execute()
    app = App()
    app.on_init()
    while True:
        m = app.shortest_path_to_apple()
        if m is None:
            print('NO PATH FOUND')
            time.sleep(30)
        for choice in m:
            _, reward = app.do_step(choice)
        if app.is_quit:
            app = App()
            app.on_init()
        # time.sleep(.1)


if __name__ == '__main__':
    # random_games()
    # play_games()
    shortest_path_games()
