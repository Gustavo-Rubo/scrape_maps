import json
import time
import random
import requests
import numpy as np
from os import path
from multiprocessing import Pool

panoids = np.array([])
if path.exists('panoids.npy'):
    panoids = list(np.load('panoids.npy'))

user_panoids = np.array([])
if path.exists('user_panoids.npy'):
    user_panoids = list(np.load('user_panoids.npy'))

def interp2d(p1, p2, d):
    p1 = np.array(p1)
    p2 = np.array(p2)
    length = np.linalg.norm(p1-p2)
    n = length//d
    return list(zip(np.arange(p1[0], p2[0], (p2[0]-p1[0])/n), np.arange(p1[1], p2[1], (p2[1]-p1[1])/n)))

# returns fill points in paralelogram (p1, p2, p3, p4 are defined clockwise)
def fill_points(p1, p2, p3, p4, d):
    l1 = interp2d(p1, p4, d)
    l2 = interp2d(p2, p3, d)
    ps = []
    n = min(len(l1), len(l2))
    ps = [interp2d(l1[i], l2[i], d) for i in range(n)]
    return [item for sublist in ps for item in sublist]

def get_url(coord):
    url = f'https://www.google.com/maps/preview/photo?'\
        f'authuser=0&hl=pt-BR&gl=br&pb=!1e3!5m54!2m2!1i203'\
        f'!2i100!3m3!2i4!3sCAEIBAgFCAYgAQ!5b1!7m42!1m3!1e1'\
        f'!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e8'\
        f'!2b0!3e3!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3'\
        f'!1e9!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2'\
        f'!1m3!1e10!2b0!3e4!2b1!4b1!8m0!9b0!11m1!4b1!6m3'\
        f'!1sl5XrZNXpEpGw5OUP2LCf6Ak!7e81!15i11021!9m2!2d'\
        f'{coord[1]}!3d{coord[0]}!10d30.619798400234394'

    return url


def get_panoids(coord):
    try:
        url = get_url(coord)
        headers = {'Cookie': '1P_JAR=2023-08-31-18; NID=511=DLlB7fwIV1RltKvOEuIfxg9tio-Zfo4N5JQ7d74XY2iKKBgHSiC3DQ3G_EE8aDXyRrETgSxhLo5gejro6m06ygyBe3v-KYQ5Bggl_ILFN5dY9dNfX2z8_qINh1mhuCMLYi5pk_FCBmYhPe3_DOekFbZY3z5L5QnUfO3fv3H0mwi3N8lRhMOKUIcLbq5E8zooib8ng7zu-q2h4W4ywq1X83xzCwB1QRwiLqLuvEd145yLqKo-5X0e15IqKopTnzEe7IxRfdWOkA; AEC=Ad49MVHV-liDfobvLNn1FY9nsQmpIWGyH279z0Kg-icdNGD2AC_OXNkPDYk; OGPC=19037049-1:; OTZ=7168444_68_64_73560_68_416340; GOOGLE_ABUSE_EXEMPTION=ID=0f1f29dcf7ee7703:TM=1693505131:C=r:IP=143.107.107.242-:S=Xw1etVXV1-npf_FoMspkA8k'}
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            print(f'http status {res.status_code}')
            return [['-']]

        res = json.loads(res.content[4:])
        if res[0] is None:
            print('-')
            return [['-']]

        panoids = []
        for b in res[0]:
            panoids.append([b[0], *b[8][0][1:]])
        print(panoids)
        return panoids

    except:
        print('request failed')
        return [['-']]


coord1 = (-23.557219596586915, -46.72547921173824)
coord2 = (-23.559999403940296, -46.73783883085288)
# coord1 = (-23.562674361214523, -46.72381087772634)
# coord2 = (-23.563028395587935, -46.72441169250808)

# raia
# vertices = [
#     (-23.551174633220622, -46.73134619863761),
#     (-23.559953815898076, -46.71324114839362),
#     (-23.560514381489387, -46.71377759019548),
#     (-23.551887832071223, -46.731633352053414)
# ]

# tv. 8
# vertices = [
#     (-23.557585000740993, -46.71957495341949),
#     (-23.55795871813798, -46.71882393489689),
#     (-23.56061404798524, -46.71993973384475),
#     (-23.56027967606871, -46.721055532792505)
# ]

# av. da universidade
# vertices = [
#     (-23.560440250108066, -46.719016283766905),
#     (-23.5629185128293, -46.71354457738802),
#     (-23.56470834016572, -46.71442434194306),
#     (-23.562259614209086, -46.71963855625716)
# ]

# lineu
# vertices = [
#     (-23.567717555391187, -46.730775088075596),
#     (-23.562171105242196, -46.7196170985971),
#     (-23.56282017001765, -46.719102114467326),
#     (-23.56879928256079, -46.730024069553)
# ]

# almeida prado
# vertices = [
#     (-23.559682993832908, -46.7433975637004),
#     (-23.55893556778384, -46.738140434042265),
#     (-23.559820677115066, -46.7379473149936),
#     (-23.560784456050527, -46.743140071635516)
# ]

# travessa R
# vertices = [
#     (-23.55933268659516, -46.7364936943128),
#     (-23.559411362983802, -46.73550664139739),
#     (-23.562991088830707, -46.73617182923169),
#     (-23.56289274601697, -46.737309085851614)
# ]

# mello moraes p1
# vertices = [
#     (-23.560581668689885, -46.712643491777754),
#     (-23.565911836870548, -46.71228944018801),
#     (-23.565685653317782, -46.71398459628186),
#     (-23.560355475980213, -46.7137807483972)
# ]

# ernesto moraes leme
# vertices = [
#     (-23.559947014147088, -46.74188320214952),
#     (-23.56848308766441, -46.734823628036025),
#     (-23.56950580580257, -46.735596104230694),
#     (-23.560714103340466, -46.74329940850641)
# ]

# lineu sul
# vertices = [
#     (-23.568070064676157, -46.734888001040886),
#     (-23.56631961926398, -46.729459210006155),
#     (-23.568365081268713, -46.728472157090756),
#     (-23.57029250669926, -46.73368637140474)
# ]

# luciano gualberto
# vertices = [
#     (-23.560048565130174, -46.72699928536493),
#     (-23.5628021957089, -46.72109842554323),
#     (-23.563470925851508, -46.721699240361296),
#     (-23.560638633691426, -46.72749281182129)
# ]

# almeida prado
# vertices = [
#     (-23.55635888213657, -46.73442289234088),
#     (-23.55163810576983, -46.73165485263972),
#     (-23.55183480816939, -46.73111841083786),
#     (-23.556614586011772, -46.73383280635853)
# ]

# tv 12
# vertices = [
#     (-23.561163939779764, -46.72858840788022),
#     (-23.56402572321951, -46.72276264991213),
#     (-23.565127149029298, -46.72322398986171),
#     (-23.56280627672978, -46.72947890127129)
# ]

# poli
# vertices = [
#     (-23.551978275507963, -46.73090583645795),
#     (-23.553394522549574, -46.72783738935137),
#     (-23.558626636227903, -46.73047668301647),
#     (-23.556895734459207, -46.73390991054832)
# ]

# lago
# vertices = [
#     (-23.562312399821913, -46.72728973989385),
#     (-23.56587237850229, -46.726603094387485),
#     (-23.565931382861027, -46.727976385400225),
#     (-23.562341902804064, -46.72846722964892)
# ]

# r. anf
vertices = [
    (-23.559967618565043, -46.723247144896256),
    (-23.556702522670395, -46.721358869753736),
    (-23.557017234254772, -46.72073659726309),
    (-23.560479011791408, -46.722710703093895)
]

# lucio martins
# vertices = [
#     (-23.55445669780072, -46.725691622144645),
#     (-23.55485501131267, -46.72485477293375),
#     (-23.556792469711244, -46.72600275839033),
#     (-23.55661544424252, -46.726743048076884)
# ]

# lineu sul
# vertices = [
#     (-23.56268766663088, -46.74111942463358),
#     (-23.56744738179926, -46.73626999074485),
#     (-23.568352101539, -46.73721412831611),
#     (-23.563435071335675, -46.742492715646314)
# ]

coords = fill_points(vertices[0], vertices[1], vertices[2], vertices[3], 1.5e-4)
random.shuffle(coords)

start = time.time()
panoids_temp = []
for i in range(len(coords)//50):
    for j in range(50):
        if 50*i + j < len(coords):
            panoids_temp.append(get_panoids(coords[50*i+j]))
            # time.sleep(26)
stop = time.time()

all_new_panoids = []
for p in panoids_temp:
    all_new_panoids.extend(p)

new_panoids = [p for p in all_new_panoids if len(p[0]) == 22]
new_user_panoids = [p for p in all_new_panoids if len(p[0]) == 44]

if len(new_panoids) != 0:
    if len(panoids) == 0:
        panoids = new_panoids
    else:
        panoids = np.append(panoids, new_panoids, axis=0)
if len(new_user_panoids) != 0:
    if len(user_panoids) == 0:
        user_panoids = new_user_panoids
    else:
        user_panoids = np.append(user_panoids, new_user_panoids, axis=0)

print(f'run time: {stop - start:.0f}s')
print(f'time per request: {(stop - start)/len(coords):.2f}s')
print('new panoids:', len(np.unique(new_panoids, axis=0)))
print('new user panoids:', len(np.unique(new_user_panoids, axis=0)))
print('panoids:', len(np.unique(panoids, axis=0)))
print('user panoids:', len(np.unique(user_panoids, axis=0)))
np.save('panoids', np.unique(panoids, axis=0))
np.save('user_panoids', np.unique(user_panoids, axis=0))
