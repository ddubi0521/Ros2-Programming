# 🤖 Heart Robot (ROS2)

ROS2 기반으로 로봇 모델을 구성하고,  
팔을 흔드는 동작(Arm Wave Motion)을 수행하는 제어 노드를 구현한 프로젝트입니다.

---

## 📌 프로젝트 개요

- ROS2 (Humble) 환경에서 동작
- URDF/Xacro를 활용한 로봇 모델링
- `ros2_control` 기반 관절 제어
- Python 노드를 이용한 팔 동작 생성

---

## ⚙️ 주요 기능

### 1. 로봇 모델 구성
- URDF/Xacro 기반 로봇 구조 정의
- 팔, 다리, 머리, 토끼귀 포함
- 관절(`joint`) 및 링크(`link`) 구성

---

### 2. 팔 동작 제어 (Arm Wave)
- ROS2 Node 기반 제어
- `Float64MultiArray`를 이용한 관절 명령 전송
- 시간 기반 동작 제어 (`get_clock().now()` 활용)

### 3. 동작 흐름:
1. startup → 팔을 서서히 올림
2. wave → sin 함수 기반으로 팔 흔들기
3. reset → 팔을 자연스럽게 내림
4. stop → 초기 자세 복귀 후 종료

---

## 🚀 실행 방법

```bash
# workspace 이동
cd ~/cnu_ros2/heart_robot

# 빌드
colcon build --symlink-install

# 환경 설정
source install/setup.bash

# 실행
ros2 launch heart_robot_description display.launch.py

ros2 launch heart_robot_description gazebo.launch.py
ros2 run heart_robot_control arm_wave
