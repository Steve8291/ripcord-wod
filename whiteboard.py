#!/usr/bin/env python3

import requests
import re
from datetime import datetime
import subprocess

DEBUG = False
URL = 'https://crossfitripcord.sites.zenplanner.com/leaderboard-day.cfm'
HTML_FILE = '/usr/local/github/ripcord-wod/index.html'
CACHE_FILE = '/var/cache/ripcord-wod/raw_string'


# Live Site: https://steve8291.github.io/ripcord-wod/

# ##### Test Strings:
# raw_string = "No workouts posted for this day"
# raw_string = "<h2 >240710 - Wednesday </h2><div class='workout'><div class='sectionTitle'><a name='GeneralWarm-up'></a><h2>General Warm-up</h2></div><div class='skillDesc'>00-10<br><br>400m Run <br>Into:<br>40’ Monster walk<br>20 Leg swings (10 each direction)<br>Squat therapy (3x 1:00 on/off)</div><hr><div class='sectionTitle'><a name='Strength'></a><h2>Strength</h2></div><div class='skillName'>240707 - Front squats </div><div class='skillDesc'>10-40<br><br>Front squats <br>10-8-6-4-2-4-6<br>Work up in weight after each round </div><div class='skillResult'></div><hr><div class='sectionTitle'><a name='WOD'></a><h2>WOD</h2></div><div class='skillDesc'></div><hr><div class='skillName'>240707 - Quick one </div><div class='skillDesc'>40-50<br><br>3RDS:<br>12 Box jumps <br>12 Kettlebell swings <br>200m Run </div><div class='skillResult'></div><hr><div class='sectionTitle'><a name='Mobility'></a><h2>Mobility</h2></div><div class='skillDesc'>Couch stretch <br>Dragon <br>Pigeon pose </div><hr></div>"
# raw_string = "<h2 >240704 - 4th of July WOD</h2><div class='workout'><div class='sectionTitle'><a name='CommunityWOD'></a><h2>Community WOD</h2></div><div class='skillName'>240704 - 1776 WOD </div><div class='skillDesc'>1: Dumbbell snatch 50/35<br>2: T2B<br>3: Synchro Burpees over a rope <br>4: Box Jump overs 24/20<br>5: Pull-ups <br>6: Wall-balls <br>7: Synchro Rope lunges <br>8: Push-ups <br>9: Synchro box step-ups <br>10: Deadlifts 165/145<br><br>176 Double-under between each set <br><br>Teams of 4<br>44 reps each </div><div class='skillResult'></div><hr></div>"
# raw_string = "<h2 >Trample</h2><div class='workout'><div class='sectionTitle'><a name='practicewod'></a><h2>practice wod</h2></div><div class='skillDesc'>0-10<br><br>2:00 Bike/Row/Run<br>2 Rounds<br>10 Scorpions<br>10 PVC Pipe Thrusters<br>10 Mountain Climbers<br>10 PVC Pipe Overhead Squats<br>5 Strict Pull-Ups</div><hr><div class='sectionTitle'><a name='practicewod'></a><h2>practice wod</h2></div><div class='skillName'>240702</div><div class='skillDesc'>20-50<br>24 Minute AMRAP <br>10 Overhead Squat 75/55<br>100m Run <br>20 Box Jumps 24/20<br>100m Run<br>10 Thrusters 75/55<br>100m Run<br>20 Pull-Ups<br>100m Run</div><div class='skillResult'></div><hr></div>"
# raw_string = "<h2 >Rupture</h2><div class='workout'><div class='sectionTitle'><a name='WarmUp'></a><h2>Warm Up</h2></div><div class='skillDesc'>200m Jog<br>40’ Monster Walk<br>2 Rounds<br>10 Leg Swings each Direction<br>10 Air Squats<br>10 Cossack Squats<br>5 Inch Worm w/ Push-Up</div><hr><div class='sectionTitle'><a name='Strength'></a><h2>Strength</h2></div><div class='skillName'>Front Squat</div><div class='skillDesc'>10x3 @ 65-70%<br>Every 2:00</div><div class='skillResult'></div><hr><div class='sectionTitle'><a name='Metcon'></a><h2>Metcon</h2></div><div class='skillName'>240703</div><div class='skillDesc'>8 Minute AMRAP<br>10 KB Swings 53/35<br>10 KB OH Walking Lunge 53/35<br>10 Push-Ups<br>30 Double Unders</div><div class='skillResult'></div><hr></div>"
# raw_string = "<h2 >240528 - Tuesday</h2><div class='workout'><div class='sectionTitle'><a name='GeneralWarm-up'></a><h2>General Warm-up</h2></div><div class='skillDesc'>00-10<br><br>2 RDS:<br>200m Run<br>20 Banded good mornings <br>10 Scorpions <br>5 Up-downs <br>10 Russian twists <br>20 Band pull-apart <br></div><hr><div class='sectionTitle'><a name='WhiteBoard'></a><h2>White Board</h2></div><div class='skillDesc'>10-15<br><br>WOD set-up and demo </div><hr><div class='sectionTitle'><a name='WOD'></a><h2>WOD</h2></div><div class='skillName'>240527 - Team relay </div><div class='skillDesc'>15-45<br><br>Team relay:<br><br>15 Double-under <br>5 Deadlifts 155/125<br>— Next in line begins—-<br>10 Sit-ups <br>8/6 Cal Row <br>5 Box jumps </div><div class='skillResult'></div><hr><div class='sectionTitle'><a name='Mobility'></a><h2>Mobility</h2></div><div class='skillDesc'>50-60<br><br>Calf stretch <br>Couch stretch <br>Banded hamstring stretch </div><hr></div>"
# raw_string = "<h2 >240522 - Wednesday </h2><div class='workout'><div class='sectionTitle'><a name='GeneralWarm-up'></a><h2>General Warm-up</h2></div><div class='skillDesc'>00-15<br><br>800m Snake run <br><br>2 RDS:<br>20 Band pull-apart <br>20 Banded Face-pulls <br>20 Banded Tricep push-downs <br></div><hr><div class='sectionTitle'><a name='Strength'></a><h2>Strength</h2></div><div class='skillDesc'>15-40<br><br>Bro sesh<br>3RDS:<br>8 Dumbbell Bench press <br>12 Dumbbell curls (6 per arm)<br>8 Dips<br>12 Gorilla row (6 per arm)<br></div><hr><div class='sectionTitle'><a name='WOD'></a><h2>WOD</h2></div><div class='skillName'>240519 - WOD</div><div class='skillDesc'>40-50<br><br>5RDS:<br>10 Wall balls 20/14<br>20 Double-under<br>10 Dumbbell Snatch </div><div class='skillResult'></div><hr><div class='sectionTitle'><a name='Mobility'></a><h2>Mobility</h2></div><div class='skillDesc'>50-60<br><br>Roll:<br>T-spine <br>Lats <br>Quads <br>Hamstrings </div><hr></div>"
# raw_string = "<h2 >240422 - Monday </h2><div class='workout'><div class='sectionTitle'><a name='GeneralWarm-up'></a><h2>General Warm-up</h2></div><div class='skillDesc'>3:00 Bike, row or run <br>Into 2RDS:<br>20 Banded good mornings <br>10 Box step-ups <br>20 Russian twists <br>10 Box jumps <br></div><hr><div class='sectionTitle'><a name='SpecificWarm-up'></a><h2>Specific Warm-up</h2></div><div class='skillDesc'>10-20 <br><br>Hang clean position refresher:<br>- Deadlift <br>- Loading in the power or launch position <br>- Bar path <br>- Extension <br>- Receiving </div><hr><div class='sectionTitle'><a name='WhiteBoard'></a><h2>White Board</h2></div><div class='skillDesc'>20-30<br><br>Workout breakdown and set-up <br></div><hr><div class='sectionTitle'><a name='WOD'></a><h2>WOD</h2></div><div class='skillDesc'></div><hr><div class='skillName'>240421 - Partner WOD </div><div class='skillDesc'>30-50<br><br>Partner 22min AMRAP:<br>You go,I go<br><br>10 Hang power cleans 95/65<br>5 Burpee box jumps 24/20<br>10 AbMat sit-ups <br>5 Box jump overs <br></div><div class='skillResult'></div><hr><div class='sectionTitle'><a name='Mobility'></a><h2>Mobility</h2></div><div class='skillDesc'>50-60<br><br>Banded hip distraction <br>Banded Hamstring stretch <br>Calf stretch </div><hr></div>"
# raw_string = "<h2 >240712 - Friday </h2><div class='workout'><div class='sectionTitle'><a name='GeneralWarm-up'></a><h2>General Warm-up</h2></div><div class='skillDesc'>00-15<br><br>Handball <br><br>3RDS:<br>200m Row <br>10 Dislocates <br>10 ASQ<br>10 Up-downs <br><br>15-20<br><br>Set-up </div><hr><div class='sectionTitle'><a name='WOD'></a><h2>WOD</h2></div><div class='skillName'>240707 - U go, I go </div><div class='skillDesc'>20-50<br><br>22 min AMRAP:<br><br>U go, I go <br>5 Wall balls 20/14<br>2 Bar Muscle-up<br>5 G2OH w/plate 55/35<br>40 Double-under</div><div class='skillResult'></div><hr><div class='sectionTitle'><a name='Mobility'></a><h2>Mobility</h2></div><div class='skillDesc'>50-60<br><br>Friendship walk <br></div><hr></div>"


html_template = """<!DOCTYPE html>
<html>
<head>
  <title>Ripcord WOD</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="refresh" content="300">
  <style>
* {
  box-sizing: border-box;
}

:root {
  --color-blue: #1376bc;
  --color-accent: var(--color-blue);
  --columns: 2;
  --gap: 2vw;
}

html[style] body {
  visibility: visible;
}

body {
  background-color: black;
  color: white;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  font-family: system-ui, sans-serif;
  font-size: calc(10vw * var(--scale, 1));
  gap: 1em var(--gap);
  margin: 0;
  max-height: calc(100vh - var(--gap));
  padding: var(--gap);
  visibility: hidden;
}

section {
  width: calc((100vw - var(--gap) * (1 + var(--columns))) / var(--columns));
}

h2 {
  color: var(--color-accent);
  font-size: 0.75em;
  font-weight: bold;
  margin: 0;
}

ul {
  list-style: none;
  margin: 0 0 0 1em;
  padding: 0;
}

li {
  margin-top: 0.25em;
  text-indent: -1em;
}

li:empty {
  font-size: 0.4em;
}
  </style>
  <script>
const root = document.documentElement;
const prop = '--scale';
function isOverflown (element) {
  return element.scrollHeight > element.clientHeight || element.scrollWidth > element.clientWidth;
}
function scalePage () {
  if (!isOverflown(document.body)) {
    return;
  }
  const scale = (root.style.getPropertyValue(prop) || 1) - 0.01;
  root.style.setProperty(prop, scale);
  scalePage()
}
function resize () {
  root.style.removeProperty(prop);
  scalePage();
}
function debounce (mainFunction, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => {
      mainFunction(...args);
    }, delay);
  };
};
const debouncedResize = debounce(resize, 500);
window.addEventListener('load', scalePage);
window.addEventListener('resize', debouncedResize);
  </script>
</head>
<body>
"""

html_no_wod = """<!DOCTYPE html>
<html>
  <head>
    <title>Ripcord WOD</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="300">
    <style>
      body {
        background-color: black;
        font-family: system-ui, sans-serif;
      }

      img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        margin-top: 2vw;
        width: 60vw;
      }

      h1 {
        text-align: center;
        font-weight: bold;
        color: white;
        margin-top: 1vw;
        font-size: 6vw;
      }
    </style>
  </head>
  <body>
    <img src="https://www.crossfitripcord.com/wp-content/uploads/2016/11/Ripcord-Logo_white-Medium.png" alt="CrossFit Ripcord">
    <h1>No Workout Posted Today</h1>
  </body>
</html>
"""


def fetchWOD(url):
    try:
        response = requests.get(url, timeout=10)
        status = response.status_code
        html_content = response.text

        raw_regex = r".*class='workout'.*"
        no_wod = re.search(r'No workouts posted for this day', html_content)
        if no_wod:
            raw_string = no_wod.group()
        else:
            raw_string = re.search(raw_regex, html_content).group()

    except Exception as error:
        if DEBUG:
            print('############### fetchWOD Error ##############')
            print(f'HTML Status Code: {status}')
            print(error)
            print('#############################################\n')
        exit()

    return raw_string


def getHTMLClasses(raw_string):
    html_class_list = re.findall(r"<div (class=.*?)</div>", raw_string)
    html_wod_name = re.match(r"^<h2 >(.*)</h2><div class='workout'>", raw_string).group(1)  # type: ignore[union-attr]

    wod_name = html_wod_name.strip()
    wod_name = re.sub(r"^\d{6}", "", wod_name).strip()  # remove 6 digits
    wod_name = re.sub(r"^-", "", wod_name).strip()  # remove hyphen or colon at start
    wod_name = re.sub(r"(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)", "", wod_name).strip()  # remove days

    if DEBUG:
        print('############### html_wod_name ###############')
        print(html_wod_name)
        print('#############################################\n')
        print('############## html_class_list ##############')
        for i in html_class_list:
            print(i)
        print('#############################################\n')

    return wod_name, html_class_list


def getSections(wod_name, html_class_list):
    title_list = []
    # ['GeneralWarm-up (00-10)', 'Strength (10-40)', 'WOD (40-50)', 'Mobility']
    skill_list = []
    # [['400m Run', 'Into:', '40’ Monster walk', '20 Leg swings (10 each direction)', 'Squat therapy (3x 1:00 on/off)'], ['Front squats', '10-8-6-4-2-4-6', 'Work up in weight after each round'], ['3RDS:', '12 Box jumps', '12 Kettlebell swings', '200m Run'], ['Couch stretch', 'Dragon', 'Pigeon pose']]

    for i in html_class_list:
        if "class='sectionTitle'" in i:
            title = re.search(r"<h2>(.*)</h2>", i).group(1)  # type: ignore[union-attr]
            title = title.strip()
            if wod_name and title in ['Metcon', 'Home WOD', 'WOD', 'Community WOD']:
                title = f'{title}: {wod_name}'
            title_list.append(title.strip())

        elif "class='skillName'" in i:
            name = re.sub(r"^class='skillName'>", "", i).strip()
            name = re.sub(r"^\d{6}", "", name).strip()  # remove 6 digits
            name = re.sub(r"^-", "", name).strip()  # remove hyphen or colon at start
            # Will not add name if wod_name contains a string and title is in list below.
            if name and (not wod_name or not re.match(r"^(?:Metcon|Home WOD|WOD|Community WOD)", title_list[-1])):
                title_list[-1] = f'{title_list[-1]}: {name}'

        elif "class='skillDesc'" in i:
            curr_skill_list = re.split("<br>", i.lstrip("class='skillDesc'>"))
            # Ignore lists where all elements are empty strings
            # Without this, the while loops below can become infinite loops
            if not any(string for string in curr_skill_list):
                continue

            # Strip all spaces from right end of elements
            curr_skill_list = [element.rstrip() for element in curr_skill_list]

            # Remove empty items at beginning and end of skill_list
            while not curr_skill_list[0].strip():
                del curr_skill_list[0]
            while not curr_skill_list[-1].strip():
                del curr_skill_list[-1]

            # If first item is time domain, remove it and add to title. Ex: "00-10" or "0-10"
            if re.fullmatch(r"(\d{1,2}-\d{2})", curr_skill_list[0]):
                time_domain = curr_skill_list.pop(0)
                title_list[-1] = f'{title_list[-1]} ({time_domain})'
                while not curr_skill_list[0].strip():
                    del curr_skill_list[0]
            skill_list.append(curr_skill_list)

    if DEBUG:
        print('############ title & skill_list #############')
        for i in range(len(title_list)):
            print(title_list[i])
            print(skill_list[i])
        print('#############################################\n')

    return title_list, skill_list


def generateHTML(title_list, skill_list):
    with open(HTML_FILE, 'a') as html_file:
        html_file.truncate(0)
        html_file.write(html_template)

        for i in range(len(title_list)):
            html_file.write(f"  <section>\n    <h2>{title_list[i]}</h2>\n    <ul>\n")

            for skill in skill_list[i]:
                html_file.write(f"      <li>{skill}</li>\n")

            html_file.write("    </ul>\n  </section>\n")

        html_file.write("</body>\n</html>")

    if DEBUG:
        print('################ HTML Format ################')
        for i in range(len(title_list)):
            print(title_list[i])
            for skill in skill_list[i]:
                print(f"\t{skill}")
            print("")
        print('#############################################\n')


def generateNoWodHTML():
    with open(HTML_FILE, 'w') as html_file:
        html_file.write(html_no_wod)

    if DEBUG:
        print('################ HTML Format ################')
        print('No Workout Posted Today')
        print('#############################################\n')


def updateGitRepo():
    date = datetime.today().strftime('%m-%d-%Y')
    git_command = ["git", "-C", "/usr/local/github/ripcord-wod"]
    output_1 = subprocess.run(git_command + ["add", "index.html"], capture_output=True)
    if output_1.returncode == 0:
        output_2 = subprocess.run(git_command + ["commit", "-m", date], capture_output=True)
        if output_2.returncode == 0:
            output_3 = subprocess.run(git_command + ["push"], capture_output=True)
            if output_3.returncode == 0:
                with open(CACHE_FILE, 'w') as cache_file:
                    cache_file.write(raw_string)

    if DEBUG:
        print('################# Git Repo ##################')
        print('git add index.html - Return code:', output_1.returncode)
        print(output_1.stdout.decode("utf-8"))
        print('---------------------------------------------')
        print('git commit -m "date" - Return code:', output_2.returncode)
        print(output_2.stdout.decode("utf-8"))
        print('---------------------------------------------')
        print('git push - Return code:', output_3.returncode)
        print(output_3.stdout.decode("utf-8"))
        print('#############################################\n')


def isNewWod(raw_string):
    with open(CACHE_FILE, 'a+') as cache_file:
        cache_file.seek(0)
        cached_line = cache_file.readline().strip()
        if cached_line != raw_string:
            return True
        else:
            return False


# Main
raw_string = fetchWOD(URL)
if isNewWod(raw_string):
    if raw_string == 'No workouts posted for this day':
        generateNoWodHTML()
    else:
        wod_name, html_class_list = getHTMLClasses(raw_string)
        title_list, skill_list = getSections(wod_name, html_class_list)
        generateHTML(title_list, skill_list)
    updateGitRepo()
