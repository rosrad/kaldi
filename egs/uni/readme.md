<!-- Read me for DNN based Direction Of Arrival (DOA) -->

本说明文档是用于说明基于DNN的声源定位

# 整体调用流程
    1. 训练数据准备及DNN训练
    ./init_dnn.py, 格式如下:
    ./init_dnn.py --tag [tagname] training_corpus_dirname
    这里 training_corpus_dirname 是相对脚本内部的 simu_root 目录，
    可根据个人需求修改脚本适配数据目录。

    2. 测试及egs收集 [./doa.py]
    脚本功能
        1. 数据准备[if need]
        2. 对测试集DNN解码
        3. 错误率统计
        4. 错误语音样本提取。
    
    格式如下:
    ./doa.py -[opt] DNN_DIR TAG[测试集]

    DNN_DIR 是指 之前生成的模型目录
    TAG 是指 测试训练集的 TAG 类型[一般最好对应于DNN的TAG]
    --eval-only 是否只进行错误率统计[之前必须依据进行过解码。]

# 内部详解
    1.数据准备
    2.模型训练
    3.测试数据集解码

## 数据格式
    - table文件
      对于kaldi的io操作，有一套比较统一的文件存储格式。
      table 文件存储，文件格式 如下
  
    - key [whitespace] content
      key     :  标记id
      content :  具体对应的文件内容或者读取方式[pipeline]。


## 数据准备
    由于目前的模型训练及解码完全是基于kaldi的框架进行的，
    所以我们需要以kaldi的数据处理方式进行数据准备.
    数据准备的table 文件一般存储于[./data/]的对应文件下，
    例如 train数据 存储于[./data/cmn_gcc/simu/reverb/t60_0.3].

    在数据特征提取时候，一般我们需要准备
    以下几个文件

    - 音频文件table[wav.scp]

    wav.scp 文件用于说明 音频文件的读取方式[最后输出为wav格式].
    一般形式如下：

    - 短语音
    <语段ID> <语音文件路径>
    - 格式转换[pcm -> wav]
    <语段ID> <语音文件的格式转换>
    [例如我们当前的pcm文件，需要使用管道转换为wav的pipeline]

    - 长语音
    <语音ID> <语音文件路径>
    由于长语音中并不是所有的部分都是我们需要的，也就是需要使用
    vad的label进行切分语段形成段语音。我们需要生产segment
    文件来进行指明如何切分。
    
    - 语段文件[segment]
    格式如下:
    <语段ID> <语音id> <开始时间> <结尾时间>

    <语音ID> 就是wav.scp 文件中指定文件的。
    <语段ID> 用来指定 语段的标识
    

    以上内容就足以完成特征提取的内容。
    但是由于我们需要给没给 <语段> 指定对应的 语音角度[DOA]
    我们这里使用 utt2doa来表明 对应信息

    - DOA信息 [utt2doa]

    格式:
    <语段ID> <角度[0-359]>

    - 说话人信息 [utt2spk及spk2utt]

    由于kaldi系统在使用过程中，多个地方依赖这2个文件。
    我们对两个文件进行伪造。
    使用 utt2doa 来 指定 utt2spk.
    而 spk2utt 则可以根据 utt2spk 来生产。
  
  ### 代码 [./local/data_prepare.py]
  目前[data_prepare.py] 会根据指定的音频文件夹和对于的后缀进行扫描
  并且根据文件的音频[.pcm 或者 .wav]及label文件[.txt]，
  来生产对应的数据文件[wav.scp ,segment, utt2doa, utt2spk, spk2utt]。
  - 使用方法
    ./local/data_prepare.py --ext=wav[语音后缀] 音频文件夹[in] 数据保存路径[out]
  此脚本用于训练数据集及测试数据集的准备。
    
## 模型训练
    - 数据准备
    主要是准备用于训练 DNN 的训练数据集,使用[./local/data_prepare.py].
    在此之后一般还需要将训练集拆分为 训练集[tr90] 和 交叉验证集[cv10].
    使用[./local/randsub_tr_cv.sh]进行拆分。
    
    - 训练
    使用[./local/train_doa.sh] 进行基于DOA 预测的DNN 训练。 
    使用格式如下:
    ./local/train_doa.sh $train_data $DNN_DIR
    1. train_data 指明 训练数据集
    2. $DNN_DIR 指明 输出的DNN模型目录

    

## 测试集解码
    - 准备
      类似于模型训练，测试集在进行解码之前也是需要数据准备。同样使用[./local/data_prepare.py]
      进行数据的基本格式准备和特征抽取。
    - 解码
      对应于上述DNN模型的解码，使用[./local/decode_doa.sh]. 格式如下:
      ./local/decode_doa.sh $DNN_DIR $eval_data
      1. $DNN_DIR 是指之前生成的模型目录
      2. $eval_data 指明 需要进行解码的数据目录[由数据准备阶段生成]
      

