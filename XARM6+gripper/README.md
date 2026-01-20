# xArm6 Robot Assets

These are the local assets for the xArm6 robot, copied from the default location at `~/.maniskill/data/robots/xarm6/`.

The code in the agents directory now prefers these local assets over the ones in the default location. If the local assets don't exist, it will fall back to the default location.

This helps with project portability and makes development easier.

# xArm6 Robot Description & Simulation (RLLab/Sapien/ROS)

这个仓库包含了 **UFACTORY xArm 6** 机械臂及其相关配件的仿真模型文件（URDF, OBJ, STL, SRDF）。

本项目特别针对 **强化学习 (RL)** 和 **物理仿真** 环境（如 PyBullet, Sapien, Gazebo）进行了优化，修正了运动学链 (Kinematic Chain)，并支持多种末端执行器和传感器配置。

## 🤖 支持的硬件与模型

### 机械臂 (Robot Arm)

* **xArm 6**: 6自由度协作机械臂。

### 末端执行器 (End Effectors)

* **xArm Gripper**: 官方原厂夹爪（包含完整的联动关节 `mimic` 逻辑）。
* **Robotiq 2F-85**: 支持 Robotiq 85 两指夹爪配置（见 `xarm6_robotiq.urdf`）。
* **Allegro Hand**: 灵巧手配置（见 `xarm6_allegro_*.urdf`）。

### 传感器与配件 (Sensors & Accessories)

* **6-Axis Force Torque Sensor (AI1302)**: 六维力矩传感器，已正确配置在法兰与末端之间。
* **Camera Stand (for Intel RealSense D435)**: 摄像头支架，模型包含安装偏移量。

## 主要文件说明

| 文件名 | 描述 | 备注 |
| --- | --- | --- |
| **`xarm6_with_gripper_v1.urdf`** | **[推荐]** 主模型文件 | 包含 **xArm6 + 力矩传感器 + D435支架 + 夹爪** 的完整串联结构。修复了 `mimic` 联动和模型缩放问题。 |
| `xarm6_robotiq.urdf` | Robotiq版模型 | 搭载 Robotiq 2F-85 夹爪的版本。 |
| `xarm6_robot_white.urdf` | 纯机械臂模型 | 无末端执行器，白色外观。 |
| `xarm6_allegro_right.urdf` | 灵巧手版模型 | 搭载 Allegro Hand (右手) 的版本。 |

## 🛠️ 模型特性与修复 (Key Features)

1. **非 ROS 环境兼容性**:
* 所有 `mesh filename` 路径均采用**相对路径**（例如 `visual/base.stl` 而非 `package://...`），可直接在 PyBullet、Sapien 或 Web Viewer 中加载，无需 ROS `package path` 环境配置。


2. **正确的运动学链 (Correct Kinematic Chain)**:
* 针对 `xarm6_with_gripper_v1.urdf`，末端安装顺序已修正为物理真实的安装顺序：
> `Link6 (法兰)` -> `力矩传感器 (FT Sensor)` -> `摄像头支架 (Camera Stand)` -> `夹爪 (Gripper)`


* 修正了 Z 轴偏移和 90° 旋转安装角度。


3. **单位与缩放修复**:
* 针对从 CAD 导出的 STL 文件（力传感器和支架），已在 URDF 中应用 `scale="0.001 0.001 0.001"`，解决了模型在仿真中尺寸过大（毫米 vs 米）的问题。


4. **关节联动 (Mimic Joints)**:
* 恢复了 xArm Gripper 的 `<mimic>` 标签，确保在仿真中驱动 `drive_joint` 时，手指关节会正确跟随开合。



## 快速开始 (Usage)

### 在 Python (PyBullet/Sapien) 中加载

```python
import pybullet as p
import pybullet_data

# ... 初始化 pybullet ...

# 加载模型 (注意使用 v1 版本)
robot_id = p.loadURDF("xarm6_with_gripper_v1.urdf", [0, 0, 0], useFixedBase=True)

# 控制夹爪
# index 取决于关节索引，通常驱动 drive_joint 即可带动整个夹爪

```

### 文件目录结构

```text
.
├── visual/              # 机械臂本体视觉模型 (STL)
├── collision/           # 机械臂碰撞模型 (简化 OBJ/STL)
│   ├── ft_sensor.stl    # 六维力传感器模型
│   └── cam_stand.stl    # 摄像头支架模型
├── meshes/
│   └── gripper/xarm/    # 夹爪相关模型
├── xarm6_with_gripper_v1.urdf  # 核心模型文件
└── README.md

```

## 注意事项

* **模型路径**: 如果您移动了 URDF 文件的位置，请确保 `visual` 和 `collision` 文件夹相对位置保持不变，否则加载器会报错找不到网格文件。
* **力矩传感器**: 当前模型仅包含传感器的几何碰撞体（Collision）和视觉（Visual），如需物理力矩反馈数据，需在仿真器中对应 Link (`link_ft_sensor`) 处添加传感器插件。

## License

此仓库遵循原始 xArm 开源协议 (详见 `LICENSE` 文件)。
