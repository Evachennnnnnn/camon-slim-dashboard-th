import re

# 读取文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 替换Google Trends链接中的PH为TH
content = content.replace('geo=PH', 'geo=TH')

# 2. 替换产品名称
content = content.replace('CAMON Slim 5G', 'CAMON Slim')
content = content.replace('HONOR 600S', 'OPPO Reno 16 F')
content = content.replace('vivo V80 Lite', 'VIVO V80 Lite')
content = content.replace('REDMI Note 17 Pro', 'Redmi Note 17 Pro')

# 3. 替换菲律宾KOL名字为待更新
ph_kols = ['Ychan Laurenz', 'Luis Angeles', 'TechBroll', 'Poknat', 'eyjay.jimenez']
for kol in ph_kols:
    content = content.replace(kol, '待更新')

# 4. 替换菲律宾视频名字
ph_videos = ['TVC', 'EMOTIONAL VIDEO 1', 'MEDIA REMIX', 'MagBadge Functions', 'Teaser-HQ ID Video']
for video in ph_videos:
    content = content.replace(video, '待更新')

# 5. 替换所有菲律宾相关的数据值
# 查找D对象并替换所有菲律宾数据
pattern = r'const D = \{[\s\S]*?\n\};'
match = re.search(pattern, content)

if match:
    old_d = match.group(0)
    
    # 替换所有菲律宾数据为泰国数据
    new_d = old_d
    # 替换所有菲律宾数值
    new_d = new_d.replace('21.13%', '待更新')
    new_d = new_d.replace('15.81%', '待更新')
    new_d = new_d.replace('13.06%', '待更新')
    new_d = new_d.replace('10.93%', '待更新')
    new_d = new_d.replace('432.73M', '待更新')
    new_d = new_d.replace('246.74M', '待更新')
    new_d = new_d.replace('10.16M', '待更新')
    new_d = new_d.replace('679.47M', '待更新')
    new_d = new_d.replace('35.86M', '待更新')
    new_d = new_d.replace('3.17M', '待更新')
    new_d = new_d.replace('59.99%', '待更新')
    new_d = new_d.replace('61.82%', '待更新')
    
    # 替换菲律宾KOL数据
    new_d = new_d.replace('"value":"8.2M"', '"value":"待更新"')
    new_d = new_d.replace('"value":"5.9M"', '"value":"待更新"')
    new_d = new_d.replace('"value":"5.8M"', '"value":"待更新"')
    new_d = new_d.replace('"value":"5.7M"', '"value":"待更新"')
    new_d = new_d.replace('"value":"4.6M"', '"value":"待更新"')
    new_d = new_d.replace('"value":"22.6M"', '"value":"待更新"')
    new_d = new_d.replace('"value":"18.7M"', '"value":"待更新"')
    new_d = new_d.replace('"value":"12.7M"', '"value":"待更新"')
    new_d = new_d.replace('"value":"11.8M"', '"value":"待更新"')
    new_d = new_d.replace('"value":"8.8M"', '"value":"待更新"')
    
    # 替换菲律宾受众数据
    new_d = new_d.replace('"cost":"5,127.93"', '"cost":"待更新"')
    new_d = new_d.replace('"cpm":"0.27"', '"cpm":"待更新"')
    new_d = new_d.replace('"cpe":"0.08"', '"cpe":"待更新"')
    new_d = new_d.replace('"vtr":"95.1%"', '"vtr":"待更新"')
    
    # 替换所有菲律宾日期
    new_d = new_d.replace('"10/18"', '"待更新"')
    new_d = new_d.replace('"10/16"', '"待更新"')
    new_d = new_d.replace('"10/13"', '"待更新"')
    
    content = content.replace(old_d, new_d)

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("All PH data cleaned!")
