## 主流直播平台炉石视频整合

作为一个炉石爱好者, 每次看直播的时候总是各个平台跳来跳去, 特别爽, 于是想着自己写一个直播聚合的网站, 满足自己皇帝选妃的心态.

演示地址: http://tv.lecher.tech:8080

## 配置
配置文件在: conf/tv.json 中, 大部分的配置项看名字就知道了.

### 路径规则
对HTML页面的解析使用的是BeautifulSoup, 因此定义了一套自己的简易路径. 使用"."来分割路径.

- (tag_name, attribute), 这个规则表示找到标签为tag_name, 且有一个属性的值为attribute的节点
- tag_name, 直接找标签为tag_name的节点, 不进行属性过滤
- \[attr_name\], 获取前一个匹配到的节点的属性名为attr_name的属性值, 只能用于最后一节
- text, 获取节点的文本值，只能用于最后一节

示例: 路径(div, video-cover).img.\[data-original\]的匹配过程:

1. 找到标签为div, 属性值包含video-cover的第一个节点 nodeA
2. 在nodeA中找到第一个标签为img的节点 nodeB
3. 获取nodeB中属性名为data-original的属性值

### 几个特殊配置项说明
items_path: 用来获取主播列表的路径, 这个路径将获取所有符合的匹配节点
info_path: 单个主播的路径配置, info_path中的路径匹配都是单个匹配，只会拿取匹配到的第一项
min_hot: 能够显示主播热度的阈值

## 服务器启动命令
- 最简单的启动方式: ```python -m src.main```, 监听9999端口
- 指定端口: ```python -m src.main --port=PORT```

默认日志输出在错误输出流中

