# Ultralytics (YOLO) 框架使用指南

> **环境**：Python 3.x，PyTorch，ultralytics 包
> **最后更新**：2026-03-27

## 概述

Ultralytics (YOLO) 是目前业界最流行且功能最强大的开源计算机视觉框架之一。通过官方的 `ultralytics` 仓库，可以非常便捷地实现目标检测、图像分类、实例分割、姿态估计（关键点检测）以及定向边界框（OBB）等计算机视觉任务。该仓库统一了以往复杂的配置流程，无论是经典版本还是最新的前沿模型（如 YOLO11 和 YOLO26），都可以用极简的命令直接调用。

## 1. 环境准备与安装

Ultralytics 提供了高度封装的 Python 包，强烈推荐使用 `pip` 进行安装，它会自动处理 PyTorch 等核心底层依赖项。

```bash
# 推荐：直接通过 pip 安装最新版
pip install ultralytics -i https://pypi.tuna.tsinghua.edu.cn/simple

# 可选：如果需要修改源码或为仓库做贡献，可以克隆并以可编辑模式安装
git clone https://github.com/ultralytics/ultralytics
cd ultralytics
pip install -e .
```

## 2. 核心使用方式

Ultralytics 的设计理念是"开箱即用"，它提供了两种主要的交互接口：**命令行界面 (CLI)** 和 **Python API**。

### 2.1 命令行界面 (CLI)

CLI 让你无需编写任何 Python 代码即可执行常见的模型任务。基本语法结构为：

`yolo <TASK> <MODE> <ARGS>`

- **TASK（任务）**：`detect`（默认，目标检测）、`segment`（分割）、`classify`（分类）、`pose`（姿态估计）、`obb`（定向框）
- **MODE（模式）**：`train`（训练）、`val`（验证）、`predict`（推理预测）、`export`（导出模型）
- **ARGS（参数）**：指定数据源、网络大小和超参数，如 `model=yolo11n.pt`、`source=image.jpg`、`epochs=100` 等

**典型应用：**

```bash
# 推理预测：使用预训练的 Nano 模型检测图像中的物体
yolo predict model=yolo11n.pt source='https://ultralytics.com/images/bus.jpg'

# 训练模型：在 COCO8 数据集上训练 100 个 epoch
yolo train data=coco8.yaml model=yolo11n.pt epochs=100 imgsz=640

# 导出模型：将 PyTorch 模型转换为 ONNX 格式以便跨平台部署
yolo export model=yolo11n.pt format=onnx
```

> **注意：** 指定 `model=yolo11n.pt` 等标准权重且本地不存在时，Ultralytics 会自动从云端下载该权重的最新版本。

### 2.2 Python API

在自己的应用后端、UI 界面或自动化脚本中集成视觉能力时，Python API 是最佳选择。

```python
from ultralytics import YOLO

# 1. 加载模型
# 可以加载官方预训练权重 (例如 yolo11n.pt, yolo11s-seg.pt) 或自行训练后的 best.pt
model = YOLO('yolo11n.pt')

# 2. 执行推理 (Predict)
# 支持海量数据源：图片路径、OpenCV 视频帧、网络流、YouTube 链接或目录
results = model.predict(source='https://ultralytics.com/images/bus.jpg', save=True, conf=0.5)

# 处理返回结果以便后续业务逻辑使用
for result in results:
    boxes = result.boxes          # 边界框信息 (包含坐标、置信度、类别)
    masks = result.masks          # 分割掩码 (用于 segment 任务)
    keypoints = result.keypoints  # 关键点信息 (用于 pose 任务)
    probs = result.probs          # 类别概率 (用于 classify 任务)

# 3. 训练自定义数据 (Train)
# model.train(data='your_dataset.yaml', epochs=50, imgsz=640, device=0)
```

## 3. 训练自己的数据集

在实际业务场景中，通常需要让模型识别特定的新物体（如工厂流水线上的零件瑕疵）。核心步骤如下：

1. **准备数据并标注**：使用 CVAT、Roboflow 或 Label Studio 等工具框选图片中的目标，并将标注导出为 **YOLO 格式**（每张图片对应一个 `.txt` 文件，内容结构通常为 `class x_center y_center width height` 的归一化数值）。

2. **创建 YAML 配置文件 (`data.yaml`)**：告诉 Ultralytics 框架去哪里加载图片以及包含哪些目标类别。

    ```yaml
    train: /path/to/dataset/train/images  # 训练集路径
    val: /path/to/dataset/val/images      # 验证集路径

    nc: 2                                 # 类别总数
    names: ['cat', 'dog']                 # 类别具体名称
    ```

3. **启动训练**：

    ```bash
    yolo task=detect mode=train data=data.yaml model=yolo11n.pt epochs=100 batch=16
    ```

训练完成后，模型权重文件（如 `best.pt`）和性能评估图表（混淆矩阵、F1-Confidence 曲线等）会自动保存在 `runs/detect/train/` 目录下。

## 4. 模型部署与硬件优化

在生产环境中，PyTorch 原生的 `.pt` 权重文件在推理时往往不能将硬件性能发挥到极致。`export` 功能支持将模型导出为十几种不同格式：

| 格式 | 参数 | 适用场景 |
|------|------|----------|
| TensorRT | `format=engine` | NVIDIA GPU，极致推理加速 |
| ONNX | `format=onnx` | 跨语言（C++/C#）或 CPU 端推理 |
| OpenVINO | `format=openvino` | Intel CPU 和集成显卡 |
| CoreML / NCNN / TFLite | 对应格式名 | 移动端（iOS/Android）及边缘设备 |

```python
# 将训练好的模型导出为 TensorRT 引擎
model = YOLO('runs/detect/train/weights/best.pt')
model.export(format='engine', device=0)
```

## 5. 进阶特性

| 特性 | 说明 |
|------|------|
| 多目标跟踪 (Tracking) | 推理命令加 `tracker=botsort.yaml`，在视频流中赋予目标唯一 ID 并实现跨帧追踪 |
| 回调函数系统 (Callbacks) | 在训练/推理生命周期各阶段挂载自定义逻辑，集成 W&B、MLflow 等监控面板 |
| 超参数调优 (Tune) | `yolo tune` 结合遗传算法，自动寻找能让当前数据集获得最高精度的超参数组合 |

## 参考资料

- [Ultralytics 官方文档](https://docs.ultralytics.com/)
