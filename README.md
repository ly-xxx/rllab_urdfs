# rllab_urdfs

RLLab 机器人 URDF 模型库，包含多种工业机器人和移动机器人的完整 URDF 描述文件。

## 📁 在线预览

查看模型效果：[robotsfan.com URDF Viewer](https://viewer.robotsfan.com/) - 直接拖拽URDF文件即可预览

## 🤖 包含的机器人模型

### RM75-B 系列
- **RM75+gripper**: RM75-B 协作机械臂 + CRT-CTAG2F90 夹爪
- **RM75+hand**: RM75-B 协作机械臂 + RH56DFTP 灵巧手

### xArm6 系列
- **XARM6+gripper**: xArm6 协作机械臂 + Robotiq 夹爪
- **XARM6+cam+gripper**: xArm6 机械臂 + 相机 + Robotiq 夹爪
- **XARM6+force_sensor+cam+gripper**: xArm6 机械臂 + 力传感器 + 相机 + Robotiq 夹爪

### 移动机器人
- **ARX-lift2**: ARX 升降移动机器人（带双臂机械手）

## 🚀 快速开始

### 验证 URDF 文件
```bash
# 以 RM75+hand 为例
cd RM75+hand
python test_model.py --mode validate
```

### 使用 PyBullet 测试
```bash
# 安装 PyBullet (如果还没安装)
pip install pybullet

# 运行测试
python test_model.py --mode pybullet
```

### ROS 中使用
```xml
<!-- 在你的 launch 文件中 -->
<param name="robot_description"
       textfile="$(find rm75_hand)/urdf/rm75b_with_dexterous_hand.urdf"/>
```

## 📋 模型特性

| 模型 | 自由度 | 末端执行器 | 主要应用 |
|------|--------|------------|----------|
| RM75+gripper | 7DOF | 并联夹爪 | 抓取操作 |
| RM75+hand | 13DOF | 五指灵巧手 | 精细操作 |
| XARM6+gripper | 6DOF | 并联夹爪 | 工业应用 |
| ARX-lift2 | 8DOF | 双臂机械手 | 移动操作 |

## 🛠️ 开发与测试

### 环境要求
- Python 3.6+
- PyBullet (可选，用于物理仿真)
- ROS/ROS2 (可选，用于机器人控制)

### 测试脚本
每个模型目录都包含测试脚本：
- `test_model.py`: 统一的测试工具
- 支持验证、PyBullet 仿真、ManiSkill2 仿真

### 自定义修改
1. 修改关节参数：编辑 `urdf/*.urdf` 文件
2. 添加新的末端执行器：参考现有模型结构
3. 调整 mesh 路径：确保 package:// 路径正确

## 📚 详细文档

每个模型都有独立的文档：
- `RM75+hand/README.md` - RM75-B + 灵巧手详细说明
- `RM75+hand/QUICKSTART.md` - 快速开始指南
- `XARM6+gripper/README.md` - xArm6 系列说明

## 🤝 贡献指南

1. **添加新模型**：
   - 创建新的文件夹
   - 包含完整的 URDF、meshes 和配置文件
   - 添加测试脚本和文档

2. **改进现有模型**：
   - 验证关节限位和物理参数
   - 优化碰撞检测网格
   - 完善可视化材质

3. **代码规范**：
   - URDF 文件使用标准的 XML 格式
   - 关节命名遵循 ROS 规范
   - mesh 文件使用 STL 格式

## 📄 许可证

本项目中的 URDF 模型基于相应机器人的原始设计和开源许可证。使用时请遵守：
- 各机器人制造商的使用条款
- 开源许可证要求
- 学术/商业使用限制

## 🔗 相关链接

- [ROS URDF 文档](http://wiki.ros.org/urdf)
- [Gazebo 仿真](http://gazebosim.org/)
- [PyBullet 物理引擎](https://pybullet.org/)
- [ManiSkill2 框架](https://github.com/haosulab/ManiSkill)

---

**维护者**: RLLab Team
