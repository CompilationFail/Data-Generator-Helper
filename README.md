# Data-Generator-Helper

## 数据格式化工具

主要面向若干常见的开源 OJ 。

### syzoj formatter

用以生成 [syzoj](https://github.com/syzoj/syzoj) 所需要的 `data.yml` 文件。

您需要给每一个 subtask 建立一个文件夹，将 `python` 代码或者打包的可执行文件放到同一个目录下运行。

代码在执行时会扫描当前目录下的所有文件夹（不包括当前目录下的文件！），

将每一个文件夹视作一个子任务，对于每一个文件夹内的文件尝试匹配。

现有的功能：

1. 设置子任务分数和分数计算方式。
2. 设置输入输出文件后缀（`.in; .out/.ans`）。
3. 设置简易的 `Special Judge`。

### hydrooj formatter

用以生成 [hydrooj](https://github.com/hydro-dev/Hydro) 所需要的 `config.yaml` 文件。

在初始界面可以设置题目的 时空限制 以及 文件输入（输入文件名，留空表示没有文件输入输出）。

如果选择 `nosubtask` ，则会自行对于当前目录下的文件进行配对，然后尽可能平均地分配每一个子任务的分数。

如果选择 `subtask` ，则会按照文件夹分配子任务，配置方式类似 syzoj formatter。

默认的语言选项（可以提交的语言）有 `cpp17o2,cpp11o2,cpp14o2` 。

需要注意的是，sum 选项的意义是：这个子任务每通过一个点获得您所配置的得分（而不是自动均分）。

<br>

<br>

不太会写，几乎没有做异常处理，可能出现很多问题。

