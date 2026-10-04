# PromptBlocks Chrome Extension

在 ChatGPT / Claude / Gemini 等AI对话页面直接插入 PromptBlocks 积木拼装的 Prompt。

## 安装

1. 下载 `chrome-extension` 文件夹
2. 打开 Chrome，访问 `chrome://extensions/`
3. 开启右上角"开发者模式"
4. 点击"加载已解压的扩展程序"
5. 选择 `chrome-extension` 文件夹
6. 扩展图标出现在工具栏，访问任何AI对话页面即可使用

## 支持平台

- ChatGPT (chatgpt.com)
- Claude (claude.ai)
- Gemini (gemini.google.com)
- 阶跃星辰 (platform.stepfun.com)
- DeepSeek (chat.deepseek.com)
- 文心一言 (yiyan.baidu.com)
- 通义千问 (tongyi.aliyun.com)

## 使用

1. 点击工具栏的 PromptBlocks 图标
2. 搜索或按分类选择积木
3. 拼装区会实时生成 Prompt
4. 点"插入到页面"直接填入AI对话输入框，或点"复制"手动粘贴

## 数据

积木数据从 blocks.json 自动生成，72+积木，8大分类。重新生成：

```bash
python gen_ext_data.py
```
