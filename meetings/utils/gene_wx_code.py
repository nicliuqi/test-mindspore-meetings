import logging
import stat
import sys
import tempfile
import os
from django.conf import settings
from obs import ObsClient
from meetings.utils import wx_apis

logger = logging.getLogger('log')


def save_temp_img(content):
    tmpdir = tempfile.gettempdir()
    tmp_file = os.path.join(tmpdir, 'tmp.jpeg')
    flags = os.O_CREAT | os.O_WRONLY
    modes = stat.S_IWUSR
    with os.fdopen(os.open(tmp_file, flags, modes), 'wb') as f:
        f.write(content)
    return tmp_file


def upload_to_obs(tmp_file, activity_id):
    access_key_id = settings.DEFAULT_CONF.get('MINDSPORE_ACCESS_KEY_ID', '')
    secret_access_key = settings.DEFAULT_CONF.get('MINDSPORE_SECRET_ACCESS_KEY', '')
    endpoint = settings.DEFAULT_CONF.get('MINDSPORE_OBS_ENDPOINT', '')
    bucketName = settings.DEFAULT_CONF.get('MINDSPORE_OBS_BUCKETNAME', '')
    if not access_key_id or not secret_access_key or not endpoint or not bucketName:
        logger.error('losing required arguments for ObsClient')
        sys.exit(1)
    obs_client = ObsClient(access_key_id=access_key_id,
                           secret_access_key=secret_access_key,
                           server='https://%s' % endpoint)
    object_key = 'mindspore/miniprogram/activity/{}/wx_code.jpeg'.format(activity_id)
    obs_client.uploadFile(bucketName=bucketName, objectKey=object_key, uploadFile=tmp_file, taskNum=10,
                          enableCheckpoint=True)
    img_url = 'https://%s.%s/%s' % (bucketName, endpoint, object_key)
    return img_url


def run(activity_id):
    content = wx_apis.gene_code_img(activity_id)
    tmp_file = save_temp_img(content)
    img_url = upload_to_obs(tmp_file, activity_id)
    return img_url

