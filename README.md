# Gomoku-ai
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-green)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

&gt; 基于 Pygame 的五子棋人机对战游戏，AI 采用 **Minimax + Alpha-Beta 剪枝** 算法，具备即时杀棋识别与启发式局面评估能力。

---

## 功能特性

- [x] 可视化 15×15 标准五子棋棋盘
- [x] 人机对战（玩家执黑先行，AI 执白后手）
- [x] 实时胜负判定与平局检测
- [x] AI 智能分层决策：
  - **L1 规则层**：即时响应必胜/必败点
  - **L2 搜索层**：Minimax 博弈树搜索 + Alpha-Beta 剪枝
  - **L3 评估层**：连子形状评分 + 棋盘位置偏好
- [x] 最后落子标记、悬停预览、步数统计
- [x] 侧边栏 UI 与重新开始功能

---

## 安装与运行

### 环境要求
- Python 3.7+
- Pygame

### 快速开始

```bash
# 克隆仓库
git clone https://github.com/yourusername/gomoku-ai.git
cd gomoku-ai

# 安装依赖
pip install pygame

# 启动游戏
python gomoku.py
