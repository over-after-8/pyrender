# Authorization

- Sẽ có các permissions và các role
- các controllers sẽ được decorated bằng hàm check_permission
- một role sẽ có các permission
- [???] một permission sẽ thuộc nhiều role khác nhau???
- role sẽ được tạo dựa trên application
- một application sẽ có các role sau:
    - <view_model>.user: chỉ được thao tác crud trên những bản ghi mà user đó tạo ra
    - <view_model>.editor: được thao tác crud với tất cả các bản ghi của application.view_model đó
    - <view_model>.viewer: dược xem tất cả các bản ghi của application đó nhưng ko có các thao tác thêm, sửa, xoá
    - <application>.admin: thao tác crud trên tất cả các view_model

- hàm check_permission sẽ check theo permission, các permission trên mỗi view model:
    - <view_model>.edit.all
    - <view_model>.delete.all
    - <view_model>.edit
    - <view_model>.delete

- hàm check_permission được định nghĩa như sau
```python

def check_permission(func):
    def wrap_func(self_object, *arg, **kwarg):
        ...
    return wrap_func

```
