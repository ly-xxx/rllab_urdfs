# 快速开始指南

## 📦 文件说明

这个文件夹包含了 RM75-B 机械臂与 RH56DFTP 灵巧手的完整组合模型。

### 主要文件
- `urdf/RM75B_with_dexterous_hand.urdf` - 主 URDF 文件
- `meshes/` - 所有 3D 模型文件
- `test_model.py` - 测试脚本
- `README.md` - 详细文档

## 🚀 快速测试

### 方法 1: 验证 URDF 文件

```bash
cd /path/to/RM75B_with_dexterous_hand
python test_model.py --mode validate
```

### 方法 2: 使用 PyBullet 测试

```bash
# 安装 PyBullet (如果还没安装)
pip install pybullet

# 运行测试
python test_model.py --mode pybullet
```

这将打开一个 3D 窗口，显示机器人模型并进行简单的动画演示。

### 方法 3: 使用 ManiSkill2 测试

```bash
# 确保已安装 ManiSkill2
python test_model.py --mode maniskill
```

## 📝 在您的项目中使用

### Python (PyBullet)

```python
import pybullet as p

# 初始化
p.connect(p.GUI)
p.setGravity(0, 0, -9.8)

# 加载机器人
urdf_path = "path/to/RM75B_with_dexterous_hand/urdf/RM75B_with_dexterous_hand.urdf"
robot_id = p.loadURDF(urdf_path, useFixedBase=True)

# 获取关节数量
num_joints = p.getNumJoints(robot_id)
print(f"Total joints: {num_joints}")

# 控制关节
p.setJointMotorControl2(
    robot_id,
    jointIndex=0,  # joint1
    controlMode=p.POSITION_CONTROL,
    targetPosition=0.5
)
```

### Python (ManiSkill2/SAPIEN)

```python
import sapien.core as sapien

# 创建场景
engine = sapien.Engine()
scene = engine.create_scene()

# 加载机器人
loader = scene.create_urdf_loader()
loader.fix_root_link = True
urdf_path = "path/to/RM75B_with_dexterous_hand/urdf/RM75B_with_dexterous_hand.urdf"
robot = loader.load(urdf_path)

# 获取关节
joints = robot.get_active_joints()
for joint in joints:
    print(f"Joint: {joint.name}")
```

### ROS/ROS2

```xml
<!-- 在你的 launch 文件中 -->
<param name="robot_description"
       textfile="$(find RM75B_with_dexterous_hand)/urdf/RM75B_with_dexterous_hand.urdf"/>
```

## 🎮 控制接口

### RM75-B 关节 (7个)
- `joint_1` - 基座旋转 (-3.106 ~ 3.106 rad)
- `joint_2` - 肩部俯仰 (-2.269 ~ 2.269 rad)
- `joint_3` - 肘部俯仰 (-3.106 ~ 3.106 rad)
- `joint_4` - 腕部旋转 (-2.356 ~ 2.356 rad)
- `joint_5` - 腕部俯仰 (-3.106 ~ 3.106 rad)
- `joint_6` - 腕部旋转 (-2.234 ~ 2.234 rad)
- `joint_7` - 末端旋转 (-6.28 ~ 6.28 rad)

### 灵巧手主要关节 (6个)
- `right_thumb_1_joint` - 拇指基部 (0 ~ 1.16 rad)
- `right_thumb_2_joint` - 拇指第二关节 (0 ~ 0.59 rad)
- `right_index_1_joint` - 食指 (0 ~ 1.44 rad)
- `right_middle_1_joint` - 中指 (0 ~ 1.44 rad)
- `right_ring_1_joint` - 无名指 (0 ~ 1.44 rad)
- `right_little_1_joint` - 小指 (0 ~ 1.44 rad)

> **注意**: 手指的第二关节通过 `mimic` 机制自动跟随第一关节运动。

## 🔧 调整安装位置

如果需要调整灵巧手相对于机械臂的位置，编辑 URDF 文件中的 `hand_mount_joint`:

```xml
<joint name="hand_mount_joint" type="fixed">
    <parent link="link_7"/>
    <child link="hand_base_link"/>
    <!-- 修改这里的 xyz (位移) 和 rpy (旋转) -->
    <origin rpy="0 0 0" xyz="0 0 0"/>
</joint>
```

### 常见调整示例

**向前偏移 5cm:**
```xml
<origin rpy="0 0 0" xyz="0 0 0.05"/>
```

**旋转 90 度:**
```xml
<origin rpy="0 0 1.5708" xyz="0 0 0"/>
```

**组合:**
```xml
<origin rpy="0 0 1.5708" xyz="0 0 0.05"/>
```

## 📊 模型统计

- **总链接数**: ~40 (机械臂 8 + 灵巧手 ~32)
- **总关节数**: ~36
- **可控关节**: 13 (机械臂 7 + 灵巧手主关节 6)
- **力传感器**: 16 个
- **Mesh 文件**: ~60 个

## ⚠️ 常见问题

### Q: 找不到 mesh 文件？

**A**: 确保使用正确的 package 路径。如果在 ROS 中使用，需要设置正确的 ROS_PACKAGE_PATH。

### Q: PyBullet 中模型显示不正确？

**A**: 检查 mesh 文件路径是否正确。PyBullet 需要将 `package://` 路径转换为绝对路径。

### Q: 关节不能移动？

**A**: 检查关节限位是否正确设置，以及是否对正确的关节索引进行控制。

### Q: 碰撞检测问题？

**A**: 确保使用了正确的碰撞网格文件 (collision meshes)。

## 📚 更多信息

- 完整文档: 查看 `README.md`
- 测试脚本: 运行 `python test_model.py --help`
- ManiSkill 文档: https://github.com/haosulab/ManiSkill

## 🤝 反馈和支持

如有问题或建议，请联系维护者或提交 issue。

---

**祝您使用愉快！** 🎉

