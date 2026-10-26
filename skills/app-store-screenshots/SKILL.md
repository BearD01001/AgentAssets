---
name: app-store-screenshots
description: Design and export App Store marketing screenshots from real app captures and verified product information, including localized copy, layered compositions, device-size variants, and optional App Store Connect upload verification. Use for store screenshot artwork rather than general release management or ordinary UI screenshot testing.
---

# App Store Screenshots

把真实 App 界面做成能说明产品价值的上架图片。先读 [制作说明](references/production-guide.zh-CN.md)，它也可单独提供给用户或其他 AI。用 [制作简报](assets/brief-template.yaml) 记录当前产品的要求，填好的副本放在产品工作区。

## 制作决策

1. 阅读用户指定的产品网站、当前版本功能和现有截图。建立“卖点 → 已核实依据 → 截图 → 构图 → 文案”对应关系。无法访问资料时明确说明；不要用旧宣传页覆盖新增功能，也不要把尚未证实的能力写成承诺。
2. 优先使用用户挑选的真实截图；仅在需要补齐界面且已获授权时操作模拟器。演示数据要有自然差异，避免每类同样条数、完全一致的标题长度与重复封面。按实际画面识别素材，不依赖文件名推断页面。
3. 提炼与 App 主题一致的视觉方向。浅色科技感是一种可选配方，见说明文档第 4 节；沿用用户已批准的风格时，不重新探索无关风格。
4. 让构图解释功能：同一界面状态用对齐蒙版对比，库与详情用局部叠层，导出操作与结果用双画面，宽屏适配用实际宽屏界面。保持截图真实且主要内容清晰。
5. 用户希望先定稿再多语言时，先完成首个语言的代表页与整组预览。语言扩展时保留已批准风格，重排标题、行距和副文案；区分营销文案语言与 App 界面语言。
6. 从当前 Apple 要求与目标栏位确认尺寸。尺寸或比例变化时优先重新排版或等比缩放并重定位，避免拉伸截图。导出最终 PNG、整组预览、可编辑源和素材/文案清单。

## 验收与交付

逐张检查原尺寸与缩略预览：关键文案可读、无溢出、截图比例正确、裁切不误导、光晕/轨道/颗粒在最终导出中实际可见。保留确定性生成参数，避免修一个语言改变全组粒子布局。

可用结构检查工具核对上传目录（不替代视觉验收）：

```sh
python3 scripts/validate_exports.py \
  /path/to/product/final/en-US/iphone-WxH \
  --size 1206x2622 --count 6 \
  --manifest /path/to/product/final/en-US/iphone-WxH-manifest.json
```

上例尺寸只是用法示例，替换为当前确认的目标尺寸。脚本仅检查 PNG 结构、尺寸、透明通道和散列，不能证明 ICC 色彩正确、像素可解码或视觉质量合格。

## 可选上传

用户要求上传时，读取制作说明第 8 节。确认目标 App、版本、语言、设备栏位和文件顺序；延续已有授权，不重复索取同一授权。只操作已授权的截图范围。上传本身不包含修改构建、文字元数据、发布设置或提交审核。

成功标准是每个栏位每张图都显示实际预览、顺序正确，且保存后通过刷新或切换语言仍可读回；只有资产数量或云朵占位不算完成。占位持续时按说明进行有限重试，并保留已完成部分和可恢复路径。

最终区分本地导出、已上传、已完成处理/验证、待处理四种状态，并提供最终文件和实际页面凭证。项目专属素材、账号、产品标识及上传状态保存在产品工作区，不写入共享 skill。
