from typing import List

from Structures import *
from Topo import *
from datetime import datetime, timedelta
import pandas as pd


class Loader:
    # the Loader class is responsible for managing 5 entities
    flights = []
    airports = {}
    staffs = []
    pd_crew: pd.DataFrame
    pd_flight: pd.DataFrame

    # get methods
    def get_staff_by_id(self, staff_no) -> Staff:
        return self.staffs[staff_no] if staff_no < len(self.staffs) else None

    def get_airport_by_name(self, airport_name) -> Airport:
        return self.airports[airport_name] if self.airports.__contains__(airport_name) else None

    def get_flight_by_id(self, flight_no) -> Flight:
        return self.flights[flight_no] if flight_no < len(self.flights) else None

    # add methods, where an entity cast in with its `no` filled in methods
    def add_staff(self, staff: Staff):
        staff.no = len(self.staffs)
        self.staffs.append(staff)

    def add_airport(self, airport: Airport):
        if not self.airports.__contains__(airport.name):
            self.airports[airport.name] = airport

    def add_flight(self, flight: Flight):
        flight.no = len(self.flights)
        self.flights.append(flight)

    # help load from file
    def __init__(self, crew_file: str, flight_file: str):
        self.pd_crew = pd.read_csv(crew_file)
        self.pd_flight = pd.read_csv(flight_file)

    # load data from files
    # airports should be loaded from flight.csv, and they should be firstly read
    def load_airports(self):
        airport_names = set()
        airport_names.update(list(self.pd_flight.groupby(by=["DptrStn"]).groups.keys()))
        airport_names.update(list(self.pd_flight.groupby(by=["ArrvStn"]).groups.keys()))
        for airport_name in airport_names:
            airport = Airport()
            airport.name = airport_name
            self.add_airport(airport)

    # staff should be loaded from crew.csv; the airports must be loaded before it
    def load_staff(self):
        for index, row in self.pd_crew.iterrows():
            # 生成staff
            staff = Staff()
            staff.no = row["EmpNo"]
            staff.has_captain = row["Caption"] == "Y"
            staff.has_officer = row["FirstOfficer"] == "Y"
            # 指定基地
            base_port = self.get_airport_by_name(row["Base"])
            staff.base_port = base_port
            staff.duty_cost = row["DutyCostPerHour"]
            staff.pare_cost = row["ParingCostPerHour"]
            # 基地加入该员工
            base_port.staffs.append(staff)
            # 类全局加入该员工
            self.add_staff(staff)

    # flights load from file
    def load_flights(self):
        # todo 获取所有航班中最早起飞的时间点作为宇宙大爆炸开始的时间
        base_time: datetime
        for index, row in self.pd_flight.iterrows():
            dptr_date = row['DptrDate'].split("/")[2] + '-' + row['DptrDate'].split("/")[0] + '-' + \
                   row['DptrDate'].split("/")[1] + '-' + row['DptrTime']
            arrv_date = row['ArrvDate'].split("/")[2] + '-' + row['ArrvDate'].split("/")[0] + '-' + \
                   row['ArrvDate'].split("/")[1] + '-' + row['ArrvTime']

            # 生成新航班
            flight = Flight()
            dptr_time = datetime.strptime(dptr_date, '%Y-%m-%d-%H:%M')
            arrv_time = datetime.strptime(arrv_date, '%Y-%m-%d-%H:%M')
            arrv_time.fromtimestamp()
            # 赋值起飞时间(单位为分钟)
            flight.arrv_time = (arrv_time - base_time).total_seconds()//60
            flight.dptr_time = (dptr_time - base_time).total_seconds()//60
            # 赋值抵达与起飞机场
            dptr_port = self.get_airport_by_name(row["DptrStn"])
            flight.dptr_port = dptr_port
            arrv_port = self.get_airport_by_name(row["ArrvStn"])
            flight.arrv_port = arrv_port
            # 抵达与起飞机场分别容纳这些航班
            dptr_port.flights.append((flight, False))
            arrv_port.flights.append((flight, True))
            # 赋值属性
            # todo 属性赋值

