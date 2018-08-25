# 设计文档

记录使用到的库，算法。方便沟通协作，后续维护。

## 总体思路

使用 Git 或 Mercurial 这类源代码管理工具时，可以通过运行 `git diff` 或者  `hg diff` 获取本次提交涉及的改动。

通过获取本次提交的改动，然后提取 diff 的信息，用于得到本次提交会涉及到哪些文件，文件改动的行数。

## diff 格式

![diff by example](./diff.jpg)

- [阮一峰：读懂 diff](http://www.ruanyifeng.com/blog/2012/08/how_to_read_diff.html)

## 获取本次提交的 diff

### Mercurial

```python
import hglib

hglib.open('.')
hglib.diff() 返回字符串
```

<https://www.mercurial-scm.org/wiki/PythonHglib>

`pip install python-hglib`

### Git

<https://github.com/gitpython-developers/GitPython>

## 从 diff 中提取相关信息

```python
import unidiff

diff_str = ''

patchs = unidiff.PatchSet(diff_str)
for patch in patchs:
    pass
```

<https://github.com/matiasb/python-unidiff>

### Python 源代码文件

```python
modified_files = [file.path for file in patchs.modified_files
                    if file.path.endwith('.py')]
added_files = [file.path for file in patchs.added_files
                    if file.path.endwith('.py')]
```

### 文件改动的行数

```python
for patch in patchs:
    for hunk in patch:
        end = hunk.target_start + hunk.target_length
        file_range.append(
            list(range(hunk.target_start, hunk.target_length)))
```

## 在 Python 中运行 pylint

```python
from pylint import epylint as lint

(pylint_stdout, pylint_stderr) = lint.py_run('models.py --output-format=json', return_std=True)
```

```python
pylint_stdout = [
 {u'column': 0,
  u'line': 24,
  u'message': u'standard import "import uuid" should be placed before "import chardet"',
  u'message-id': u'C0411',
  u'module': u'hydrogen.models',
  u'obj': u'',
  u'path': u'hydrogen/models.py',
  u'symbol': u'wrong-import-order',
  u'type': u'convention'}]
```

<https://pylint.readthedocs.io/en/latest/>

## 输出改动部分的检查结果

检查每条信息的行数，是都否在本次修改之列，是则输出。

## 测试

记录单元测试的思路。

## 相似的项目

<https://pypi.org/project/git-lint/>