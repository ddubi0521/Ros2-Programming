import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

class ArmWaveNode(Node):
    def __init__(self):
        super().__init__('arm_wave_node')

        # 파라미터 선언
        self.declare_parameter('topic_name', '/arm_controller/commands')
        self.declare_parameter('dt', 0.03)

        self.declare_parameter('startup_time', 2.0) # 팔 드는 시간
        self.declare_parameter('wave_duration', 10.0) # 팔 흔드는 시간
        self.declare_parameter('reset_time', 2.0)     # 팔 내리는 시간

        self.declare_parameter('shoulder_pos', -2.5) 
        self.declare_parameter('elbow_offset', 0.2) 
        self.declare_parameter('elbow_amp', 0.6)
        self.declare_parameter('omega', 4.0)

        # 파라미터 값 읽기
        self.topic_name = self.get_parameter('topic_name').value
        self.dt = self.get_parameter('dt').value

        self.startup_time = self.get_parameter('startup_time').value
        self.wave_duration = self.get_parameter('wave_duration').value
        self.reset_time = self.get_parameter('reset_time').value

        self.shoulder_pos = self.get_parameter('shoulder_pos').value
        self.elbow_offset = self.get_parameter('elbow_offset').value
        self.elbow_amp = self.get_parameter('elbow_amp').value
        self.omega = self.get_parameter('omega').value

        # Publisher 생성
        self.pub = self.create_publisher(
            Float64MultiArray,
            self.topic_name,
            10
        )

        self.timer = self.create_timer(self.dt, self.update)

        # 시작 시간 저장
        self.start_time = self.get_clock().now()
        
        self.done = False

        # log 확인용
        self.get_logger().info('Arm wave node started.')

    def publish_cmd(self, values):
        msg = Float64MultiArray()
        msg.data = values
        self.pub.publish(msg)

    def update(self):
        # 이미 동작이 끝났으면 계속 정지 자세 유지
        if self.done:
            self.publish_cmd([0.0, 0.0, 0.0, 0.0])
            return
        
        # 현재 시간
        now = self.get_clock().now()

        # 경과 시간(초)
        elapsed = (now - self.start_time).nanoseconds * 1e-9

        # start
        if elapsed < self.startup_time:
            fraction = elapsed / self.startup_time
            current_shoulder = self.shoulder_pos * fraction

            self.publish_cmd([current_shoulder, current_shoulder, 0.0, 0.0])
            return

        # 팔 흔들기 동작
        wave_t = elapsed - self.startup_time

        if wave_t < self.wave_duration:
            s = math.sin(self.omega * wave_t)
            elbow_pos = self.elbow_offset + self.elbow_amp * s # 팔꿈치 각도 계산

            self.publish_cmd([self.shoulder_pos, self.shoulder_pos, elbow_pos, elbow_pos])
            
            return
        
        # 천천히 팔 내리기
        reset_t = wave_t - self.wave_duration

        if reset_t < self.reset_time:
            fraction = reset_t / self.reset_time

            # 1 -> 0으로 천천히 감소
            current_shoulder = self.shoulder_pos * (1.0 - fraction)

            # 팔꿈치도 자연스럽게 0으로 복귀
            current_elbow = self.elbow_offset * (1.0 - fraction)

            self.publish_cmd([current_shoulder, current_shoulder, current_elbow, current_elbow])
            return
        
        # 완전히 정지
        self.publish_cmd([0.0, 0.0, 0.0, 0.0])
        self.done = True
        self.get_logger().info('Arm wave motion finished.')

def main(args=None):
    rclpy.init(args=args)
    node = ArmWaveNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # 종료 시 안전하게 초기화 (팔 내림)
        node.publish_cmd([0.0, 0.0, 0.0, 0.0])
        node.destroy_node()

        rclpy.shutdown()

if __name__ == '__main__':
    main()