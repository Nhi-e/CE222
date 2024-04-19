import math
ordem = ('S', 'D')
Vdd = 'Vdd'
Vss = 'Vss'
Vout = 'Out'
class Transistor:
    def __init__(self, id, points):
        self.id = id
        self.points = points
        
class Link:
    def __init__(self, point, position):
        self.point = point
        self.position = position
pud = [Transistor('A', [('P2', 'Vdd')]),
       Transistor('D', [('P1', 'Vdd')]),
       Transistor('E', [('P2', 'P1')]),
       Transistor('B', [('Out', 'P2')]),
       Transistor('C', [('Out', 'P2')])]

pdn = [Transistor('A', [('Out', 'P3')]),
       Transistor('D', [('P3', 'Vss')]),
       Transistor('E', [('P3', 'Vss')]),
       Transistor('B', [('Out', 'P4')]),
       Transistor('C', [('P4', 'Vss')])]
def points(pud, pdn): #xác định các vị trí VDD, GND, VOUT
    ids = [transistor.id for transistor in pud]
    #lấy danh sách các POINTS của đỉnh
    pud_names = list(set([point for transistor in pud for point in transistor.points]))
    pdn_names = list(set([point for transistor in pdn for point in transistor.points]))
    points_pud = []
    points_pdn = []
    #duyệt qua các đỉnh trong pud và pdn
    for point in pud_names:
        links = []
        for pud_transistor in pud:
            #Duyệt qua các Points trong đỉnh
            for p in pud_transistor.points:
                if p == point: 
                    for value in p:
                        #print("value", value) 
                        #print("points", point)                                     
                        #Nếu points là vdd thì thêm transistor đó vào LINKS (transistor.ID, "S"). Đây cũng là một tuple
                        if value == Vdd:
                            links.append((pud_transistor.id, 'S'))
                            #print("links_pud:", pud_transistor.id)
                        #Nếu points là vout thì thêm transistor đó vào LINKS (transistor.ID, "D"). Đây cũng là một tuple
                        elif value == Out:
                            links.append((pud_transistor.id, 'D'))
                        
        points_pud.append((point, links))
        #print("points_pud: \n" , points_pud )
    for point in pdn_names:
        links = []
        for pdn_transistor in pdn:
            #Duyệt qua các Points trong đỉnh
            for p in pdn_transistor.points:
                if p == point: 
                    for value in p:
                        #print("value", value) 
                        #print("points", point)                                     
                        #Nếu points là vdd thì thêm transistor đó vào LINKS (transistor.ID, "S"). Đây cũng là một tuple
                        if value == Vss:
                            links.append((pdn_transistor.id, 'S'))
                            #print("links_pud:", pud_transistor.id)
                        #Nếu points là Out thì thêm transistor đó vào LINKS (transistor.ID, "D"). Đây cũng là một tuple
                        elif value == Out:
                            links.append((pdn_transistor.id, 'D'))
                        
        points_pdn.append((point, links)) #('P2','Vdd'), ('A', 'S')
        #print("points_pdn:", points_pdn)

    #Tìm phần tử đầu tiên là Vdd
    vdd_ele = next((a for a in points_pud if a[0][1] == Vdd), None)
    vdd_index = points_pud.index(vdd_ele) if vdd_ele else None
    #print("vdd_ele:", vdd_ele)
    #print("vdd_index:", vdd_index)
    #for a in points_pud:
        #print("vdd_index:", a[0][1])

    #Tìm phần tử đầu tiên là Vss
    vss_ele = next((a for a in points_pdn if a[0][1] == Vss), None)
    vss_index = points_pdn.index(vss_ele) if vss_ele else None
    #print("vss_ele:", vss_ele)
    #print("vss_index:", vss_index)
    #for a in points_pud:
        #print("vdd_index:", a[0][1])
    #Đảo các đỉnh có nối với Vdd/Vss lên đầu/cuối
    pud_2 = list_swap(points_pud, vdd_index, 0) if vdd_index is not None else points_pud
    pdn_2 = list_swap(points_pdn, vss_index, 0) if vss_index is not None else points_pdn
    #print("pdn_2", pdn_2)
    vout1_ele = next((a for a in pud_2 if a[0][0] == Out), None)
    vout1_index = pud_2.index(vout1_ele) if vout1_ele else None

    vout2_ele = next((a for a in pdn_2 if a[0][0] == Out), None)
    vout2_index = pdn_2.index(vout2_ele) if vout2_ele else None

    pud_3 = list_swap(pud_2, vout1_index, round(len(points_pud) / 2)) if vout1_index is not None else pud_2
    pdn_3 = list_swap(pdn_2, vout2_index, round(len(points_pdn) / 2)) if vout2_index is not None else pdn_2
    #print("pdn_3", pdn_3)
    return pud_3, pdn_3

def filter_transistor(id, g):
    for transistor in g:
        if transistor.id == id:
            return transistor
    return None

def list_swap(lst, n1, n2):
    lst[n1], lst[n2] = lst[n2], lst[n1]
    return lst
#trích xuất các ĐIỂM KẾT NỐI duy nhất trong pud và pdn
def nodes(pud, pdn):
    nodes_pud = list(set([item for transistor in pud for points in transistor.points for item in points]))
    nodes_pdn = list(set([item for transistor in pdn for points in transistor.points for item in points]))
    #print("nodes_pud", nodes_pud)
    #print("nodes_pdn", nodes_pdn)
    return nodes_pud, nodes_pdn

def index_of(l, x):
    if isinstance(l, list):
        for i, y in enumerate(l):
            if x == y:
                return i
    elif isinstance(l, tuple) and len(l) > 0:
        if x == l[0]:
            return 0
        elif x == l[1]:
            return 1
    return -1

Vdd = 'Vdd'
Vss = 'Vss'
Out = 'Out'

def next_step(graph, point):
        return [(edge, vertex) for edge, vertex in graph if edge == point]

def remove_edge(edge, vertices, graph):
        return [(e, v) for e, v in graph if (e, v) != edge and v not in vertices]
def reach(graph, x):
    visited = [x]
    
    def loop(g, next_point):
        nonlocal visited
        next_vertices = next_vertex(g, next_point)
        
        if next_vertices:
            for next_step in next_vertices:
                next_edge, next_vertex = next_step
                if next_vertex not in visited:
                    visited.append(next_vertex)
                    loop(remove_edge(next_edge, (x, next_vertex), g), next_vertex)
    
    loop(graph, x)
    return len(visited)
def next_vertex(g, x): #next_vertex(pud, start_ele)
    acc = []
    for i in g:
        if isinstance(i, tuple) and i[0] == 'transistor':
            id, (e1, e2) = i[1]
            if e1 == x:
                acc.append((id, e2))
            elif e2 == x:
                acc.append((id, e1))
    return acc

def path_start(pud, pdn):
    # Vertices to begin
    pud_point = [a for a in pud]
    #Chứa các điểm kết nối trong pud
    vertices_pud = list(set([item for transistor in pud for item in transistor.points]))
    #print("start", vertices_pud)
    pdn_point = [a for a in pud]
    #Chứa các điểm kết nối trong pdn
    vertices_pdn = list(set([item for transistor in pdn for item in transistor.points]))
    
    start_ele_pud = None
    start_ele_pdn = None

    for vertex in vertices_pud:
        #print("start", vertex[0], vertex[1])
        deg = sum(1 for transistor in pud for point1, point2 in transistor.points if point1 == vertex[0] or point2 == vertex[0])
        #print("end", deg)
        #Tìm điểm kết nối có bậc lẻ ở pud
        if deg % 2 != 0:
            start_ele_pud = vertex[0]
            #print("oke", start_ele_pud)         
            break
    for vertex in vertices_pdn:
        #print("start", vertex[0], vertex[1])
        deg = sum(1 for transistor in pdn for point1, point2 in transistor.points if point1 == vertex[0] or point2 == vertex[0])
        #print("end", deg)
        #Tìm điểm kết nối có bậc lẻ ở pud
        if deg % 2 != 0:
            start_ele_pdn = vertex[0]
            #print("oke", start_ele_pdn)         
            break
    if start_ele_pud:
        #Trả về điểm kết nối bậc lẻ của pud
        return (start_ele_pud, True)
    elif start_ele_pdn:
        #Trả về điểm kết nối bậc lẻ của pdn
        return (start_ele_pdn, False)
    else:
        return (Vdd, True)

def euler_path(pud, pdn):
    #Đỉnh bậc lẻ và cờ (xem nó thuộc pud hay pdn)
    start_ele, pud_flag = path_start(pud, pdn)
    print("start_ele", start_ele)
    #Lấy các điểm kết nối của pud và pdn
    nodes_pud, nodes_pdn = nodes(pud, pdn)
    
    if pud_flag:
        path1, edge1 = any_path(pud, start_ele)
        #print("end", path1)
        path2, edge2 = any_path(pdn, nodes_pdn[0])
    else:
        path1, edge1 = any_path(pud, nodes_pud[0])
        path2, edge2 = any_path(pdn, start_ele)
    
    return path1, edge1, path2, edge2

def any_path(g, vertex): #any_path(pud, start_ele)
    # Tìm đỉnh tiếp theo cho start_ele
    next_vertices = next_vertex(g, vertex)
    if not next_vertices:
        return [], []
    next_ele = 0
    if len(set([v for _, v in next_vertices])) <= 1:
        next_ele = 0
    else:
        for a, _ in next_vertices:
            for i in range(len(next_vertices)):
                if len(set([v for _, v in next_vertices])) <= 1 or \
                        len(set([v for _, v in next_vertex(remove_edge(a, (vertex, next_vertices[i][1]), g), vertex)])) <= 1:
                    next_ele = i
                    break
    
    stack = next_vertices[next_ele][1]
    id = next_vertices[next_ele][0]
    p2 = stack[1]
    
    euler1, euler2 = any_path(remove_edge(id, (vertex, p2), g), p2)
    return [(id, [vertex] + stack)] + euler1, [id] + euler2
# Testing the function
pud = [Transistor('A', [('P2', 'Vdd')]),
       Transistor('D', [('P1', 'Vdd')]),
       Transistor('E', [('P2', 'P1')]),
       Transistor('B', [('Out', 'P2')]),
       Transistor('C', [('Out', 'P2')])]

pdn = [Transistor('A', [('Out', 'P3')]),
       Transistor('D', [('P3', 'Vss')]),
       Transistor('E', [('P3', 'Vss')]),
       Transistor('B', [('Out', 'P4')]),
       Transistor('C', [('P4', 'Vss')])]

#pud_result, pdn_result = points(pud, pdn)
#nodes_pud, nodes_pdn = nodes(pud, pdn)
#a, b = path_start(pud, pdn)
#print("S", a)
path1, edge1, path2, edge2 = euler_path(pud, pdn)
#print(path1, edge1, path2, edge2)
start_test = ('P2', 'Vdd')
next_test = next_vertex(pud, start_test)
print("S", next_test)