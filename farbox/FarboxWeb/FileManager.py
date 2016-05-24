import os
import hashlib
from .models import RealFile
from .models import VirtualFile
def handle_upload_file(f):
    #得到UPLOAD_FILES文件夹的绝对路径
    FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'UPLOAD_FILES')
    #如果目录不存在,则创建它
    if(not os.path.exists(FILE_PATH)):
        os.mkdir(path=FILE_PATH)


    #计算文件hash值
    md5obj = hashlib.md5()
    #将文件写入缓冲区
    with open(os.path.join(FILE_PATH, 'temp_file'), 'wb+') \
            as temp_file:
        for chunk in f.chunks():
            temp_file.write(chunk)
            md5obj.update(chunk)  #更新hash值

        temp_file.close()

    #读取完毕后,将临时文件重命名为hash值
    os.rename(os.path.join(FILE_PATH, 'temp_file'),
              os.path.join(FILE_PATH, md5obj.hexdigest()))

    real_file = RealFile(file_name=f.name,
                         file_hash=md5obj.hexdigest(),
                         file_size=f.size)

    real_file.save()
    return md5obj.hexdigest()

def save_virtual_file(file_hash, virtual_path):
    parent_id = 0
    path_names = virtual_path.splite('/')

    for name in path_names[:-1]:
        vi_pa = VirtualFile.objects.get(parent_id=parent_id, path_name=name)
        parent_id=vi_pa.path_id

    vi_pa = VirtualFile(parent_id=parent_id,
                        path_names=path_names[-1],
                        is_file=True,
                        realfilename=file_hash)
    vi_pa.save()