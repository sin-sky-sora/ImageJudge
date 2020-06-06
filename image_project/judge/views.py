import numpy as np
from django.shortcuts import render
from .models import ImageModel
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.applications.vgg19 import VGG19
from keras.applications.resnet50 import ResNet50
from googletrans import Translator
from django.urls import reverse_lazy
from fjango.views.generic import CreateView

translator = Translator()

class create(CreateView):
    template_name = "create.html"
    model = ImageModel
    fields = '__all__'
    success_url = reverse_lazy()##判定ページへ飛ばす

def judgefunc(request):
    # response = HttpResponse("judge")
    # response.delete_cookie('user')
    # try:
    #     user = request.COOKIES.get('user')
    # except:
    #     set_uuid = uuid.uuid4()

    #     response.set_cookie('user', set_uuid,60*60*24)
    #     print(set_uuid)
    #     print("UUIDを作ったよ")
    # else:
    #     print("COOKIEをゲット")
    #     print(request.COOKIES.get('user'))
    if request.method == "POST":
        model = ImageModel()
        model.images = request.FILES['images']#htmlでの名前
        model.save()
        image,list_all = judge(request,model.pk)
        return render(request, "judge.html", {"img":image,"data":list_all})
    return render(request,"index.html")

# MODE : caffe
# INPUTSIZE : 224*224
model_vgg16 = VGG16(weights="imagenet",include_top=True)
model_vgg19 = VGG19(weights="imagenet",include_top=True)
model_resnet = ResNet50(weights="imagenet",include_top=True)

def getmodel(num):
    if(num == 1):
        return model_vgg16
    elif(num == 2):
        return model_vgg19
    elif(num == 3):
        return model_resnet
    else:
        return None


def judge(request,primary):
    getmodel = ImageModel.objects.get(pk=primary)
    request_model = getmodel.learn_model##使用するモデルのpk
    # PILのimageで読み込み modelのデフォルト値が224*224のためリサイズして読み込む
    img = image.load_img(getmodel.images,target_size=(224,224))
    # PILの場合 画像として読み込まれるため、配列に変換、画像としてはRGBで読み込まれる
    # CV2の場合 配列として読み込まれるがBGRで読み込まれる
    # PLTの場合 配列として読み込まれ、RGBで読み込まれる
    x = image.img_to_array(img)
    # 3次元（rows,cols,channels）から
    # 4次元（samples,rows,cols,channels）に変換
    # axisは追加位置
    x = np.expand_dims(x,axis=0)
    model_name = getmodel(request_model)
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
    return getter.images , list_all
