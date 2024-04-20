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
pud = [
    Transistor('A', ('P1', 'Vdd')),
    Transistor('B', ('P1', 'Vdd')),
    Transistor('E', ('P2', 'P1')),
    Transistor('D', ('Out', 'P2')),
    Transistor('C', ('Out', 'P2'))
]

pdn = [
    Transistor('A', ('Out', 'P3')),
    Transistor('B', ('P3', 'Vss')),
    Transistor('E', ('Out', 'Vss')),
    Transistor('D', ('Out', 'P4')),
    Transistor('C', ('P4', 'Vss'))
]
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
    nodes_pud = []
    for transistor in pud:
        for points in transistor.points:
            nodes_pud.append(points)
    nodes_pud = list(set(nodes_pud))
    nodes_pdn = []
    for transistor in pdn:
        for points in transistor.points:
            nodes_pdn.append(points)
    nodes_pdn = list(set(nodes_pdn))
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
def next_vertex(g, x): #next_vertex(pud, start_ele)
    # Tìm đỉnh kế tiếp nối với start_ele => trả về cạnh đó
    acc = []
    for i in g:
        #print("i", i[0])
        if i:
            id = i.id 
            e = i.points
            #print("e", x)
            if e[0] == x:
                acc.append((id, e[1]))
                
            elif e[1] == x:
                acc.append((id, e[0]))
    return acc
def reach(graph, x):
    #số lượng các đỉnh có thể đạt được tử đỉnh x
    visited = [x]
    next_vertex = []
    def loop(g, next_point):
        nonlocal visited
        next_vertices = [] #trả về các cạnh nối với điểm next_point
        for i in g:
            if i:
                id = i.id 
                e = i.points
                #print("e", e[0][0])
            if e[0][0] == x:
                next_vertices.append((id, e[0]))
                #print("e", next_vertices)
            elif e[0][1] == x:
                next_vertices.append((id, e[0]))
                
        if next_vertices:
            #duyệt qua các phần tử trong next_vertices
            for next_step in next_vertices:
                next_edge, next_vertex = next_step
                #print("next_edge", next_edge)
                #print("next_vertex", next_vertex)
                if next_vertex not in visited:
                    #print("not visited", next_vertex)
                    visited.append(next_vertex)
                    loop(remove_edge(next_edge, (x, next_vertex), g), next_vertex)
    
    loop(graph, x)
    return len(visited)
def path_start(pud, pdn):
    # Vertices to begin
    pud_point = [a for a in pud]
    #Chứa các điểm kết nối trong pud
    vertices_pud = list(set([item for transistor in pud for item in transistor.points]))
    #print("start", vertices_pud)
    pdn_point = [a for a in pdn]
    #Chứa các điểm kết nối trong pdn
    vertices_pdn = list(set([item for transistor in pdn for item in transistor.points]))
    #print("pdn", vertices_pdn)
    start_ele_pud = None
    start_ele_pdn = None

    for vertex in vertices_pud:
        #print("start", vertex)
        deg = sum(1 for transistor in pud for point in transistor.points if point == vertex)
        #print("end", deg)
        #Tìm điểm kết nối có bậc lẻ ở pud
        if deg % 2 != 0:
            start_ele_pud = vertex
            #print("oke", start_ele_pud)         
            break
    for vertex in vertices_pdn:
        #print("start", vertex)
        deg = sum(1 for transistor in pdn for point in transistor.points if point == vertex)
        #print("end", deg)
        #Tìm điểm kết nối có bậc lẻ ở pud
        if deg % 2 != 0:
            start_ele_pdn = vertex
            break
    if start_ele_pud:
        #print("oke", start_ele_pud) 
        return (start_ele_pud, True)
    elif start_ele_pdn:
        #Trả về điểm kết nối bậc lẻ của pdn
        #print("oke", start_ele_pdn)
        return (start_ele_pdn, False)
    else:
        return (Vdd, True)

def euler_path(pud, pdn):
    #Đỉnh bậc lẻ và cờ (xem nó thuộc pud hay pdn)
    start_ele, pud_flag = path_start(pud, pdn)
    
    #Lấy các điểm kết nối của pud và pdn
    nodes_pud, nodes_pdn = nodes(pud, pdn)
    #print("end", nodes_pud[0])
    if pud_flag:
        #print("start_ele", start_ele)
        #print("pdn", nodes_pdn[0])
        path1, edge1 = any_path(pud, start_ele)
        path2, edge2 = any_path(pdn, nodes_pdn[0])
    else:
        path1, edge1 = any_path(pud, nodes_pud[0])
        #print("start_ele", start_ele)
        path2, edge2 = any_path(pdn, start_ele)
        
    
    return path1, edge1, path2, edge2

def any_path(g, vertex): #any_path(pud, start_ele)
    #tìm đường đi tiếp theo cho start_ele
    #print('vertex', vertex)
    next_vertices = next_vertex(g, vertex) #next_vertex trả về cạnh nối với start_ele
    
    if not next_vertices:
        return [], []
    next_ele = 0
    #print(next_vertices)
    #Nếu chỉ có 1 cạnh để đi tiếp => chọn cạnh đó
    if len(set([item for sublist in map(lambda x: x[1], next_vertices) for item in sublist])) <= 1:
        #print("chi co 1 canh")
        next_ele = 0
    else:
        #print("nhieu hon 1 canh")
        #i là chỉ số, a là phẩn tử tương ứng với chỉ số
        for i, a in enumerate(next_vertices):
            #print('a0', a[0])
            #print([vertex] + [a[1]])
            #print('vertex',vertex)
            result = remove_edge(a[0], ([vertex] + [a[1]]), g)
            #for transistor in result:
                #print(f"Transistor ID: {transistor.id}, Points: {transistor.points}")
            #reach: khoảng cách từ điểm bắt đầu đến các đỉnh khác trong đồ thị - số lượng đỉnh từ điểm bắt đầu
            #reach(remove_edge): Sau khi loại bỏ cạnh
            #print("reach", reach(remove_edge(a[0], [vertex] + [a[1]], g), vertex))
            #print((reach(g, vertex)))
            
            #Chọn đỉnh có số lượng đỉnh ít nhất
            if all(reach(g, vertex) <= reach(remove_edge(a[0], [vertex] + [a[1]], g), vertex) for _ in range(i + 1)):
                next_ele = i
                break
    stack = next_vertices[next_ele]
    #print('stack', stack)
    id_ = stack[0]
    #print('id_', id_)
    p2 = stack[1]
    #print('points', p2)
    result = remove_edge(id_, [vertex] + [p2], g)
    #for transistor in result:
        #print(f"Transistor ID: {transistor.id}, Points: {transistor.points[0]}")
    #euler1: đường đi từ điểm bắt đầu đến đỉnh tiếp theo
    #euler2: id của đỉnh tiếp theo
    euler1, euler2 = any_path(remove_edge(id_, [vertex] + [p2], g), p2)
    #print('euler1', euler1)
    #print('euler2', euler2)
    return [(id_, [vertex] + [p2])] + euler1, [id_] + euler2
    #return vertex
def remove_edge(id, points, g): #(tên đỉnh, điểm kết nối, pud/pdn) (A, 'P1, P2', pud)
    g_new = remove_edge_2(id, points, g)  # Gọi hàm remove_edge_2 để loại bỏ cạnh từ đồ thị g   
    return remove_edge_2(id, reverse_pair(points), g_new)  # Áp dụng hàm remove_edge_2 lần nữa sau khi đảo ngược cặp points
def remove_edge_2(id_, points, g):
    result = []
    result_done = []
    for a in g:
        if a.id != id_ :
            result.append(a)
    for b in result:
        s = [b.points[0]] + [b.points[1]]
        if (s != points):
            result_done.append(b)
    return result_done
def reverse_pair(points):
    if isinstance(points, tuple):  # Kiểm tra xem points có phải là một cặp không
        return (points[1], points[0])  
# Testing the function
pud = [
    Transistor('A', ('P1', 'Vdd')),
    Transistor('B', ('P1', 'Vdd')),
    Transistor('E', ('P2', 'P1')),
    Transistor('D', ('Out', 'P2')),
    Transistor('C', ('Out', 'P2'))
]

pdn = [
    Transistor('A', ('Out', 'P3')),
    Transistor('B', ('P3', 'Vss')),
    Transistor('E', ('Out', 'Vss')),
    Transistor('D', ('Out', 'P4')),
    Transistor('C', ('P4', 'Vss'))
]

#pud_result, pdn_result = points(pud, pdn)
#nodes_pud, nodes_pdn = nodes(pud, pdn)
#a, b = path_start(pud, pdn)
#print("S", a)
path1, edge1, path2, edge2 = euler_path(pud, pdn)
print('canh pud', path1)
print('dinh pud', edge1)
print('canh pdn', path2)
print('dinh pdn', edge2)
#start_ele_test = ('P3')
#next_vertices = [('A', 'Out'), ('D', 'Vss'), ('E', 'Vss')]
#next_test = next_vertex(pdn, start_ele_test)
#print("canh noi voi P3", next_test)
#path, edges = any_path(pdn, start_ele_test)
#print("path", path) #danh sách các đỉnh trên đường đi
#print("edge", edges) #danh sách các cạnh trên đường đi

#result = remove_edge_2('A', ('P3', 'Vss'), pdn)
#for transistor in result:
    #print(f"Transistor ID: {transistor.id}, Points: {transistor.points[0]}")
    
#result2 = reverse_pair(('P3', 'Vss'))
#print(result2)

