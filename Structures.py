class Airport:
    # primary key
    name = ''
    # staffs that base on it
    staffs = []
    nodes = []
    # flights 储存元组(flight, bool) bool为True代表航班为离开航班
    flights = []


class Flight:
    # 基本属性
    # primary key
    no = 0
    captain = 1
    first_officer = 1
    flight_number = ''
    # time (自宇宙大爆炸开始的分钟数)
    dptr_time: int = 0
    arrv_time: int = 0
    # 抵达与离开的机场编号
    arrv_port: Airport = 0
    dptr_port: Airport = 0
    # 所对应的 edge
    edge = None

    # 正确性检验函数
    def is_valid(self) -> bool:
        return self.dptr_port is not None and self.arrv_port is not None\
            and self.dptr_time > 0 and self.arrv_time > 0 and self.edge is not None


class Node:
    # primary key
    no = 0
    inEdges = []
    outEdges = []

    airport: Airport = None


# edge
class Edge:
    # primary key
    no = 0
    # the flight info
    flight = None
    # start and end nodes
    start_node: Node = None
    end_node: Node = None

    # methods
    def is_flight(self):
        return self.flight is None

    def get_flight(self):
        return self.flight

    def is_valid(self):
        return not (self.start_node is None and self.end_node is None)


# staff
class Staff:
    # primary key
    no = 0
    # attr
    has_captain: bool = False
    has_officer: bool = False
    base_port: Airport = None
    duty_cost: int = 0
    pare_cost: int = 0

    # methods
    def can_mix(self):
        return self.has_captain and self.has_officer


