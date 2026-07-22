# 220tech · W1-16 MediaSet 类型化 + 表格行变换

> **版本**：v1.0 · 2026-07-22 · **关联**：220plan §1.2.2 W1-16 · Phase 5 · 高优先级
> **依赖**：W1-9 MediaReferenceStore（取 media ref）、W1-8 transform_ops（表格变换）
> **范围**：类型化媒体集合（DICOM/音频/文档/图像）+ 表格行变换（MediaSet 当作表格应用算子）

## 1. 目标
- MediaSet：一组 MediaReference + 类型约束
- 四种类型：DICOM（医疗影像）/ AUDIO / DOCUMENT / IMAGE
- 表格行变换：每行 = 一个 media 的元数据，应用 W1-8 transform_ops（filter/sort/expression 等）

## 2. 数据模型
```python
class MediaSet(BaseModel):
    id: str
    name: str
    type: Literal["dicom","audio","document","image"]
    media_ref_ids: list[str]
    schema: list[SchemaField]   # 表格 schema（含 media_ref_id + 元数据列）
    created_at: str
```

## 3. 类型约束矩阵
| MediaSet.type | 接受 MediaReference.kind |
| --- | --- |
| dicom | image |
| audio | audio |
| document | document |
| image | image |

## 4. MediaSetStore
```python
class MediaSetStore:
    def create(name, set_type) -> MediaSet
    def add_media(set_id, ref_id) -> MediaSet       # 校验类型匹配
    def remove_media(set_id, ref_id) -> MediaSet
    def get_rows(set_id) -> list[dict]              # 从 media_refs 派生表格行
    def transform(set_id, ops) -> list[dict]        # 复用 W1-8 apply_transform
    def get/list/delete
```

## 5. REST API (`/v1/media-sets`)
| POST | `/v1/media-sets` | 创建 |
| GET | `/v1/media-sets` | 列表 |
| GET | `/v1/media-sets/{id}` | 详情 |
| POST | `/v1/media-sets/{id}/media` | 添加 media |
| DELETE | `/v1/media-sets/{id}/media/{ref_id}` | 移除 media |
| GET | `/v1/media-sets/{id}/rows` | 表格行 |
| POST | `/v1/media-sets/{id}/transform` | 变换 |

## 6. 测试 ≥ 16
引擎：create/add_media（类型匹配/不匹配）/remove/get_rows/transform（filter/sort）/list/delete/404 等；API ≥ 6。

## 7. 文件清单
| `aos_api/media_set.py` | 新增 |
| `aos_api/routers/media_sets.py` | 新增 |
| `aos_api/main.py` | 修改 |
| `tests/test_media_set.py` | 新增 |
