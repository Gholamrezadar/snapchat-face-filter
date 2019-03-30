import cv2
import numpy as np

lips = []
selected = False
Done = False
LipScale = 1.4

# Callback Functions
def onMouse(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN and not selected:
		lips.append([x, y])
		cv2.circle(tommy, (x, y), 2, (0, 0, 255), -1)


if __name__ == "__main__":
	tommy = cv2.imread("Tommy800.png")
	tommy_orig = tommy.copy()
	tommy_scaled = []

	# Main Window
	cv2.namedWindow("Tommy")
	cv2.setMouseCallback("Tommy", onMouse)

	# Main Loop
	while True:
		if cv2.waitKey(100) == ord("a"):
			selected = True
			print(lips)

		if not selected:
			cv2.imshow("Tommy", tommy)
		elif not Done:
			lips_mask = np.zeros(tommy_orig.shape, tommy_orig.dtype)
			lips_mask = cv2.fillPoly(lips_mask, [np.array(lips, np.int32)], (255, 255, 255),lineType=cv2.LINE_AA)

			lips_mask    = lips_mask [min(lips,key=lambda x:x[1])[1]:max(lips,key=lambda x:x[1])[1],min(lips,key=lambda x:x[0])[0]:max(lips,key=lambda x:x[0])[0]]
			tommy_scaled = tommy_orig[min(lips,key=lambda x:x[1])[1]:max(lips,key=lambda x:x[1])[1],min(lips,key=lambda x:x[0])[0]:max(lips,key=lambda x:x[0])[0]]

			lips_mask    = cv2.resize(lips_mask,    None, fx=LipScale, fy=LipScale, interpolation = cv2.INTER_CUBIC)
			tommy_scaled = cv2.resize(tommy_scaled, None, fx=LipScale, fy=LipScale, interpolation = cv2.INTER_CUBIC)

			avg_x = (min(lips,key=lambda x:x[0])[0]+max(lips,key=lambda x:x[0])[0])//2
			avg_y = (min(lips,key=lambda x:x[1])[1]+max(lips,key=lambda x:x[1])[1])//2
			tommy_orig = cv2.seamlessClone(tommy_scaled, tommy_orig, lips_mask, (avg_x,avg_y), cv2.NORMAL_CLONE)

			Done = True
		else:
			cv2.imshow("Tommy", tommy_orig)
			cv2.imshow("Mask",  tommy_scaled)

		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cv2.destroyAllWindows()
