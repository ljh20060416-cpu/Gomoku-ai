# Gomoku-ai
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-green)](https://www.pygame.org/)

一个使用 Pygame 实现的五子棋人机对战游戏，采用基于 Minmax 算法与 Alpha-Beta 剪枝的 AI 对手。

## 功能特点

- **图形界面**：简洁的棋盘绘制与棋子展示。
- **人人对战（默认玩家执黑先行）**：玩家点击鼠标落子，AI 自动执白响应。
- **AI 决策**：
  - 采用带有历史表启发的迭代加深 Minmax 搜索。
  - Alpha-Beta 剪枝优化搜索效率。
  - 基于位置的权重评估与棋型评分表。
- **交互提示**：
  - 实时显示当前回合。
  - 鼠标悬停显示半透明落子预览。
  - 最后一次落子位置用红点标记。
- **游戏重置**：按 `R` 键重新开始对局。

## 环境要求

- Python 3.7+
- Pygame 库

## 安装与运行

1. 克隆或下载本项目代码。
2. 安装依赖：
   ```bash
   pip install pygame
