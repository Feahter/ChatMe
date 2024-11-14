#!/bin/bash
###
 # @Author: Arthur arthur@lwork.com
 # @Date: 2024-11-14 18:50:48
 # @LastEditors: Arthur arthur@lwork.com
 # @LastEditTime: 2024-11-14 20:20:15
 # @FilePath: /ChatMe/scripts/run_tests.sh
 # @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
### 

# 测试运行脚本
# 用于运行所有测试并生成覆盖率报告

# 设置错误时退出
set -e

# 显示信息
echo "=== 运行AI语音助手测试 ==="

# 检查虚拟环境
if [ -z "$VIRTUAL_ENV" ]; then
    echo "警告: 未检测到虚拟环境，建议在虚拟环境中运行测试"
    read -p "是否继续？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 安装测试依赖
echo "确保测试依赖已安装..."
pip install -e .[test]

# 清理之前的测试结果
echo "清理之前的测试结果..."
rm -rf htmlcov/
rm -f .coverage
rm -f coverage.xml

# 运行测试
echo "运行测试..."
pytest \
    --verbose \
    --cov=chatMe \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-report=xml \
    tests/

# 运行类型检查
echo "运行类型检查..."
mypy chatMe/

# 运行代码风格检查
echo "运行代码风格检查..."
flake8 chatMe/
black --check chatMe/

# 显示测试覆盖率报告
echo "=== 测试覆盖率报告 ==="
coverage report

# 生成HTML报告
echo "HTML覆盖率报告已生成在 htmlcov/index.html"

# 检查测试覆盖率是否达标
coverage_threshold=80
current_coverage=$(coverage report | grep TOTAL | awk '{print $4}' | sed 's/%//')

if (( $(echo "$current_coverage < $coverage_threshold" | bc -l) )); then
    echo "警告: 测试覆盖率($current_coverage%)低于目标阈值($coverage_threshold%)"
    exit 1
fi

echo "=== 测试完成 ==="