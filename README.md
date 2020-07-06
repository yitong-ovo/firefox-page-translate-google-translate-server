# firefox-page-translate-google-translate-server
使用免费公开的 google translate 服务在 firefox 中进行页面翻译。
<del>你觉得我会写个认真的 Readme 吗?</del>

# Why？
我上个月[配置](https://blog.groverchou.com/2020/04/09/%E5%90%AF%E7%94%A8-Firefox-%E5%86%85%E7%BD%AE%E5%85%A8%E9%A1%B5%E9%9D%A2%E7%BF%BB%E8%AF%91%E5%8A%9F%E8%83%BD/)好了使用 google translate api 的 firefox，用的很舒服，直到...

收到了 Google Cloud 的账单。

用了大概半个月，翻译的数量是 500w 字符，大概是 $101，持续这样的话有些成受不住。

找了找有不少可以使用 translate.google.com 的库，那就试着做个假的 api，然后去 FireFox 里换一下 URL 就可以了。

# HowTo?
FireFox(78.0.1,MacOS)
去 `/Applications/Firefox.app/Contents/Resources/browser/` 找到 `omni.ja` 文件，自己备份一下。

然后去终端里，建一个临时文件夹，我这里的是 `omni`，去临时文件夹里解压。
```bash
unzip ../omni.ja.bak-77.0.1
```
编辑 `modules/translation/GoogleTranslator.jsm`
```javascript
// 找到并注释掉第 32 行:
const URL = "https://translation.googleapis.com/language/translate/v2";
// 然后在下面加一行:
const URL = Services.prefs.getStringPref("browser.translation.google.apiURL", "");
```
然后就可以打包 `omni.ja` 了。
```
rm ../omni.ja ;zip -qr0XD ../omni.ja *;
```
配置 FireFox 的话，可以参考[这个](https://blog.groverchou.com/2020/04/09/%E5%90%AF%E7%94%A8-Firefox-%E5%86%85%E7%BD%AE%E5%85%A8%E9%A1%B5%E9%9D%A2%E7%BF%BB%E8%AF%91%E5%8A%9F%E8%83%BD/)文章进行配置，key 的话可以随意写。

然后记得添加 `browser.translation.google.apiURL` 字符串，设置为你的 API 的地址，例如 `http://localhost:5000/api/translate`。

# 不准确的对比

- google translate api 
  - 大概 2-4s 
  - 更少翻译请求(分块)出错
- 本项目(?)，跑在 Cloud Run 上
  - 大概 5-10s，在接受范围内。 
  - 有时候会有一块分块超时之类的原因失败

