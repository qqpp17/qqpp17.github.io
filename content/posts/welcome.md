---
title: "欢迎来到我的博客"
date: 2026-08-12T14:00:00+08:00
draft: false
description: "这是潘华珍的个人学习博客的第一篇文章。"
tags:
  - 随笔
---

你好！这是使用 **Hugo + PaperMod** 搭建的个人博客。

在这里我会记录学习笔记、技术分享和一些日常思考。

## 如何写新文章

在 `content/posts/` 目录下新建一个 `.md` 文件，正文用下面的格式开头即可：

```markdown
---
title: "文章标题"
date: 2026-08-12T14:00:00+08:00
draft: false
---

正文内容……
```

写完后在本地运行 `hugo server` 预览，确认无误后 `git push` 即可自动部署到 GitHub Pages。
