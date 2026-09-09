# 2D 平台跳跃游戏

一个用 Python 和 Pygame 开发的简单 2D 平台跳跃游戏。

## 🎮 游戏规则

- **目标**：从底部跳跃到顶部的平台，避免敌人
- **操作**：
  - `←` / `A` - 向左移动
  - `→` / `D` - 向右移动
  - `SPACE` - 跳跃
  - `R` - 重新开始游戏

- **敌人**：红色方块会在平台上移动，接触敌人会失败
- **胜利**：成功到达顶部平台！

## 📦 安装

1. 确保安装了 Python 3.7+
2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 🚀 运行游戏

```bash
python main.py
```

## 🎯 游戏特性

- ✅ 重力和跳跃系统
- ✅ 平台碰撞检测
- ✅ 移动敌人
- ✅ 胜利和失败条件
- ✅ 简单的游戏 UI

## 📝 代码结构

- `Player` - 玩家角色类
- `Platform` - 平台类
- `Enemy` - 敌人类
- `Game` - 游戏主逻辑类

## 🎨 自定义

你可以通过修改以下内容来定制游戏：
- 改变 `SCREEN_WIDTH` 和 `SCREEN_HEIGHT` 调整游戏窗口大小
- 调整 `GRAVITY` 和 `JUMP_POWER` 改变物理效果
- 在 `init_level()` 中添加更多平台和敌人
- 改变颜色常量（WHITE, BLUE, GREEN, RED）

祝你游戏愉快！🎉
