import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
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
    Transistor('C', ('Out', 'P1')),
    Transistor('D', ('P2', 'P1')),
    Transistor('E', ('Out', 'P2')),
]

pdn = [
    Transistor('A', ('Out', 'P3')),
    Transistor('B', ('P3', 'Vss')),
    Transistor('C', ('Out', 'P4')),
    Transistor('D', ('P4', 'Vss')),
    Transistor('E', ('P4', 'Vss')),
]
def points(pud, pdn): #xác định các vị trí VDD, GND, VOUT
    ids = [transistor.id for transistor in pud]
    #lấy danh sách các POINTS của đỉnh
    pud_names = []
    for transistor in pud:
        for point in transistor.points:
            if point not in pud_names:
                pud_names.append(point)
                
    pdn_names = []
    for transistor in pdn:
        for point in transistor.points:
            if point not in pdn_names:
                pdn_names.append(point)
    #print(pud_names)
    points_pud = []
    points_pdn = []
    for point in pud_names:
        links = []
        for pud_transistor in pud:
            if point in pud_transistor.points:
                if point == pud_transistor.points[0]:
                    links.append((pud_transistor.id, 'S'))
                else:
                    links.append((pud_transistor.id, 'D'))
        links.reverse()
        points_pud.append((point, links))
        #points_pud.reverse()
        #print("points_pud: \n" , points_pud )
    for point in pdn_names:
        links = []
        for pdn_transistor in pdn:
            if point in pdn_transistor.points:
                #print(point, pdn_transistor.points[0])
                if point == pdn_transistor.points[0]:
                    links.append((pdn_transistor.id, 'S'))
                else:
                    links.append((pdn_transistor.id, 'D'))
        links.reverse()
        points_pdn.append((point, links))
        #print("points_pdn: \n" , points_pdn )

    #Tìm phần tử đầu tiên là Vdd
    vdd_ele = next((a for a in points_pud if a[0] == Vdd), None)
    vdd_index = points_pud.index(vdd_ele) if vdd_ele else None
    #print("vdd_ele:", vdd_ele, vdd_index)

    #Tìm phần tử đầu tiên là Vss
    vss_ele = next((a for a in points_pdn if a[0] == Vss), None)
    vss_index = points_pdn.index(vss_ele) if vss_ele else None
    #print("vss_ele:", vss_ele, vss_index)
    #for a in points_pdn:
        #print("vss_index:", a[0])
    #Đảo các đỉnh có nối với Vdd/Vss lên đầu/cuối
    pud_2 = list_swap(points_pud, vdd_index, 0) if vdd_index is not None else points_pud
    pdn_2 = list_swap(points_pdn, vss_index, 0) if vss_index is not None else points_pdn
    #print("pud_2", pud_2)
    vout1_ele = next((a for a in pud_2 if a[0] == Out), None)
    vout1_index = pud_2.index(vout1_ele) if vout1_ele else None
    #print("vout1_ele", vout1_ele, vout1_index)
    vout2_ele = next((a for a in pdn_2 if a[0] == Out), None)
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
    nodes_pud = list(dict.fromkeys(nodes_pud))
    nodes_pdn = []
    for transistor in pdn:
        for points in transistor.points:
            nodes_pdn.append(points)
    nodes_pdn = list(dict.fromkeys(nodes_pdn))
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
            #print("e", e, x)
            if e[0] == x:
                acc.append((id, e[1]))
                #print(acc)
            elif e[1] == x:
                acc.append((id, e[0]))
    #print(x, acc)
    acc.reverse()
    return acc
def reach(graph, x):
    #số lượng các đỉnh có thể đạt được tử đỉnh x
    visited = [x]
    next_v = []
    def loop(g, next_point):
        nonlocal visited
        #next_vertices = [] #trả về các cạnh nối với điểm next_point
        next_vertices = next_vertex(g, next_point)
        #print(next_vertices)
        if next_vertices:
            #duyệt qua các phần tử trong next_vertices
            for next_step in next_vertices:
                next_edge, next_v = next_step
                #print("next_edge", next_edge)
                #print("next_vertex", next_v)
                if next_v not in visited:
                    #print("not visited", next_vertex)
                    visited.append(next_v)
                    loop(remove_edge(next_edge, (next_point, next_v), g), next_v)
    
    loop(graph, x)
    return len(visited)
def path_start(pud, pdn):
    # Vertices to begin
    #pud_point = [a for a in pud]
    #Chứa các điểm kết nối trong pud
    vertices_pud = []
    nodes_pud = []
    for transistor in pud:
        for points in transistor.points:
            nodes_pud.append(points)

    vertices_pud = list(dict.fromkeys(nodes_pud))
    #print("start", vertices_pud)
    vertices_pdn = []
    nodes_pdn = []
    for transistor in pdn:
        for points in transistor.points:
            nodes_pdn.append(points)
    vertices_pdn = list(dict.fromkeys(nodes_pdn))
    #print("start", vertices_pdn)
    #pdn_point = [a for a in pdn]

    start_ele_pud = None
    start_ele_pdn = None
    
    for vertex in vertices_pud:
        #print("end", vertex)
        deg = sum(1 for transistor in pud for point in transistor.points if point == vertex)
        #Tìm điểm kết nối có bậc lẻ ở pud
        if deg % 2 != 0:
            start_ele_pud = vertex
            #print("oke", start_ele_pud)         
            break
    for vertex in vertices_pdn:
        #print("start", vertex)
        deg = sum(1 for transistor in pdn for point in transistor.points if point == vertex)
        #Tìm điểm kết nối có bậc lẻ ở pud
        if deg % 2 != 0:
            start_ele_pdn = vertex
            break
    if start_ele_pud:
        #print("oke", start_ele_pud) 
        return (start_ele_pud, True)
    elif start_ele_pdn:
        return (start_ele_pdn, False)
    else:
        return (Vdd, True)

def euler_path(pud, pdn):
    #Đỉnh bậc lẻ và cờ (xem nó thuộc pud hay pdn)
    start_ele, pud_flag = path_start(pud, pdn)
    
    nodes_pud, nodes_pdn = nodes(pud, pdn)

    if pud_flag == True:       
        
        path1, edge1 = any_path(pud, start_ele)
        path2, edge2 = any_path(pdn, nodes_pdn[0])
    else:
        path1, edge1 = any_path(pud, nodes_pud[0])
        #print("start_ele", start_ele)
        path2, edge2 = any_path(pdn, start_ele)
        #print("pdn", nodes_pud[0])
        #print(path2)
    #print("edges", edge1)
    #print(path1)
    return path1, edge1, path2, edge2

def any_path(g, vertex): #any_path(pud, start_ele)
    next_vertices = []
    #print(vertex)
    next_vertices = next_vertex(g, vertex) #next_vertex trả về cạnh nối với start_ele
    #print(next_vertices)
    if not next_vertices:
        return [], []
    next_ele = 0
    
    for next_step in next_vertices:
        if len(set([v for (neighbors,_) in next_vertices for v in neighbors])) <= 1:
            next_ele = 0
        else:
        #print("nhieu hon 1 canh")
        #i là chỉ số, a là phẩn tử tương ứng với chỉ số
            for i, a in enumerate(next_vertices):
                    #print((vertex,a))
                    #print(vertex, reach(g, vertex))
                    if reach(g, vertex) <= reach(remove_edge(a[0], (vertex,a[1]), g), vertex):
                        next_ele = i
                        break
        
    stack = next_vertices[next_ele]
    #print('stack', stack, next_ele)
    id_ = stack[0]
    #print('id_', id_)
    p2 = stack[1]
    #print('points', p2)
    #result = remove_edge(id_, [vertex] + [p2], g)
    #for transistor in result:
        #print(f"Transistor ID: {transistor.id}, Points: {transistor.points[0]}")
    #euler1: đường đi từ điểm bắt đầu đến đỉnh tiếp theo
    #euler2: id của đỉnh tiếp theo2
    euler1, euler2 = any_path(remove_edge(id_, [vertex] + [p2], g), p2)
    #print('euler2', euler2)
    #print('euler1', euler1)
    #print([(id_, [vertex] + [p2])] + euler1) #Danh sách các cạnh đã đi qua
    #print([id_] + euler2) #chứa ID các cạnh đã đi qua
    return [(id_, [vertex] + [p2])] + euler1, [id_] + euler2
def remove_edge(id, points, g): #(tên đỉnh, điểm kết nối, pud/pdn) (A, 'P1, P2', pud)
    g_new = remove_edge_2(id, points, g)  # Gọi hàm remove_edge_2 để loại bỏ cạnh từ đồ thị g  
    #print("g_new", g_new) 
    return remove_edge_2(id, reverse_pair(points), g_new)  # Áp dụng hàm remove_edge_2 lần nữa sau khi đảo ngược cặp points
def remove_edge_2(id_, points, g):
    #print(points)
    result = []
    result_done = []
    #print('a')
    for a in g:
        #print(a.points)
        if (a.id != id_):
            result.append(a)
        #elif a.points != points:
            #result.append(a)
    for b in result:
        #print(b.points)
        if (b.points != points):
            result_done.append(b)
    return result_done
def reverse_pair(points):
    if isinstance(points, tuple):  # Kiểm tra xem points có phải là một cặp không
        return (points[1], points[0]) 
class SizeWindow:
    def __init__(self, col, lin):
        self.col = col
        self.lin = lin

class line:
    def __init__(self, x0, y0, x1, y1, color):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.color = color

size_janela = SizeWindow(600, 800) 

def polarity(pud, pdn):
    path1, edge1, path2, edge2 = euler_path(pud, pdn)

    polarity_pud = polarity_euler(path1, pud) # path 1 
    polarity_pdn = polarity_euler(path2, pdn) # path 2

    return polarity_pud, polarity_pdn

# hàm xác định thứ tự các cực (S và D) của một transitor 
def polarity_euler(euler1, g):
    #print('euler', euler1)
    polarity_list = []
    for transis in euler1:
        id, pola = transis
        trans =  filter_transistor(id, g)
        pola_g = trans.points
        if pola[0] == pola_g[0] and pola[1] == pola_g[1]:
            polarity_list.append([id, ordem])
        else:
            polarity_list.append([id, [ordem[1], ordem[0]]])
    return polarity_list

def line_hor(pud, pdn):
    points_pud, points_pdn = points(pud, pdn)
    line_pud = len(points_pud)
    line_pdn = len(points_pdn)
    y2 = 0.3 * size_janela.col / line_pud
    y3 = 0.3 * size_janela.col / line_pdn
    x0 = 0
    x1 = size_janela.lin
    
    line_hor_pud = []
    line_hor_pdn = []
    for a, i in zip(points_pud, range(1, len(points_pud) + 1)):
        id = a[0]
        color = "black"
        if id == "Vdd" or id == "Vss":
            color = "blue"
        elif id == "Out":
            color = "brown"
        else:
            color = "blue"
        line_hor_pud.append([id, line(x0, i * y2, x1, i * y2, color)])
        #print(a[0], color)
    for a, i in zip(points_pdn, range(1, len(points_pdn) + 1)):
        id = a[0]
        if id == "Vdd" or id == "Vss":
            color = "blue"
        elif id == "Out":
            color = "green"
        else:
            color = "blue"        
        line_hor_pdn.append([id, line(x0, size_janela.col - i * y3, x1, size_janela.col - i * y3, color)])
    return line_hor_pud, line_hor_pdn

def find_polarity (id , polarity):
    for i in polarity:
        id_temp , polarity_temp = i
        if id == id_temp :
            return  polarity_temp
    return []

def line_ver(pud, pdn): #tạo các đường thẳng dọc
    path1, edge1, path2, edge2 = euler_path(pud, pdn)
    #print(path1)
    #print(path2)
    polarity_pud, polarity_pdn = polarity(pud, pdn)    
    qnt_con = len(edge1)
    #print(qnt_con)
    #Tìm các cạnh giống nhau, thường rỗng
    equal = equal_pos(edge1, edge2)
    x = 0.8 * size_janela.lin / qnt_con #640
    y0 = 0.15 * size_janela.col         #90
    y1 = 0.4 * size_janela.col          #240
    y2 = 0.6 * size_janela.col          #360
    y3 = 0.85 * size_janela.col         #510
    return (lines_ver(polarity_pud, edge1, equal, x, y0, y1, y0),
            lines_ver(polarity_pdn, edge2, equal, x, y2, y3, y1))

def lines_ver(polarity, euler, eq, x, y0, y1, yc):
    result = []
    for id, i in zip(euler, range(1, len(euler) + 1)):
        if id in eq:
            result.append([id, next((pair[1] for pair in polarity if pair[0] == id), None), line(i * x, yc, i * x, y1, "red")])
        else:
            result.append([id, next((pair[1] for pair in polarity if pair[0] == id), None), line(i * x, y0, i * x, y1, "red")])
    return result

def equal_pos(edge1, edge2): #tìm đỉnh chung của euler path pud và pdn
    result = []
    #i và j là chỉ số của id
    for i, id1 in enumerate(edge1):
        #print(i)
        for j, id2 in enumerate(edge2):
            if id1 == id2:
                result.append([id1, j])
                break
    return result

def assc(A, lista):
    for sublist in lista:
        if A in sublist:
            return True
    return False

def line_vout():
    #trả về đường thẳng có tên "Vout", tọa độ x0, y0, x1, y1 và color
    return [["Vout", line(0, 0.5 * size_janela.col, size_janela.lin, 0.5 * size_janela.col, "blue")]] 
def line_vout_ver2():
    return [line(0, 0.5 * size_janela.col, size_janela.lin, 0.5 * size_janela.col, "blue")]
fig, ax = plt.subplots()

def draw_stick_basic(pud, pdn):
    #hor: ngang, ver: dọc
    line_hor_pud, line_hor_pdn= line_hor(pud, pdn) #lines
    #x0,y0,x1,y1
    #print(line_hor_pdn[2][1].x0, line_hor_pdn[2][1].y0, line_hor_pdn[2][1].x1, line_hor_pdn[2][1].y1, line_hor_pdn[2][1].color )
    points_pud, points_pdn = points(pud, pdn) #transistor 
    euler1, euler2, euler3, euler4 = euler_path(pud, pdn) #euler
    line_id_pud, line_id_pdn = line_ver(pud, pdn) #line
    #print(line_id_pdn)
    #print(line_id_pud)
    line_out_ver2 = line_vout_ver2() #lines
    
    qnt_con = len(euler2)
    
    eq = equal_pos(euler2, euler4) #euler
    #print('eq',eq)
    x = 0.8 * (size_janela.lin) / (2 * qnt_con)
    vout_p_value = next((item[1] for item in line_hor_pud if item[0] == 'Out'), None)
    y_p_type = vout_p_value.y0
    #print(y_p_type)
    vout_n_value = next((item[1] for item in line_hor_pdn if item[0] == 'Out'), None)
    y_n_type = vout_n_value.y0
    #print(y_n_type)
    draw_id(line_id_pud, eq, True)
    draw_id(line_id_pdn, eq, False)

    draw_other_id(line_hor_pud, euler2, points_pud, line_id_pud, x, y_p_type)
    draw_other_id(line_hor_pdn, euler4, points_pdn, line_id_pdn, x, y_n_type, False)
    
    for i in line_out_ver2:
        if isinstance(i, line): #lines
            x0 = i.x0
            y0 = i.y0
            x1 = i.x1
            y1 = i.y1
            color = i.color
            plt.plot([x0, x1], [y0, y1], color=color, linewidth=2)
            plt.text(0.95 * x1, y1, 'Vout', color='black')
    
def draw_id(line_id, eq, top):
    #line_id: danh sách các đoạn cần vẽ
    for i in line_id:
        #print(i)
        if isinstance (i, list):
            #print("ab" , i[2].x0)
            id = i[0]
            x0 = i[2].x0
            y0 = i[2].y0
            x1 = i[2].x1
            y1 = i[2].y1
            color = i[2].color
            #print('line', x0, y0, x1,y1)
            plt.plot([x1, x1], [y0, y1], color='red', linewidth=3)
            if top or id not in eq:
                plt.text(x0, y0 if top else y1, str(id), color=color)

def draw_other_id(line_pud, euler2, points_pud, line_id, x, y_p_type, pud=True):
    for a, b in zip(line_pud, range(len(line_pud))):
        #line_pud: id, line
        id = a[0]
        x0 = a[1].x0
        x1 = a[1].x1
        y0 = a[1].y0
        y1 = a[1].y1
        color = a[1].color

        if id == "Vdd" or id == "Vss" or id == "Out":
            plt.plot([x0, x1], [y0, y1], color=color, linewidth=3, linestyle='-')
            #print([y0, y1])
        #else:
        nos = []
        node1 = []
        node1_p = []
        node2 = []
        node2_p = []
            #nos = [i[1] for i in points_pud if i[0] == id and i[1]]
        len_nos = 0
        nos = [i[1] for i in points_pud if i[0] == id]
        for node in nos:           
            temp1 = node[:-1]
            temp3 = node[1:]
            for temp2 in temp1:
                node1 = temp2[0]
                node1_p = temp2[1]
                index_node1 = euler2.index(node1) if node1 in euler2 else -1
                line1 = next((line for line in line_id if line[0] == node1), None)
                x1 = line1[2].x0
                y01 = line1[2].y0
                y11 = line1[2].y1
            for temp2 in temp3:
                node2 = temp2[0]
                node2_p = temp2[1]
                index_node2 = euler2.index(node2) if node2 in euler2 else -1
                line2 = next((line for line in line_id if line[0] == node2), None)
                x2 = line2[2].x0
                y02 = line2[2].y0
                y12 = line2[2].y1
                print(x2)
            if (not seguido(index_node1, index_node2) or (seguido(index_node1, index_node2) and not ligado(line1, node1_p, line2, node2_p, index_node1, index_node2)) or id == Vdd or id == Vss):
                plt.plot([x1, x1, x2, x2], [y_p_type, (line_pud[1][1].y0),  (line_pud[1][1].y0), y_p_type], color=color, linewidth=2, linestyle='-')
                plt.plot(x1, y_p_type, 'o', color='black', markersize=6)
                plt.plot(x2, y_p_type, 'o', color='black', markersize=6)
    
        #if id == Out:
            #for i in points_pud:
                #print(i[1])
            #nos = [i[1] for i in points_pud if i[0] == id ]
            #for j in nos:
                #for item in line_id:
                    #if item[0] == j:
                        #pol = item[2]
                        #x1 = item[3]
                        #y1 = item[5]
                #plt.plot([x1, x1], [y_p_type, 0.5 * SizeWindow(size_janela)], color='blue', linewidth=2, linestyle='-')
                #plt.plot(x1, y_p_type, 'o', color='black', markersize=6)
def seguido(index_node1, index_node2):
    #kiểm tra 2 đỉnh kể nhau (chỉ số cách nhau 1)
    return (index_node1 + 1 == index_node2) or (index_node1 - 1 == index_node2)
def ligado(pol, node1_p, pol2, node2_p, index_node1, index_node2):
    if index_node1 < index_node2:
        return (index_of(pol, node1_p) == 1) and (index_of(pol2, node2_p) == 0)
    else:
        return (index_of(pol, node1_p) == 0) and (index_of(pol2, node2_p) == 1)
def index_of(l, x):
    if isinstance(l, list):
        for i, y in enumerate(l):
            if x == y:
                return i
        return None
    elif isinstance(l, tuple) or isinstance(l, str):
        return 0 if l == x else 1
    else:
        return None
    return draw_stick_basic


#plt.savefig('stick_diagram.png')
# Testing the function
pud = [
    Transistor('A', ('P1', 'Vdd')),
    Transistor('B', ('P1', 'Vdd')),
    Transistor('C', ('Out', 'P1')),
    Transistor('D', ('P2', 'P1')),
    Transistor('E', ('Out', 'P2')),
]

pdn = [
    Transistor('A', ('Out', 'P3')),
    Transistor('B', ('P3', 'Vss')),
    Transistor('C', ('Out', 'P4')),
    Transistor('D', ('P4', 'Vss')),
    Transistor('E', ('P4', 'Vss')),
]

pud_result, pdn_result = points(pud, pdn)
#nodes_pud, nodes_pdn = nodes(pud, pdn)
#a, b = path_start(pud, pdn)
#print("S", a)
path1, edge1, path2, edge2 = euler_path(pud, pdn)
#print('canh pud', path1)
#print('dinh pud', edge1)
#print('canh pdn', path2)
#print('dinh pdn', edge2)
#line_pud, line_pdn = line_ver(pud, pdn)
#print(line_pud)
#print(line_pdn)
#plt.show(draw_stick_basic(pud,pdn))

draw_stick_basic(pud, pdn)
#plt.show()
#result = equal_pos(edge1, edge2)
#print(result)
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

