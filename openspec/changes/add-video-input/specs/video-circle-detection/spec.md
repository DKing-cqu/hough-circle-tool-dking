# Spec Delta

## Purpose

为图片霍夫圆工具增加视频输入路径：逐帧检测并输出标注视频与逐帧 CSV，使同一套参数可以在连续画面上复核。

## ADDED Requirements

### Requirement: 导入本地视频并逐帧检测

工具 SHALL 接受本地视频文件路径，逐帧解码并调用现有霍夫圆检测函数。视频模式 MUST 复用 `hough.HoughParams` 与 `hough.PRESETS` 作为唯一参数来源，MUST NOT 复制或改写检测算法。视频无法打开或解码失败时 MUST 输出错误信息并以非零状态退出，MUST NOT 留下不完整的输出文件。

#### Scenario: 用预设处理样例视频

- **WHEN** 用户以 `coins` 预设处理一段包含硬币的视频
- **THEN** 工具逐帧输出检测结果，帧数与解码帧数一致，参数值与 `hough.PRESETS["coins"]` 相同

#### Scenario: 视频不可读

- **WHEN** 用户指定的路径不存在或不是可解码视频
- **THEN** 工具打印包含路径的错误信息，退出码非零，且不生成标注视频或 CSV 文件

### Requirement: 输出标注视频

工具 SHALL 生成带圆标注的视频文件。标注视频 MUST 保持输入的分辨率与帧率，MUST 只在检测到圆的帧上绘制圆与圆心，且 MUST NOT 修改输入文件。

#### Scenario: 标注视频可播放

- **WHEN** 视频模式处理完成
- **THEN** 输出视频可被播放器打开，分辨率与输入一致，帧数与输入解码帧数一致

#### Scenario: 无圆帧保持原样

- **WHEN** 某一帧未检测到圆
- **THEN** 该帧在标注视频中不绘制任何圆，仍保留原画面

### Requirement: 输出逐帧 CSV

工具 SHALL 生成逐帧 CSV，每帧一行，MUST 包含帧号、时间（秒）、圆数量，以及每个圆的圆心与半径。帧号 MUST 从 0 开始且连续，时间 MUST 单调递增；圆数量为 0 时坐标字段 MUST 留空。

#### Scenario: CSV 行数与视频帧数一致

- **WHEN** 视频模式处理一个 N 帧视频
- **THEN** CSV 数据行数为 N，帧号覆盖 0 到 N-1，时间列为帧号除以帧率

#### Scenario: 未检测到圆

- **WHEN** 某帧没有检测到圆
- **THEN** 该行圆数量为 0，圆心与半径字段均为空

### Requirement: 与图片模式结果一致

对同一画面内容、同一参数，视频模式单帧的检测结果 MUST 与图片模式一致。实现 MUST 直接复用 `hough.detect_circles`，MUST NOT 为视频单独维护一份参数或检测逻辑。

#### Scenario: 抽帧对照

- **WHEN** 从样例视频抽取若干帧并分别以视频模式与图片模式检测
- **THEN** 两种模式的圆数量与圆心、半径完全相同

### Requirement: 处理进度与错误报告

工具 SHALL 在处理过程中报告进度，MUST 在处理结束时报告处理帧数与输出路径。中途失败时 MUST 指出失败的帧号与原因。

#### Scenario: 正常结束

- **WHEN** 视频处理完成
- **THEN** 终端输出处理帧数、标注视频路径与 CSV 路径

#### Scenario: 中途解码失败

- **WHEN** 视频在某一帧后无法继续解码
- **THEN** 工具报告已处理帧数与失败帧号，退出码非零
