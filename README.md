# hass-伯虎空气检测仪插件

## 配置


### 检测仪配置
设置伯虎空气检测仪的 idx 对应值 如下:

| 传感器  | idx 值 | 
| ------ |:---:|
| PM1     | 1 | 
| PM2.5   | 2 | 
| PM10    | 3 |
| HOCO    | 4 |
| CO2     | 5 |
| T-H     | 6 |


### Mac OS

  * 添加 airmonitor.py 文件
    > 路径: /Users/用户名/.homeassistant/custom_components/senser
    
    > “custom_components/senser” 如果不存在请自行创建

  * 添加配置
    文件默认路径: 
    > /Users/用户名/.homeassistant/configuration.yaml

	添加以下代码：
	
      	sensor:
          - platform: airmonitor

 重启 hass

