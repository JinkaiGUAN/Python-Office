## 结构预览

```shell
-- 4-vgtime
	-- data # 存放全部游戏封面和游戏详情信息
		-- Images 
		-- final_details.csv 
		-- first_game_info.csv 

	-- docs # 需求文档
	-- input_files # 存放需要的初始excel和csv文件
		-- A1_主播表.xlsx
		-- NewGameList.csv #所有游戏中文名称 用来进行搜索爬虫
		-- final_details  # 为上述data文件夹中的拷贝文件
		-- 新用户名表.xlsx
	-- log # log文件夹， 按照运行程序的日期建立相应log文件夹
	-- output_files # 输出文档
		-- A1_主播表.csv
		-- new_details.csv # 将原来的final_details.csv文件中的日期进行更改调整
	-- src # 存放所有代码文件
		-- step1_vgtime_parse_2.py # 爬取数据
		-- step2_change_anchor_name.py # 更改主播表中的用户名
		-- step3_search_stream.py # 将平台数据写入到主播表
	-- gamelist20210830.xlsx # 将此文件保存成csv放入input_files文件夹中。
```



## 运行步骤

### 爬取游戏信息

1. 将gamelist20210830.xlsx保存成`NewGameList.csv`文件放入input_files文件夹。

2. 将`step1_vgtime_parse_2.py`中`main_process`函数内的`offsets`设置成相应的数字：

    	- 比如我们有89个游戏要爬取， 分为四份， 可以设置为0， 25， 50， 75
    	- 那么`offsets = [0, 25, 50, 75]`

3. 运行`step1_vgtime_parse_2.py`文件即可。

    ![image-20210904150301748](D:\TyporaImages\image-20210904150301748.png)





### 替换主播表中`userId`

1. 将主播表与新用户名表存放在`input_files`文件夹中.
2. 在`step2_change_anchor_name.py`文件中， 下图位置的`anchor_file_names`将上述文件夹中需要的**全部主播表**的文件名写入.
3. 如果新用户名表名称未变， 在下图代码红色框中则不需要改变。
4. 运行该程序即可。



![image-20210904150741331](D:\TyporaImages\image-20210904150741331.png)





### 将平台写入主播表

1. 更改需要写入的主播表名称写入下方途中的红色方框。

![image-20210904151249444](D:\TyporaImages\image-20210904151249444.png)

