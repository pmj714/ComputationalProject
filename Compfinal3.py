import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation



class Car:
    def __init__(self, speed, id1, position, fol_dist, accel, stop):
        self.id = id1
        self.max_speed = speed
        self.position = position
        self.prior_position = 0
        self.cur_speed = 0
        self.fol_dist = fol_dist
        self.accel = accel
        self.stop = stop
        self.steps = 0
        self.cum_speed = 0
        self.avg_speed = 0
        self.perc_speed = 0
        self.in_decel = 0
        self.done_stop = 0
    def do_move(self, for_pos, p_speed):
        max_dist = for_pos - self.position
        if max_dist < 0:
            max_dist = max_dist + 1000
        if(self.position < self.stop):
            self.done_stop = 0
        new_speed = self.calc_speed(max_dist, p_speed)

        if(self.cur_speed > new_speed):
            if(self.in_decel == 0):
                diff = self.cur_speed - new_speed
                diff =  1 * diff
                new_speed = self.cur_speed - diff
            self.in_decel = 1
        else:
            self.in_decel = 0


        dist = (new_speed + self.cur_speed) / 2
        self.cur_speed = new_speed
        self.prior_position = self.position
        self.position += dist
        self.cum_speed += self.cur_speed
        if(self.position != 0):
            self.steps += 1
        if(self.position > for_pos and self.position > 0 and for_pos != -1):
            print("EXITING", self.id, self.position, self.cur_speed, for_pos, p_speed)
            #exit(10)
        return(self.prior_position, self.position, new_speed)
    def calc_speed(self, max_dist, p_speed):
        print(max_dist)
        if((self.stop != 0) and (self.position > self.stop) and (not self.done_stop)):
            self.in_decel = 1
            self.done_stop = 1
            return 0
        if(max_dist < self.fol_dist):
            if(self.cur_speed == 0):
                return 0
            else:
                if(p_speed * .9 > self.cur_speed + self.accel):
                    return(self.cur_speed + self.accel)
                else:
                    return(p_speed * .9)
        elif(max_dist >= 1.5 * self.max_speed):
            if(self.cur_speed >= self.max_speed - self.accel):
                return(self.max_speed)
            else:
                return(self.cur_speed + self.accel)
        elif(max_dist >= 1.5 * self.cur_speed):
            return(self.cur_speed)
        else:
            return(self.cur_speed + (p_speed - self.cur_speed) / (max_dist))



def update_road(road, first, second, id1):
    first = int(first)
    second = int(second)
    road[first] = 0
    if(second >= len(road)):
        return(road, 1)
    else:
        road[second] = id1
    return(road, 0)


def create_road(N):
    road = [0] * N
    return(road)



def do_step(road, car_list, exit_list, step):
    pos2 = car_list[-1].position
    pos1 = 0
    flag = 0
    sp = car_list[-1].cur_speed
    pos_list = []
    for car in car_list[:]:
        if(1):
            pos1, pos2, sp = car.do_move(pos2, sp)
            print(car.id, pos1, pos2, car.cur_speed)
            if(pos2 > road):
                #car_list.remove(car)
                car.position = pos2 - road
                #car_list.append(car)
                exit_list.append(car)
            else:
                pos_list.append(pos2)
                #flag += 1
            #road, fl = update_road(road, pos1, pos2, car.id)
    return pos_list


def do_many_steps(N, car_list, exit_list):
    road = N
    count = 0
    step = 0
    while(len(car_list)):
        print("Step ", step)
        do_step(road, car_list, exit_list, step)
        step += 1


CARS = []


def car_maker_manual(CARS):
    car1 = Car(8, 0, "car1", 0, 1, 4, 0, 0)
    car2 = Car(4, 2, "car2", 0, 1, 3, 0, 0)
    car3 = Car(10, 3, "car3", 0, 1, .5, 0, 0)
    car4 = Car(3.5, 4, "car4", 0, 1, 2, 0, 0)
    car5 = Car(5, 5, "car5", 0, 2, 4, 0, 0)
    car6 = Car(3.2, 6, "car6", 0, 1, 1.2, 0, 0)
    CARS.append(car1)
    CARS.append(car2)
    CARS.append(car3)
    CARS.append(car4)
    CARS.append(car5)
    CARS.append(car6)
    return CARS

def car_maker_random(CARS, vel_max, max_accel, M, road):
    for i in range(0, M):
        vel = np.random.randint(30, 31) / 10
        accel = np.random.randint(9, 10) / 10
        stri = "Car " + str(i)
        if(i == 0):
            stop = road/2
        else:
            stop = 0
        car = Car(vel, stri, road * (M - i) / M, 10, accel, stop)
        CARS.append(car)
    return(CARS)





####################################################

road = 1000
exit_list = []
CARS = car_maker_random(CARS, 3, 3, 90, road)

fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, xlim = (-1.3, 1.3), ylim=(-1.3,1.3))

graph_list = []
index_list = []

####################################################
def init():
    global CARS, road, exit_list
    x = ax.plot([], [], 'b.')
    return x

def animate(i):
    global CARS, exit_list, road, ax, fig, graph_list
    print("\nSTEP", i, "\n\n")
    pos_list = do_step(road, CARS, exit_list, i)


    idx = [i] * len(pos_list)
    index_list.append(idx)
    graph_list.append(pos_list)
    pos_list = np.asarray(pos_list)
    zero_list = [0] * len(pos_list)
    pos_list = pos_list / road * 2 * np.pi



    x = ax.plot(np.cos(pos_list) , np.sin(pos_list), 'b.')
    return x

##############################################################
ani = animation.FuncAnimation(fig, animate, frames=6000,
                              interval=10, blit=True, init_func=init)

plt.show()
##########################################################



#do_many_steps(1000, CARS, exit_list)

index_list = list(map(list, zip(*index_list)))
graph_list =  list(map(list, zip(*graph_list)))


for i in range(0, len(graph_list)):
    plt.plot(index_list[i], graph_list[i], ".")

plt.title("1000 Length Road with 90 Cars")
plt.xlabel("Number of Steps Taken")
plt.ylabel("Position")
#plt.savefig("JamPlot.png", dpi=600)
plt.show()




'''
for i in exit_list:
    avg = i.cum_speed / i.steps
    i.avg_speed = avg
    perc = avg / i.max_speed
    i.perc_speed = perc
    avg_speed.append(avg)
    perc_speed.append(perc)


avg_speed = np.asarray(avg_speed)
perc_speed = np.asarray(perc_speed)
print(avg_speed)
print(np.average(avg_speed))
print(perc_speed)
print(np.average(perc_speed))
'''















