import json
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

# GLOBAL VARIABLES */

FANS_BASEURL = 'http://www.diablofans.com/builds/'

with open(r'data\itemlist.json', 'r') as f:
    itemList = json.load(f)

with open(r'data\statlist2.json', 'r') as f1:
    statList = {int(k): v for k, v in json.load(f1).items()}

with open(r'data\typelist.json', 'r') as f2:
    typeList = json.load(f2)

# FUNCTION DECLARATIONS */
print('Build Number \n http://www.diablofans.com/builds/88437')
buildnumber = input('E.G. 88437: ')
while True:
    try:
        url = 'http://www.diablofans.com/builds/{}'.format(buildnumber)
        page = requests.get(url)
        page = page.content
        break
    except Exception:
        print('Exception')

fourthree = input('Items must roll with all stats or stats - 1? \n'
                  'E.G. If a helm needs Socket, CHC, Int, Vit roll with 4 or 3? \n [4\\3]: ')
buildtype = input(r'Full file or just the build? [Full\Build]: ').lower()

i = 0
equalstring = '=================='
while i <= len(url):
    equalstring += '='
    i += 1

print(equalstring)
print('Loading build from {}'.format(url))
print(equalstring + '\n')

soup = BeautifulSoup(page, 'html.parser')


def switch(importance):
    if importance == "1":
        return "Required"
    elif importance == "2":
        return "Recommended"
    elif importance == "3":
        return "Adequate"


def getItemInfos(name):
    for item in itemList:
        if item['name'].strip() == name:
            return item['type']


def getItemSlot(slot):
    slotObj = {}
    itemArr = []
    statArr = []

    ItemSlot_soup = soup.select('#item-{} li[data-item-id]'.format(slot))
    # print 'ItemSlot_soup: %s'%ItemSlot_soup
    for item in ItemSlot_soup:
        name = item.find('a').get_text()
        importance = switch(item.get('data-item-importance')[0])
        type = getItemInfos(name)

        print('NAME={} | TYPE={} | SLOT={}'.format(name, type, slot))

        itemdetails = {
            'name': name,
            'type': type,
            'importance': importance,
        }
        itemArr.extend([itemdetails])

    StatSlot_soup = soup.select('#item-{} .item-stat a'.format(slot))
    for stats in StatSlot_soup:
        stattitle = stats.get('title')
        stattitle_soup = BeautifulSoup(stattitle, 'html.parser')
        statArr.extend([stattitle_soup.get_text().rsplit(':', 1)[0]])

    slotObj['items'] = itemArr
    slotObj['stats'] = statArr
    return slotObj


resObj = OrderedDict()
# print soup.find(attrs={'class':'build-title'})
resObj['build_name'] = soup.find(attrs={'class': 'build-title'}).get_text()
resObj['build_url'] = FANS_BASEURL + soup.find(attrs={'class': 'd3build-bbcode-button'}).get('data-build-id')
resObj['build_class'] = soup.find(attrs={'class': 'classBadge'}).get('title')

resObj['item_head'] = getItemSlot('head')
resObj['item_shoulders'] = getItemSlot('shoulders')
resObj['item_amulet'] = getItemSlot('amulet')
resObj['item_torso'] = getItemSlot('torso')
resObj['item_wrists'] = getItemSlot('wrists')
resObj['item_hands'] = getItemSlot('hands')
resObj['item_waist'] = getItemSlot('waist')
resObj['item_legs'] = getItemSlot('legs')
resObj['item_feet'] = getItemSlot('feet')
resObj['item_rings'] = getItemSlot('rings')
resObj['item_weapon'] = getItemSlot('weapon')
resObj['item_offhand'] = getItemSlot('offhand')

if soup.select('#kanai-weapon .db-title span'):
    resObj['kanai_weapon'] = soup.select('#kanai-weapon .db-title span')[0].get_text()
    print('Kanai Weapon Slot | NAME={}'.format(resObj['kanai_weapon']))

if soup.select('#kanai-armor .db-title span'):
    resObj['kanai_armor'] = soup.select('#kanai-armor .db-title span')[0].get_text()
    print('Kanai Armor Slot | NAME={}'.format(resObj['kanai_armor']))

if soup.select('#kanai-jewelry .db-title span'):
    resObj['kanai_jewelry'] = soup.select('#kanai-jewelry .db-title span')[0].get_text()
    print('Kanai Jewelry Slot | NAME={}'.format(resObj['kanai_jewelry']))


def getItemType(name):
    type = "undefined"
    for item in itemList:
        # print 'item in itemlist: {}'.format(item)
        if name['name'] == item['name']:
            type = item['type']
            pickitType = typeList[type]
            return pickitType


def getPickitStat(stat):
    global statList
    for arr in statList:
        pickit = statList[arr][1]
        full = statList[arr][0]
        if (full == stat):
            return pickit


def generateString(item):
    k = 0
    string = ""
    while k < len(item['items']):
        name = item['items'][k]['name']
        statCount = len(item['stats'])
        stats = item['stats']
        atleastString = generateAtLeastString(statCount, stats)
        type = getItemType(item['items'][k])

        string += type + ' = name=' + name + ' ' + atleastString + '\n'

        # string += '\n'
        k += 1
    global pickitList
    pickitList += string


def generateCubeString(name):
    for item in itemList:
        if name == item['name']:
            type = item['type']
            pickitType = typeList[type]
            type = pickitType
    global pickitList
    pickitList += type + ' = name=' + name + ' ' + '& can_cubed=1 & cubed=0\n'


def generateAtLeastString(statCount, stats):
    string = ''
    if not stats or statCount == '0':
        return string

    i = 0

    while i < len(stats):
        pickit = getPickitStat(stats[i])
        if pickit == 'not_imp':
            stats.pop(i)
            i -= 1
        else:
            i += 1
    string += '& at_least['
    if fourthree == '4':
        string += str(statCount) + ', '
    else:
        string += str(statCount - 1) + ', '
    j = 0
    while j < len(stats):
        pickit = getPickitStat(stats[j])
        string += pickit
        if j < len(stats) - 1:
            string += ', '
            j += 1
        else:
            string += ']'
            j += 1
            return string


if buildtype == "full":
    with open(r'data\essentials.txt', 'r') as essentials:
        with open('pickit_sc_70.ini', 'w') as a_file:
            a_file.write(essentials.read())
            a_file.write('\n')

pickitList = ';||||' + resObj['build_class'] + '-Build: ' + resObj['build_name'] + ' Link: ' + resObj[
    'build_url'] + ' ||||\n'

for entry in resObj:
    if entry.startswith('item'):
        generateString(resObj[entry])
    if entry.startswith('kanai'):
        generateCubeString(resObj[entry])

pickitList += ';|||| End of Build ||||'


if buildtype == "full":
    with open(r'data\essentials.txt', 'r') as essentials:
        with open('pickit_sc_70.ini', 'w') as a_file:
            a_file.write(essentials.read())
            a_file.write('\n')
    with open('pickit_sc_70.ini', 'a') as a_file:
        pickitList += '\n'
        a_file.write(pickitList)
    if buildtype == "full":
        with open(r'data\essentials2.txt', 'r') as essentials2:
            with open('pickit_sc_70.ini', 'a') as a_file:
                a_file.write(essentials2.read())
    print('INFO | save successful')
else:
    with open(buildnumber + '.ini', 'w') as a_file:
        pickitList += '\n'
        a_file.write(pickitList)
    print('INFO | save successful')
