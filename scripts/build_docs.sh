#!/bin/bash
###
 # @Author: Arthur arthur@lwork.com
 # @Date: 2024-11-14 18:51:14
 # @LastEditors: Arthur arthur@lwork.com
 # @LastEditTime: 2024-11-14 20:20:08
 # @FilePath: /ChatMe/scripts/build_docs.sh
 # @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
### 

# 文档构建脚本
# 用于生成项目文档

# 设置错误时退出
set -e

# 显示信息
echo "=== 构建AI语音助手文档 ==="

# 检查sphinx是否安装
if ! command -v sphinx-build &> /dev/null; then
    echo "安装文档生成依赖..."
    pip install -e .[docs]
fi

# 清理之前的构建
echo "清理之前的构建..."
rm -rf docs/_build/

# 创建API文档
echo "生成API文档..."
sphinx-apidoc -f -o docs/api/ chatMe/

# 构建HTML文档
echo "构建HTML文档..."
cd docs
make html
cd ..

# 构建PDF文档（如果安装了latex）
if command -v pdflatex &> /dev/null; then
    echo "构建PDF文档..."
    cd docs
    make latexpdf
    cd ..
fi

# 检查文档质量
echo "检查文档质量..."
sphinx-build -W -b linkcheck docs/ docs/_build/linkcheck/

# 运行文档测试
echo "运行文档测试..."
sphinx-build -b doctest docs/ docs/_build/doctest/

# 显示结果
echo "=== 文档构建完成 ==="
echo "HTML文档位置: docs/_build/html/index.html"
if [ -f "docs/_build/latex/aivocieassistant.pdf" ]; then
    echo "PDF文档位置: docs/_build/latex/aivocieassistant.pdf"
fi

# 启动本地文档服务器（如果指定）
if [ "$1" == "--serve" ]; then
    echo "启动文档服务器..."
    python -m http.server 8000 --directory docs/_build/html/
fi

# 部署到GitHub Pages（如果指定）
if [ "$1" == "--deploy" ]; then
    echo "部署到GitHub Pages..."
    git checkout gh-pages
    cp -r docs/_build/html/* .
    git add .
    git commit -m "Update documentation"
    git push origin gh-pages
    git checkout main
fi