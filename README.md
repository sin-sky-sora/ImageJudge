# imageJudge

### 始める前に
>モデルの作成
>
>`python manage.py makemigrations`
>
>`python manage.py migrate`
>
>管理者アカウントの作成
>
>`python manage.py createsuperuser`
>
>

### 実行環境
> keras == 2.3.1
>
>tensorflow == 2.2.0
>
>Django == 3.0.7
>

### runserverについて
>`python manage.py runserver --nothreading --neload`
>で実行
>
>`python manage.py runserver`だと
>
>AttributeError: '_thread._local' object has no attribute 'value'
>
>これが解決できなかった...
