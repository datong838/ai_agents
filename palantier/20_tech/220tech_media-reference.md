# 220tech · W1-9 MediaReference Bridge

> **版本**：v1.0 · 2026-07-22 · **关联**：220plan §1.2.2 W1-9 · Phase 5 · 高优先级
> **依赖**：无新增（独立模块）；W1-17 角色体系可选集成
> **范围**：S3/本地双适配 + 缩略图占位 + 签名直链 + 权限继承标记

## 1. 目标
- MediaReference：引用底层存储（不存数据本身）
- 双适配器：LocalAdapter（真实文件）+ S3Adapter（mock，接口对齐）
- 缩略图：本期返回占位 URL（真实生成 Phase 6 用 Pillow/ffmpeg）
- 签名直链：带过期时间的 URL
- 权限继承：记录 owner_object_type + owner_object_id，继承 Ontology 权限

## 2. 数据模型
```python
class MediaReference(BaseModel):
    id: str
    kind: Literal["image","video","audio","document"]
    storage: Literal["s3","local"]
    bucket: str
    path: str
    version: str = "1"
    mime: str = ""
    size_bytes: int = 0
    thumbnails: dict[str, str] = {}      # size -> url
    owner_object_type: str = ""
    owner_object_id: str = ""
    created_at: str
```

## 3. MediaStorageAdapter（抽象）
```python
class MediaStorageAdapter:
    def exists(self, bucket, path) -> bool
    def signed_url(self, bucket, path, expires_seconds=3600) -> str
    def read_bytes(self, bucket, path, max_bytes) -> bytes
```
- LocalAdapter: 真实文件系统操作
- S3Adapter: mock 实现（返回伪造 URL，不真实连 S3）

## 4. MediaReferenceStore
```python
class MediaReferenceStore:
    def register(kind, storage, bucket, path, ...) -> MediaReference
    def get(id) / list_all() / delete(id)
    def get_signed_url(id, expires=3600) -> str
    def generate_thumbnail(id, sizes=["small","medium","large"]) -> dict
    def list_by_owner(object_type, object_id) -> list[MediaReference]
    def set_adapter(storage_kind, adapter)
```

## 5. REST API (`/v1/media-references`)
| POST | `/v1/media-references` | register |
| GET | `/v1/media-references` | list |
| GET | `/v1/media-references/{id}` | detail |
| DELETE | `/v1/media-references/{id}` | delete |
| GET | `/v1/media-references/{id}/signed-url` | 签名直链 |
| POST | `/v1/media-references/{id}/thumbnails` | 生成缩略图 |
| GET | `/v1/media-references/by-owner/{object_type}/{object_id}` | 按属主查 |

## 6. 测试（≥ 16）
引擎：register/get/list/delete/signed_url（local真实/s3 mock）/thumbnail/owner/exists/404 等 ≥10；API ≥6。

## 7. 文件清单
| `aos_api/media_reference.py` | 新增 |
| `aos_api/routers/media_references.py` | 新增 |
| `aos_api/main.py` | 修改 |
| `tests/test_media_reference.py` | 新增 |

## 8. 不做的事
- ❌ 真实 S3 连接（Phase 6 接 boto3）
- ❌ 真实缩略图生成（Phase 6 用 Pillow/ffmpeg）
- ❌ 大文件分片上传（Phase 6 multipart）
