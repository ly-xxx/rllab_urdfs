#!/usr/bin/env python3
"""
测试 RM75-B with Dexterous Hand 组合模型
支持 PyBullet 和 ManiSkill2 两种测试方式
"""

import os
import sys
import argparse

def test_with_pybullet():
    """使用 PyBullet 测试模型"""
    try:
        import pybullet as p
        import pybullet_data
        import time
        import numpy as np
    except ImportError:
        print("❌ PyBullet 未安装。请运行: pip install pybullet")
        return False
    
    print("🚀 使用 PyBullet 加载模型...")
    
    # 连接到物理引擎
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.8)
    
    # 加载地面
    p.loadURDF("plane.urdf")
    
    # 获取 URDF 文件路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    urdf_path = os.path.join(script_dir, "urdf", "RM75B_with_dexterous_hand.urdf")
    
    if not os.path.exists(urdf_path):
        print(f"❌ URDF 文件不存在: {urdf_path}")
        p.disconnect()
        return False
    
    # 加载机器人
    robot_id = p.loadURDF(
        urdf_path,
        basePosition=[0, 0, 0.5],
        baseOrientation=p.getQuaternionFromEuler([0, 0, 0]),
        useFixedBase=True,
        flags=p.URDF_USE_INERTIA_FROM_FILE
    )
    
    print(f"✅ 成功加载机器人模型 (ID: {robot_id})")
    
    # 获取关节信息
    num_joints = p.getNumJoints(robot_id)
    print(f"\n📊 机器人总关节数: {num_joints}")
    
    # 打印所有关节信息
    print("\n关节列表:")
    print("-" * 80)
    print(f"{'ID':<4} {'关节名':<30} {'类型':<15} {'下限':<10} {'上限':<10}")
    print("-" * 80)
    
    controllable_joints = []
    for i in range(num_joints):
        joint_info = p.getJointInfo(robot_id, i)
        joint_name = joint_info[1].decode('utf-8')
        joint_type = joint_info[2]
        lower_limit = joint_info[8]
        upper_limit = joint_info[9]
        
        type_name = {
            p.JOINT_REVOLUTE: "REVOLUTE",
            p.JOINT_PRISMATIC: "PRISMATIC",
            p.JOINT_FIXED: "FIXED",
        }.get(joint_type, f"UNKNOWN({joint_type})")
        
        print(f"{i:<4} {joint_name:<30} {type_name:<15} {lower_limit:<10.3f} {upper_limit:<10.3f}")
        
        # 收集可控关节
        if joint_type in [p.JOINT_REVOLUTE, p.JOINT_PRISMATIC]:
            if lower_limit < upper_limit:
                controllable_joints.append(i)
    
    print("-" * 80)
    print(f"可控关节数: {len(controllable_joints)}")
    
    # 设置相机视角
    p.resetDebugVisualizerCamera(
        cameraDistance=1.5,
        cameraYaw=45,
        cameraPitch=-30,
        cameraTargetPosition=[0, 0, 0.5]
    )
    
    # 简单动画：让机器人关节缓慢运动
    print("\n🎬 开始动画演示 (按 Ctrl+C 退出)...")
    print("提示: 机械臂和灵巧手会缓慢运动")
    
    try:
        t = 0
        while True:
            # 为每个可控关节设置目标位置（使用正弦波）
            for idx, joint_id in enumerate(controllable_joints):
                joint_info = p.getJointInfo(robot_id, joint_id)
                lower_limit = joint_info[8]
                upper_limit = joint_info[9]
                
                # 计算目标位置（在关节限位范围内）
                mid = (lower_limit + upper_limit) / 2
                amp = (upper_limit - lower_limit) / 4
                target_pos = mid + amp * np.sin(t * 0.5 + idx * 0.3)
                
                # 设置关节位置
                p.setJointMotorControl2(
                    robot_id,
                    joint_id,
                    p.POSITION_CONTROL,
                    targetPosition=target_pos,
                    force=100
                )
            
            p.stepSimulation()
            time.sleep(1./240.)
            t += 1./240.
            
    except KeyboardInterrupt:
        print("\n\n⏹️  停止演示")
    
    p.disconnect()
    print("✅ PyBullet 测试完成")
    return True


def test_with_maniskill():
    """使用 ManiSkill2 测试模型"""
    try:
        import sapien.core as sapien
        from sapien.utils import Viewer
    except ImportError:
        print("❌ ManiSkill2/SAPIEN 未安装。请参考 ManiSkill2 官方文档安装")
        return False
    
    print("🚀 使用 ManiSkill2/SAPIEN 加载模型...")
    
    # 创建引擎和场景
    engine = sapien.Engine()
    renderer = sapien.SapienRenderer()
    engine.set_renderer(renderer)
    
    scene = engine.create_scene()
    scene.set_timestep(1 / 100.0)
    
    # 添加光源
    scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])
    scene.add_point_light([1, 2, 2], [1, 1, 1])
    scene.add_point_light([1, -2, 2], [1, 1, 1])
    scene.add_point_light([-1, 0, 1], [1, 1, 1])
    
    # 添加地面
    scene.add_ground(altitude=0)
    
    # 获取 URDF 文件路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    urdf_path = os.path.join(script_dir, "urdf", "RM75B_with_dexterous_hand.urdf")
    
    if not os.path.exists(urdf_path):
        print(f"❌ URDF 文件不存在: {urdf_path}")
        return False
    
    # 加载机器人
    loader = scene.create_urdf_loader()
    loader.fix_root_link = True
    robot = loader.load(urdf_path)
    robot.set_root_pose(sapien.Pose([0, 0, 0]))
    
    print(f"✅ 成功加载机器人模型")
    print(f"📊 机器人关节数: {len(robot.get_joints())}")
    print(f"📊 机器人链接数: {len(robot.get_links())}")
    
    # 打印关节信息
    print("\n关节列表:")
    print("-" * 80)
    active_joints = robot.get_active_joints()
    for i, joint in enumerate(active_joints):
        print(f"{i:<4} {joint.name:<30} [{joint.get_limit()[0]:.3f}, {joint.get_limit()[1]:.3f}]")
    print("-" * 80)
    
    # 创建查看器
    viewer = Viewer(renderer)
    viewer.set_scene(scene)
    viewer.set_camera_xyz(x=1.5, y=0, z=1.0)
    viewer.set_camera_rpy(r=0, p=-0.5, y=0)
    
    print("\n🎬 开始交互式查看 (关闭窗口退出)...")
    print("提示: 使用鼠标拖动查看模型")
    
    # 主循环
    while not viewer.closed:
        scene.step()
        scene.update_render()
        viewer.render()
    
    print("✅ ManiSkill2 测试完成")
    return True


def validate_urdf():
    """验证 URDF 文件的完整性"""
    import xml.etree.ElementTree as ET
    
    print("🔍 验证 URDF 文件...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    urdf_path = os.path.join(script_dir, "urdf", "RM75B_with_dexterous_hand.urdf")
    
    if not os.path.exists(urdf_path):
        print(f"❌ URDF 文件不存在: {urdf_path}")
        return False
    
    try:
        tree = ET.parse(urdf_path)
        root = tree.getroot()
        
        # 统计信息
        links = root.findall('.//link')
        joints = root.findall('.//joint')
        materials = root.findall('.//material')
        
        print(f"✅ URDF 文件格式正确")
        print(f"   - Links: {len(links)}")
        print(f"   - Joints: {len(joints)}")
        print(f"   - Materials: {len(materials)}")
        
        # 检查 mesh 文件引用
        meshes = root.findall('.//mesh')
        print(f"\n📁 检查 mesh 文件引用 ({len(meshes)} 个)...")
        
        missing_meshes = []
        for mesh in meshes:
            filename = mesh.get('filename')
            if filename:
                # 将 package:// 路径转换为实际路径
                if filename.startswith('package://RM75B_with_dexterous_hand/'):
                    relative_path = filename.replace('package://RM75B_with_dexterous_hand/', '')
                    actual_path = os.path.join(script_dir, relative_path)
                    if not os.path.exists(actual_path):
                        missing_meshes.append(filename)
        
        if missing_meshes:
            print(f"⚠️  发现缺失的 mesh 文件:")
            for mesh_file in missing_meshes[:5]:  # 只显示前5个
                print(f"   - {mesh_file}")
            if len(missing_meshes) > 5:
                print(f"   ... 还有 {len(missing_meshes) - 5} 个")
            return False
        else:
            print("✅ 所有 mesh 文件都存在")
        
        return True
        
    except ET.ParseError as e:
        print(f"❌ URDF 文件解析错误: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='测试 RM75-B with Dexterous Hand 模型')
    parser.add_argument(
        '--mode',
        choices=['pybullet', 'maniskill', 'validate'],
        default='pybullet',
        help='测试模式: pybullet (PyBullet 测试), maniskill (ManiSkill2 测试), validate (仅验证 URDF)'
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("RM75-B with RH56DFTP Dexterous Hand - 模型测试工具")
    print("=" * 80)
    print()
    
    if args.mode == 'validate':
        success = validate_urdf()
    elif args.mode == 'pybullet':
        success = validate_urdf()
        if success:
            print()
            success = test_with_pybullet()
    elif args.mode == 'maniskill':
        success = validate_urdf()
        if success:
            print()
            success = test_with_maniskill()
    
    print()
    print("=" * 80)
    if success:
        print("✅ 测试完成！")
    else:
        print("❌ 测试失败，请检查错误信息")
    print("=" * 80)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

