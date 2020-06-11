import numpy as np
import uuid
from django.shortcuts import render
from .models import ImageModel, LearningModel
from keras.preprocessing import image
from keras.applications.imagenet_utils import decode_predictions
from keras.applications.resnet50 import preprocess_input
from googletrans import Translator
from django.urls import reverse_lazy

## 翻訳Class
translator = Translator()
## 各種モデル
from keras.applications.vgg16 import VGG16
model_vgg16 = VGG16(weights="imagenet",include_top=True)
from keras.applications.vgg19 import VGG19
model_vgg19 = VGG19(weights="imagenet",include_top=True)
from keras.applications.resnet50 import ResNet50
model_resnet = ResNet50(weights="imagenet",include_top=True)
from keras.applications.xception import Xception
model_xception = Xception(weights="imagenet",include_top=True)
from keras.applications.inception_v3 import InceptionV3
model_inceptionv3 = InceptionV3(include_top=True, weights='imagenet')
from keras.applications.inception_resnet_v2 import InceptionResNetV2
model_inceptionresnet = InceptionResNetV2(include_top=True, weights='imagenet')
from keras.applications.mobilenet import MobileNet
model_mobilenet = MobileNet(include_top=True,weights='imagenet')
from keras.applications.densenet import DenseNet121,DenseNet169,DenseNet201
model_dense121 = DenseNet121(include_top=True,weights='imagenet')
model_dense169 = DenseNet169(include_top=True,weights='imagenet')
model_dense201 = DenseNet201(include_top=True,weights='imagenet')
from keras.applications.nasnet import NASNetLarge,NASNetMobile
model_naslarge = NASNetLarge(include_top=True,weights='imagenet')
model_nasmobile = NASNetMobile(include_top=True,weights='imagenet')
from keras.applications.mobilenet_v2 import MobileNetV2
model_mobilenetv2 = MobileNetV2(include_top=True,weights='imagenet')

#  caffe  : VGG16 VGG19 ResNet50
#  tf 299 : Xception InceptionV3 InceptionResNetV2
#  tf 224 : MobileNet NASNet MobileNetV2
#  torch  : DenseNet

models = {0:"ALL",1:"VGG16",2:"VGG19",3:"ResNet50",4:"Xception",5:"InceptionV3",6:"InceptionResNetV2",7:"MobileNet",8:"DenseNet121",9:"DenseNet169",10:"DenseNet201",11:"NASNetLarge",12:"NASNetMobile",13:"MobileNetV2"}

def inputfunc(request):
    return render(request,"create.html",,{"models":models})

def judgefunc(request):
    if request.method == "POST":
        model = ImageModel()
        model.images = request.FILES['images']#htmlでの名前
        try:
            request.POST['learning']
        except:
            print("learning : False")
        else:
            model.learning = True
            model.answer = request.POST['answer']
        try:
            request.POST['release']
        except:
            print("release : False")
        else:
            model.release = True
        model.title = request.POST['title']
        model.learn_model = request.POST['learn_model']
        model.user = uuid.uuid4()   ##cookie取得、保存ができてないので適当に保存
        model.save()
        if int(request.POST['learn_model']) == 0:
          judge_all(model.pk)
        else:
          judge(model.pk)
        GetAnswer = LearningModel.objects.filter(image_pk=model.pk)
        image = ImageModel.objects.get(pk=model.pk)
        if int(request.POST['learn_model']) == 0:
          return render(request,"judge_all.html",{"img":image,"data":GetAnswer,"models":models})
        else:
          return render(request, "judge.html", {"img":image,"data":GetAnswer,"models":models})
    return render(request,"index.html")

def get_model(num):
  if(num == 1):
    return model_vgg16,224
  elif(num == 2):
    return model_vgg19,224
  elif(num == 3):
    return model_resnet,224
  elif(num == 4):
    return model_xception,299
  elif(num == 5):
    return model_inceptionv3,299
  elif(num == 6):
    return model_inceptionresnet,299
  elif(num == 7):
    return model_mobilenet,224
  elif(num == 8):
    return model_dense121,224
  elif(num == 9):
    return model_dense169,224
  elif(num == 10):
    return model_dense201,224
  elif(num == 11):
    return model_naslarge,331
  elif(num == 12):
    return model_nasmobile,224
  elif(num == 13):
    return model_mobilenetv2,224
  else:
    return None,0


def judge(primary):
    model = ImageModel.objects.get(pk=primary)
    request_model = model.learn_model##使用するモデルのpk
    # PILのimageで読み込み modelのデフォルト値が224*224のためリサイズして読み込む
    model_name,size = get_model(request_model)
    img = image.load_img(model.images,target_size=(size,size))
    # PILの場合 画像として読み込まれるため、配列に変換、画像としてはRGBで読み込まれる
    # CV2の場合 配列として読み込まれるがBGRで読み込まれる
    # PLTの場合 配列として読み込まれ、RGBで読み込まれる
    x = image.img_to_array(img)
    # 3次元（rows,cols,channels）から
    # 4次元（samples,rows,cols,channels）に変換
    # axisは追加位置
    x = np.expand_dims(x,axis=0)

    if(model_name == None):
        print("error")
    # モデルの予測
    preds = model_name.predict(preprocess_input(x))
    results = decode_predictions(preds, top=5)[0]# 上位5個を取得
    list_all = []
    count = 0
    rel = 0
    ## 結果の表示
    for result in results:
        temp = []
        text = str(result[1]).split("_")
        tr = ""
        for st in text:
            tr += str(st)+" "
        trans = translator.translate(tr,dest="ja")
        maker.image_pk = primary
        maker.en = tr
        maker.jp = trans.text
        maker.tie = round(result[2]*100,2)
        maker.model = request_model
        maker.save()
        rel += result[2]*100
        if(rel > 99):
            break

def judge_all(primary):
  model = ImageModel.objects.get(pk=primary)
  request_model = model.learn_model##使用するモデルのpk
  for request_model in range(1,len(models)):
      # PILのimageで読み込み modelのデフォルト値が224*224のためリサイズして読み込む
      model_name,size = get_model(request_model)
      print("NOW MODEL : "+str(models[request_model]))
      if(model_name == None):
          print("error")
      img = image.load_img(model.images,target_size=(size,size))
      # PILの場合 画像として読み込まれるため、配列に変換、画像としてはRGBで読み込まれる
      # CV2の場合 配列として読み込まれるがBGRで読み込まれる
      # PLTの場合 配列として読み込まれ、RGBで読み込まれる
      x = image.img_to_array(img)
      # 3次元（rows,cols,channels）から
      # 4次元（samples,rows,cols,channels）に変換
      # axisは追加位置
      x = np.expand_dims(x,axis=0)
      # モデルの予測
      preds = model_name.predict(preprocess_input(x))
      results = decode_predictions(preds, top=5)[0]# 上位5個を取得
      rel = 0
      ## 結果の表示
      for result in results:
          maker = LearningModel()
          # temp = []
          text = str(result[1]).split("_")
          tr = ""
          for st in text:
              tr += str(st)+" "
          trans = translator.translate(tr,dest="ja")
          maker.image_pk = primary
          maker.en = tr
          maker.jp = trans.text
          maker.tie = round(result[2]*100,2)
          maker.model = request_model
          maker.save()
          rel += result[2]*100
          if(rel > 99):
              break
      print("End Model")
