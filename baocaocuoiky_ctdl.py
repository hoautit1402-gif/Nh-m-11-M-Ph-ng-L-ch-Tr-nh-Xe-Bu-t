# ==========================================
# PHẦN 1: CẤU TRÚC DỮ LIỆU CƠ BẢN
# ==========================================


class Node:
  """Đại diện cho một Nút (Trạm xe buýt) trong Danh sách liên kết đơn."""

  def __init__(self, station_name):
    self.station_name = station_name  # Tên trạm
    self.next = None  # Con trỏ trỏ tới trạm tiếp theo


class LinkedList:
  """Danh sách liên kết đơn quản lý danh sách các trạm dừng của một tuyến xe buýt.

  (Đáp ứng yêu cầu thiết kế CTDL lưu thông tin tuyến xe qua các trạm)[cite: 1]
  """

  def __init__(self, route_name):
    self.route_name = route_name  # Tên tuyến (VD: Tuyến 01)
    self.head = None

  def add_station(self, station_name):
    """Thêm một trạm vào cuối danh sách liên kết của tuyến."""
    new_node = Node(station_name)
    if not self.head:
      self.head = new_node
      return
    current = self.head
    while current.next:
      current = current.next
    current.next = new_node

  def get_stations(self):
    """Chuyển danh sách liên kết thành Python List để dễ hiển thị/duyệt."""
    stations = []
    current = self.head
    while current:
      stations.append(current.station_name)
      current = current.next
    return stations


class Queue:
  """Cấu trúc dữ liệu Hàng đợi (Queue) phục vụ cho thuật toán tìm kiếm BFS."""

  def __init__(self):
    self.items = []

  def is_empty(self):
    return len(self.items) == 0

  def enqueue(self, item):
    self.items.append(item)

  def dequeue(self):
    if not self.is_empty():
      return self.items.pop(0)
    return None


# ==========================================
# PHẦN 2: HỆ THỐNG MẠNG LƯỚI XE BUÝT (ĐỒ THỊ)
# ==========================================


class BusSystem:
  """Quản lý mạng lưới giao thông dựa trên cấu trúc Đồ thị (Graph)."""

  def __init__(self):
    self.routes = {}  # Lưu danh sách các tuyến (dùng Danh sách liên kết)
    self.graph = {}  # Đồ thị kề: Trạm -> Danh sách (Trạm kề, Tuyến xe)

  def add_route(self, route_name, station_list):
    """Thêm một tuyến xe buýt mới vào hệ thống."""
    # 1. Tạo Danh sách liên kết đơn cho tuyến này
    route_ll = LinkedList(route_name)
    for station in station_list:
      route_ll.add_station(station)
    self.routes[route_name] = route_ll

    # 2. Xây dựng Đồ thị (Graph) từ tuyến xe buýt này
    stations = route_ll.get_stations()
    for i in range(len(stations)):
      station = stations[i]
      if station not in self.graph:
        self.graph[station] = []

      # Nối trạm hiện tại với các trạm liền kề trên cùng tuyến
      if i > 0:
        prev_station = stations[i - 1]
        self.graph[station].append((prev_station, route_name))
      if i < len(stations) - 1:
        next_station = stations[i + 1]
        self.graph[station].append((next_station, route_name))

  def get_all_stations(self):
    """Lấy danh sách tất cả các trạm duy nhất có trong hệ thống (Sắp xếp cố định)."""
    return sorted(list(self.graph.keys()))

  def find_route(self, start_station, end_station):
    """Tìm đường đi từ trạm bắt đầu đến trạm kết thúc,

    ưu tiên giảm thiểu số lần chuyển tuyến (Biến thể BFS)[cite: 1].
    """
    if start_station not in self.graph or end_station not in self.graph:
      return (
          None,
          "Trạm xuất phát hoặc trạm đến không tồn tại trong hệ thống!",
      )

    if start_station == end_station:
      return None, f"Bạn đang ở tại trạm {start_station} rồi!"

    # Queue lưu trữ trạng thái: (trạm hiện tại, tuyến xe đang đi, danh sách đường đi, số lần chuyển tuyến)
    queue = Queue()

    # Khởi tạo từ trạm xuất phát
    for neighbor, route in self.graph[start_station]:
      queue.enqueue(
          (neighbor, route, [(start_station, "Xuất phát"), (neighbor, route)], 0)
      )

    visited = set([start_station])
    best_path = None
    min_transfers = float("inf")

    while not queue.is_empty():
      current_station, current_route, path, transfers = queue.dequeue()

      if current_station == end_station:
        if transfers < min_transfers:
          min_transfers = transfers
          best_path = path
        continue

      visited.add(current_station)

      # Duyệt các trạm kề
      for neighbor, route in self.graph[current_station]:
        # Kiểm tra xem có cần chuyển tuyến không
        new_transfers = transfers if route == current_route else transfers + 1

        # Tránh lặp vô hạn và tối ưu nhánh tìm kiếm
        if neighbor not in [s[0] for s in path]:
          queue.enqueue(
              (
                  neighbor,
                  route,
                  path + [(neighbor, route)],
                  new_transfers,
              )
          )

    if best_path is None:
      return None, "Không tìm thấy lộ trình phù hợp giữa hai trạm này!"

    return best_path, min_transfers


# ==========================================
# PHẦN 3: CHƯƠNG TRÌNH TƯƠNG TÁC (NHẬP BẰNG SỐ THỨ TỰ)
# ==========================================
if __name__ == "__main__":
  # Khởi tạo hệ thống
  bus_net = BusSystem()

  # Xây dựng bộ dữ liệu giả lập (Đủ 5 tuyến và ~20 trạm tại Biên Hòa)[cite: 1]
  bus_net.add_route(
      "Tuyến 01",
      [
          "Bến xe Biên Hòa",
          "Ngã Tư Vũng Tàu",
          "KCN Biên Hòa 1",
          "Big C Đồng Nai",
          "Khu Công Nghiệp Amata",
      ],
  )
  bus_net.add_route(
      "Tuyến 02",
      [
          "Khu Công Nghiệp Amata",
          "Ngã Tư Tam Hiệp",
          "Bệnh viện Đa khoa Đồng Nai",
          "Khu Phố 4",
          "Cầu Mới",
      ],
  )
  bus_net.add_route(
      "Tuyến 03",
      [
          "Bến xe Biên Hòa",
          "Chợ Biên Hòa",
          "Cầu Hóa An",
          "Ngã Tư Tam Hiệp",
          "Trường Đại học Lạc Hồng",
      ],
  )
  bus_net.add_route(
      "Tuyến 04",
      [
          "KCN Biên Hòa 1",
          "Công viên Biên Hùng",
          "Bệnh viện Đa khoa Đồng Nai",
          "Trung tâm Văn hóa",
          "Chợ Tân Mai",
      ],
  )
  bus_net.add_route(
      "Tuyến 05",
      [
          "Cầu Hóa An",
          "Nhà máy Thủy tinh",
          "Chợ Tân Mai",
          "Khu Phố 4",
          "Bến xe Phía Nam",
      ],
  )

  print("==================================================")
  print(" HỆ THỐNG MÔ PHỎNG LỊCH TRÌNH XE BUÝT BIÊN HÒA ")
  print("==================================================")
  print(
      f"Tổng số tuyến xe: {len(bus_net.routes)} | Tổng số trạm duy nhất:"
      f" {len(bus_net.get_all_stations())}"
  )

  # Lấy danh sách các trạm cố định để ánh xạ theo chỉ số (Index)
  stations_list = bus_net.get_all_stations()

  # Vòng lặp cho phép người dùng nhập liên tục bằng số
  while True:
    print("\n--- DANH SÁCH CÁC TRẠM CÓ TRONG HỆ THỐNG ---")
    for idx, station in enumerate(stations_list, 1):
      print(f"{idx}. {station}")
    print("-" * 50)

    print("[NHẬP LỘ TRÌNH TÌM KIẾM]")
    start_input = input(
        "Nhập số thứ tự trạm xuất phát (hoặc bấm 'q' để thoát): "
    ).strip()
    if start_input.lower() == "q":
      print("Đã thoát chương trình!")
      break

    end_input = input(
        "Nhập số thứ tự trạm đến: "
    ).strip()

    # Kiểm tra xem người dùng có nhập đúng định dạng số không
    if not start_input.isdigit() or not end_input.isdigit():
      print(" Lỗi: Vui lòng chỉ nhập số thứ tự tương ứng trong danh sách!")
      print("=" * 50)
      continue

    start_idx = int(start_input) - 1
    end_idx = int(end_input) - 1

    # Kiểm tra tính hợp lệ của phạm vi số
    if (
        0 <= start_idx < len(stations_list)
        and 0 <= end_idx < len(stations_list)
    ):
      start = stations_list[start_idx]
      end = stations_list[end_idx]

      print(f"\nĐang tìm đường từ [{start}] đến [{end}]...")
      path, transfers = bus_net.find_route(start, end)

      if isinstance(transfers, str):
        print(f"Lỗi: {transfers}")
      else:
        print(f" Thành công! Tổng số lần chuyển tuyến: {transfers}")
        print("Chi tiết hành trình:")
        for i, step in enumerate(path):
          station, route = step
          if i == 0:
            print(f"  [Bắt đầu] Tại trạm: {station}")
          else:
            print(f"  -> Đi tiếp đến trạm: {station} (Bằng tuyến: {route})")
    else:
      print(" Lỗi: Số thứ tự trạm bạn nhập không có trong danh sách!")

    print("=" * 50)