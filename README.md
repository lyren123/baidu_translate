# baidu_translate
Cracking Baidu Translation Interface

百度翻译接口参数破解，执行baidu_translate.py即可

百度翻译接口地址"https://fanyi.baidu.com/v2transapi"

其中token字段可以从百度翻译首页"https://fanyi.baidu.com/"获取,(注意点：若首次未携带cookie值访问的首页获取的token字段无效,第二次访问百度翻译首页中的token字段才有用)

sign加密字段由js动态生成，复制百度js加密字段部分代码到本地，保存为baidu.js文件在本地生成sign字段
通过语言检测接口,获得翻译的类型 "https://fanyi.baidu.com/langdetect"
