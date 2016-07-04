在python 的 virtualenv下，无法使用pip进行安装。

就需要下载：

`wget http://effbot.org/downloads/Imaging-1.1.7.tar.gz`。

并使用`python setup.py build`及`python setup.py install`加以安装。

但是，pip 中PIL是叫做Pillow的，因此只需：

`pip install Pillow`
