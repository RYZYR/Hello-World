import os
import cv2
import threading
import time
import urllib.request
import urllib.error
import urllib3
import requests
import time
import cv2
import json

class FaceRecog(threading.Thread):
    #获取所有属性,并以列表的形式打印信息

    #获取单个属性
    def get_face_info(self,filepath,info):
        http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
        file = open(filepath, "rb")
        files = {"image_file": file} #字典
        info_list=[]
        info_list.append(info)
        data={
            "api_key":self.key,
            "api_secret":self.secret,
            "return_attributes":info_list
        }
        emotion_response = requests.post(http_url, data=data, files=files)  # 获取情绪属性
        emotion_dict = emotion_response.json()
        return emotion_dict
    def get_all_info(self,filepath):

        emotion_dict = self.get_face_info(filepath, 'emotion')

        for i in emotion_dict.get('faces'):
            emotion_1=i.get('attributes').get('emotion')
            self.emotion_list.append(max(emotion_1, key=emotion_1.get))     #打印返回信息人脸情绪

        #获取face_tokens集 利用emotion_dict
        for i in emotion_dict.get('faces'):
            faces_token_1=i.get('face_token')
            self.faces_token.append(faces_token_1)
        if emotion_dict==[]:
            print("未检测到人脸")
            return

    def get_eyestatus(self,face_token):
        http_url = "https://api-cn.faceplusplus.com/facepp/v3/face/analyze"
        data = {
            "api_key": self.key,
            "api_secret": self.secret,
            "face_tokens":face_token,
            "return_attributes": 'eyestatus'
        }
        response = requests.post(http_url, data=data)
        eyestatus_dict = response.json()
        # 眼睛被遮挡的置信度
        occlusion = 50
        # 眼睛睁开的置信度
        eye_open = 50
        eyestatus = eyestatus_dict.get('faces')[0].get('attributes').get('eyestatus')
        left_normal_glass_eye_open = eyestatus['left_eye_status']['normal_glass_eye_open']
        right_normal_glass_eye_open = eyestatus['right_eye_status']['normal_glass_eye_open']
        left_no_class_eye_open = eyestatus['left_eye_status']['no_glass_eye_open']
        right_no_glass_eye_open = eyestatus['right_eye_status']['no_glass_eye_open']
        left_occlusion = eyestatus['left_eye_status']['occlusion']
        right_occlusion = eyestatus['right_eye_status']['occlusion']
        if left_occlusion > occlusion and right_occlusion > occlusion:
            return "眼部被遮挡"
        else:
            if left_no_class_eye_open > eye_open or left_normal_glass_eye_open > eye_open or right_no_glass_eye_open > eye_open or right_normal_glass_eye_open > eye_open:
                return '睁眼'
            else:
                return '闭眼'

    # 说明:此函数用来比对搜索到的人脸，判断其是否已经存在于face_set集合
    def searchFace(self,face_token,outer_id):
        http_url = "https://api-cn.faceplusplus.com/facepp/v3/search"
        #############files={"image_file":open(filepath,"rb")}
        emotion_data = {"api_key": self.key,
                        "api_secret": self.secret,
                        "outer_id":outer_id,
                        "face_token":face_token
                        }
        compInfo = requests.post(http_url, data=emotion_data)  # 获取情绪属性
        req_dict=compInfo.json()

        if req_dict["results"][0]["confidence"]>50:
            name_id=req_dict["results"][0]["user_id"]
            #返回搜索到的对应学生的ID，未搜索到则返回[]
        return name_id

    def stop(self):
        self.isRunning = False

    def run(self):
        self.stu_list['startTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.stu_list['endTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open(os.getcwd() + r"\srtpApp\jsonData\data.json", "w") as f:
            self.info["info"] = self.stu_list
            json.dump(self.info["info"], f)
            f.close()
        t1=time.time()#初始时间
        start=time.time()
        cap = cv2.VideoCapture("http://192.168.36.100:8080/?action=stream")    #打开摄像头
        runNum = 0
        while self.isRunning:
              ret,frame=cap.read()          #提取关键帧
              cv2.imshow("GetImage",frame)  #实时展示
              t2=time.time()                #与初始时间比较获取时间间隔
              end=time.time()
              if t2-t1>=2:#每隔5秒提取一次
                runNum += 1
                imageFilePath="C:\\Users\\"+str(int(t1))+".jpg"#图片保存路径(需要修改)
                self.stu_list['countCapture'] = self.stu_list['countCapture'] + 1
                self.stu_list['endTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                cv2.imwrite(imageFilePath,frame)#保存关键帧
                # print(imageFilePath)
                self.get_all_info(imageFilePath)  #图片上传并获取信息
                print("--------------------"+str(runNum)+"---------------------")
                #人脸比对
                for i in self.faces_token:
                    name=self.searchFace(i,"student")
                    print(name)
                    #如果比对不成功或没有比对到人脸
                    if len(name)!=10 or name=="":
                        continue
                    #学生睁眼状态加1【认真听课】
                    if self.get_eyestatus(i) == '睁眼':
                        self.stu_list[name]['detect_success'] = self.stu_list[name]['detect_success']+1
                    # 记录学生最后一次露面时间（签退时间）
                    self.stu_list[name]['end'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    self.stu_list[name]['count'] = self.stu_list[name]['count'] + 1
                    # 记录该学生第一次露面时间（签到时间）
                    if self.stu_list[name]['start'] == 0:
                        self.stu_list[name]['start'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                self.faces_token=[]
                t1=time.time()#重置初试时间

                # print(self.stu_list)
                #保存一分钟统计信息
                if end-start>=5:
                    with open(os.getcwd()+r"\srtpApp\jsonData\data.json","w") as f:
                        self.info["info"]=self.stu_list
                        json.dump(self.info["info"],f)
                        f.close()
                    start=end
              # if cv2.waitKey(100) & 0xff == ord('q'): # 按q退出
              #     break

    def __init__(self):
        threading.Thread.__init__(self)
        self.isRunning = True
        self.key = "EUNIPCuYk7Mj4toPxmFgxTSUeCQnA-OT"
        self.secret = "TevGdS9j-lPUZq0zxEDECssVZsdxZ-G5"
        self.info={"info":[]}
        self.emotion_list = []
        self.faces_token = []
        self.stu_list = {
                            #添加学号与检测结果的键值对
                            #格式'学号值':{'detect_success':0,'count':0,'start':0,'end':0},
                            'countCapture':0,
                            'endTime':0,
                            'startTime':0
                         }

class VideoCamera(object):
    def __init__(self):
        self.is_record = False
    def start_record(self):
        self.is_record = True
        self.recordingThread = FaceRecog()
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False
        if self.recordingThread != None:
            self.recordingThread.stop()


# v = VideoCamera()
# v.start_record()
#
# time.sleep(15)
# v.stop_record()