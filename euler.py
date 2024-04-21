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
                        #print("points", point)                                     
                    if p == Vdd:
                        links.append((pud_transistor.id, 'S'))
                            #print("links_pud:", pud_transistor.id)
                    elif p == Out:
                        links.append((pud_transistor.id, 'D'))
                        
        points_pud.append((point, links))
        #print("points_pud: \n" , points_pud )
    for point in pdn_names:
        links = []
        for pdn_transistor in pdn:
            #Duyệt qua các Points trong đỉnh
            for p in pdn_transistor.points:
                if p == point: 
                    #print("points", point)                                     
                        #Nếu points là vdd thì thêm transistor đó vào LINKS (transistor.ID, "S"). Đây cũng là một tuple
                    if p == Vss:
                        links.append((pdn_transistor.id, 'S'))
                            #print("links_pud:", pud_transistor.id)
                        #Nếu points là Out thì thêm transistor đó vào LINKS (transistor.ID, "D"). Đây cũng là một tuple
                    elif p == Out:
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
                #print("e", e[1], x)
            if e[0] == x:
                next_vertices.append((id, e[1]))
                #print("e", next_vertices)
            elif e[1] == x:
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
        #print("end", vertex)
        deg = sum(1 for transistor in pud for point in transistor.points if point == vertex)
        #print("end", vertex, deg)
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
    nodes_pud, nodes_pdn = nodes(pud, pdn)
    #print("end", nodes_pud)
    edge1 = []
    if pud_flag:       
        #print("pdn", nodes_pdn[0])
        path1, edge1 = any_path(pud, start_ele)
        print("edges", edge1)
        path2, edge2 = any_path(pdn, nodes_pdn[0])
    else:
        path1, edge1 = any_path(pud, nodes_pud[0])
        #print("start_ele", start_ele)
        path2, edge2 = any_path(pdn, start_ele)
        #print(path2)
        
    #print(path1)
    return path1, edge1, path2, edge2

def any_path(g, vertex): #any_path(pud, start_ele)
    #tìm đường đi tiếp theo cho start_ele
    #print('vertex', vertex)
    next_vertices = []
    next_vertices = next_vertex(g, vertex) #next_vertex trả về cạnh nối với start_ele
    
    if not next_vertices:
        return [], []
    next_ele = 0
    #print('vertex', next_vertices)
    #Nếu chỉ có 1 cạnh để đi tiếp => chọn cạnh đó
    unique_pairs = set(next_vertices)
    num_unique_pairs = len(unique_pairs)

    #print("Số lượng cặp cạnh không trùng nhau:", num_unique_pairs)
    
    if num_unique_pairs <= 1:
        #print("chi co 1 canh")
        next_ele = 0
    else:
        #print("nhieu hon 1 canh")
        #i là chỉ số, a là phẩn tử tương ứng với chỉ số
        for i, a in enumerate(next_vertices):
            #print('a0', a[0])
            #print([vertex] + [a[1]])
            #print('vertex',vertex)
            #result = remove_edge(a[0], ([vertex] + [a[1]]), g)
            #for transistor in result:
                #print(f"Transistor ID: {transistor.id}, Points: {transistor.points}")
            #reach: khoảng cách từ điểm bắt đầu đến các đỉnh khác trong đồ thị - số lượng đỉnh từ điểm bắt đầu
            #reach(remove_edge): Sau khi loại bỏ cạnh
            #print("reach", reach(remove_edge(a[0], [vertex] + [a[1]], g), vertex))
            #print((reach(g, vertex)))
            
            #Chọn đỉnh có số lượng đỉnh ít nhất
            if all(reach(g, vertex) <= reach(remove_edge(a[0], [vertex] + [a[1]], g), vertex) for _ in range(i + 1)):
                next_ele = i
                #print(i)
                break
    stack = next_vertices[next_ele]
    #print('stack', stack)
    id_ = stack[0]
    #print('id_', id_)
    p2 = stack[1]
    #print('points', p2)
    #result = remove_edge(id_, [vertex] + [p2], g)
    #for transistor in result:
        #print(f"Transistor ID: {transistor.id}, Points: {transistor.points[0]}")
    #euler1: đường đi từ điểm bắt đầu đến đỉnh tiếp theo
    #euler2: id của đỉnh tiếp theo
    euler1, euler2 = any_path(remove_edge(id_, [vertex] + [p2], g), p2)
    #print('euler1', euler1)
    #print('euler2', euler2)
    #print([(id_, [vertex] + [p2])] + euler1) #Danh sách các cạnh đã đi qua
    #print([id_] + euler2) #chứa ID các cạnh đã đi qua
    return [(id_, [vertex] + [p2])] + euler1, [id_] + euler2
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
    polarity_list = []
    for transistor in euler1:
        id, pola = transistor
        pola = sorted(pola)   # su dung ham nay de tu dong sap xep cac phan tu trong mang ma khong can quan tam vi tri
        # Tim id cua transistor co trong do thi
        transistor =  filter_transistor(id, g)
        pola_g = sorted(transistor.points) 

        if pola == pola_g:
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
    
    lines = []
    for i, a in enumerate(points_pud):
        id = a[0]
        
        if "Vdd" in id or "Out" in id:
            color = "blue"
        else:
            color = "yellow"
        lines.append([id, line(x0, i * y2, x1, i * y2, color)])
        #print(a[0], color)
    for i, a in enumerate(points_pdn):
        id = a[0]
        if "Vss" in id or "Out" in id:
            color = "blue"
        else:
            color = "green"
        lines.append([id, line(x0, size_janela.col - i * y3, x1, size_janela.col - i * y3, color)])
    return lines

def find_polarity (id , polarity):
    for i in polarity:
        id_temp , polarity_temp = i
        if id == id_temp :
            return  polarity_temp
    return []

def line_ver(pud, pdn): #tạo các đường thẳng dọc
    path1, edge1, path2, edge2 = euler_path(pud, pdn)
    #print(edge1, path1)
    
    #Phân cực S và D
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
    #print(y1)
    lines_pud = []
    lines_pdn = []

    for i, id in enumerate(edge1):
        #print(id)
        if assc(id, equal): # dieu kien kiem tra xem co transistor nao giong nhau o pud va pdn khong                      
            lines_pud.append([id, find_polarity(id,polarity_pud), line(i * x, y0, i * x, y1, "red")])
            #print(lines_pud[2].y0)
    for i, id in enumerate(edge1):
        #print(id)
        if assc(id, equal):
            lines_pdn.append([id, find_polarity(id,polarity_pud), line(i * x, y2, i * x, y3, "red")])

    return lines_pud, lines_pdn

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
    line_pud= line_hor(pud, pdn) #lines
    #print(line_pud)
    points_pud, points_pdn = points(pud, pdn) #transistor 
    #for i in points_pud:
        #print(i[1])
    euler1, euler2, euler3, euler4 = euler_path(pud, pdn) #euler
    #print(euler2)
    line_id_pud, line_id_pdn = line_ver(pud, pdn) #line
    #line_out = line_vout() #lines
    line_out_ver2 = line_vout_ver2() #lines
    qnt_con = len(euler2)
    #print(qnt_con)
    eq = equal_pos(euler2, euler4) #euler
    #print('eq',eq)
    x = 0.8 * (size_janela.lin) / (2 * qnt_con)
    vout_p_value = next((item[1] for item in line_pud if item[0] == 'Out'), None)
    #print(vout_p_value)
    #for item in line_pud:
        #print(item[1])
        #if item[0] == 'Out':
            #print(item[0])
    
    # # vout_n_value = next((item[1] for item in line_pdn if item[0] == 'Vout'), None)
    # # y_n_type = line.y0(vout_n_value)
    #y_p_type = line.y0([item[1] for item in line_pud if item[0] == Vout][0]) 
    y_p_type = vout_p_value.y0
    #print(y_p_type)
    # #y_n_type = line.y0([item[1] for item in line_pdn if item[0] == Vout][0]) #lines/transistor

    draw_id(line_id_pud, eq, True)
    draw_id(line_id_pdn, eq, False)

    draw_other_id(line_pud, euler2, points_pud, line_id_pud, x, y_p_type)
    # # draw_other_id(line_pdn, euler4, points_pdn, line_id_pdn, x, y_n_type, False)
    
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
            #print('line', x0, x1,y0,y1)
            plt.plot([x0, x1], [y0, y1], color='red', linewidth=3)
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
        #print(id)
        #x0, y0, x1, y1, color = line
        if id in [Vdd, Vss, Out]:
            plt.plot([x0, x1], [y0, y1], color=color, linewidth=3, linestyle='-')
        #chứa các điểm trong pud có link_point = id
        #nos(id, points)
        nos = [i for i in points_pud if i[0] == id and i[1]]
        #print(nos)
        len_nos = 0
        for i in nos:     
            len_nos = (len(i[1]))
            #print(i[1])
        #print(len_nos)
        #Nếu 2 nút nối cùng với 1 ID   
        if len_nos == 2:
            node1 = nos[0][1][0][0]
            node1_p = nos[0][1][0][1] #vị trí của node1
            node2 = nos[0][1][1][0]
            node2_p = nos[0][1][1][1]
            #print(node1, node1_p, node2, node2_p)
            #index_node1 = []
            if (node1 == euler2[0]):
                index_node1 = euler2.index(node1)
                #print(index_node1)
            if (node2 == euler2[0]):
                index_node2 = euler2.index(node2)
                #print(index_node2)
            #index_node2 = euler2.index(node2)
            line1 = next((line for line in line_id if line[0] == node1), None)
            #line1 = line_id[0][node1] #line_id = line_id_pud
            #for line in line_id:
                #print(line[0])
            #print(line1[0][2])
            line2 = next((line for line in line_id if line[0] == node2), None)
            if(line1):
                x1 = line1[2].x0
                y01 = line1[2].y0
                y11 = line1[2].y1
            if(line2):
                x2 = line2[2].x0
                y02 = line2[2].y0
                y12 = line2[2].y1
            #if (not seguido(index_node1, index_node2) or (seguido(index_node1, index_node2) and not ligado(line1, node1_p, line2, node2_p, index_node1, index_node2)) or id == Vdd or id == Vss):
                #plt.plot([x1, x1, x2, x2], [y_p_type, line.y0(line_pud[id][1]), line.y0(line_pud[id][1]), y_p_type], color=color, linewidth=2, linestyle='-')
                #plt.plot(x1, y_p_type, 'o', color='black', markersize=6)
                #plt.plot(x2, y_p_type, 'o', color='black', markersize=6)
    
        #if id == Vout:
            #nos = [i for i in points_pud if i.link_point == id and i.link_position]
            #for j in nos:
                #node, node_p = j
                #line = line_id[node]
                #x1, y01, _, y11, _ = line
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

