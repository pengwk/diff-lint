# diff-lint

只输出每次提交的 lint 信息

## 为什么要？

当单个文件代码量很大时，直接使用 pylint 会出现很多无关本次提交的信息，严重影响了体验。

## 希望支持的功能

- [ ] 支持 Mercurial pre-commit hook
- [ ] 支持 Git pre-commit hook
- [ ] 能在 macOS 上运行
- [ ] 能在 Linux 上运行
- [ ] 能在 Windows 上运行
- [ ] 能在命令行里直接使用，如：`$ diff-lint`
- [ ] 高亮错误，不同级别的信息颜色不同
- [ ] CodeStyle 问题可以给出修正意见
- [ ] 对于不必要的警告，提示增加何种注释可以消除
- [ ] 支持通过 pip 安装
