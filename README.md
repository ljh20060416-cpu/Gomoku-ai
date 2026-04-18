# Gomoku-ai
这是一个基于 Python 的五子棋人机对战游戏，AI 采用 Minimax + Alpha-Beta 剪枝算法
五子棋 AI 对战游戏 (Gomoku AI)
项目简介
基于 Python + Pygame 开发的图形化五子棋游戏
支持人机对战（玩家执黑，AI 执白）
AI 采用博弈树搜索算法，具备即时胜负判断与局势评估能力
功能特性
可视化界面：棋盘、棋子、星位标记、最后落子提示
人机对战：玩家先手（黑棋），AI 自动响应（白棋）
胜负判定：实时检测五连、平局判断
AI 智能层：
即时杀棋识别（进攻/防守）
Minimax 博弈树搜索
Alpha-Beta 剪枝优化
启发式评估函数
游戏控制：重新开始按钮、步数统计、回合状态显示
技术架构
核心模块
表格
模块	职责
draw_* 系列函数	渲染引擎（棋盘、棋子、UI 面板）
check_win	胜负判定逻辑
evaluate_position	盘面评分系统
minimax	博弈树搜索核心
ai_move	AI 决策主入口
get_candidates	候选落位生成与剪枝
AI 算法分层
规则层：必胜/必败点即时响应
搜索层：Minimax + Alpha-Beta（深度 1-2）
评估层：连子形状评分 + 位置偏好
运行环境
Python 3.x
Pygame 库
快速开始
bash
复制
pip install pygame
python gomoku.py
项目结构
plain
复制
.
├── gomoku.py          # 主程序（完整单文件）
└── README.md          # 项目说明
算法参数
表格
参数	默认值	说明
BOARD_SIZE	15	棋盘尺寸（15×15）
CELL_SIZE	50	格子像素大小
SEARCH_DEPTH	1-2	AI 搜索深度（动态调整）
CANDIDATE_RADIUS	2	候选点生成半径
MAX_CANDIDATES	12	每轮评估最大候选数
自定义与扩展
调整 evaluate_line 中的分值权重改变 AI 风格
修改 depth 变量增加搜索深度（权衡性能）
扩展 get_candidates 半径扩大搜索范围
许可证
[MIT / 自定义]
