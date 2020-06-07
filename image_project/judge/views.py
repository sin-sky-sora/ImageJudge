import numpy as np
from django.shortcuts import render
from .models import ImageModel
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.applications.vgg19 import VGG19
from keras.applications.resnet50 import ResNet50
from googletrans import Translator
from django.urls import reverse_lazy

translator = Translator()

def inputfunc(request):
    return render(request,"create.html")

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
        image,list_all = judge(request,model.pk)
        return render(request, "judge.html", {"img":image,"data":list_all})
    return render(request,"index.html")

# MODE : caffe
# INPUTSIZE : 224*224
model_vgg16 = VGG16(weights="imagenet",include_top=True)
model_vgg19 = VGG19(weights="imagenet",include_top=True)
model_resnet = ResNet50(weights="imagenet",include_top=True)
# from keras.applications.xception import Xception
# model_xception = Xception(weight="imagenet",include_top=True)
# from keras.applications.inception_v3 import InceptionV3
# model_inceptionv3 = InceptionV3(include_top=True, weights='imagenet')
# from keras.applications.inception_resnet_v2 import InceptionResNetV2
# model_inceptionresnet = InceptionResNetV2(include_top=True, weights='imagenet')

#  caffe  : VGG16 VGG19 ResNet50
# tf1 299 : Xception InceptionV3 InceptionResNetV2
# tf2 224 : MobileNet NASNet MobileNetV2
#  torch  : DenseNet
### NASNet --> 331*331 もあり
# model_size = {"caffe":224,"tf1":299,"tf2":224,"torch":224}

def get_model(num):
    if(num == 1):
        return model_vgg16,224
    elif(num == 2):
        return model_vgg19,224
    elif(num == 3):
        return model_resnet,224
    else:
        return None


def judge(request,primary):
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
        # print("翻訳前："+tr)
        # print("翻訳後："+trans.text)
        # print("{:.01f}%".format(result[2]*100))
        temp.append(tr)             #en
        temp.append(trans.text)     #ja
        temp.append("{:.01f}%".format(result[2]*100))
        list_all.insert(count,temp)
        count+=1
        rel += result[2]*100
        if(rel > 95):
            break
    # print(list_all)
    return model.images , list_all
