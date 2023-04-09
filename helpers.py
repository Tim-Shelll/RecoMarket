import cv2
import os

def get_valid_order(purchases):
    orders = {}
    for purchase in purchases:
        if (purchase[1], purchase[4]) not in orders:
            orders[(purchase[1], purchase[4])] = [purchase]
        else:
            orders[(purchase[1], purchase[4])].append(purchase)

    return orders

def refactor_img(path):
    img = cv2.imread(path)
    if  img is None:
        print('img is None')
    else:
        ref_img = cv2.resize(img, (img.shape[1] // 3 * 2, img.shape[0] // 3 * 2))
        cv2.imwrite(os.getcwd() + r'/static/users/andrey.jpg', ref_img)

PATH = r'static\users\andrey.jpg'