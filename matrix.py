#!/usr/bin/env python3
import curses
import random
import time

def matrix(stdscr, duration=300):
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()

    # Define color pairs
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # dim green
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # medium green
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # bright head
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)  # erased tail

    sh, sw = stdscr.getmaxyx()
    symbols = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄ0123456789"

    # Each column stores a list of characters and a speed counter
    columns = [[] for _ in range(sw)]
    speeds = [random.randint(1, 3) for _ in range(sw)]  # frames to move down per column
    speed_counters = [0 for _ in range(sw)]              # counter to track movement

    head_length = 8         # length of bright head
    trail_length = 12       # length of fading trail
    switch_chance = 0.3     # chance a character switches per frame

    start_time = time.time()
    ignore_until = start_time + 1

    while True:
        now = time.time()
        stdscr.clear()

        for x in range(sw):
            # Randomly add new character at top
            if random.random() < 0.1:
                columns[x].append({'y': 0, 'age': 0, 'char': random.choice(symbols)})

            new_column = []
            for char_info in columns[x]:
                y = char_info['y']
                age = char_info['age']

                # Slow character switching
                if random.random() < switch_chance:
                    char_info['char'] = random.choice(symbols)
                char = char_info['char']

                # Only move this column if its speed counter reaches its speed
                if speed_counters[x] >= speeds[x]:
                    char_info['y'] += 1
                    char_info['age'] += 1

                # Determine color based on age for smooth fading
                if age == 0:
                    color = curses.color_pair(3)
                elif 1 <= age <= head_length:
                    color = curses.color_pair(3)
                elif head_length < age <= head_length + trail_length // 2:
                    color = curses.color_pair(2)
                elif head_length + trail_length // 2 < age <= head_length + trail_length:
                    color = curses.color_pair(1)
                else:
                    color = curses.color_pair(4)

                # Draw bold character
                if y < sh:
                    try:
                        stdscr.addstr(y, x, char, color | curses.A_BOLD)
                    except curses.error:
                        pass

                new_column.append(char_info)

            columns[x] = [c for c in new_column if c['y'] < sh]

            # Update speed counter for this column
            speed_counters[x] += 1
            if speed_counters[x] > speeds[x]:
                speed_counters[x] = 0

        stdscr.refresh()
        time.sleep(0.05)  # adjust speed; smaller = faster

        # Stop after duration
        if now - start_time > duration:
            break

        # Stop on key press after first second
        if now > ignore_until:
            key = stdscr.getch()
            if key != -1:
                break

def main():
    curses.wrapper(matrix)

if __name__ == "__main__":
    main()

