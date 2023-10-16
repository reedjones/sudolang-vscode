import json 
import pathlib 
import os 
import re

regex = (r"(?P<title>(?<=(^#)\s).*)\n+(?P<description>^[A-Za-z].*(?:\n[A-Za-z].*)*)\n+(?P<content>(.|\n)*)\n")




def load(what):
  assert os.path.isfile(what)
  with what.open(mode='r', encoding='utf-8') as f:
    return f.read() 

def load_json(what):
  return json.load(load(what))

# current working directory
# print(pathlib.Path().absolute())

ROOT_PATH = pathlib.Path().absolute()
print(pathlib.Path().resolve())
SUDO_LANG_PATH =  ROOT_PATH / "sudolang-llm-support"
EXAMPLES_PATH = SUDO_LANG_PATH / "examples"
print(ROOT_PATH, SUDO_LANG_PATH, EXAMPLES_PATH)

print(EXAMPLES_PATH)
print(pathlib.Path(EXAMPLES_PATH).iterdir())


def get_files():
  data = []
  print('hell')
  files = [i for i in pathlib.Path(EXAMPLES_PATH).iterdir() if '.sudo' in str(i)]
  for filename in files:
    # print(filename)
    item = {'name':filename.name, 'content':load(filename), 'path':filename }
    yield item 


def make_snippit_code(name, body, description):
  d = dict()
  d[name] = {
    "prefix": f"sudo example {name.lower()}",
    "body": body,
    "description":description
  }
  return d
  
    



example = """
# AIFriend

Roleplay as an expert chatbot character designer.
Your job is to craft in-depth character descriptions to instruct the
chatbot on the role it will play as a chat friend.

function list():select=state,format=yaml

AIFriend {
  State {
    Name
    Appearance
    Hometown
    Gender
    Age
    Likes
    Dislikes
    Occupation
    HobbiesAndActivities
    Favorites {
      Music
      TV
      Film
      Foods
      Colors
    }
    // close family and friends
    Relationships
    Pets
  }
  Constraints {
    You are instructing a chatbot on its persona. It will be a chat friend.
    Its responses should be natural chat interactions and emotes.

    Instruct the AI:
    - The persona must strictly generate their own dialog and emotes -
      avoid generating any extra text or narrative.
    - Avoid speaking or acting on behalf of other people or character.
    - Always stay in character. Never break the 4th wall.
    - You are a friend, not an assistant. Engage in normal, "human"
    - Typical chat responses are brief and informal.
  }
  /craft - Generate a comprehensive character description,
    imperatively instructing the AI how to play the role: "Roleplay as..."
  /randomize [short description?] - Initialize all state props to creative,
    random values which form a congruent character persona
  /pick [property] - List 10 creative options for the selected
    character property, which agree with other property settings
  /list - List current property settings
  /revise
}

/randomize
"""




def test_regex(test_str):
  matches = re.finditer(regex, test_str, re.MULTILINE)
  for matchNum, match in enumerate(matches, start=1):
    print(f"Name: {match['title']}")
    print(f"description: {match['description']}")
    print(f"content: {match['content']}")
    # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    # for groupNum in range(0, len(match.groups())):
    #   groupNum = groupNum + 1
    #   print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))


def parse_content(test_str):
  matches = re.finditer(regex, test_str, re.MULTILINE)
  for matchNum, match in enumerate(matches, start=1):
    return match



def dump(what, where):
  with open(where, "w") as outfile:
    json.dump(what, outfile)



def main():
  targets = [i for i in get_files() if i['name'].endswith('.sudo')]
  for target in targets:
    print(f"loading {target['name']}")
    d = parse_content(target['content'])
    snippit = make_snippit_code(d['title'], d['content'], d['description'])
    new_path = target['path'].with_suffix(".json")
    dump(snippit, new_path)
    print(f"Wrote snippit {d['title']} to {new_path} \n")







if __name__ == '__main__':
  main()
   
