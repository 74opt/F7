from colored import fg, bg, attr, stylize
import copy

'''
Notes for tiles:
Basic:
    g = grass
    s = stone
    d = dirt
Interactive:
    e = entrance
    q = quest
Solid (cant go through):
    a = water
    w = wall 
    r = tree/bush
Player:
    f = player
'''

g = stylize('░', fg(82))  # grass 1
v = stylize('░', fg(28))  # grass 2
b = stylize('░', fg(40))  # grass 3

s = stylize('▓', fg(238))  # stone 1
z = stylize('▓', fg(251))  # stone 2
x = stylize('▓', fg(245))  # stone 3

d = stylize('░', fg(95))  # dirt 1
n = stylize('▓', fg(94))  # dirt 2

q = stylize('Q', fg(14))  # quest (might scrap oof)

a = stylize('▒', fg(33))  # water 1
u = stylize('▒', fg(27))  # water 2

w = stylize('█', fg(241))  # wall

r = stylize('#', fg(65))  # tree/bush 1
h = stylize('#', fg(70))  # tree/bush 2
y = stylize('#', fg(28))  # tree/bush 3

f = stylize('7', fg(196))  # player

k = ' '  # blank


# new area symbols
# formatting: ab = area a leads to area b
def area_color(symbol):
    return stylize(symbol, fg(201))


pf = area_color('F')  # plains to forest
fp = area_color('P')  # forest to plains
fc = area_color('C')  # forest to city
cf = area_color('F')  # city to forest

level_dict = {
    'plains': [[k,k,k,k,k,r,r,h,y,r,r,r,r,y,h,h,h,h,y,r,h,y,r,h,y,h,y,y,h,r,h,r,r,r,h,y,r,h,h,h,r,y,y,y,a,a,u,u,u,u,u,u,u,u,u,u,u,u,u,u],
               [k,k,k,k,y,h,r,r,h,y,y,h,g,g,g,g,g,g,g,g,g,g,g,g,r,y,h,g,g,d,g,g,g,h,r,h,g,g,g,g,g,r,y,a,a,a,u,u,u,u,u,u,u,u,u,u,u,u,u,u],
               [k,k,k,h,y,y,r,h,r,r,g,g,g,y,g,g,g,g,g,y,g,g,g,g,g,g,g,g,g,d,g,g,g,g,g,g,g,g,g,g,g,g,v,a,a,u,u,u,u,u,u,u,u,u,u,u,u,a,a,u],
               [k,k,k,r,r,y,h,y,g,g,g,g,g,g,b,b,b,b,g,g,g,g,g,g,g,g,g,g,g,d,g,g,g,g,h,g,g,r,g,g,g,v,v,a,a,u,u,u,u,u,u,u,u,u,u,a,a,a,a,u],
               [k,k,k,r,h,h,y,g,g,g,g,g,b,b,b,b,w,w,w,w,g,g,g,g,g,h,g,g,g,d,d,g,g,g,g,g,g,g,g,g,g,v,v,a,a,u,u,u,u,u,u,u,u,u,a,a,v,v,a,a],
               [k,k,k,r,y,r,g,g,g,g,r,g,b,b,b,b,w,s,s,w,g,g,g,g,g,g,g,g,g,g,d,g,g,g,g,g,g,g,g,g,v,v,a,a,u,u,u,u,u,u,u,u,u,a,a,v,v,v,a,a],
               [k,k,r,h,h,r,g,g,h,g,g,b,b,b,b,b,w,s,s,w,w,w,w,w,g,g,g,g,g,g,d,g,g,g,g,g,g,g,g,v,v,s,s,s,s,s,s,s,u,u,u,u,u,s,s,s,s,g,v,a],
               [k,k,h,y,r,y,g,y,y,g,g,g,g,b,b,b,w,s,s,s,s,x,x,w,g,g,g,g,g,g,d,g,g,g,g,g,g,g,g,v,s,z,z,z,z,z,z,z,z,z,z,u,u,a,a,v,g,g,v,a],
               [k,k,r,r,r,h,g,g,r,g,g,g,b,b,b,b,w,s,s,s,x,x,x,z,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,z,z,z,z,z,z,z,z,u,u,u,u,a,v,v,r,g,v,a],
               [k,k,h,r,y,y,r,g,g,g,g,g,b,b,b,b,w,w,w,w,w,w,w,w,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,v,v,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,v,v,a],
               [k,y,y,h,h,y,r,g,g,g,g,b,b,b,b,b,b,b,b,b,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,v,s,s,s,s,s,s,s,u,u,u,u,s,s,s,s,g,g,g,v,a,a],
               [k,y,r,h,r,y,h,g,h,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,y,g,g,g,v,v,v,v,a,a,u,u,u,u,u,u,u,a,a,v,g,g,g,g,g,v,a,u],
               [k,r,y,h,h,h,y,g,g,g,g,g,g,g,g,g,g,g,h,g,g,g,y,g,g,v,v,r,v,v,v,v,v,v,v,v,v,v,a,a,a,a,u,u,u,u,u,u,a,a,v,v,g,g,g,g,v,v,a,u],
               [k,h,y,r,y,y,y,g,g,h,g,g,g,g,g,g,g,g,g,g,g,v,v,v,v,v,a,a,a,a,a,a,a,a,a,a,a,a,a,a,u,u,u,u,u,u,a,a,a,a,v,g,g,g,g,g,v,a,a,u],
               [k,k,k,y,h,h,r,g,g,g,g,r,g,g,g,g,r,g,v,v,v,v,a,a,a,a,a,a,a,a,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,a,a,a,a,v,v,h,r,g,g,g,v,a,u,u],
               [k,k,k,k,k,r,h,y,h,y,g,g,g,g,g,g,v,v,v,a,a,a,a,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,a,a,a,a,a,a,v,v,v,h,g,g,g,g,g,v,a,u,u],
               [k,k,k,k,k,r,r,y,y,y,r,g,g,g,y,v,v,a,a,a,u,u,u,u,u,u,u,u,u,u,u,a,a,a,a,a,a,a,a,a,a,a,v,v,v,v,v,v,g,g,g,g,g,g,g,v,a,a,u,u],
               [k,k,k,k,k,k,k,k,h,h,y,h,y,g,v,v,a,a,u,u,u,u,u,u,a,a,a,a,a,a,a,a,v,v,v,v,v,v,v,v,v,v,g,g,g,y,g,g,g,v,v,v,v,v,v,v,a,u,u,u],
               [k,k,k,k,k,k,k,k,y,h,r,r,r,v,v,a,a,u,u,u,u,u,u,a,a,v,v,v,v,v,v,v,v,v,v,v,v,v,v,v,r,v,v,v,v,v,v,v,v,v,a,a,a,a,a,a,a,u,u,u],
               [k,k,k,k,k,k,k,k,r,r,a,a,a,a,a,a,u,u,u,u,u,u,u,u,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,u,u,u,u,u,u,u,u,u]],

    'forest': [[g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g],
               [g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
               [x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,w],
               [s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,w],
               [x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,w],
               [g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
               [d,d,d,g,g,g,d,d,g,g,g,g,d,g,d,g,d,d,d,g,g,g,g,g,g,g,g,d,d,g,g,g,g,g,g,g,d,d,d,d,g,g,g,d,d,d,d,d,g,g,g,g,g,g,g,d,d,d,d,g],
               [r,d,h,y,h,h,d,d,y,r,y,h,d,h,y,d,h,y,r,y,h,d,h,y,d,h,y,y,y,r,y,h,y,y,y,d,h,r,y,h,d,r,r,r,y,h,d,h,d,h,d,d,d,y,y,r,h,d,r,y],
               [d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,n,n,n,n,n,n,n],
               [d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,n,n,n,n,a,a,a,a,a],
               [d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,n,n,a,a,a,a,a,u,u,u],
               [d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,n,n,a,a,u,u,u,u,u,u,u],
               [d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,n,n,a,a,u,u,u,u,u,u,u,u],
               [d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,n,n,a,a,u,u,u,u,u,u,u,u,u],
               [d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,n,n,a,a,a,u,u,u,u,u,u,u,u,u,u],
               [d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,n,n,a,a,u,u,u,u,u,u,u,u,u,u,u,u],
               [d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,n,n,a,a,u,u,u,u,u,u,u,u,u,u,u,u],
               [d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,n,n,a,a,a,u,u,u,u,u,u,u,u,u,u,u,u],
               [d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,n,n,a,a,u,u,u,u,u,u,u,u,u,u,u,u,u],
               [d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,fp,d,d,d,d,d,d,d,d,d,d,d,d,d,n,n,a,a,u,u,u,u,u,u,u,u,u,u,u,u,u]]
}

level_names = {
    'plains': 'Kwéleches Plains',
    'forest': 'Harrison Forest',
    'city': 'Reliquiae Main'
}

# tiles that you can't go to
collision = [a, u, w, r, h, y, k]

current_level = None
current_level_name = None


def change_level(level):  # this function doesn't work outside of the file???
    global current_level
    global current_level_name
    current_level = copy.deepcopy(level_dict[level])
    current_level_name = level
    return


def draw_level(level):
    for i in range(len(level)):
        for j in range(len(level[0])):
            print(level[i][j], end='')
        print('')
    return


change_level('plains')
