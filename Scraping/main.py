import telebot
from telebot import types
import os
import random
import os.path
import cv2
from telebot.types import Message
import re
import glob
import math
import numpy as np
import matplotlib.pyplot as plt
import shutil
import datetime

now = datetime.datetime.now()
admin = -910592818
my_id = 1212566690
bot = telebot.TeleBot('5492673659:AAFGpE8BY77GSJ4Pl7pRRHXBH1doIQtus5k')
k = 1
j = 1


@bot.message_handler(content_types='text')
def start(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        m1 = types.KeyboardButton('Готово ✅')
        m2 = types.KeyboardButton('Удалить фото')
        markup.add(m1)
        mm2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, )
        z2 = 'Завершить ⛔'
        z3 = 'Связь с разработчиком 📞'
        z4 = 'Ещё раз ↺'
        z5 = 'Пожертвовать 💸'
        mm2.add(z2, z3, z4, z5)
        Spasibo = types.ReplyKeyboardMarkup(resize_keyboard=True)
        ff1 = '/start'
        ff2 = 'История 🕓'
        Spasibo.add(ff1, ff2)
        zanovo = types.ReplyKeyboardMarkup(resize_keyboard=True)
        za1 = 'Ещё раз ↺'
        zanovo.add(za1)
        Clean = types.ReplyKeyboardMarkup(resize_keyboard=True)
        cl1 = 'Очистить историю'
        cl2 = 'Назад'
        Clean.add(cl1, cl2)
        if message.text == '/start':
            bot.send_message(message.chat.id, 'Пришлите фотографии и нажмите "Готово"', reply_markup=markup)
            user_id = message.from_user.id
            user_name = message.from_user.username
            global k
            k = 1
            filename = "InputImages/list_user_id.txt"
            with open(filename, "r") as f:
                doc_contents = f.read()
            if str(user_id) not in doc_contents:
                with open(filename, "a") as f:
                    f.write(str(user_id) + ',')
            filename_2 = "InputImages/last_user_name.txt"
            with open(filename_2, "r") as f:
                doc_contents = f.read()
            if str(user_name) not in doc_contents:
                with open(filename_2, "a") as f:
                    f.write("@" + str(user_name) + ',')

            if os.path.exists(f'InputImages/Telegr/{user_id}') == False:
                os.mkdir(f'InputImages/Telegr/{user_id}')
            if os.path.exists(f'InputImages/Telegr/{user_id}/history') == False:
                os.mkdir(f"InputImages/Telegr/{user_id}/history")
            if os.path.exists(f'InputImages/Telegr/{user_id}/rabota') == False:
                os.mkdir(f'InputImages/Telegr/{user_id}/rabota')
        if message.text == 'Готово ✅':
            mas = bot.send_message(message.chat.id, 'Идёт процесс сшивки 🪡🧵🪡')

            def ReadImage(ImageFolderPath):
                Images = []

                if os.path.isdir(ImageFolderPath):
                    ImageNames = os.listdir(ImageFolderPath)
                    ImageNames_Split = [[int(os.path.splitext(os.path.basename(ImageName))[0]), ImageName] for ImageName
                                        in ImageNames]
                    ImageNames_Split = sorted(ImageNames_Split, key=lambda x: x[0])
                    ImageNames_Sorted = [ImageNames_Split[i][1] for i in range(len(ImageNames_Split))]

                    for i in range(len(ImageNames_Sorted)):
                        ImageName = ImageNames_Sorted[i]
                        InputImage = cv2.imread(ImageFolderPath + "/" + ImageName)

                        # Checking if image is read
                        if InputImage is None:
                            print("Not able to read image: {}".format(ImageName))
                            exit(0)

                        Images.append(InputImage)
                else:
                    print("\nEnter valid Image Folder Path.\n")

                if len(Images) < 2:
                    bot.delete_message(message.chat.id, mas.message_id)
                    bot.send_message(message.chat.id, 'Введите минимум 2 изображения')
                    print("\nNot enough images found. Please provide 2 or more images.\n")
                    exit(1)

                return Images

            def FindMatches(BaseImage, SecImage):

                Sift = cv2.SIFT_create()
                BaseImage_kp, BaseImage_des = Sift.detectAndCompute(cv2.cvtColor(BaseImage, cv2.COLOR_BGR2GRAY), None)
                SecImage_kp, SecImage_des = Sift.detectAndCompute(cv2.cvtColor(SecImage, cv2.COLOR_BGR2GRAY), None)

                BF_Matcher = cv2.BFMatcher()
                InitialMatches = BF_Matcher.knnMatch(BaseImage_des, SecImage_des, k=2)

                GoodMatches = []
                for m, n in InitialMatches:
                    if m.distance < 0.75 * n.distance:
                        GoodMatches.append([m])

                return GoodMatches, BaseImage_kp, SecImage_kp

            def FindHomography(Matches, BaseImage_kp, SecImage_kp):

                if len(Matches) < 4:
                    print("\nNot enough matches found between the images.\n")
                    bot.delete_message(message.chat.id, mas.message_id)
                    bot.send_message(message.chat.id, 'Недостаточно совпадений между изображениями, из-за этого')
                    exit(0)

                BaseImage_pts = []
                SecImage_pts = []
                for Match in Matches:
                    BaseImage_pts.append(BaseImage_kp[Match[0].queryIdx].pt)
                    SecImage_pts.append(SecImage_kp[Match[0].trainIdx].pt)

                BaseImage_pts = np.float32(BaseImage_pts)
                SecImage_pts = np.float32(SecImage_pts)

                (HomographyMatrix, Status) = cv2.findHomography(SecImage_pts, BaseImage_pts, cv2.RANSAC, 4.0)

                return HomographyMatrix, Status

            def GetNewFrameSizeAndMatrix(HomographyMatrix, Sec_ImageShape, Base_ImageShape):

                (Height, Width) = Sec_ImageShape

                InitialMatrix = np.array([[0, Width - 1, Width - 1, 0],
                                          [0, 0, Height - 1, Height - 1],
                                          [1, 1, 1, 1]])

                FinalMatrix = np.dot(HomographyMatrix, InitialMatrix)

                [x, y, c] = FinalMatrix
                x = np.divide(x, c)
                y = np.divide(y, c)

                min_x, max_x = int(round(min(x))), int(round(max(x)))
                min_y, max_y = int(round(min(y))), int(round(max(y)))

                New_Width = max_x
                New_Height = max_y
                Correction = [0, 0]
                if min_x < 0:
                    New_Width -= min_x
                    Correction[0] = abs(min_x)
                if min_y < 0:
                    New_Height -= min_y
                    Correction[1] = abs(min_y)

                if New_Width < Base_ImageShape[1] + Correction[0]:
                    New_Width = Base_ImageShape[1] + Correction[0]
                if New_Height < Base_ImageShape[0] + Correction[1]:
                    New_Height = Base_ImageShape[0] + Correction[1]

                x = np.add(x, Correction[0])
                y = np.add(y, Correction[1])
                OldInitialPoints = np.float32([[0, 0],
                                               [Width - 1, 0],
                                               [Width - 1, Height - 1],
                                               [0, Height - 1]])
                NewFinalPonts = np.float32(np.array([x, y]).transpose())

                HomographyMatrix = cv2.getPerspectiveTransform(OldInitialPoints, NewFinalPonts)

                return [New_Height, New_Width], Correction, HomographyMatrix

            def StitchImages(BaseImage, SecImage):

                SecImage_Cyl, mask_x, mask_y = ProjectOntoCylinder(SecImage)

                SecImage_Mask = np.zeros(SecImage_Cyl.shape, dtype=np.uint8)
                SecImage_Mask[mask_y, mask_x, :] = 255

                Matches, BaseImage_kp, SecImage_kp = FindMatches(BaseImage, SecImage_Cyl)

                HomographyMatrix, Status = FindHomography(Matches, BaseImage_kp, SecImage_kp)

                NewFrameSize, Correction, HomographyMatrix = GetNewFrameSizeAndMatrix(HomographyMatrix,
                                                                                      SecImage_Cyl.shape[:2],
                                                                                      BaseImage.shape[:2])

                SecImage_Transformed = cv2.warpPerspective(SecImage_Cyl, HomographyMatrix,
                                                           (NewFrameSize[1], NewFrameSize[0]))
                SecImage_Transformed_Mask = cv2.warpPerspective(SecImage_Mask, HomographyMatrix,
                                                                (NewFrameSize[1], NewFrameSize[0]))
                BaseImage_Transformed = np.zeros((NewFrameSize[0], NewFrameSize[1], 3), dtype=np.uint8)
                BaseImage_Transformed[Correction[1]:Correction[1] + BaseImage.shape[0],
                Correction[0]:Correction[0] + BaseImage.shape[1]] = BaseImage

                StitchedImage = cv2.bitwise_or(SecImage_Transformed, cv2.bitwise_and(BaseImage_Transformed,
                                                                                     cv2.bitwise_not(
                                                                                         SecImage_Transformed_Mask)))

                return StitchedImage

            def Convert_xy(x, y):
                global center, f

                xt = (f * np.tan((x - center[0]) / f)) + center[0]
                yt = ((y - center[1]) / np.cos((x - center[0]) / f)) + center[1]

                return xt, yt

            def ProjectOntoCylinder(InitialImage):
                global w, h, center, f
                h, w = InitialImage.shape[:2]
                center = [w // 2, h // 2]
                f = 1200  # 1100 field; 1000 Sun; 1500 Rainier; 1050 Helens

                TransformedImage = np.zeros(InitialImage.shape, dtype=np.uint8)

                AllCoordinates_of_ti = np.array([np.array([i, j]) for i in range(w) for j in range(h)])
                ti_x = AllCoordinates_of_ti[:, 0]
                ti_y = AllCoordinates_of_ti[:, 1]

                ii_x, ii_y = Convert_xy(ti_x, ti_y)

                ii_tl_x = ii_x.astype(int)
                ii_tl_y = ii_y.astype(int)

                GoodIndices = (ii_tl_x >= 0) * (ii_tl_x <= (w - 2)) * \
                              (ii_tl_y >= 0) * (ii_tl_y <= (h - 2))

                ti_x = ti_x[GoodIndices]
                ti_y = ti_y[GoodIndices]

                ii_x = ii_x[GoodIndices]
                ii_y = ii_y[GoodIndices]

                ii_tl_x = ii_tl_x[GoodIndices]
                ii_tl_y = ii_tl_y[GoodIndices]

                dx = ii_x - ii_tl_x
                dy = ii_y - ii_tl_y

                weight_tl = (1.0 - dx) * (1.0 - dy)
                weight_tr = (dx) * (1.0 - dy)
                weight_bl = (1.0 - dx) * (dy)
                weight_br = (dx) * (dy)

                TransformedImage[ti_y, ti_x, :] = (weight_tl[:, None] * InitialImage[ii_tl_y, ii_tl_x, :]) + \
                                                  (weight_tr[:, None] * InitialImage[ii_tl_y, ii_tl_x + 1, :]) + \
                                                  (weight_bl[:, None] * InitialImage[ii_tl_y + 1, ii_tl_x, :]) + \
                                                  (weight_br[:, None] * InitialImage[ii_tl_y + 1, ii_tl_x + 1, :])

                min_x = min(ti_x)

                TransformedImage = TransformedImage[:, min_x: -min_x, :]

                return TransformedImage, ti_x - min_x, ti_y

            if __name__ == "__main__":

                user_id = message.from_user.id
                Images = ReadImage(f"InputImages/Telegr/{user_id}/rabota")

                BaseImage, _, _ = ProjectOntoCylinder(Images[0])
                for i in range(1, len(Images)):
                    StitchedImage = StitchImages(BaseImage, Images[i])

                    BaseImage = StitchedImage.copy()

                cv2.imwrite(f"InputImages/Telegr/{user_id}/rabota/Stitched_Panorama.jpg", BaseImage)
                img = cv2.imread(f"InputImages/Telegr/{user_id}/rabota/Stitched_Panorama.jpg")

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                max_area = 0
                max_contour = None
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area > max_area:
                        max_area = area
                        max_contour = contour
                x, y, w, h = cv2.boundingRect(max_contour)

                img = img[y:y + h, x:x + w]
                cv2.imwrite(f'InputImages/Telegr/{user_id}/rabota/Stitched_Panorama.png', img)
                os.remove(f'InputImages/Telegr/{user_id}/rabota/Stitched_Panorama.jpg')
                bot.send_photo(message.chat.id,
                               photo=open(f'InputImages/Telegr/{user_id}/rabota/Stitched_Panorama.png', 'rb'),
                               reply_markup=mm2)
                bot.delete_message(message.chat.id, mas.message_id)

        if message.text == 'Удалить фото':
            user_id = message.from_user.id
            list_of_files = glob.glob(f"InputImages/Telegr/{user_id}/rabota")
            latest_file = max(list_of_files, key=os.path.getctime)
            os.remove(latest_file)
            bot.reply_to(message, 'Фото удалено')

    except:
        if len(os.listdir(f'InputImages/Telegr/{user_id}/rabota')) >= 2:
            bot.send_message(message.chat.id, 'Произошла ошибка, повторите попытку', reply_markup=zanovo)
            bot.delete_message(message.chat.id, mas.message_id)
            user_id = message.from_user.id
            try:
                if os.path.exists(f'InputImages\Telegr\{user_id}\\rabota') == True:
                    dir = f'InputImages\Telegr\{user_id}\\rabota'
                    shutil.rmtree(dir)
            except:
                pass
    if message.text == 'Ещё раз ↺':
        try:
            user_id = message.from_user.id
            if os.path.exists(f'InputImages/Telegr/{user_id}/rabota/Stitched_Panorama.png') == True:
                shutil.move(f'InputImages/Telegr/{user_id}/rabota/Stitched_Panorama.png',
                            f'InputImages/Telegr/{user_id}/history/Stitched_Panorama.png')
                os.rename(f'InputImages/Telegr/{user_id}/history/Stitched_Panorama.png',
                          f'InputImages/Telegr/{user_id}/history/{fu()}.png')
            bot.send_message(message.chat.id, 'Принято, пришлите мне фотографии', reply_markup=markup)
            if os.path.exists(f'InputImages\Telegr\{user_id}\\rabota') == True:
                dir = f'InputImages\Telegr\{user_id}\\rabota'
                shutil.rmtree(dir)
            if os.path.exists(f'InputImages/Telegr/{user_id}/rabota') == False:
                os.mkdir(f'InputImages/Telegr/{user_id}/rabota')
            i = 1
        except:
            bot.send_message(message.chat.id, 'Произошла ошибка, повторите попытку', reply_markup=Spasibo)
            user_id = message.from_user.id
            if os.path.exists(f'InputImages\Telegr\{user_id}\\rabota') == True:
                dir = f'InputImages\Telegr\{user_id}\\rabota'
                shutil.rmtree(dir)

    if message.text == 'Завершить ⛔':
        try:
            user_id = message.from_user.id
            if os.path.exists(f'InputImages/Telegr/{user_id}/rabota/Stitched_Panorama.png') == True:
                # try:
                os.rename(f'InputImages/Telegr/{user_id}/rabota/Stitched_Panorama.png',
                          f'InputImages/Telegr/{user_id}/history/{fu()}.png')
                # shutil.move(f'InputImages/Telegr/{user_id}/rabota/{str(now.strftime("%d-%m-%Y %H-%M-%S"))}.png', f'InputImages/Telegr/{user_id}/history/{str(now.strftime("%d-%m-%Y %H-%M-%S"))}.png')
            # except:
            #     os.remove(f'InputImages/Telegr/{user_id}/history/Stitched_Panorama.png')
            #     os.rename(f'InputImages/Telegr/{user_id}/history/Stitched_Panorama.png', f'InputImages/Telegr/{user_id}/history/{str(now.strftime("%d-%m-%Y %H-%M-%S"))}.png')

            bot.send_message(message.chat.id, 'Принято, жду Вас снова!', reply_markup=Spasibo)
            if os.path.exists(f'InputImages\Telegr\{user_id}\\rabota') == True:
                dir = f'InputImages\Telegr\{user_id}\\rabota'
                shutil.rmtree(dir)
            i = 1
        except:
            bot.send_message(message.chat.id, 'Произошла ошибка, повторите попытку', reply_markup=Spasibo)
            user_id = message.from_user.id
            if os.path.exists(f'InputImages\Telegr\{user_id}\\rabota') == True:
                dir = f'InputImages\Telegr\{user_id}\\rabota'
                shutil.rmtree(dir)
    if message.text == 'Связь с разработчиком 📞':
        user_id = message.from_user.id
        if os.path.exists(f'InputImages/Telegr/{user_id}/rabota/Stitched_Panorama.png') == True:
            shutil.move(f'InputImages/Telegr/{user_id}/rabota/Stitched_Panorama.png',
                        f'InputImages/Telegr/{user_id}/history/Stitched_Panorama.png')
            os.rename(f'InputImages/Telegr/{user_id}/history/Stitched_Panorama.png',
                      f'InputImages/Telegr/{user_id}/history/{str(now.strftime("%d-%m-%Y %H-%M-%S"))}.png')
        bot.send_message(message.chat.id, 'Я вас слушаю')
        bot.register_next_step_handler(message, ad)

        if os.path.exists(f'InputImages\Telegr\{user_id}\\rabota') == True:
            dir = f'InputImages\Telegr\{user_id}\\rabota'
            shutil.rmtree(dir)
        i = 1
    if message.text == 'История 🕓':
        try:
            user_id = message.from_user.id
            if os.path.exists(f'InputImages/Telegr/{user_id}/rabota/Stitched_Panorama.png') == True:
                shutil.move(f'InputImages/Telegr/{user_id}/rabota/Stitched_Panorama.png',
                            f'InputImages/Telegr/{user_id}/history/Stitched_Panorama.png')
                os.rename(f'InputImages/Telegr/{user_id}/history/Stitched_Panorama.png',
                          f'InputImages/Telegr/{user_id}/history/{str(now.strftime("%d-%m-%Y %H-%M-%S"))}.png')
            if os.path.exists(f'InputImages\Telegr\{user_id}\\rabota') == True:
                dir = f'InputImages\Telegr\{user_id}\\rabota'
                shutil.rmtree(dir)
            if os.path.exists(f'InputImages/Telegr/{user_id}/history') == False:
                bot.send_message(message.chat.id, 'Ваша история пуста')
            else:
                bot.send_message(message.chat.id, 'Ваша история:', reply_markup=Clean)
                listdir = os.listdir(f'InputImages/Telegr/{user_id}/history')
                for image in listdir:
                    try:
                        name = os.path.basename(f'InputImages/Telegr/{user_id}/history/{image}')
                        photo = f'InputImages/Telegr/{user_id}/history/{image}'
                        bot.send_photo(message.from_user.id, photo=open(photo, 'rb'))
                        # bot.send_message(message.chat.id, name[:-8])
                    except:
                        pass
        except:
            bot.send_message(message.chat.id, 'Произошла ошибка, повторите попытку', reply_markup=Spasibo)
            user_id = message.from_user.id
            try:
                if os.path.exists(f'InputImages\Telegr\{user_id}\\rabota') == True:
                    dir = f'InputImages\Telegr\{user_id}\\rabota'
                    shutil.rmtree(dir)
                if os.path.exists(f'InputImages/Telegr/{user_id}/history') == True:
                    dir = f'InputImages/Telegr/{user_id}/history'
                    shutil.rmtree(dir)
            except:
                pass
    if message.text == 'Очистить историю':
        try:
            user_id = message.from_user.id
            dir = f'InputImages\Telegr\{user_id}\\history'
            shutil.rmtree(dir)
            bot.send_message(message.chat.id, 'История очищена', reply_markup=Spasibo)
        except:
            bot.send_message(message.chat.id, 'Произошла ошибка, повторите попытку', reply_markup=Spasibo)
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Принято!', reply_markup=Spasibo)
    if message.text == '/sendall' and message.chat.id == 1212566690:
        bot.send_message(1212566690, "Напишите сообщение для рассылки")
        bot.register_next_step_handler(message, sendi)
    if message.text == '/sendall' and message.chat.id != 1212566690:
        bot.send_message(message.chat.id, 'У Вас недостаточно прав для рассылки')
    if message.text == '/secret':
        f = open('InputImages\last_user_name.txt').read()
        bot.send_message(1212566690, 'Список пользователей:')
        bot.send_message(1212566690, f)
    if message.text == 'Пожертвовать 💸':
        bot.send_message(message.chat.id,
                         'Спб: +79534952919 Тинкофф(Арсений Л) \nПо номеру карты: <a href="tg://user?id=0">2200 7706 1583 9679</a> \nСпасибо за пожертвование!',
                         parse_mode='html', reply_markup=mm2)


@bot.message_handler(content_types=['photo'])
def pho(message):
    global k
    user_id = message.from_user.id
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f'InputImages/Telegr/{user_id}/rabota' + '/' + f'{k}.jpg'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Фото добавлено")
        k += 1
    except Exception as e:
        print(e)


def ad(message):
    mm2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, )
    z2 = 'Завершить ⛔'
    z3 = 'Связь с разработчиком 📞'
    z4 = 'Ещё раз ↺'
    z5 = 'Пожертвовать 💸'
    mm2.add(z2, z3, z4, z5)
    tt = message.text
    f = message.chat.username
    text = []
    name = []
    text.append(tt)
    name.append(f)
    bot.send_message(admin, f'Сообщение от @{name[0]}:\n{text[0]} \n')
    text.clear()
    name.clear()
    bot.send_message(message.chat.id, 'Сообщение отправлено', reply_markup=mm2)


def sendi(message):
    tt = message.text
    text = []
    text.append(tt)
    with open("InputImages\list_user_id.txt", 'r') as a:
        user_id = a.readline().split(',')
    for i in user_id:
        bot.send_message(i, message.text)


def fu():
    c = random.randint(1, 99999)
    ster = str(now.strftime("%d-%m-%Y %H-%M-%S")) + f'{c}'
    c += 1
    return ster


bot.polling(none_stop=True)