## class AvatarSnap

### 仅 quan_avatar 中使用的方法
* AvatarSnap.crop(im, src, aid, name, temp_name)	将图片裁剪为 320 * 320
* AvatarSnap.temp_name_get(origin_name)				生成一个唯一文件名
* AvatarSnap.avatar_make(name)						crop 后的图片裁剪为不同大小

### 查找头像
* AvatarSnap.avatar_find(src, aid, size, none)		查找账户头像的指定尺寸
* AvatarSnap.avatar_all(src, aid, none)				查找账户头像的全部尺寸 [缓]

