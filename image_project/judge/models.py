from django.db import models

# Create your models here.
LearnChoise = ((1,"VGG16"),(2,"VGG19"),(3,"ResNet50"),(4,"Xception"),(5,"InceptionV3"),(6,"InceptionResNetV2"),(7,"MobileNet"),(8,"DenseNet121"),(9,"DenseNet169"),(10,"DenseNet201"),(11,"NASNetLarge"),(12,"NASNetMobile"),(13,"MobileNetV2"))
class ImageModel(models.Model):
    images = models.ImageField(upload_to='images',null=True, blank=True)
    ##画像のアップロード場所
    user = models.UUIDField()
    ##ユーザー識別用のUUID      COOKIEに保存
    release = models.BooleanField(default=False)
    ##公開or非公開
    learning = models.BooleanField(default=False)
    ##学習に協力するか否か
    answer = models.CharField(max_length=255,null=True,blank=True)
    ##答え（学習に協力する場合入力を求める）
    title = models.CharField(max_length=255)
    ##表示するタイトル
    learn_model = models.IntegerField()
    ##使用するモデルの選択

class LearningModel(models.Model):
    image_pk = models.IntegerField()
    ##画像のpkと結びつけ
    en = models.CharField(max_length=255)
    ##英語
    jp = models.CharField(max_length=255)
    ##日本語訳
    tie = models.FloatField()
    ##確率
