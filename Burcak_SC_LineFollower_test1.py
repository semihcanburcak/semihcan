from Scratches import Line_Follower
from picar import front_wheels
from picar import back_wheels
import time
import picar

picar.setup()

REFERENCES = [200, 200, 200, 200, 200]
#calibrate = True
calibrate = False
forward_speed = 80
backward_speed = 70
turning_angle = 40
last_off = True




max_off_track_count = 40

delay = 0.0005

fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
lf = Line_Follower.Line_Follower()

lf.references = REFERENCES
fw.ready()
bw.ready()
fw.turning_max = 45


def straight_run():
	while True:
		bw.speed = 70
		bw.forward()
		fw.turn_straight()

def setup():
	if calibrate:
		cali()



def main():
    global turning_angle
    off_track_count = 0


    a_step = 5
    b_step = 15
    c_step = 25


    if lt_status_now == [0, 0, 0, 0, 0]:
        step = 0

    elif lt_status_now == [1, 0, 0, 0, 0] or lt_status_now == [0, 0, 0, 0, 1]:
        step = a_step

    elif lt_status_now == [0, 1, 0, 0, 0] or lt_status_now == [0, 0, 0, 1, 0]:
        step = b_step

    elif lt_status_now == [0, 0, 1, 0, 0]:
        step = c_step


    if	lt_status_now == [0,0,1,0,0]:
		off_track_count = 0
		bw.speed = backward_speed
		fw.turn(0)

    elif lt_status_now == [1, 0, 0, 0, 0]:
		bw.speed = 55
		delay = 0.5
        turning_angle = int(90 - step)
        last_off = False

    elif lt_status_now == [0, 0, 0, 0, 1]:
		bw.speed = 55
		delay = 0.5
		turning_angle = int(90 + step)

        last_off = True

    elif lt_stautus_now == [0, 1, 0, 0, 0]:
		bw.speed = 45
		delay = 0.5
		turning_angle = int(90 - step)
        last_off = False

    elif lt_status_now == [0, 0, 0, 1, 0]:
		bw.speed = 45
		delay = 0.5
        turning_angle = int (90 + step)
        last_off = True

    elif lt_status_now == [0, 0, 1, 0, 0]:
		bw.speed = 30
		delay = 0.5
        if last_off == True:
            turning_angle = int(90 + step)
        elif last_off == False:
            turning_angle = int(90 - step)





def cali():
	references = [0, 0, 0, 0, 0]
	print("cali for module:\n  first put all sensors on white, then put all sensors on black")
	mount = 100
	fw.turn(70)
	print("\n cali white")
	time.sleep(4)
	fw.turn(90)
	white_references = lf.get_average(mount)
	fw.turn(95)
	time.sleep(0.5)
	fw.turn(85)
	time.sleep(0.5)
	fw.turn(90)
	time.sleep(1)

	fw.turn(110)
	print("\n cali black")
	time.sleep(4)
	fw.turn(90)
	black_references = lf.get_average(mount)
	fw.turn(95)
	time.sleep(0.5)
	fw.turn(85)
	time.sleep(0.5)
	fw.turn(90)
	time.sleep(1)

	for i in range(0, 5):
		references[i] = (white_references[i] + black_references[i]) / 2
	lf.references = references
	print("Middle references =", references)
	time.sleep(1)


def destroy():
	bw.stop()
	fw.turn(90)

if __name__ == '__main__':
	try:
		try:
			while True:
				setup()
				main()
				#straight_run()
		except Exception as e:
			print(e)
			print('error try again in 5')
			destroy()
			time.sleep(5)
	except KeyboardInterrupt:
		destroy()
